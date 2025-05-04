#!/usr/bin/env bash
IP=$1
if [ -z "$IP" ]; then
  echo "Usage: $0 <IP>"
  exit 1
fi

/usr/bin/sudo /usr/sbin/ufw deny from "$IP"
/usr/bin/sudo /usr/sbin/ufw reload
echo "IP $IP blocked successfully."