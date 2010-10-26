#!python

# Python imports
import os
import ConfigParser
from ctypes import *

from vm_inspector.vm_os_profiler.os_consts import *
from vm_inspector.vm_os_profiler import *
from vm_inspector.utils import find_path , readfile, vm_find_path
from loadconfig import conf

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

class vm_os_regpath_not_found(Exception):
    def __init__(self):
        self.fault = "Registry path is not found."
        Exception.__init__(self, self.fault)

class vm_os_windows(vm_os_profiler_base):
    def __new__(cls, **args):
        #if not os.path.exists(args['fs_mountpoint']):
            #raise vm_fs_not_mounted_error()
        #else:
        return object.__new__(cls)

    def __init__(self, **args):
        self.fs_mntpt = args["fs_mountpoint"]
        self.reg_path = None
        self.os_details = dict()
        self.installed_apps = []
        self.os_details['os_type'] = 'Windows'
        self.bin_dir = args["bin_dir"]


    def __get_reg_path(self):
        for x in os_regpath_list:
            try:
                #self.reg_path = find_path(os.path.join(self.fs_mntpt, x))
                self.reg_path = vm_find_path(self.fs_mntpt, x)
            except:
                self.reg_path = ""
            else:
                if self.reg_path != "":
                    break
        if self.reg_path == "":
            raise vm_os_regpath_not_found 

        # write the registry file
        self.reg_path = readfile(self.fs_mntpt, self.reg_path, "file")

    def __read_registry(self, read_info, reg_hive):
        if read_info[1] == "string" :
            data = self.fn_get_strings(self.reg_handle, read_info[0], 
                                        read_info[2]);
        elif read_info[1] == "dword" :
            data = self.fn_get_dwords(self.reg_handle, read_info[0], 
                                        read_info[2]);
        strings = []
        if bool(data) :
            i=0
            while bool(data[i]) :
                strings.append(data[i])
                i= i+1
        return strings

    def __get_current_version_info(self):
        for line in self.__read_registry(os_reg_key_map['current_version'], 
                                         
                                         self.reg_path):
            info = line.split(',')
            self.os_details[os.path.basename(info[0])] = info[2]

    def __get_installed_apps(self):
        self.installed_app = []
        self.installed_hotfix = [] 
        
        for line in self.__read_registry(os_reg_key_map['installed_apps'],
                                         self.reg_path):
            info = line.split(',')
            if info[0].split('/')[-1] == 'DisplayName':
                self.installed_app.append(info[2])

    def __get_subcomponent_details(self):
        component_dict = {}
       
        for line in self.__read_registry(os_reg_key_map['subcomponents'],
                                         self.reg_path):
            info = line.split(',')
            if info[-2][-1] == '1':
                component_dict[info[0].split('/')[-1]] = 1

    def __get_iis_info(self):
        major = None
        minor = None
        
        for line in self.__read_registry(os_reg_key_map['iis_version'],
                                         self.reg_path):
            info = line.split(',')
            if info[0].split('/')[-1] == 'MajorVersion':
                major = int(info[-2][-1], 16)
            elif info[0].split('/')[-1] == 'MinorVersion':
                minor = int(info[-2][-1], 16)
        if major and minor:
            self.installed_app.append("ISS %d.%d" % (major, minor))

    def __check_active_directory(self):
        """
        This method checks the presence of active directory and includes
        in installed apps list if present.
        """
        try:
            hive_path = find_path(os.path.join(os.path.dirname(self.reg_path),
                                               'system'))
        except:
            hive_path = ""
            pass

        for line in self.__read_registry(os_reg_key_map['active_directory'],
                                         hive_path):
            if line.find('InstallSiteName') != -1:
                self.installed_app.append('Active Directory')

    def __get_ie_details(self):
        for line in self.__read_registry(os_reg_key_map['ie_version'],
                                         self.reg_path):
            info = line.split(',')
            if info[0].split('/')[-1] == 'Version':
                self.installed_app.append('IE %s' % info[-2]) 

    def __get_prodspec(self):
        self.os_details['prodspec'] = False
        cfg = {}
        for x in os_path_map.keys():
            spec_path = os.path.join(self.fs_mntpt, os_path_map[x], 
                    'prodspec.ini')
            if os.path.exists(spec_path):
                parser = ConfigParser.ConfigParser()
                parser.read(spec_path)
                cfg = dict(parser.items('Product Specification'))
                self.os_details.update(cfg)
                self.os_details['prodspec'] = True
     
    def __init_reglookup(self):
        """
        This method to load reg lookup lib and init its functions
        """
        try:
            self.dll = cdll.LoadLibrary('reglookuplib')
            #open fn
            self.fn_reg_open =self.dll.rll_open_file
            self.fn_reg_open.argtype=c_char_p
            self.fn_reg_open.restype=c_void_p

            #lookup current tree and get strings
            self.fn_get_strings = self.dll.rll_get_value_strings
            self.fn_get_strings.argtype=[c_int, c_char_p, c_int]
            self.fn_get_strings.restype=POINTER(c_char_p)

            #lookup current tree and get DWORDs
            self.fn_get_dwords = self.dll.rll_get_value_dwords
            self.fn_get_dwords.argtype=[c_int, c_char_p, c_int]
            self.fn_get_dwords.restype=POINTER(c_char_p)


        except Exception, e:
           print "Error loading library: " + str(e)

        try:
            self.reg_handle = self.fn_reg_open(self.reg_path)
        except Exception, e:
           print "Error opening registry hive: " + str(e)

    def __lookup_registry(self):
        """
        This method look up the registry for collecting os details and 
        updates the os_details dictionary.
        """
        self.__get_current_version_info()
        self.__get_installed_apps()
        self.__get_iis_info()
        #TODO: May need another API to read from reg
        #self.__check_active_directory()
        self.__get_ie_details()
        #TODO: reads a file, not registry so need to fit some where else
        #self.__get_prodspec()
        self.os_details['installed_app'] = ', '.join(self.installed_app)

    def get_os_details(self):
        """
        This method fetch the details and return dictionary os_details.
        """
        # Get Registry Path
        self.__get_reg_path()
        # Step 1: init library 
        self.__init_reglookup()
        # Step 2: Do registry lookup
        self.__lookup_registry()
        return self.os_details

    @staticmethod
    def can_handle(os_type):
        if (os_type & OS_TYPE_WINDOWS):
            return True
        return False

os_profiler = vm_os_windows
