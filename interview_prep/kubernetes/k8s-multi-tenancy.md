# Kubernetes Multi-Tenancy Interview Questions

---

## 1. How in EKS cost is calculated for each Namespace?

### Question
If 10 teams share one EKS cluster, how would you track the cost of each namespace?

### Answer
"In a multi-tenant EKS cluster, cost attribution is typically handled using namespace labeling combined with usage metrics. Each tenant namespace is labeled with a team or cost-center identifier. Tools like Kubecost then use Prometheus metrics to map CPU, memory, storage, and network consumption back to those namespaces and translate that into cloud infrastructure cost. For cloud resources such as EBS or load balancers, AWS cost allocation tags can also be used."

---

## 2. Multi-Tenancy Architecture Decision Framework

### Namespace vs Cluster Isolation

| Approach              | Pros                           | Cons                           |
| --------------------- | ------------------------------ | ------------------------------ |
| Namespace Isolation   | Lower cost, easier management  | Weaker isolation               |
| Cluster Isolation     | Strong isolation               | Higher cost, more complexity   |

---

## 3. Hard vs Soft Multi-Tenancy

### Soft Multi-Tenancy
- Namespaces for isolation
- Trusts all tenants
- Shared control plane

### Hard Multi-Tenancy
- Stronger isolation
- Virtual clusters or separate clusters
- Zero trust between tenants

---

## 4. NetworkPolicies per Tenant

### Purpose
Isolate network traffic between namespaces

### Example - Deny all ingress except from same namespace
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-external
  namespace: tenant-a
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: tenant-a
```

---

## 5. ResourceQuota and LimitRange

### ResourceQuota
Limits total resources per namespace

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: tenant-quota
  namespace: tenant-a
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    pods: "50"
```

### LimitRange
Default and max limits for individual pods

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: tenant-limits
  namespace: tenant-a
spec:
  limits:
  - default:
      cpu: "500m"
      memory: "512Mi"
    defaultRequest:
      cpu: "100m"
      memory: "128Mi"
    type: Container
```

---

## 6. RBAC Isolation

### Per-Tenant Role
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: tenant-developer
  namespace: tenant-a
rules:
- apiGroups: ["", "apps"]
  resources: ["pods", "deployments", "services"]
  verbs: ["get", "list", "create", "update", "delete"]
```

### RoleBinding
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: tenant-a-developers
  namespace: tenant-a
subjects:
- kind: Group
  name: tenant-a-devs
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: tenant-developer
  apiGroup: rbac.authorization.k8s.io
```

---

## 7. EKS Namespace-Level Billing / Cost Allocation

### Tools
- **Kubecost** - Maps Prometheus metrics to costs
- **AWS Cost Allocation Tags** - For cloud resources
- **OpenCost** - Open source alternative

### Strategy
1. Label namespaces with cost-center
2. Use Prometheus to collect usage metrics
3. Tools translate usage to $ cost

---

## 8. Tenant Isolation Strategies

### Levels of Isolation

| Level     | Implementation                     |
| --------- | ---------------------------------- |
| Network   | NetworkPolicies                    |
| Compute   | ResourceQuotas, LimitRanges        |
| Access    | RBAC per namespace                 |
| Storage   | StorageClass per tenant            |
| Secrets   | Separate secret namespaces         |

---

## 9. Node Scaling in Multi-Tenant Clusters

### Challenges
- Fair resource distribution
- Noisy neighbor problem
- Cost attribution

### Solutions
- Node pools per tenant
- Priority classes
- Resource quotas

---

## 10. Cost vs Security Tradeoffs

### Shared Cluster (Lower Cost)
- Namespace isolation
- NetworkPolicies
- ResourceQuotas
- RBAC

### Separate Clusters (Higher Security)
- Complete isolation
- Separate control planes
- Independent scaling
- Compliance requirements

---

## 11. Multi-Tenancy Architecture Mock Questions

1. How do you prevent one tenant from consuming all cluster resources?
2. How do you isolate network traffic between tenants?
3. How do you handle tenant-specific secrets?
4. How do you bill back infrastructure costs to teams?
5. When would you choose cluster isolation over namespace isolation?
