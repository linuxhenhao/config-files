#!/usr/bin/env bash

cmd=/usr/local/bin/btrfs-backup.py
destdir=/media/raid1      # Mount backup disk here
snapdir=.snapshots
sourcedir=/media/u-sda1  # Mount subvolid=0 here
nbackup=30            # Keep this number of backups on $destdir
nsnap=30           # keep this number of source snapshots on $sourcedir/$snapdir

args="--num-backups $nbackup --snapshot-folder ${snapdir} --num-snapshots ${nsnap}"
echo Executing $cmd $args $sourcedir $destdir
$cmd $args $sourcedir $destdir
