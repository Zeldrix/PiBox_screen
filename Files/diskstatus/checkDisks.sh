#!/bin/bash

disks=("/dev/sda1" "/dev/sdb1")
files=("/SMB/Pibox_screen/diskstatus/disk1.txt" "/SMB/Pibox_screen/diskstatus/disk2.txt")

for i in ${!disks[@]};
do
  disk=${disks[$i]}
  /SMB/Pibox_screen/diskstatus/diskStatus.sh $disk
  echo $? > ${files[$i]}
done
