#!/bin/bash

check_and_run()
{
	if [ $(ps aux|grep -i $1|wc -l) == "1" ];then
		$1 &
	fi
}
programs="xcompmgr sogou-qimpanel synap volumeicon kcpss gnome-settings-daemon lxqt-policykit-agent" #nutstore"

touch ~/start-run
for i in $programs
do
   check_and_run $i
done
   

