#!python

import sys
import os

from optparse import OptionParser

sys.path.extend([os.path.abspath('.')])
sys.path.extend([os.path.join(os.path.dirname(os.path.abspath('.')),
                              'lib')]) 

from vm_inspector import vm_inspector

if __name__ == "__main__":
    usage = "%s [-h] -d <virtual machine path>" % sys.argv[0] 
    parser = OptionParser(usage)
    parser.add_option("-d", "--vm-dir", dest="vm_dir", 
                      help="virtual machine file path")
    
    (options, args) = parser.parse_args()

    if not options.vm_dir:
        parser.print_help()
        sys.exit(1)

    bin_dir = os.path.join(os.path.dirname(__file__), "bin")
    try:
        (vmx, os_details) = vm_inspector(vm_path=options.vm_dir, 
                                         bin_path=bin_dir).inspect_vm()
        print vmx 
        print os_details
    except Exception, e:
        print str(e)
#
# vim:ts=4 sw=4 ff=unix expandtab 
#
