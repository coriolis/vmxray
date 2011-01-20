
# VM-XRay tools makefile
QEMU_DIR := src/tools/qemu
TSK_DIR := src/tools/sleuthkit
READ_REG_DIR := src/tools/readreg
TSK_TOOL_DIR := tools/fstools
VS_TOOL_DIR := tools/vstools
SRC_LIB_DIR := src/lib
SRC_BIN_DIR := src/bin
SRC_CONF_DIR := src/conf
TARGET = qemu
TARGET += sleuthkit
TARGET += readreg 
BUILD_DIR := build
TMP_BUILD_DIR := /tmp/.vmxray_build
LOCAL_DIR := /usr/local
#TOOLS_NAME=blkcalc blkcat blkls blkstat ffind fls fsstat icat ifind ils istat jcat jls
TOOLS_NAME=fls icat 

.PHONY: all
all:	$(TARGET)

.PHONY: install
install:	all
	cp ${TMP_BUILD_DIR}/lib/qemu-img-lib.so.0 ${BUILD_DIR}/bin
	cp ${READ_REG_DIR}/libreglookuplib.so ${BUILD_DIR}/bin/reglookup
	cp ${READ_REG_DIR}/libreglookuplib.so ${BUILD_DIR}/bin/reglookuplib
	cp ${TSK_DIR}/${TSK_TOOL_DIR}/icat ${BUILD_DIR}/bin
	cp ${TSK_DIR}/${TSK_TOOL_DIR}/fls ${BUILD_DIR}/bin
	cp ${TSK_DIR}/${VS_TOOL_DIR}/mmls ${BUILD_DIR}/bin
	find ${BUILD_DIR}/bin -name '*.o'  -delete
	find ${BUILD_DIR}/bin -name '*.cpp' -delete
	rm -rf ${BUILD_DIR}/bin/Makefile*
	cp -r ${SRC_LIB_DIR}/* ${BUILD_DIR}/lib
	cp ${SRC_BIN_DIR}/*.py ${BUILD_DIR}/bin/
	cp ${SRC_BIN_DIR}/inspect_vm ${BUILD_DIR}/bin/
	mkdir -p ${BUILD_DIR}/tmp	
	cp ${SRC_CONF_DIR}/*.conf ${BUILD_DIR}/bin/

qemu:
	cd $(QEMU_DIR) ;\
		./configure --target-list=x86_64-softmmu,i386-softmmu 
	make -C $(QEMU_DIR) -j3 qemu-img-lib.so.0
	mkdir -p ${TMP_BUILD_DIR}/lib
	mkdir -p ${TMP_BUILD_DIR}/include
	mkdir -p ${BUILD_DIR}/bin
	mkdir -p ${BUILD_DIR}/lib
	cp ${QEMU_DIR}/qemu-img-lib.so.0 ${TMP_BUILD_DIR}/lib 
	cp ${QEMU_DIR}/qemu-img-lib.h ${TMP_BUILD_DIR}/include 

sleuthkit:
	cd $(TSK_DIR) ; \
		./configure --with-qemuimglib=${TMP_BUILD_DIR} --without-afflib \
		--without-libewf
	make -C $(TSK_DIR) -j3

readreg:
	cd $(READ_REG_DIR) ; scons

.PHONY: clean
clean:
	make -C $(QEMU_DIR) clean distclean
	make -C $(TSK_DIR) distclean
	make -C $(READ_REG_DIR) clean
	rm -rf ${BUILD_DIR}
	rm -rf ${TMP_BUILD_DIR}
