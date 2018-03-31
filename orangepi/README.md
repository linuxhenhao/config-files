# These are some personal scripts and config files for orangepi vps
---------

file name | function
--------------------------
bakseafile.sh | using btrfsbackup.py to backup files 
btrfsbackup.py | python script using btrfs send and receive to backup snapshot
cron.py | a simple script to run tasks periodicly
seafile.py | seafile startup script
xunlei.py | xunlei xware startup script


# some details
--------
btrfsbackup.py is comming from other programer's github repo, copy right info
is in the top part of the file.

cron.py has a little difference with the Linux system's default one. If our
machine was down for a period of time, and a cron job missed, after bootup,
this script will check the log file and get this info, run the missed job.
