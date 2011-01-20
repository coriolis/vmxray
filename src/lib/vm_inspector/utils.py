#!env python
""" Utility functions for vm_inspector module.
"""

from __future__ import with_statement
import os
import re
from subprocess import Popen, PIPE
import datetime
from loadconfig import *

VERSION = 0.01
__all__ = ['check_path', 'find_path', ]


_IMG_FS_OFFSET_SECTOR = '063'

class PathNotFoundError(Exception):
    """ Exception if path does not exist.
    """
    pass

def find_existing_path(start_dir, path_element_list):
    """ return existing path irrespective of case.
    """
    if len(path_element_list) == 0:
        return start_dir 

    tmp_dir_dict = dict([(x.lower(), x) for x in os.listdir(start_dir)])

    if path_element_list[0] in tmp_dir_dict.keys():
        return find_existing_path(
            os.path.join(start_dir, tmp_dir_dict[path_element_list[0]]),
            path_element_list[1:])
    else:
        raise PathNotFoundError("Unable to find path.")

def check_path_existence(start_dir, path_element_list):
    """ Check path existence recursively. Call check_path to use this 
        function.
    """
    if len(path_element_list) == 0:
        return True

    tmp_dir_dict = dict([(x.lower(), x) for x in os.listdir(start_dir)])

    if path_element_list[0] in tmp_dir_dict.keys():
        return check_path_existence(
            os.path.join(start_dir, tmp_dir_dict[path_element_list[0]]),
            path_element_list[1:])
    else:
        return False

def check_path(path):
    """This method is a case insensitive equivalent of os.path.exists.
       path argument must be in lower case.
    """

    # get the start directory and path elements need to be searched.
    start_dir = ''
    path_elements = []
    tmp_path = path = path.lower()

    while not os.path.exists(tmp_path):
        path_elements.insert(0, os.path.basename(tmp_path))
        tmp_path = os.path.dirname(tmp_path)

    start_dir = tmp_path

    if start_dir == path:
        return True

    return check_path_existence(start_dir, path_elements)

def find_path(path):
    """ This method return exisitng path.
    """
    start_dir = ''
    path_elements = []
    tmp_path = path = path.lower()

    while not os.path.exists(tmp_path):
        path_elements.insert(0, os.path.basename(tmp_path))
        tmp_path = os.path.dirname(tmp_path)

    start_dir = tmp_path

    if start_dir == path:
        return start_dir 
    
    try:
        result = find_existing_path(start_dir, path_elements)
    except Exception, exc:
        raise Exception("%s while finding %s" % (str(exc), path))

    return result

def vm_find_path(diskfile, path, inode=None, returntype=None):
    """
        find if path is available
    """
    inode = None
    for a in path.split("/"):
        p = fls(diskfile, inode)
        inode = parse_inode(p, a)
        if not inode:
            break
    if inode:
        if returntype:
            return readfile(diskfile, inode, returntype)
        return inode
    else:
        raise Exception("Unable to find %s" %(path))

def set_fs_starting_offset(diskfile):
    global _IMG_FS_OFFSET_SECTOR
    fs_list = [ 'Linux (0x83)', 'NTFS (0x07)', ] 
    cmd = [os.path.join(conf["bin_dir"], "mmls"), '-i', "QEMU", diskfile]
    res = ''
    
    for fs_type in fs_list: 
        p1 = Popen(cmd, stdout=PIPE)
        p2 = Popen(['grep', fs_type], stdin=p1.stdout, stdout=PIPE)
        p3 = Popen(['awk', '{print $3}'], stdin=p2.stdout, stdout=PIPE)
        try:
            res = p3.communicate()[0].strip()
            if res != '':
                break
        except:
            continue

    if res == '':
        raise Exception("Unable to read partition table.")
    
    if _IMG_FS_OFFSET_SECTOR != res:
        _IMG_FS_OFFSET_SECTOR = res

    
def fls(diskfile, inode=None):
    set_fs_starting_offset(diskfile)
    offset = _IMG_FS_OFFSET_SECTOR
    cmd = [os.path.join(conf["bin_dir"], "fls"), '-o', offset, '-i', "QEMU", 
           diskfile]
    if inode:
        cmd.append(inode)
    return Popen(cmd, stdout=PIPE)

def parse_inode(p, path):
    base, target = os.path.split(path)
    for a in p.stdout.readlines():
        inode = parse_directory(a, target)        
        if inode:
            return inode
       
def parse_directory(line, string):
    regex = r'(.*)[\s](.*):[\s](%s)' %string
    match = re.search(regex, line)
    if match:
        return(match.group(2))

def readfile(disk, inode, returntype=None):
    """
    read a file and return its content
    """
    offset = _IMG_FS_OFFSET_SECTOR
    cmd = [os.path.join(conf["bin_dir"], "icat"), '-o', offset, '-i', "QEMU", 
           disk, inode]
    p = Popen(cmd, stdout=PIPE)
    if returntype:
        if returntype == "file":
            dirname, filename = os.path.split(disk)
            filename = os.path.abspath(os.path.join(conf["tmp_dir"], filename)) 
            with open(filename, "wb") as fd:
                for line in p.stdout.readlines()[4:]:
                    fd.write(line)
            return filename
        elif returntype == "list":
           filedata = []
           for line in p.stdout.readlines()[4:]:
               filedata.append(line)
           return filedata
        elif returntype == "data":
           return ''.join(p.stdout.readlines()[4:])
