#!python

# Python imports
import os
import re
#import rpm
import sys

from vm_inspector.vm_os_profiler.os_consts import *
from vm_inspector.vm_os_profiler.profilers.linux import vm_os_linux
from vm_inspector.utils import vm_find_path

class vm_fs_not_mounted_error(Exception):
    def __init__(self, msg=None):
        if msg:
            self.fault = msg
        else:
            self.fault = "Mountpoint is invalid."
        Exception.__init__(self, self.fault)

class vm_os_details_not_found(Exception):
    def __init__(self, msg=None):
        if msg:
            self.fault = msg
        else:
            self.fault = "Unable to get operating system details."
        Exception.__init__(self, self.fault)

class vm_os_debian(vm_os_linux):
    def __new__(klass, **args):
        return object.__new__(klass)

    def __init__(self, **args):
        self.fs_mntpt = args['fs_mountpoint']
        #if not os.path.ismount(self.fs_mntpt):
            #raise vm_fs_not_mounted_error()
        #else:
        self.os_details = dict()
        self.installed_apps = []

    def __get_installed_apps(self):
        """
        Get the list of installed application from mounted filesystem.
        """
        dpkg_db_dir = os.path.join(self.fs_mntpt, "var/lib/dpkg")
        cmd = "dpkg-query -W -f=\'${Package},${Status},${Version},\\\n\' --admindir=%s"\
                % dpkg_db_dir
        status_pattern = re.compile(r'install\sok\sinstalled')
        for line in os.popen(cmd).readlines():
            if status_pattern.findall(line):
                data = line.split(',')
                self.installed_apps.append("%s-%s" %(data[0], data[2],))

    def __get_installed_kernel_info(self):
        """ Method to extract kernel information from mounted root fs.
        """
        dpkg_db_dir = os.path.join(self.fs_mntpt, "var/lib/dpkg")
        try:
            cmd = "dpkg-query -W -f \'${Package}\\\n\' --admindir=%s | grep linux-image" % dpkg_db_dir
            line = os.popen(cmd).readlines()
            kernel_pkg_list = [x.strip() for x in line]
            self.os_details['str_os_kernel_bld'] = ','.join(kernel_pkg_list) 
        except:
            self.os_details['str_os_kernel_bld'] = None
        
    def get_os_details(self):
        """
        Extract the debian machine details.
        """
        fd = vm_find_path(self.fs_mntpt, os.path.join\
                ("etc", "debian_version"), returntype="list")
        #fd = open(os.path.join(self.fs_mntpt, 'etc', 'debian_version'), 'r')
        # remove the newline char
        self.os_details['distro'] = fd.readline()[:-1]
        #fd.close()
        self.os_details['os_type'] = "Linux"
        try:
            os_data = vm_find_path(self.fs_mntpt, os.path.join\
                    ("etc", "lsb-release"), returntype="data")
            #fd = open(os.path.join(self.fs_mntpt, 'etc', 'lsb-release'), 'r')
            #os_data = fd.read()
            #fd.close()
            t = re.search(r"DISTRIB_DESCRIPTION=\"(?P<distrib_name>.*)\"",
                          os_data)
            self.os_details['os_name'] = t.group('distrib_name')
        except:
            self.os_details['os_name'] = "Debian"
        self.__get_installed_apps()
        self.__get_installed_kernel_info()
        self.os_details['Applications/Internet'] = \
                ', '.join(self.installed_apps)
        return self.os_details
