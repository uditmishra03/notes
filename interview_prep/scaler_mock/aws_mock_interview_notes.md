
# AWS Mock Interview – Questions & Answers

This document summarizes the AWS-focused mock interview session, including the questions and structured answers.  
It can be used for interview preparation, revision, or reference in a GitHub repository.

---

# 1. VPC Peering vs Transit Gateway

## Question
Explain the difference between VPC Peering and AWS Transit Gateway. When would you choose one over the other?

## Answer
VPC Peering is a direct, private network connection between two VPCs. Once peered, resources can communicate using private IP addresses. It works well for simple architectures where only a few VPCs need connectivity.

However, VPC peering does not scale well because each VPC must connect individually with every other VPC.

AWS Transit Gateway acts as a centralized network hub that connects multiple VPCs and on‑premises networks. Each VPC attaches once to the gateway, and routing is centrally managed.

### When to Use
- **VPC Peering** → small environments with a few VPCs.
- **Transit Gateway** → large multi-account environments with many VPCs.

---

# 2. Limitations of VPC Peering (Transitive Routing)

## Question
Can traffic flow from VPC A to VPC C through VPC B if A is peered with B and B is peered with C?

## Answer
No. VPC Peering does not support **transitive routing**.

Example:

```
VPC A <-> VPC B <-> VPC C
```

Even though B can communicate with both A and C, A cannot communicate with C through B.

Each peering connection only allows traffic between the **two directly peered VPCs**.

---

# 3. Cost Considerations: VPC Peering vs Transit Gateway

### VPC Peering
- No hourly cost for the connection
- Only data transfer charges
- Complex mesh architecture as VPCs increase

### Transit Gateway
- Hourly attachment cost
- Data processing charges
- Simpler hub‑and‑spoke architecture

---

# 4. Security with VPC Peering and Transit Gateway

Security groups and Network ACLs still function normally.

### Security Groups
- Stateful
- Applied at instance level

### Network ACLs
- Stateless
- Applied at subnet level

Transit Gateway environments require more careful network segmentation.

---

# 5. AWS Lambda Cold Starts

A cold start occurs when Lambda must create a new execution environment before running a function.

Flow:

Request → Create environment → Initialize runtime → Load code → Execute function

Cold starts occur during first invocation, after inactivity, or during scaling.

---

# 6. Lambda Runtimes Most Affected

Java and .NET typically experience longer cold starts because the JVM/CLR must initialize.

Node.js and Python start faster due to lighter runtimes.

---

# 7. Cold Start Mitigation Strategies

- Provisioned Concurrency
- Reduce package size
- Minimize dependencies
- Use lightweight runtimes

---

# 8. Provisioned vs Reserved Concurrency

Provisioned concurrency keeps Lambda environments pre-initialized to reduce cold starts.

Reserved concurrency limits and guarantees concurrency capacity.

---

# 9. Securing API Gateway

Authorization methods include:

- IAM Authorization
- Lambda Authorizers
- Cognito User Pools
- API Keys

---

# 10. Lambda Authorizers

Flow:

Client → API Gateway → Lambda Authorizer → Token Validation → IAM Policy → Allow/Deny

---

# 11. Cognito Authorization Use Case

Best suited for authenticating **end users** such as mobile or web clients.

Cognito manages authentication and issues JWT tokens.

---

# 12. IAM Authorization with API Gateway

Requests are signed with AWS Signature V4.

IAM policies determine whether API calls are allowed.

---

# 13. SNS–SQS Fanout Pattern

Architecture:

Publisher → SNS Topic → Multiple SQS Queues → Independent Consumers

Benefits:

- Loose coupling
- Parallel processing
- Independent scaling

---

# 14. Message Durability

SQS ensures durability across multiple AZs.

Additional mechanisms:

- Visibility timeout
- Dead letter queues

---

# 15. Ordering and Deduplication

Use **SNS FIFO + SQS FIFO**.

Features:

- Message group IDs
- Deduplication IDs

---

# 16. Choosing Between RDS, Aurora, DynamoDB

RDS → traditional relational workloads.

Aurora → high-performance relational database.

DynamoDB → scalable NoSQL workloads.

---

# 17. DynamoDB Ideal Use Case

Example: user session storage or high-volume event data.

Reasons:

- Low latency
- Massive scalability
- Flexible schema

---

# 18. Aurora vs RDS

Aurora provides:

- Better performance
- Multi-AZ storage replication
- Faster failover

---

# 19. Consistency Models

Aurora → strong consistency via transactions.

DynamoDB → eventual or strong consistency options.

---

# 20. IAM Role Strategy

Roles:

- Administrator
- Editor
- Viewer

Editors → create/update  
Viewers → read-only

---

# 21. Restricting S3 Access

Use prefix-based IAM policies:

bucket/projectA/*

This limits access to project-specific folders.

---

# 22. Securing API Operations

IAM policies allow specific API methods:

Admin → full access  
Editor → update/create APIs  
Viewer → read APIs

---

# 23. Microservices Platform on AWS

Architecture:

- Amazon EKS
- Application Load Balancer
- Auto Scaling
- CloudWatch monitoring

---

# 24. Service Discovery in EKS

Handled using Kubernetes Services and cluster DNS.

---

# 25. Exposing Microservices

External → ALB + Ingress  
Internal → ClusterIP services

---

# 26. Logging and Monitoring

Tools:

- CloudWatch Logs
- Fluent Bit
- Container Insights
- Prometheus/Grafana

---

# 27. Config and Secrets

ConfigMaps → configuration

Secrets Manager / Kubernetes Secrets → sensitive data

---

# 28. Deployment Automation

CI/CD pipeline:

Build → Push to ECR → Deploy via Helm or ArgoCD

Scaling:

- Horizontal Pod Autoscaler
- Cluster Autoscaler

---

# 29. Migrating Monolithic Application

Steps:

- Lift and shift
- Move database to RDS/Aurora
- Add load balancing and scaling

---

# 30. Breaking Down the Monolith

Approach:

- Identify business domains
- Extract services
- Introduce messaging (SQS/SNS)

---

# 31. Database Migration with Minimal Downtime

Use AWS Database Migration Service.

Steps:

1. Initial data load
2. Continuous replication
3. Cutover

