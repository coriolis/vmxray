/* 
    QEMU image handler 
*/

#ifndef _QEMU_IMG_H
#define _QEMU_IMG_H

#ifdef __cplusplus
extern "C" {
#endif

#define QEMU_IMG_LIB_DLL_NAME_WIN   L"qemu-img-lib.dll"
#define QEMU_IMG_LIB_DLL_NAME_LINUX   "qemu-img-lib.so.0"

    extern TSK_IMG_INFO *qemu_open(const TSK_TCHAR *, unsigned int a_ssize);

    typedef struct {
        TSK_IMG_INFO img_info;
        void *bs;
#ifdef TSK_WIN32
        HANDLE dll;
#else
        void *dll;
#endif

    } IMG_QEMU_INFO;

#ifdef __cplusplus
}
#endif
#endif
