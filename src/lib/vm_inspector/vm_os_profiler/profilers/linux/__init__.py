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

def os_type_redhat(args):
    import redhat
    return object.__new__(redhat.vm_os_redhat, **args)

def os_type_debian(args):
    import debian
    return object.__new__(debian.vm_os_debian, **args)

_OS_TYPE_MAP = {
    OS_TYPE_LINUX_REDHAT : os_type_redhat,
    OS_TYPE_LINUX_DEBIAN : os_type_debian,
}

class vm_os_linux(vm_os_profiler_base):
    def __new__(cls, **args):
        if not os.path.exists(args['fs_mountpoint']):
            raise vm_fs_mountpoint_not_exists()
        
        try:
            return _OS_TYPE_MAP[args['os_type']](args)
        except:
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
