#!/usr/bin/env bash

cmd=/usr/local/bin/btrfs-backup.py
destdir=/media/raid1      # Mount backup disk here
dirs=( '/media/u-sda1' )  # Backup these dirs
snapdir=.snapshots
sourcedir=/media/u-sda1  # Mount subvolid=0 here
nbackup=24            # Keep this many backups on $destdir
nsnap=20            # keep this many source snapshots on $sourcedir/$snapdir

args="--num-backups $nbackup --snapshot-folder ${d} --num-snapshots ${nsnap}"
echo Executing $cmd $args $sourcedir $destdir
$cmd $args $sourcedir $destdir
