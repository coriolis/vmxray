/*
 * Windows specific and missing definitions
 */

#ifndef _WIN_SPECIFIC_H_
#define _WIN_SPECIFIC_H_

#ifdef _WIN32

#define DLL_EXPORT __declspec(dllexport) 

#define bool unsigned char
#define false 0
#define true 1

#define snprintf _snprintf
#define strcasecmp _stricmp
#define lseek _lseek

#else
#define DLL_EXPORT  
#endif

#endif 
