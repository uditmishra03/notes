# Linux Troubleshooting Interview Questions

---

## 1. Server CPU Spikes to 100% - What to Check?

### Expected Flow
```bash
top / htop
ps aux
check logs
identify offending process
kill or restart service
```

### Commands
```bash
# Real-time process monitoring
top
htop

# List all processes sorted by CPU
ps aux --sort=-%cpu | head -20

# Check system load
uptime

# Check what's running
ps -ef | grep <process_name>
```

---

## 2. Identify Which Process Is Using a Port

### Commands
```bash
lsof -i :8080
netstat -tulpn | grep 8080
ss -tulpn | grep 8080
```

### Output Example
```
COMMAND   PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
nginx    1234 root   6u  IPv4  12345      0t0  TCP *:8080
```

---

## 3. Debug a Disk Full Issue

### Commands
```bash
# Check disk usage
df -h

# Find large directories
du -sh *
du -sh /* | sort -hr | head -20

# Find large files
find / -size +1G -type f 2>/dev/null

# Find files modified in last day
find / -mtime -1 -size +100M
```

---

## 4. Process States Reference

| State | Meaning               |
| ----- | --------------------- |
| R     | Running or runnable   |
| S     | Interruptible sleep   |
| D     | Uninterruptible sleep |
| T     | Stopped               |
| Z     | Zombie (defunct)      |

---

## 5. Finding Zombie Processes

```bash
# List zombie processes
ps -eo pid,ppid,state,comm | awk '$3=="Z"'

# Get unique parent PIDs
ps -eo pid,ppid,state | awk '$3=="Z"{print $2}' | sort -u
```

---

## 6. Mapping PID to Service

### Method 1: systemctl
```bash
systemctl status <pid>
```

### Method 2: cgroup
```bash
cat /proc/<pid>/cgroup
```

### Method 3: Process tree
```bash
pstree -sp <pid>
```

---

## 7. Memory Troubleshooting

### Commands
```bash
# Memory usage overview
free -h

# Detailed memory info
cat /proc/meminfo

# Top memory consumers
ps aux --sort=-%mem | head -10

# Check for OOM killer
dmesg | grep -i "killed process"
```

---

## 8. Network Troubleshooting

### Check connectivity
```bash
ping <host>
traceroute <host>
```

### Check DNS
```bash
nslookup <domain>
dig <domain>
```

### Check listening ports
```bash
ss -tulpn
netstat -tulpn
```

### Check connections
```bash
ss -tan
netstat -an
```

---

## 9. Log Analysis

### Common log locations
```bash
/var/log/syslog       # System logs
/var/log/messages     # General messages
/var/log/auth.log     # Authentication logs
/var/log/kern.log     # Kernel logs
journalctl            # Systemd journal
```

### Useful commands
```bash
# Follow logs in real-time
tail -f /var/log/syslog

# Search for errors
grep -i error /var/log/syslog

# Recent systemd logs
journalctl -xe
journalctl -u <service> --since "1 hour ago"
```

---

## 10. Service Management

```bash
# Check service status
systemctl status <service>

# Start/Stop/Restart
systemctl start <service>
systemctl stop <service>
systemctl restart <service>

# Enable/Disable at boot
systemctl enable <service>
systemctl disable <service>

# List failed services
systemctl --failed
```

---

## 11. File Permissions

### Permission bits
```
r = 4 (read)
w = 2 (write)
x = 1 (execute)
```

### Common commands
```bash
# Change permissions
chmod 755 file
chmod u+x file

# Change owner
chown user:group file

# View permissions
ls -la
```

---

## 12. System Information

```bash
# OS version
cat /etc/os-release
uname -a

# Hardware info
lscpu
lsmem
lsblk

# Running kernel
uname -r
```

---

## 13. Process Management

```bash
# List processes
ps aux
ps -ef

# Kill process
kill <pid>        # SIGTERM (graceful)
kill -9 <pid>     # SIGKILL (force)

# Find process by name
pgrep <name>
pidof <name>
```

---

## 14. System Performance

```bash
# CPU info
mpstat
vmstat

# IO stats
iostat
iotop

# System activity
sar
```

---

## 15. Quick Troubleshooting Checklist

| Issue          | First Commands to Run              |
| -------------- | ---------------------------------- |
| High CPU       | `top`, `ps aux --sort=-%cpu`       |
| High Memory    | `free -h`, `ps aux --sort=-%mem`   |
| Disk Full      | `df -h`, `du -sh *`                |
| Network Issue  | `ping`, `ss -tulpn`, `traceroute`  |
| Service Down   | `systemctl status`, `journalctl`   |
| Port in Use    | `lsof -i :<port>`, `ss -tulpn`     |
