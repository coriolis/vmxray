#!python

# Python library imports
import os
import sys
from vm_inspector.vm_os_profiler.os_consts import *

class vm_fs_mountpoint_notfound(Exception):
    def __init__(self, msg=None):
        if msg:
            self.fault = msg
        else:
            self.fault = "Mountpoint is not defined."
        Exception.__init__(self, self.fault)

class vm_os_profiler_base(object):
    """
    This module profile the os and return dictionary.
    """
    def __new__(klass, **kwargs):
        """
        This method takes cfg_details, vm_dir, mountpoint.
        """
        os_type = None
        if kwargs.has_key("fs_mountpoint"):
            os_type = profilers.probe_os_type(kwargs["fs_mountpoint"])
        else:
            raise vm_fs_mountpoint_notfound()
        
        for profiler in profilers.known_profilers:
            if profiler.can_handle(os_type):
                kwargs['os_type'] = os_type
                return profiler.__new__(profiler, **kwargs)
        # test code for new reglookup for windows
        #if kwargs["OS"].lower() == "windows" :
            #os_type = OS_TYPE_WINDOWS
        #print "Profiling for : " + kwargs["OS"]

    def get_os_details(self):
        raise NotImplementedError('This method is not implemented yet.')

def get_os_info(**args):
    return vm_os_profiler_base(**args)

import profilers 
