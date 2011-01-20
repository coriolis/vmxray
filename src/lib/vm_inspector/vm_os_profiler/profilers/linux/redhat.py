#!python

# Python imports
import os
import re
import rpm
import sys

from vm_inspector.vm_os_profiler.os_consts import *
from vm_inspector.vm_os_profiler.profilers.linux import vm_os_linux

class vm_fs_not_mounted_error(Exception):
    def __init__(self, msg=None):
        if msg:
            self.fault = msg
        else:
            self.fault = "Mountpoint is invalid."
        Exception.__init__(self, self.fault)

class vm_os_details_not_found(Exception):
    def __init__(self, msg=None):
        if msg:
            self.fault = msg
        else:
            self.fault = "Unable to get operating system details."
        Exception.__init__(self, self.fault)

class vm_os_redhat(vm_os_linux):
    def __new__(klass, **args):
        return object.__new__(klass)

    def __init__(self, **args):
        self.fs_mntpt = args['fs_mountpoint']
        if not os.path.ismount(self.fs_mntpt):
            raise vm_fs_not_mounted_error()
        else:
            self.os_details = dict()

    def get_os_details(self):
        """
        Extract the redhat machine details.
        """

        raise Exception("Unsupported OS.")
        fd = open(os.path.join(self.fs_mntpt, 'etc', 'redhat-release'))
        # remove the newline char
        self.os_details['distro'] = fd.readline()[:-1]
        self.os_details['os_name'] = self.os_details['distro']
        fd.close()
        self.os_details['os_type'] = 'Linux'
        try:
            ts=rpm.ts(self.fs_mntpt)
            # Equivalent to rpm -qa
            mi=ts.dbMatch()
            for hdr in mi:
                try:
                    self.os_details[hdr[rpm.RPMTAG_GROUP]] += \
                            ", %s-%s-%s" % (hdr[rpm.RPMTAG_NAME],\
                                            hdr[rpm.RPMTAG_VERSION],\
                                            hdr[rpm.RPMTAG_RELEASE])
                except KeyError:
                    self.os_details[hdr[rpm.RPMTAG_GROUP]] = \
                            "%s-%s-%s" % (hdr[rpm.RPMTAG_NAME], \
                                          hdr[rpm.RPMTAG_VERSION],\
                                          hdr[rpm.RPMTAG_RELEASE])

        except rpm.error, err:
            raise vm_os_details_not_found()

        try:
            kernel_info = self.os_details['System Environment/Kernel'].split(',')
            kernel_pkg_list = []
            for x in kernel_info:
                y = re.search(r'(?P<kernel_pkg>kernel.*)', x)
                if y:
                    kernel_pkg_list.append(y.group('kernel_pkg'))

            self.os_details['str_os_kernel_bld'] = ', '.join(kernel_pkg_list)
        except:
            self.os_details['str_os_kernel_bld'] = None 
        return self.os_details
