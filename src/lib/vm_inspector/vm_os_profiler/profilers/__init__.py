#!python 

# Python library imports
import os
import re
import sys
from subprocess import Popen, PIPE

from vm_inspector.vm_os_profiler.os_consts import *
from vm_inspector.utils import vm_find_path

_prefix = "vm_inspector.vm_os_profiler.profilers"

def load_profilers():
    listing = os.listdir(os.path.dirname(__file__)) 
    dir = os.path.dirname(__file__)

    profilers = []
    for l in listing:
        modname = None
        if not os.path.isdir(os.path.join(dir, l)):
            (modname, ext) = os.path.splitext(os.path.basename(l))
            if ext.lower() not in [ '.py', '.pyc', '.pyo', ]:
                continue
        else:
            modname = l

        try:
            m = __import__(_prefix + ".%s" % modname, globals(), locals(),\
                           ['os_profiler'])

            if not hasattr(m, 'os_profiler'):
                continue

            profiler = getattr(m, 'os_profiler')
            if profiler is not None:
                profilers.append(profiler)
        except Exception, msg:
            print >>sys.stderr, 'Failed to load profiler %s: %s' % (l, msg)
            pass
    return profilers

def probe_os_type(mount_point):
    for os_type in os_path_map.keys():
        try:
            if vm_find_path(mount_point, os_path_map[os_type], inode=None):
                return os_type
        except:
            pass
    """
    for os_type in os_path_map.keys():
    if os.path.exists(os.path.join(mount_point, os_path_map[os_type])):
        return os_type
    """

known_profilers = load_profilers()
