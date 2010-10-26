#!python 

# Python library imports
import os
import re

from vm_inspector.hypervisors.consts import *
from vm_inspector.vm_config_parser import vm_config_parser_base
from vm_inspector.vm_config_parser.consts import *

class config_file_not_found(Exception):
    def __init__(self, msg):
        self.fault = "Please give vmware configuration file."
        Exception.__init__(self, msg)

class config_disk_file_not_found(Exception):
    def __init__(self, msg):
        self.fault = "Disk file name is not present in this configuration file."
        Exception.__init__(self, msg)

class config_file_not_exists(Exception):
    def __init__(self, msg):
        self.fault = "vmware configuration does not exist."
        Exception.__init__(self, msg)

class config_file_invalid(Exception):
    def __init__(self, msg):
        self.fault = "vmware configuration is invalid."
        Exception.__init__(self, msg)

class vmware_config_parser(vm_config_parser_base):
    """
    This module parses the vmware configuration file and put the details
    in cfg_details dictionary.
    """
    def __new__(klass, **args):
        return object.__new__(klass)

    def __init__(self, **args):
        cfg_file = self.__probe_vm_config(args['vm_dir'])
        if not cfg_file:
            raise config_file_not_found()

        if not os.path.exists(cfg_file):
            raise config_file_not_exists()

        self.cfg_file = cfg_file
        self.cfg_details = dict()
        self.vmx_info = dict()
        self.__parse_config()
    
    @staticmethod
    def can_parse(hvm_type):
        if(hvm_type & (HVM_TYPE_VMWARE_SERVER | HVM_TYPE_VMWARE_ESX | \
                       HVM_TYPE_VMWARE_WORKSTATION)):
            return True

        return False
    
    def __probe_vm_config(self, vm_dir):
        """
        This method look for the configuration file. It returns hypervisor type
        and config file path.
        """
        file_list = os.listdir(vm_dir)

        for file in file_list:
            if config_file['vmx'].match(file):
                return os.path.join(vm_dir, file)
    
    def __build_vmx_dict(self, vmx_dict, x, val):
        if x.find('.') == -1:
            if not vmx_dict.has_key(x):
                vmx_dict[x] = val
        else:
            y = x.split('.')
            if vmx_dict.has_key(y[0]):
                if type(vmx_dict[y[0]]) != type(dict()):
                    self_value = vmx_dict[y[0]]
                    vmx_dict[y[0]] = dict()
                    vmx_dict[y[0]]['self_value'] = self_value
                self.__build_vmx_dict(vmx_dict[y[0]], '.'.join(y[1:]), val)
            else:
                vmx_dict[y[0]] = dict()
                self.__build_vmx_dict(vmx_dict[y[0]], '.'.join(y[1:]), val)

    def __parse_config(self):
        f = open(self.cfg_file, 'r')
        try:
            for line in f:
                line = line.strip()
                if re.match(empty_line_pat, line):
                    continue

                (key, val) = line.split(' = ')

                key = key.strip()
                val = val.strip()
                val = val.replace('"', '', 2)
                self.__build_vmx_dict(self.vmx_info, key, val)
        except Exception, e:
            raise config_file_invalid(str(e))
        finally:
            f.close()

    def __get_primary_disk(self):
        """
        This method gets the primary disk from the config file and return it.
        """
        d = self.vmx_info
        disks = ['ide0:0', 'ide0:1', ' ide1:0', 'ide1:1', 'scsi0']
        keys = d.iterkeys()
        disk_list = []
        self.cfg_details['primary_disk'] = []
        for k in keys:
            if k in disks and d[k]['present'] == T:
                blkdev = None
                if k.startswith('ide'):
                    if k == "ide0:0":
                        blkdev = "hda"
                    elif k == "ide0:1":
                        blkdev = "hdb"
                    elif k == "ide1:0":
                        blkdev = "hdc"
                    elif k == "ide1:1":
                        blkdev = "hdd"
                elif k.startswith('scsi'):
                    for i in range(0, 27):
                        tmp_key = k + ':%d' % i
                        if d.has_key(tmp_key) and d[tmp_key]['present'] == T:
                            k = tmp_key
                            blkdev = 'sd' + chr(ord('a') + i)
                            break

                if (blkdev == "sda" or blkdev == "hda") and \
                   d[k].has_key('fileName'):
                    disk_list.append(d[k]['fileName'])

        if not len(disk_list):
            raise config_disk_file_not_found("Primary disk not found.") 
        else:
            for disk in disk_list:
                disk_path = os.path.dirname(self.cfg_file) + '/' + disk
                if os.path.exists(disk_path):
                    self.cfg_details['primary_disk'].append(disk)
        return
    
    def vm_read_config(self):
        """
        This method parses the vmware xml config file and fills the 
        cfg_details dictionary. This method returns the dictionary or 
        raise exception if vmx is not valid.
        """

        self.cfg_details['displayName'] = self.vmx_info['displayName']
        self.cfg_details['memsize'] = self.vmx_info['memsize']
        self.cfg_details['virtualHW.version'] = \
                self.vmx_info['virtualHW']['version']

        # ToDo:Check for the following keys needs to be added
        vmtypekey = "%s__%s" % (str(self.vmx_info['config']['version']), 
                str(self.vmx_info['virtualHW']['version']))
        self.cfg_details['vm_type'] = HVM_VMWARE_NAMEMAP[vmtypekey]

        self.__get_primary_disk()
        return self.cfg_details

    def vm_get_primary_disk(self):
        """
        Returns the primary disk filename.
        """
        if not self.cfg_details.has_key('primary_disk'):
            self.vm_read_config()
        return self.cfg_details['primary_disk']

config_parser = vmware_config_parser 

#
# vim:ts=4 sw=4 ff=unix expandtab 
#
