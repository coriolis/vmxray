/**
 * Wrapper for qemu image functions. These functions are exported from this 
 * shared library.
 */

#include "qemu-common.h"
#include "osdep.h"
#include "block_int.h"
#include "qemu-img-lib.h"
#include <stdio.h>


/**
 * Function to open qemu image file.
 */
__declspec(dllexport) void* qemu_img_open(const char *filename)
{

    BlockDriverState *bs;
    BlockDriver *drv;
    int ret;

    bdrv_init();

    bs = bdrv_new("");
    if (!bs)
        fprintf(stderr, "Not enough memory");

    drv = NULL;
    if ((ret = bdrv_open2(bs, filename, BDRV_O_CACHE_WB, drv)) < 0) {
        fprintf(stderr, "Could not open (error: %d) '%s'", ret, filename);
    }

    return bs;
}

/**
 * Function to read qemu image.
 */
__declspec(dllexport) int qemu_img_read(void *bs, int64_t offset,
                    uint8_t *buf, size_t len)
{
    return bdrv_pread((BlockDriverState *)bs, (uint64_t)offset, buf, len);
}

/**
 * Function to get image information.
 */
__declspec(dllexport) int qemu_img_get_info(void *bs, int64_t *nsectors, 
                                    unsigned int *sect_size, int64_t *size)
{
    char fmt_name[128];

    bdrv_get_format(bs, fmt_name, sizeof(fmt_name));
    bdrv_get_geometry(bs, (uint64_t*)nsectors);
    *sect_size = 512;
    *size = *nsectors * (*sect_size);
    printf("Image info: \n"
           "Format: %s\n sectors: %lld\nVirtual Size:%lld\n",
          fmt_name, (long long int)*nsectors, (long long int)*size);
    return 0;
}
