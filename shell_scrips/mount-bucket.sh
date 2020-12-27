#!/bin/bash
# This script mounts everything you need: Bucket, LST, LSD, Bucket's Scratch, and Tigress

MNTUSER=$1

echo $MNTUSER

# Put the following (appropriately edited) alias in your .bashrc folder to create the command 'mnt'
# alias mnt='/bin/mount-bucket.sh jduva'


sudo umount /home/wanglab/mounts/wang
sudo umount /home/wanglab/mounts/LightSheetTransfer
sudo umount /home/wanglab/mounts/LightSheetData
sudo umount /home/wanglab/mounts/scratch/jduva
sudo umount /home/wanglab/mounts/tigress

sudo mount -t cifs //bucket.pni.princeton.edu/wang /home/wanglab/mounts/wang -o user=$MNTUSER,dom=PRINCETON,iocharset=utf8,rw,file_mode=0664,dir_mode=0775,nolinux,noperm,vers=2.1

sudo mount -t cifs //bucket.pni.princeton.edu/wang_mkislin /home/wanglab/mounts/wang_mkislin -o user=$MNTUSER,dom=PRINCETON,iocharset=utf8,rw,file_mode=0664,dir_mode=0775,nolinux,noperm,vers=2.1

sudo mount -t cifs //bucket.pni.princeton.edu/LightSheetTransfer /home/wanglab/mounts/LightSheetTransfer -o user=$MNTUSER,dom=PRINCETON,iocharset=utf8,rw,file_mode=0664,dir_mode=0775,nolinux,noperm,vers=2.1

sudo mount -t cifs //bucket.pni.princeton.edu/LightSheetData /home/wanglab/mounts/LightSheetData -o user=$MNTUSER,dom=PRINCETON,iocharset=utf8,rw,file_mode=0664,dir_mode=0775,nolinux,noperm,vers=2.1

sudo mount -t cifs //sink.pni.princeton.edu/scratch/jduva /home/wanglab/mounts/scratch/jduva -o username=$MNTUSER,domain=PRINCETON,iocharset=utf8,rw,file_mode=0664,dir_mode=0775,nolinux,noperm,vers=2.1

sudo mount -t cifs //tigress-cifs.princeton.edu /home/wanglab/mounts/tigress -o user=$MNTUSER,dom=PRINCETON,iocharset=utf8,rw,file_mode=0664,dir_mode=0775,nolinux,noperm,vers=2.1
