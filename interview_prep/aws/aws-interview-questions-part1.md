# AWS Interview Questions - Part 1

---

## 1. VPC Peering vs Transit Gateway

### Question
Explain the difference between VPC Peering and AWS Transit Gateway. When would you choose one over the other?

### Answer
VPC Peering is a direct, private network connection between two VPCs. Once peered, resources can communicate using private IP addresses. It works well for simple architectures where only a few VPCs need connectivity.

However, VPC peering does not scale well because each VPC must connect individually with every other VPC.

AWS Transit Gateway acts as a centralized network hub that connects multiple VPCs and on‑premises networks. Each VPC attaches once to the gateway, and routing is centrally managed.

### When to Use
- **VPC Peering** → small environments with a few VPCs
- **Transit Gateway** → large multi-account environments with many VPCs

---

## 2. VPC Peering Transitive Routing Limitation

### Question
Can traffic flow from VPC A to VPC C through VPC B if A is peered with B and B is peered with C?

### Answer
No. VPC Peering does not support **transitive routing**.

```
VPC A <-> VPC B <-> VPC C
```

Even though B can communicate with both A and C, A cannot communicate with C through B.

Each peering connection only allows traffic between the **two directly peered VPCs**.

---

## 3. Cost Considerations: VPC Peering vs Transit Gateway

### VPC Peering
- No hourly cost for the connection
- Only data transfer charges
- Complex mesh architecture as VPCs increase

### Transit Gateway
- Hourly attachment cost
- Data processing charges
- Simpler hub‑and‑spoke architecture

---

## 4. Security with VPC Peering and Transit Gateway

Security groups and Network ACLs still function normally.

### Security Groups
- Stateful
- Applied at instance level

### Network ACLs
- Stateless
- Applied at subnet level

Transit Gateway environments require more careful network segmentation.

---

## 5. AWS Lambda Cold Starts

A cold start occurs when Lambda must create a new execution environment before running a function.

### Flow
```
Request → Create environment → Initialize runtime → Load code → Execute function
```

Cold starts occur during:
- First invocation
- After inactivity
- During scaling

---

## 6. Lambda Runtimes Most Affected by Cold Starts

- **Java and .NET** - longer cold starts (JVM/CLR initialization)
- **Node.js and Python** - faster starts (lighter runtimes)

---

## 7. Cold Start Mitigation Strategies

- Provisioned Concurrency
- Reduce package size
- Minimize dependencies
- Use lightweight runtimes

---

## 8. Provisioned vs Reserved Concurrency

### Provisioned Concurrency
Keeps Lambda environments pre-initialized to reduce cold starts.

### Reserved Concurrency
Limits and guarantees concurrency capacity for a function.

---

## 9. Securing API Gateway

### Authorization Methods
- IAM Authorization
- Lambda Authorizers
- Cognito User Pools
- API Keys

---

## 10. Lambda Authorizers

### Flow
```
Client → API Gateway → Lambda Authorizer → Token Validation → IAM Policy → Allow/Deny
```

---

## 11. Cognito Authorization Use Case

Best suited for authenticating **end users** such as mobile or web clients.

Cognito manages authentication and issues JWT tokens.

---

## 12. IAM Authorization with API Gateway

Requests are signed with AWS Signature V4.

IAM policies determine whether API calls are allowed.

---

## 13. SNS–SQS Fanout Pattern

### Architecture
```
Publisher → SNS Topic → Multiple SQS Queues → Independent Consumers
```

### Benefits
- Loose coupling
- Parallel processing
- Independent scaling

---

## 14. SQS Message Durability

SQS ensures durability across multiple AZs.

### Additional Mechanisms
- Visibility timeout
- Dead letter queues

---

## 15. Ordering and Deduplication in SQS

Use **SNS FIFO + SQS FIFO**.

### Features
- Message group IDs
- Deduplication IDs
