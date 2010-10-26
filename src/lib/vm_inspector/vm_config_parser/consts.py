#!python

import re
from vm_inspector.hypervisors.consts import HVM_TYPE_KVM, HVM_TYPE_QEMU
from vm_inspector.hypervisors.consts import HVM_TYPE_XEN

HVM_TYPE_VIRTUAL_BOX    =   0x010000

config_file = {
    'vmx'   :   re.compile('^.*\.vmx$'),
    'xml'   :   re.compile('^.*\.xml$'),
}

vm_config_hv_regex = {
    'libvirt'       :   re.compile(r"type=\'(kvm|qemu|xen)\'"),
    'virtualbox'    :   re.compile(r"VirtualBox\sxmlns"),
}

vm_config_hv_type = {
    'libvirt'       :   (HVM_TYPE_KVM | HVM_TYPE_QEMU | HVM_TYPE_XEN),
    'virtualbox'    :   HVM_TYPE_VIRTUAL_BOX,
}

empty_line_pat = re.compile(r"^(#.*|^\s*)$")
vmx_file_re = re.compile(r"^.*\.vmx$", re.I)
T = "TRUE"

#
# vim:ts=4 sw=4 ff=unix expandtab 
#
