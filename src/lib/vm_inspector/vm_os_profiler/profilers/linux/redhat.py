#!python

from __future__ import with_statement

# Python imports
import os
import bsddb
from time import time as now

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

class vm_os_redhat(vm_os_linux):
    def __new__(klass, **args):
        print 'test'
        return object.__new__(klass)

    def __init__(self, **args):
        self.fs_mntpt = args['fs_mountpoint']
        if not os.path.ismount(self.fs_mntpt):
            raise vm_fs_not_mounted_error()
        else:
            self.os_details = dict()

    def get_os_details(self):
        """
        Extract the redhat machine details.
        """
        buffer = vm_find_path(self.fs_mntpt, 
                              os.path.join('etc', 'redhat-release'),
                              returntype="data")
        self.os_details['distro'] = buffer.strip()
        self.os_details['os_name'] = self.os_details['distro']
        self.os_details['os_type'] = 'Linux'

        try:
            package_buffer = vm_find_path(self.fs_mntpt,
                                os.path.join('var', 'lib', 'rpm', 'Name'),
                                returntype="list")
            package_hash_file = os.path.join(os.path.dirname(self.fs_mntpt),
                                             str(now()))

            with open(package_hash_file, 'w') as fd:
                for x in package_buffer.readlines():
                    fd.write(x)

            try:
                packages_list = bsddb.hashopen(package_hash_file).keys()
            except:
                packages_list = []
            finally:
                os.unlink(package_hash_file)

            self.os_details['Applications/Internet'] = ', '.join(packages_list)
            self.os_details['installed_apps_list'] = packages_list 

        except Exception:
            raise vm_os_details_not_found()

        try:
            kernel_pkg_buffer = vm_find_path(self.fs_mntpt,
                                    os.path.join('etc', 'grub.conf'),
                                    returntype="list")
            
            kernel_pkg_list = []
            for line in kernel_pkg_buffer.readlines():
                if line.find('title') == 0:
                    kernel_pkg_list.append('kernel-%s' % str(
                        line.split(' ')[2].replace('(', '').repalce(')', '')))

            self.os_details['str_os_kernel_bld'] = ', '.join(kernel_pkg_list)
        except:
            self.os_details['str_os_kernel_bld'] = None 
        return self.os_details
