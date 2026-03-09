# AWS DevOps Interview Practice -- Session 1

## Question 1

**Application is running on EC2 behind an ALB, but users cannot access
it. How do you troubleshoot?**

### Mind Map

    User
     │
    DNS (Route53)
     │
    ALB
     │
    Target Group
     │
    EC2 Instance
     │
    Application

### Key Pointers

1.  Verify DNS resolution in Route53.
2.  Confirm domain resolves to correct ALB.
3.  Check ALB health and access logs.
4.  Verify target group health status.
5.  Ensure security groups allow required ports.
6.  Confirm EC2 instance is reachable and application port is open.
7.  Review application logs and dependencies (DB, APIs).
8.  Check CloudWatch metrics for latency and errors.

### Final Answer

Troubleshoot by following the request path. First confirm DNS resolution
in Route53. Then check the ALB to ensure it is receiving traffic and
that target group instances are healthy. If targets are unhealthy,
verify health checks, ports, and security groups. Next check the EC2
instance to confirm the application is running and listening on the
correct port. Finally review application logs and infrastructure metrics
to identify dependency or performance issues.

------------------------------------------------------------------------

## Question 2

**Traffic suddenly increases 10x and the application becomes slow. How
would you design the system to scale automatically?**

### Mind Map

    Users
     │
    CloudFront (cache)
     │
    Route53
     │
    ALB
     │
    Auto Scaling Group
     │
    EC2 Instances
     │
    Database
     ├─ Primary
     └─ Read Replicas

### Key Pointers

1.  Place application behind an Application Load Balancer.
2.  Use an Auto Scaling Group for EC2 instances.
3.  Configure scaling policies based on CPU, request count, or custom
    metrics.
4.  Use CloudWatch alarms to trigger scaling events.
5.  Use warm pools to reduce instance launch time.
6.  Introduce caching using CloudFront or Redis.
7.  Add database read replicas to scale reads.
8.  Monitor system performance and adjust thresholds.

### Final Answer

Design the system with an ALB distributing traffic to EC2 instances in
an Auto Scaling Group. Configure scaling policies based on CPU
utilization or request count so instances automatically scale during
traffic spikes. Use CloudWatch alarms to trigger scaling events. Improve
performance with caching using CloudFront or Redis, and scale the
database using read replicas. Warm pools can be used to reduce scaling
time and improve response during sudden traffic spikes.

------------------------------------------------------------------------

## Question 3

**EC2 instance is running but you cannot SSH into it. How do you
troubleshoot?**

### Mind Map

    Laptop
     │
    Internet
     │
    Internet Gateway
     │
    Route Table
     │
    Subnet
     │
    Security Group
     │
    EC2 Instance
     │
    SSH Service

### Key Pointers

1.  Verify instance has a public IP or Elastic IP.
2.  Confirm security group allows inbound port 22.
3.  Check subnet route table routes to Internet Gateway.
4.  Validate Network ACL allows inbound and outbound traffic.
5.  Ensure correct key pair is used.
6.  Check if SSH service is running on the instance.
7.  Use EC2 Instance Connect or SSM Session Manager for access.
8.  Review system logs and SSH logs if login fails.

### Final Answer

First verify the instance has a public IP and that the security group
allows inbound SSH on port 22. Then confirm the subnet route table
routes traffic to the Internet Gateway and that the Network ACL allows
the connection. Ensure the correct key pair is used. If connectivity
still fails, use EC2 Instance Connect or SSM Session Manager to access
the instance and verify the SSH service is running and inspect system
logs.
