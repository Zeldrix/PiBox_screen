#!/bin/bash

#On teste si il y a plusieurs paramètres
#On continue le prgm si il n'y a qu'un paramètre
if [ $# -gt "1" ]; then
  exit 0
fi

disk=$1

status=$(sudo mdadm --detail /dev/md0 | grep $disk)
state=$(echo $status | cut -d' ' -f5)

#echo "Status du disque $disk : $state"

if [ "$state" = "active" ]; then
  exit 1 #Disque OK
else
  exit 2 #Disque en erreur
fi
