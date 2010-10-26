#!env python

# This file contains the various constants defined for hypervisors types and
# mappings.

# VMware hvm types
HVM_TYPE_VMWARE_SERVER      = 0x0001
HVM_TYPE_VMWARE_ESX         = 0x0002
HVM_TYPE_VMWARE_WORKSTATION = 0x0004

# libvirt hvm types
HVM_TYPE_QEMU               = 0x0100
HVM_TYPE_KVM                = 0x0200
HVM_TYPE_XEN                = 0x0400

HVM_LIBVIRT_NAMEMAP = {
    'kvm'   : HVM_TYPE_KVM,
    'qemu'  : HVM_TYPE_QEMU,
    'xen'   : HVM_TYPE_XEN,
}

# Keys to this map is like config.version__virtualHW.version
HVM_VMWARE_NAMEMAP = {
    '8__7': HVM_TYPE_VMWARE_WORKSTATION,
    '8__6': HVM_TYPE_VMWARE_WORKSTATION,
    '8__4': HVM_TYPE_VMWARE_SERVER,
}

HVM_LIBVIRT_TYPES = [ HVM_TYPE_KVM, HVM_TYPE_QEMU, HVM_TYPE_XEN, ]

HVM_VMWARE_TYPES = [ HVM_TYPE_VMWARE_SERVER, HVM_TYPE_VMWARE_ESX, HVM_TYPE_VMWARE_WORKSTATION, ]

# Hypervisor type strings...
HYPERVISORS = {
    HVM_TYPE_VMWARE_ESX            : "VMware ESX Server",
    HVM_TYPE_VMWARE_SERVER         : "VMware Server",
    HVM_TYPE_VMWARE_WORKSTATION    : "VMware Workstation",
    HVM_TYPE_KVM                   : "KVM",
    HVM_TYPE_QEMU                  : "QEMU",
    HVM_TYPE_XEN                   : "XEN",
}

SUP_HYPERVISORS = {
    HVM_TYPE_VMWARE_SERVER         : "VMware Server",
    HVM_TYPE_KVM                   : "KVM",
}

