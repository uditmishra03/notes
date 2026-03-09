# AWS Interview Questions - Part 2

---

## 1. Choosing Between RDS, Aurora, DynamoDB

| Database  | Use Case                                |
| --------- | --------------------------------------- |
| RDS       | Traditional relational workloads        |
| Aurora    | High-performance relational database    |
| DynamoDB  | Scalable NoSQL workloads                |

---

## 2. DynamoDB Ideal Use Case

### Example
User session storage or high-volume event data.

### Reasons
- Low latency
- Massive scalability
- Flexible schema

---

## 3. Aurora vs RDS

### Aurora Provides
- Better performance (5x MySQL, 3x PostgreSQL)
- Multi-AZ storage replication
- Faster failover
- Auto-scaling storage

---

## 4. Consistency Models

### Aurora
Strong consistency via transactions

### DynamoDB
Eventual or strong consistency options (configurable per read)

---

## 5. IAM Role Strategy

### Typical Roles
- Administrator - Full access
- Editor - Create/Update permissions
- Viewer - Read-only access

---

## 6. Restricting S3 Access by Prefix

Use prefix-based IAM policies:

```json
{
  "Effect": "Allow",
  "Action": "s3:*",
  "Resource": "arn:aws:s3:::bucket/projectA/*"
}
```

This limits access to project-specific folders.

---

## 7. Securing API Operations with IAM

IAM policies allow specific API methods:
- Admin → full access
- Editor → update/create APIs
- Viewer → read APIs

---

## 8. Microservices Platform on AWS

### Architecture Components
- Amazon EKS
- Application Load Balancer
- Auto Scaling
- CloudWatch monitoring

---

## 9. Service Discovery in EKS

Handled using:
- Kubernetes Services
- Cluster DNS (CoreDNS)

---

## 10. Exposing Microservices

### External Access
- ALB + Ingress Controller

### Internal Access
- ClusterIP services

---

## 11. Logging and Monitoring

### Tools
- CloudWatch Logs
- Fluent Bit
- Container Insights
- Prometheus/Grafana

---

## 12. Config and Secrets Management

### ConfigMaps
For non-sensitive configuration

### Secrets
- AWS Secrets Manager
- Kubernetes Secrets
- Parameter Store

---

## 13. IAM Roles vs IAM Policies

### Policy
Defines permissions (what actions on what resources)

### Role
Entity that assumes permissions (can be assumed by services, users, or other accounts)

---

## 14. AWS Production Security Controls

### Expected Topics
- IAM least privilege
- VPC segmentation
- Security groups
- Secrets management
- Encryption at rest and in transit
- CloudTrail logging

---

## 15. How Kubernetes Integrates with AWS ALB

### Key Concepts
- ALB Ingress Controller
- Kubernetes Ingress resource
- Target group binding to pods
- Health check configuration
