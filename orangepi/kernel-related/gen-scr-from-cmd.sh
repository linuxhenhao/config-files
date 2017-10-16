#!/bin/bash
# 
if [ $1'' == '' ];then
    echo $0 xxx.cmd target.scr
    exit 0
fi
mkimage -C none -A arm -T script -d $1 $2

