#!python

# Python imports
import os
import logging

# Colama library imports

# VM_Inspector sub module imports
#from vm_inspector.vm_disk_manager import *
from vm_inspector.vm_config_parser import parse_vm_config
from vm_inspector.vm_os_profiler import *

# Exception class to catch vm_inspector exceptions.
class vm_inspector_error(Exception):
    def __init__(self, msg):
        self.fault = "vm_inspector_error: %s" % msg
        Exception.__init__(self, self.fault)

class vm_inspector(object):
    def __init__(self, **kwargs):
        if not kwargs.has_key('vm_path'):
            raise vm_inspector_error(
                "Please provide virtual machine folder path")
        else:
            self.vm_path = kwargs['vm_path']
        
        if not kwargs.has_key('bin_path'):
            raise vm_inspector_error(
                "Please provide binary file path.")
        else:
            #self.disk = vm_disk_manager(bin_dir=kwargs['bin_path'])
            self.bin_dir = kwargs['bin_path']
        
        if kwargs.has_key('config_file'):
            self.config_file = os.path.join(self.vm_path, kwargs['config_file'])
        else:
            self.config_file = None
        
        self.config_details = dict()
        self.os_details = dict()

    def inspect_vm(self):
        """
        This method inspect the virtual machine and add every piece of 
        information in its object. It returns the tuple of config_details
        and os_details.
        If anything is goes wrong the proper exception is raised.
        """
        config_details = self.get_vm_config_details()
        try:
            os_details = self.get_vm_os_details()
        except Exception, e:
            os_details = dict()
            logging.error(str(e))
        return (config_details, os_details)

    def get_vm_config_details(self):
        """
        This method returns the virtual machine configuration details.
        """
        try:
            #Step1: Parse the config file and read the config details
            vd = parse_vm_config(vm_dir=self.vm_path)
            self.config_details = vd.vm_read_config()
        except Exception, e:
            raise vm_inspector_error(str(e))
        return self.config_details

    def get_vm_os_details(self):
        """
        This method returns the virtual machine operating system details.
        """
        try:
            #Step1: Parse the config file and read the config details
            vd = parse_vm_config(vm_dir=self.vm_path)
            self.config_details = vd.vm_read_config()
            #Step2: Get the virtual machine disk file paths
            primary_disk = vd.vm_get_primary_disk()
            #Step3: For each disk in the list mount and get the os details 
            #       if any.
            for disk in primary_disk:
                os_details = None
                if os.path.exists(os.path.join(self.vm_path, disk)):
                    try:
                        #Step4: Mount the virtual machine disk.
                        #self.disk.vm_mount(os.path.join(self.vm_path, disk))
                        #vm_mntpt =  self.disk.get_mountpoint()
                        #Step5: Get the machine internal details.
                        os_profile = get_os_info(fs_mountpoint=\
                                os.path.join(self.vm_path, disk),
                                bin_dir=self.bin_dir)
                        os_details = os_profile.get_os_details()
                        if os_details:
                            self.os_details = os_details
                            break
                    except Exception, e:
                        logging.error(str(e))
                        self.disk.vm_umount()
        except Exception, e:
            raise vm_inspector_error(str(e))
        finally:
            #Step6: Unmount the virtual machine disk image.
            #self.disk.vm_umount()
            pass

        if not self.os_details:
            logging.error("Unable to get the operating system details.")

        return self.os_details

    def dump_vm_details(self, filename, vm_config, os_details):
        """
        This method dumps the virtual machine information in a file.
        If filename is not provided then vm_details.info file gets created in
        vm_dir.
        """
        vmdetails = {}
        
        vmdetails['CONFIG'] = vm_config
        vmdetails['OS'] = os_details
        
        fd = open(filename, 'w')
        fd.write("%s" % str(vmdetails))
        fd.close()

    def read_vm_details(self, filename):
        """
        This method dumps the virtual machine information in a file.
        If filename is not provided then vm_details.info file gets created in
        vm_dir.
        """

        fd = open(filename, 'r')
        vmdetails = eval(fd.read())
        fd.close()

        vm_config = vmdetails['CONFIG']
        os_details = vmdetails['OS'] 

        return (vm_config, os_details)
