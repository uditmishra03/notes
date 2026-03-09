# CI/CD Architecture Interview Questions

---

## 1. Walk Through Your CI/CD Architecture for Kubernetes Deployments

### Expected Answer Flow
```
Git → Jenkins → Build → Test → Docker → Registry → Helm → ArgoCD → Kubernetes
```

### Interview Answer
"In our setup we separate CI and deployment responsibilities.
When developers push code to a feature branch, a Jenkins pipeline is triggered through a webhook.
The staging pipeline runs build validation steps including compilation, Docker image build, SonarQube static analysis, and BlackDuck security scans.

Once the code is merged, a second pipeline pushes the validated image to our artifact repository.

Deployment is handled through a separate repository where infrastructure packaging is maintained. Using Ansible automation, Helm charts are deployed to our Kubernetes clusters."

---

## 2. How Did Jenkins Shared Libraries Help Standardize Pipelines?

### Key Points
- Code reuse
- Centralized pipeline logic
- Reduced duplication
- Easier governance

### Interview Answer
"Jenkins shared libraries allowed us to standardize CI/CD pipelines across multiple microservices.
Instead of each service maintaining its own pipeline logic, we centralized the pipeline steps such as build, testing, Docker image creation, and artifact publishing into reusable Groovy functions.

Each microservice Jenkinsfile only passes parameters such as build commands or service type. The shared library executes the standardized pipeline logic, which ensures consistency and reduces duplication.

For example, backend Java services, frontend services, and Python microservices pass different build commands as parameters, but they all reuse the same pipeline framework."

---

## 3. How Did You Reduce YAML Misconfiguration by 90%?

### Expected Explanation
- Helm schema validation
- Template standardization
- GitOps version control

---

## 4. Troubleshooting a Failing CI/CD Pipeline in Jenkins

### Good Answer Path
1. Check pipeline stage logs
2. Identify failure stage
3. Check artifact repository
4. Verify dependency versions
5. Validate container build

### Interview Answer
"When a CI/CD pipeline fails, the first step is identifying the failing stage from the Jenkins pipeline logs.

If the failure is during build or test stages, we check recent code changes and dependency updates.
If the failure occurs during container image build, we validate the Dockerfile and base image availability.

We also check whether the issue is specific to one microservice or affecting multiple pipelines. If multiple pipelines fail, the issue could be in shared libraries or Jenkins infrastructure.

In some cases we manually reproduce the build on the server to verify issues like missing base images or dependency conflicts."

---

## 5. How Do You Prevent Shared Library Changes from Breaking Pipelines?

### Strategy
- Each microservice has its own pipeline
- Shared library contains reusable pipeline logic

### Safety Measures
- Version-controlled shared libraries
- Feature branches for library changes
- Regression testing before merge
- Rollback to previous working version if needed

---

## 6. CI Pipeline Stages Breakdown

### CI Pipeline
- Git Push
- Webhook trigger
- Jenkins Staging Pipeline
- Build
- Sonar Scan
- BlackDuck/Trivy Scan
- Docker Build

### Merge Pipeline
- Merge to branch
- Push Image Stage
- Artifact Repository

### Deployment
- Deployment Repo
- Ansible
- Helm Charts
- Kubernetes Cluster

---

## 7. How Do You Ensure Pipeline Reliability with 60+ Microservices?

### Key Points
- Shared libraries
- Standardized pipelines
- Quality gates
- Artifact versioning
- GitOps deployment
- Pipeline monitoring

---

## 8. CI vs CD - Clear Separation

### CI (Continuous Integration)
- Build
- Test
- Security validation
- Artifact creation

### CD (Continuous Deployment)
- Deployment automation
- Environment promotion
- Rollback capability

---

## 9. GitOps Deployment Practices

### Principles
- Git as single source of truth
- Declarative infrastructure
- Automated reconciliation
- Version control for everything

### Tools
- ArgoCD
- Flux
- Jenkins X

---

## 10. Artifact Management

### Best Practices
- Version tagging
- Immutable artifacts
- Security scanning before storage
- Retention policies

### Common Artifact Repositories
- JFrog Artifactory
- Nexus
- AWS ECR
- Harbor

---

## 11. Production Deployment Failed - How to Handle?

### Good Answer
1. Rollback deployment immediately
2. Check logs for root cause
3. Identify what changed
4. Fix pipeline or configuration
5. Re-deploy with fix

---

## 12. Secure Multi-Account AWS CI/CD Architecture

### Typical Structure
```
Dev Account
CI/CD Account
Shared Services
Production Account
```

### Pipeline Flow
```
Developer → CI pipeline → Artifact store → AssumeRole → Production deploy
```

### Benefits
- No developer production access
- Audit trail
- Controlled deployments

---

## 13. Artifact Signing

### Purpose
- Ensure artifact integrity
- Prevent tampering
- Verify trusted builds

### Tools
- AWS Signer
- cosign
- Notary
- GPG

### Pipeline Flow
```
Build → Security Scan → Sign → Store → Verify → Deploy
```

---

## 14. Preventing Pipeline Bypass

### Controls
- Remove developer production permissions
- Deploy only via CI pipeline role
- Use cross-account IAM roles
- Use SCP restrictions
- Use infrastructure as code

---

## 15. Auditing Deployments

### Monitoring Stack
- AWS CloudTrail
- CloudWatch
- AWS Config
- GuardDuty

### Centralized Architecture
```
All accounts → CloudTrail logs → Security account
```
