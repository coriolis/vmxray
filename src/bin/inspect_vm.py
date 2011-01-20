#!python

import sys
import os

from optparse import OptionParser

sys.path.extend([os.path.abspath('.')])
sys.path.extend([os.path.join(os.path.dirname(os.path.abspath('.')),
                              'lib')]) 

from vm_inspector import vm_inspector

def print_vm_config_details(vm_config):
    data = """        Virtual Machine Name:   %(displayName)s
        Created with:           %(vm_type_str)s
        Memory Size(MB):        %(memsize)s
        Primary Disk:           %(primary_disk_str)s
    """ % vm_config

    print "Virtual machine configuration details:"
    print data

def print_vm_os_details(os_details):
    data = """        Operating System Name:  %(os_name)s
        Operating System Type:  %(os_type)s
        Distro Name:            %(distro)s
        Installed Kernel:       %(str_os_kernel_bld)s
    """ % os_details

    print "Operating system details:"
    print data

def print_installed_applications(os_details):
    print "Application installed in this virtual machine:"
    
    app_list = os_details['installed_apps_list']

    for i in range(0, len(app_list)):
        print "\t%s" % app_list[i].strip()

if __name__ == "__main__":
    usage = "%s [-h] [-q] -d <virtual machine path>" % sys.argv[0] 
    parser = OptionParser(usage)
    parser.add_option("-d", "--vm-dir", dest="vm_dir", 
                      help="virtual machine file path")
    parser.add_option("-q", "--quite", dest="hide_app",
                      action="store_true", 
                      help="Hide installed applications list.")
    
    (options, args) = parser.parse_args()

    if not options.vm_dir:
        parser.print_help()
        sys.exit(1)

    bin_dir = os.path.join(os.path.dirname(__file__), "bin")
    try:
        (vmx, os_details) = vm_inspector(vm_path=options.vm_dir, 
                                         bin_path=bin_dir).inspect_vm()
        print_vm_config_details(vmx)
        print_vm_os_details(os_details)
        if not options.hide_app:
            print_installed_applications(os_details)
    except Exception, e:
        print str(e)
#
# vim:ts=4 sw=4 ff=unix expandtab 
#
