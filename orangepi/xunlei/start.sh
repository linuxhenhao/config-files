#!/bin/bash
#start thunder

while [ x$(pidof ETMDaemon) = x"" ];
do
    ./portal
    sleep 15
done
    
