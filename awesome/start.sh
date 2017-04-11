#!/bin/bash

check_and_run()
{
	if [ $(ps aux|grep -i $1|wc -l) == "0" ];then
		$1 &
	fi
}
programs="xcompmgr sogou-qimpanel synap volumeicon" #nutstore"

for i in $programs
do
   check_and_run $i
done
   

