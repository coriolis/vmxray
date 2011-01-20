#!python

# Python imports
from __future__ import with_statement

import os
import re

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
        self.os_details = dict()
        self.installed_apps = []

    def __get_installed_apps(self):
        """ Get the list of installed application from disk image.
        """
        pkg_list = []
        pkg_entry = dict()
        buffer = vm_find_path(self.fs_mntpt, os.path.join("var", "lib", 
                              "dpkg", "status"), returntype="list")
        
        for x in buffer:
            if x == '\n':
                pkg_list.append(pkg_entry)
                pkg_entry = dict()
            else:
                try:
                    details = x.split(':')
                    if details[0] in ('Package', 'Version'):
                        pkg_entry[details[0]] = ':'.join(details[1:]).strip() 
                except:
                    pass
        
        self.installed_apps = ["%s-%s" % (x['Package'], x['Version']) \
                               for x in pkg_list]
        self.installed_apps.sort()

    def __get_installed_kernel_info(self):
        """ Method to extract kernel information from disk image.
        """

        kernel_pkgs = []
        buffer = vm_find_path(self.fs_mntpt, os.path.join("var", "lib", 
                              "dpkg", "status"), returntype="list")
        
        for x in buffer:
            if x.startswith('Package:'):
                details = x.split(':')
                if details[1].strip().startswith('linux-image'):
                    kernel_pkgs.append(details[1].strip())

        self.os_details['str_os_kernel_bld'] = ', '.join(kernel_pkgs)
        
    def get_os_details(self):
        """ Extract the debian machine details.
        """
        debian_version = vm_find_path(self.fs_mntpt, os.path.join\
                ("etc", "debian_version"), returntype="data")
        ubuntu_version = vm_find_path(self.fs_mntpt, os.path.join\
                ("etc", "lsb-release"), returntype="data")
        
        self.os_details['distro'] = debian_version.strip() 
        self.os_details['os_type'] = "Linux"
        
        try:
            t = re.search(r"DISTRIB_DESCRIPTION=\"(?P<distrib_name>.*)\"",
                          ubuntu_version)
            self.os_details['os_name'] = t.group('distrib_name')
        except:
            self.os_details['os_name'] = "Debian"

        self.__get_installed_apps()
        self.__get_installed_kernel_info()
        
        self.os_details['Applications/Internet'] = \
                ', '.join(self.installed_apps)
        self.os_details['installed_apps_list'] = self.installed_apps
        
        return self.os_details
