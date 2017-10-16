#!/bin/bash
export ARCH=arm
export CROSS_COMPILE=arm-linux-gnueabihf-
export KBUILD_OUTPUT=$OUT/.tmp/linux-arm
KERNEL_SRC=linux
mkdir -p $KBUILD_OUTPUT $OUT/plus2
cp ${KERNEL_SRC}/.config ${KBUILD_OUTPUT}/

make -C $KERNEL_SRC -j8 clean
make -C $KERNEL_SRC -j8 zImage dtbs

cp -f $KBUILD_OUTPUT/arch/arm/boot/zImage $OUT/plus2/
cp -f $KBUILD_OUTPUT/.config $OUT/plus2/linux.config
cp -f $KBUILD_OUTPUT/arch/arm/boot/dts/sun8i-h3-orangepi-plus.dtb $OUT/plus2/
