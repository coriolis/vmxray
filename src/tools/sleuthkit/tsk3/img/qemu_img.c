/* 
  Handler for QEMU image reading 
*/
#include "tsk_img_i.h"
#include "qemu_img.h"

#ifdef TSK_WIN32
#include <windows.h>
#else
#include <dlfcn.h>
#define _countof(x) ((sizeof(x))/sizeof(x[0]))
#endif

typedef void * (* qemu_img_open_t)(const char *filename);
typedef int (* qemu_img_read_t)(void *, int64_t offset, uint8_t *buf, size_t len);
typedef int (* qemu_img_get_info_t)(void *, int64_t *nsectors, 
                                    unsigned int *sect_size, int64_t *size);

qemu_img_open_t qemu_img_open = NULL;
qemu_img_read_t qemu_img_read = NULL;
qemu_img_get_info_t qemu_img_get_info = NULL;

/* Load DLL/shared library for QEMU stubs */
int qemu_load_lib(IMG_QEMU_INFO *qemu_info)
{
#ifdef TSK_WIN32
    HANDLE hd = INVALID_HANDLE_VALUE;
    
    hd = LoadLibrary(QEMU_IMG_LIB_DLL_NAME_WIN);
    if(hd == NULL)
    {
        fprintf(stderr, "Failed to load library %ls, error %ld \n",
                QEMU_IMG_LIB_DLL_NAME_WIN, GetLastError());
        return -1;
    }
    qemu_info->dll = hd;

    qemu_img_read = (qemu_img_read_t) GetProcAddress(hd, "qemu_img_read");
    if(qemu_img_read == NULL)
    {
        fprintf(stderr, "Failed to load symbol 'qemu_img_read' from library %ls, error %ld \n",
                QEMU_IMG_LIB_DLL_NAME_WIN, GetLastError());
        return -1;
    }

    qemu_img_open = (qemu_img_open_t)GetProcAddress(hd, "qemu_img_open");
    if(qemu_img_open == NULL)
    {
        fprintf(stderr, "Failed to load symbol 'qemu_img_open' from library %ls, error %ld \n",
                QEMU_IMG_LIB_DLL_NAME_WIN, GetLastError());
        return -1;
    }
    qemu_img_get_info = (qemu_img_get_info_t)GetProcAddress(hd, "qemu_img_get_info");
    if(qemu_img_get_info == NULL)
    {
        fprintf(stderr, "Failed to load symbol 'qemu_img_get_info' from library %ls, error %ld \n",
                QEMU_IMG_LIB_DLL_NAME_WIN, GetLastError());
        return -1;
    }
#else
    void *hd = NULL;
    char *error;

    hd = dlopen(QEMU_IMG_LIB_DLL_NAME_LINUX, RTLD_LAZY);
    if (!hd) {
        fprintf(stderr, "Failed to load library %s due to %s",
                QEMU_IMG_LIB_DLL_NAME_LINUX, dlerror());
        return -1;
    }
    qemu_info->dll = hd;
    
    qemu_img_read = (qemu_img_read_t)dlsym(hd, "qemu_img_read");
    if ((error = dlerror()) != NULL) {
        fprintf(stderr, "Failed to load symbol 'qemu_img_read' from library"
                " %s, error %s \n",
                QEMU_IMG_LIB_DLL_NAME_LINUX, error);
        return -1;
    }

    qemu_img_open = (qemu_img_open_t)dlsym(hd, "qemu_img_open");
    if ((error = dlerror()) != NULL) {
        fprintf(stderr, "Failed to load symbol 'qemu_img_open' from library"
                " %s, error %s \n",
                QEMU_IMG_LIB_DLL_NAME_LINUX, error);
        return -1;
    }
    
    qemu_img_get_info = (qemu_img_get_info_t)dlsym(hd, "qemu_img_get_info");
    if ((error = dlerror()) != NULL) {
        fprintf(stderr, "Failed to load symbol 'qemu_img_get_info' from library"
                " %s, error %s \n",
                QEMU_IMG_LIB_DLL_NAME_LINUX, error);
        return -1;
    }
#endif

    return 0;
}

/* Image close */
void qemu_close(TSK_IMG_INFO * img_info)
{
    IMG_QEMU_INFO *qemu_info = (IMG_QEMU_INFO *) img_info;

#ifdef TSK_WIN32
    FreeLibrary(qemu_info->dll);
#else
    dlclose(qemu_info->dll);
#endif

    free(qemu_info);
}

/* Read */
ssize_t qemu_read(TSK_IMG_INFO * img_info, TSK_OFF_T offset, char *buf, 
                  size_t len)
{
    IMG_QEMU_INFO *qemu_info = (IMG_QEMU_INFO *) img_info;
    return qemu_img_read(qemu_info->bs, offset, (uint8_t*)buf, len);
}

/* Open and init image through QEMU */
TSK_IMG_INFO *qemu_open(const TSK_TCHAR * image, unsigned int a_ssize)
{

    IMG_QEMU_INFO *qemu_info;
    TSK_IMG_INFO *img_info;
    int64_t sectors = 0;
    char filename[4096];

    if ((qemu_info =
            (IMG_QEMU_INFO *) tsk_malloc(sizeof(IMG_QEMU_INFO))) == NULL)
        return NULL;

    if(qemu_load_lib(qemu_info))
    {
        printf("Failed to load qemu DLL \n");
        return NULL;
    }
    img_info = (TSK_IMG_INFO *) qemu_info;

    img_info->itype = TSK_IMG_TYPE_QEMU;
    img_info->read = qemu_read;
    img_info->close = qemu_close;

    //qemu does not take widechar, convert to char
    if(sizeof(TSK_TCHAR) > sizeof(char))
        snprintf(filename, _countof(filename), "%ls", image);
    else
        snprintf(filename, _countof(filename), "%s", image);
    
    //open qemu 
    qemu_info->bs = qemu_img_open(filename);

    //get required img info
    qemu_img_get_info(qemu_info->bs, &sectors, &img_info->sector_size, &img_info->size);

    return img_info;
}
