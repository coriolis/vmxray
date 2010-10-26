#!env python

# Python imports
import os
import sys

from vm_inspector.vm_os_profiler import vm_os_profiler_base
from vm_inspector.vm_os_profiler.os_consts import *

class vm_fs_not_mounted_error(Exception):
    def __init__(self, msg=None):
        if msg:
            self.fault = msg
        else:
            self.fault = "Mountpoint is invalid."
        Exception.__init__(self, self.fault)

class vm_fs_mountpoint_not_exists(Exception):
    def __init__(self, msg=None):
        if msg:
            self.fault = msg
        else:
            self.fault = "Mountpoint path does not exists."
        Exception.__init__(self, self.fault)

class vm_fs_unsupported_linux_distro(Exception):
    def __init__(self, msg=None):
        if msg:
            self.fault = msg
        else:
            self.fault = "Unsupported Linux distribution."
        Exception.__init__(self, self.fault)

class vm_os_linux(vm_os_profiler_base):
    def __new__(cls, **args):
        if not os.path.exists(args['fs_mountpoint']):
            raise vm_fs_mountpoint_not_exists()

        #if not os.path.ismount(args['fs_mountpoint']):
            #raise vm_fs_not_mounted_error()
        
        fs_mntpt = args['fs_mountpoint']
        #if os.path.exists(os.path.join(fs_mntpt, \
                                       #os_path_map[OS_TYPE_LINUX_REDHAT])):
            #import redhat
            #return object.__new__(redhat.vm_os_redhat, **args)
        #elif os.path.exists(os.path.join(fs_mntpt, \
                                         #os_path_map[OS_TYPE_LINUX_DEBIAN])):
            #import debian
            #return object.__new__(debian.vm_os_debian, **args)
        if args["os_type"] == OS_TYPE_LINUX_REDHAT:
            import redhat
            return object.__new__(redhat.vm_os_redhat, **args)
        elif args["os_type"] == OS_TYPE_LINUX_DEBIAN:
            import debian
            return object.__new__(debian.vm_os_debian, **args)
        else:
            raise vm_fs_unsupported_linux_distro()

    def __init__(self, **args):
        print 'vm_os_linux::init'

    @staticmethod
    def can_handle(os_type):
        if(os_type & (OS_TYPE_LINUX_REDHAT | OS_TYPE_LINUX_DEBIAN)):
            return True

        return False

os_profiler = vm_os_linux

#
# vim:ts=4 sw=4 ff=unix expandtab 
#
