# Docker Networking Interview Questions

---

## 1. Why Can Containers Sniff Traffic on Same Bridge Network?

### Docker Bridge Network Architecture

```
┌─────────────────────────────────────────────────────┐
│                    HOST                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │Container1│  │Container2│  │Container3│          │
│  │  eth0    │  │  eth0    │  │  eth0    │          │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘          │
│       │             │             │                 │
│       │  veth pair  │  veth pair  │  veth pair     │
│       │             │             │                 │
│  ┌────┴─────────────┴─────────────┴────┐           │
│  │           docker0 bridge             │           │
│  │      (Layer 2 broadcast domain)      │           │
│  └──────────────────┬──────────────────┘           │
│                     │                               │
│              ┌──────┴──────┐                        │
│              │  eth0 (host)│                        │
│              └─────────────┘                        │
└─────────────────────────────────────────────────────┘
```

### Why Sniffing Is Possible
The `docker0` bridge behaves like a **Layer 2 switch/hub**:
1. **Shared broadcast domain** - All containers on same bridge share L2 segment
2. **ARP is visible** - Containers can see ARP requests from neighbors
3. **Promiscuous mode** - Container with `NET_RAW` capability can enable promiscuous mode
4. **tcpdump works** - Tools like tcpdump can capture all traffic on the bridge

---

## 2. Docker Networking Components

| Component              | Function                                        |
| ---------------------- | ----------------------------------------------- |
| **veth pair**          | Virtual ethernet - connects container to bridge |
| **docker0**            | Default Linux bridge for containers             |
| **Network namespace**  | Isolated network stack per container            |
| **NET_RAW capability** | Allows raw socket operations (sniffing)         |

---

## 3. How to Isolate Container Traffic

### Method 1: Separate Docker Networks (Recommended)
```bash
# Create isolated networks
docker network create app-network
docker network create db-network

# Run containers on separate networks
docker run --network app-network app-container
docker run --network db-network db-container
```

**Why it works:** Each network has its own bridge - no shared L2 domain.

### Method 2: Drop Network Capabilities
```bash
docker run --cap-drop=NET_RAW --cap-drop=NET_ADMIN myimage
```

| Capability  | What it allows                  |
| ----------- | ------------------------------- |
| `NET_RAW`   | Raw sockets, packet sniffing    |
| `NET_ADMIN` | Network configuration, iptables |

### Method 3: Macvlan Networking
```bash
docker network create -d macvlan \
  --subnet=192.168.1.0/24 \
  --gateway=192.168.1.1 \
  -o parent=eth0 \
  macvlan-net
```

### Method 4: Kubernetes Network Policies
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

### Method 5: Encrypted Overlay Networks (Docker Swarm)
```bash
docker network create --opt encrypted --driver overlay secure-net
```

---

## 4. Macvlan Networking Deep Dive

### How Macvlan Works
Macvlan assigns each container:
- **Unique MAC address**
- **Unique IP address**
- **Direct connection to physical network**

### Why Sniffing is Prevented
- No shared bridge
- Each container is a separate L2 entity
- Physical switch handles traffic forwarding

### Creating Macvlan Network
```bash
docker network create -d macvlan \
  --subnet=192.168.1.0/24 \
  --gateway=192.168.1.1 \
  -o parent=eth0 \
  my-macvlan

docker run --network my-macvlan --ip 192.168.1.100 nginx
```

### Important Limitation
**Containers CANNOT communicate with the host by default!**

### Macvlan Modes

| Mode         | Behavior                                   |
| ------------ | ------------------------------------------ |
| **bridge**   | Containers can communicate with each other |
| **vepa**     | Traffic goes to external switch and back   |
| **private**  | Containers are completely isolated         |
| **passthru** | Single container gets direct NIC access    |

---

## 5. When to Use Macvlan

✅ **Good for:**
- Legacy applications requiring specific IPs
- Applications that need to appear as physical hosts
- High-performance networking (no bridge overhead)

❌ **Avoid when:**
- Containers need to talk to host frequently
- Running in cloud (most clouds limit MAC addresses)
- You need simple container-to-container communication

---

## 6. Docker Network Types Summary

| Network Type | Use Case                        |
| ------------ | ------------------------------- |
| bridge       | Default, container to container |
| host         | Share host network stack        |
| overlay      | Multi-host (Swarm/K8s)          |
| macvlan      | Direct physical network access  |
| none         | No networking                   |

---

## 7. Best Practice Recommendation for Production

1. **Always use custom networks** (never default bridge)
2. **Drop NET_RAW capability** by default
3. **Use network policies** in Kubernetes
4. **Encrypt overlay traffic** for multi-host
