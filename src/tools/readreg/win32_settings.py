ICONV_PATH='C:\\bin\\libiconv-1.9.2-1-lib'
ICONV_INCLUDE=ICONV_PATH + '\\include'
ICONV_LIB=ICONV_PATH + '\\lib'
INCLUDEPATH=[ICONV_INCLUDE]
#, 'C:\\Program Files\\Microsoft SDKs\\Windows\\v6.0A\\include']
VC_LIB_PATH= 'C:\\Program Files\\Microsoft Visual Studio 9.0\\VC\\lib'
PLATFORM_SDK_LIB_PATH='C:\\Program Files\\Microsoft SDKs\\Windows\\v6.0A\\lib'
LIBPATH=[VC_LIB_PATH, PLATFORM_SDK_LIB_PATH, ICONV_LIB]
LIBS=['libiconv']
