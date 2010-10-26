#!python

# Python library imports
import os
import sys
import re

class vm_config_parser_error(Exception):
    def __init__(self, msg):
        self.fault = "VM Config Parser: %s" % msg
        Exception.__init__(self, self.fault)

    def __str__(self):
        return self.fault

class vm_config_parser_base(object):
    """
    This class imports the parsers based on the hypervisor type.
    """

    def __new__(cls, **kwargs):
        if not os.path.exists(kwargs['vm_dir']):
            raise vm_config_parser_error(
                "Virtual machine directory does not exist.")
        
        (vm_hv_type, vm_config_file) = \
                parsers.probe_vm_config(kwargs['vm_dir'])

        if not vm_hv_type:
            raise vm_config_parser_error("Unable to find hypervisor type.")

        if not vm_config_file:
            raise vm_config_parser_error("unable to find config file.")
        
        for parser in parsers.known_parsers:
            if parser.can_parse(vm_hv_type):
                if not kwargs.has_key('config_file') or \
                   not kwargs['config_file']:
                    kwargs['config_file'] = vm_config_file
                return parser.__new__(parser, **kwargs)

    def vm_read_config(self):
        raise NotImplementedError(
            'vm_config_parser_base.vm_read_config not implemented.')

    def vm_get_primary_disk(self):
        raise NotImplementedError(
            'vm_config_parser_base.vm_get_primary_disk not implemented.')


def parse_vm_config(**args):
    return vm_config_parser_base(**args)

import parsers

#
# vim:ts=4 sw=4 ff=unix expandtab 
#
