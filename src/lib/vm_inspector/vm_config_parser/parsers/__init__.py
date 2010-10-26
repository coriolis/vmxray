#!env python

import os
import re
import sys
from vm_inspector.hypervisors.consts import *
from vm_inspector.vm_config_parser.consts import *

_prefix = "vm_inspector.vm_config_parser.parsers"

class config_file_not_exists(Exception):
    def __init__(self, msg):
        self.fault = msg
        Exception.__init__(self, self.fault)

def load_parsers():
    listing = os.listdir(os.path.dirname(__file__)) 
    dir = os.path.dirname(__file__)

    parsers = []
    for l in listing:
        modname = None
        if not os.path.isdir(os.path.join(dir, l)):
            (modname, ext) = os.path.splitext(os.path.basename(l))
            if ext.lower() not in [ '.py', '.pyc', '.pyo', ]:
                continue
        else:
            modname = l

        try:
            m = __import__(_prefix + ".%s" % modname, globals(), locals(), \
                           ['config_parser'])

            if not hasattr(m, 'config_parser'):
                continue

            parser = getattr(m, 'config_parser')
            if parser is not None:
                parsers.append(parser)
        except Exception, msg:
            print >>sys.stderr, 'Failed to load parser %s: %s' % (l, msg)
            pass
    return parsers
    
def _probe_hv_type(file):
    """
    This method probes the hypervisor type and return it.
    """
    if not file or not os.path.exists(file):
        raise config_file_not_exists("Unable to open config file.")
    fd = os.open(file, os.O_RDONLY)
    file_text = os.read(fd, 1024)
    os.close(fd)

    for key in vm_config_hv_regex.keys():
        if vm_config_hv_regex[key].search(file_text):
            return vm_config_hv_type[key]

    return None

def probe_vm_config(vm_dir):
    """
    This method look for the configuration file. It returns hypervisor type
    and config file path.
    """
    file_list = os.listdir(vm_dir)
    hv_type_vmware = (HVM_TYPE_VMWARE_SERVER | HVM_TYPE_VMWARE_ESX | 
                      HVM_TYPE_VMWARE_WORKSTATION)
    
    # First we try to find vmx file. If not found then look for xml file.
    for file in file_list:
        if config_file['vmx'].match(file):
            return hv_type_vmware, file

    for file in file_list:
        if config_file['xml'].match(file):
            return _probe_hv_type(os.path.join(vm_dir, file)), file

known_parsers = load_parsers()

#
# vim:ts=4 sw=4 ff=unix expandtab 
#
