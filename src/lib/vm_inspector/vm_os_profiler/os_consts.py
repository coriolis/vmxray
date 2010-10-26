#!python

import os

# This file contains the constants of supported operating systems.

# Linux Constants
OS_TYPE_LINUX_REDHAT    =   0x000001
OS_TYPE_LINUX_DEBIAN    =   0x000002

# Windows Constants
OS_TYPE_WINDOWS_NT      =   0x000100
OS_TYPE_WINDOWS_2K      =   0x000200
OS_TYPE_WINDOWS_XP      =   0x000400
OS_TYPE_WINDOWS_2K3     =   0x000800
OS_TYPE_WINDOWS_VISTA   =   0x001000
OS_TYPE_WINDOWS_2K8     =   0x002000

# Generic os constants
OS_TYPE_LINUX   = (OS_TYPE_LINUX_REDHAT | OS_TYPE_LINUX_DEBIAN)
OS_TYPE_WINDOWS = (OS_TYPE_WINDOWS_NT | OS_TYPE_WINDOWS_2K | \
        OS_TYPE_WINDOWS_XP | OS_TYPE_WINDOWS_2K3 | OS_TYPE_WINDOWS_VISTA \
        | OS_TYPE_WINDOWS_2K8)

# os path map
os_path_map = {
    OS_TYPE_WINDOWS_NT      :   "pagefile.sys",
    OS_TYPE_WINDOWS_2K      :   "pagefile.sys",
    OS_TYPE_WINDOWS_XP      :   "pagefile.sys",
    OS_TYPE_WINDOWS_2K3     :   "pagefile.sys",
    OS_TYPE_WINDOWS_VISTA   :   "pagefile.sys",
    OS_TYPE_WINDOWS_2K8     :   "pagefile.sys",
    OS_TYPE_LINUX_REDHAT    :   "etc/redhat-release",
    OS_TYPE_LINUX_DEBIAN    :   "etc/debian_version",
    #    OS_TYPE_WINDOWS_NT      :   "Winnt/system32",
    #    OS_TYPE_WINDOWS_2K      :   "WINNT/system32",
    #    OS_TYPE_WINDOWS_XP      :   "WINDOWS/system32",
    #    OS_TYPE_WINDOWS_2K3     :   "WINDOWS/system32",
    #    OS_TYPE_WINDOWS_VISTA   :   "Windows/System32",
    #    OS_TYPE_WINDOWS_2K8     :   "Windows/System32",
    #    OS_TYPE_LINUX_REDHAT    :   "etc/redhat-release",
    #    OS_TYPE_LINUX_DEBIAN    :   "etc/debian_version",
}

# Registry path list
os_regpath_list = ["Winnt/system32/config/software",
                   "Winnt/system32/config/software.sav",
                   "WINNT/system32/config/software",
                   "WINNT/system32/config/software.sav",
                   "WINDOWS/system32/config/software",
                   "WINDOWS/system32/config/software.sav",
                   "Windows/System32/config/SOFTWARE",
                   "Windows/System32/config/SOFTWARE.sav", ]

os_reg_key_map = {
    #purpose            :  [  Key, value_type, Subtree lookup]
    'current_version'   : ["/Microsoft/Windows NT/CurrentVersion", "string", 0],
    'installed_apps'    : ["/Microsoft/Windows/CurrentVersion/Uninstall", "string", 1],
    'subcomponents'     : ["/Microsoft/Windows/CurrentVersion/Setup/OC Manager/Subcomponents", "dword", 0],
    'ie_version'        : ["/Microsoft/Internet Explorer", "string", 0],
    'active_directory'  : ["/ControlSet001/Services/NTDS/Parameters", "all", 0],
    'iis_version'       : ["/Microsoft/InetMgr/Parameters", "dword", 0],
}

os_reg_key_map_old = {
    'current_version'   : " -t SZ -H -O -S -p /Microsoft/Windows\ NT/CurrentVersion %s",
    'installed_apps'    : " -t SZ -H -S -p /Microsoft/Windows/CurrentVersion/Uninstall %s",
    'subcomponents'     : " -t DWORD -H -O -S -p /Microsoft/Windows/CurrentVersion/Setup/OC\ Manager/Subcomponents  %s",
    'ie_version'        : " -t SZ -H -O -S -p /Microsoft/Internet\ Explorer %s",
    'active_directory'  : " -H -O -S -p /ControlSet001/Services/NTDS/Parameters %s",
    'iis_version'       : " -t DWORD -H -O -S -p /Microsoft/InetMgr/Parameters  %s",
}

OS_TYPE_PATH_MAP = {
    'Windows'   :   os_regpath_list,
    'Linux'     :   ['etc/init.d',  ],
}

