#!/bin/bash
if [ $1'' == '' ];then
    echo $0 xxx.initrd.img uInitrd
    exit 0
fi
mkimage -A arm -T ramdisk -C none -n uInitrd -d $1 $2
