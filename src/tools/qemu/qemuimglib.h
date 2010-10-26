#ifndef QEMU_IMG_LIB_H
#define QEMU_IMG_LIB_H

#ifndef WIN32
#define __declspec(x)
void* qemu_img_open(const char *);
int qemu_img_read(void *, int64_t, uint8_t *, size_t );
int qemu_img_get_info(void *, int64_t *, unsigned int *, int64_t *);
#endif

#endif
