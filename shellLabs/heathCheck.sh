### Create a monitoring shell script to monitor cpu, memory, and disk usage, 
### It should show warning if values goes above 80% as WARNING AND above 85-90 % as CRITICAL

#!/bin/bash
cpu=$(top -bn1 | grep Cpu | awk '{printf "%0.f" ,100 - $8}')
mem=`free | awk '/Mem/ {printf "%.0f", $3/$2 * 100}'`
disk=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')

echo "CPU Usage: $cpu%"
echo "Mem usage: $mem%"
echo "Disk usage: $disk%"

if [ $cpu -gt 80 ] || [ $mem -gt 75 ]; then
    echo "Warning HIGH CPU or MEMORY"
    echo 1
fi

if [ $disk -gt 85 ]; then
    echo "CRITICAL Disk almost full"
    exit 2
fi
echo "System is working fine!"
