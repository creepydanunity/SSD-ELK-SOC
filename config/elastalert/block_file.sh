#!/usr/bin/env bash

FILE_PATH=$1
SOURCE_IP=$2

# Block the source IP 
if [ -n "$SOURCE_IP" ]; then
  echo "Blocking IP: $SOURCE_IP"
  /usr/bin/sudo /usr/sbin/ufw deny from "$SOURCE_IP"
  /usr/bin/sudo /usr/sbin/ufw reload
  echo "IP $SOURCE_IP blocked successfully."
else
  echo "No IP provided, skipping IP blocking."
fi

# Delete the file 
if [ -e "$FILE_PATH" ]; then
  echo "Deleting file: $FILE_PATH"
  rm -f "$FILE_PATH"
  echo "File $FILE_PATH deleted successfully."
else
  echo "File $FILE_PATH not found."
fi
