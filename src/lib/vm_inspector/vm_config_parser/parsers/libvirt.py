#python

# Python library imports
import os
import re
from xml.dom import minidom

from vm_inspector.hypervisors.consts import *
from vm_inspector.vm_config_parser import vm_config_parser_base
from vm_inspector.vm_config_parser.consts import *

class config_file_not_found(Exception):
    def __init__(self, msg):
        self.fault = "Please give libvirt configuration file."
        Exception.__init__(self, msg)

class config_file_not_exists(Exception):
    def __init__(self, msg):
        self.fault = "libvirt configuration does not exist."
        Exception.__init__(self, msg)

class config_file_invalid(Exception):
    def __init__(self, msg):
        self.fault = "libvirt configuration xml is invalid."
        Exception.__init__(self, msg)

class libvirt_config_parser(vm_config_parser_base):
    """
    This module parses the libvirt configuration file and put the details
    in cfg_details dictionary.
    """
    def __new__(klass, **args):
        return object.__new__(klass)

    def __init__(self, **args):
        self.vm_dir = args['vm_dir']
        cfg_file = self.__probe_vm_config(args['vm_dir'])
        if not cfg_file:
            raise config_file_not_found()

        if not os.path.exists(cfg_file):
            raise config_file_not_exists()

        self.cfg_file = cfg_file
        self.cfg_details = dict()
    
    def __probe_vm_config(self, vm_dir):
        """
        This method look for the configuration file. It returns hypervisor type
        and config file path.
        """
        file_list = os.listdir(vm_dir)

        for file in file_list:
            if config_file['xml'].match(file):
                return os.path.join(vm_dir, file)
    
    @staticmethod
    def can_parse(hvm_type):
        if(hvm_type & (HVM_TYPE_QEMU | HVM_TYPE_KVM | HVM_TYPE_XEN)):
            return True

        return False

    def vm_read_config(self):
        """
        This method parses the libvirt xml config file and fills the 
        cfg_details dictionary. This method returns the dictionary or 
        raise exception if xml is not valid.
        """
        cfg_file = self.cfg_file
        # get vm_type from xml file.
        xmldoc = minidom.parse(cfg_file)
        vm_domain = xmldoc.getElementsByTagName('domain')[0]
        vm_type = vm_domain.attributes['type'].value
        # Set value in cfg details.
        self.cfg_details['vm_type'] = HVM_LIBVIRT_NAMEMAP[vm_type]
        self.cfg_details['vm_type_str'] = vm_type
        self.cfg_details['displayName'] = (
                xmldoc.getElementsByTagName('name')[0].firstChild.data)
        self.cfg_details['memsize'] = str(
                int(xmldoc.getElementsByTagName(
                    'memory')[0].firstChild.data) >> 10)
        # Get primary disk details.
        disk_list = xmldoc.getElementsByTagName('disk')
        primary_disk_list = []
        for disk in disk_list:
            disk_type = disk.attributes['type']
            device = disk.attributes['device']
            target = disk.getElementsByTagName('target')[0]
            target_bus = target.attributes['bus'].value
            target_dev = target.attributes['dev'].value
            disk_image = disk.getElementsByTagName('source')[0].attributes.values()[0].value
            if (disk_type.value == 'file' and device.value == 'disk' and \
                (target_dev == 'hda' or target_dev == 'sda') and \
                (target_bus == 'ide' or target_bus == 'scsi')):
                primary_disk_list.append(os.path.basename(disk_image))
                break

        self.cfg_details['primary_disk'] = primary_disk_list
        self.cfg_details['primary_disk_str'] = ','.join(primary_disk_list)

        if not self.cfg_details:
            raise config_file_invalid()
        else:
            return self.cfg_details

    def vm_get_primary_disk(self):
        if not self.cfg_details:
            self.vm_read_config()
        return self.cfg_details['primary_disk']

config_parser = libvirt_config_parser 

#
# vim:ts=4 sw=4 ff=unix expandtab 
#
