#!/bin/bash
###
#It should:
#
#Print IP address.
#
#Print default gateway.
#
#Check connectivity to 8.8.8.8.
#
#Check DNS resolution of google.com.
#
#List listening ports.
#
#Print firewall status (ufw or iptables).
#
#Log output with timestamp.


log() {
    echo -e "$(date '+%F-%T'):: $1"
}

log "Fetching Ip address..."
ip -4 addr show scope global | awk '{print $2}' | cut -d/ -f1

log "Fetching Default address..."
ip route | awk '/default/ {print $3}'

log "Checking connectivity with 8.8.8.8..."
ping -c2 8.8.8.8 &> /dev/null
if [ "$?" -eq 0 ]; then
    log "Connection OK"
else
    log "Connection FAILED"
fi


log "Checking DNS resolution..."
nslookup google.com &> /dev/null
if [ "$?" -eq 0 ]; then
    log "DNS resolution OK"
else
    log "DNS resolution FAILED"
fi

log "Listening Services: "
ss -tulpn

log "Firewall status:"
if command -v ufw &> /dev/null; then
    ufw status
else
    iptable -L -n v 
fi
