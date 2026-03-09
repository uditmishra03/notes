# Terraform Interview Questions

---

## 1. Why Do We Store Terraform State Remotely?

### Expected Answer
- Collaboration between team members
- Prevent state corruption
- Team access
- State locking capability

---

## 2. Why is DynamoDB Used with Terraform State in S3?

### Key Concept
- State locking
- Prevent concurrent execution
- Avoid race conditions

### How It Works
Before running `terraform apply`, Terraform tries to acquire a lock on the state file.
- If Engineer A has the lock, Engineer B cannot modify the state and the operation is blocked
- Once the apply completes, the lock is released

---

## 3. Two Engineers Run `terraform apply` Simultaneously - What Happens?

### Answer
Terraform uses state locking to prevent concurrent modifications.

Before running terraform apply, Terraform tries to acquire a lock on the state file.
- If Engineer A has the lock, Engineer B cannot modify the state and the operation is blocked or fails.
- Once the apply completes, the lock is released.

In AWS, we typically store state in S3 and use DynamoDB for distributed locking.

This prevents race conditions, state corruption, and conflicting infrastructure changes.

---

## 4. What Are Terraform Modules and Why Are They Useful?

### Expected Answer
- Reusable infrastructure code
- Standardized environment creation
- DRY principle for infrastructure
- Encapsulation of best practices

---

## 5. Why Not Let Developers Create Infra Manually from AWS Console?

### Problems with Manual Creation
- No version control
- No audit trail
- Configuration drift
- Inconsistent environments
- No reproducibility

### Benefits of Terraform
- Infrastructure as Code
- Version controlled
- Peer reviewed changes
- Consistent environments
- Automated deployment

---

## 6. What is Terraform Drift and How Do You Handle It?

### What is Drift?
Terraform drift happens when infrastructure is modified outside Terraform — for example manual console changes.

### Detection
Drift is detected using `terraform plan`, where Terraform compares:
- The real infrastructure state
- Against the Terraform state file
- And the desired configuration in code

### Handling Drift
Once detected, we decide whether the manual change was intentional or not:
- If unintended → run `terraform apply` to reconcile back to desired state
- If intentional → update Terraform code or import the change so state and code stay aligned

---

## 7. Terraform State File Security

### Best Practices
- Store in encrypted S3 bucket
- Enable versioning
- Restrict access via IAM
- Never commit to git
- Use state locking

---

## 8. Terraform Workspaces

### Use Case
- Multiple environments (dev, staging, prod)
- Same configuration, different state

### Commands
```bash
terraform workspace new dev
terraform workspace select prod
terraform workspace list
```

---

## 9. Terraform Import

### Use Case
Bring existing infrastructure under Terraform management

### Command
```bash
terraform import aws_instance.example i-1234567890abcdef0
```

### Steps
1. Write resource block in .tf file
2. Run terraform import
3. Run terraform plan to verify

---

## 10. Terraform Lifecycle Rules

### Common Rules
```hcl
lifecycle {
  create_before_destroy = true
  prevent_destroy = true
  ignore_changes = [tags]
}
```

### Use Cases
- Zero downtime updates
- Protect critical resources
- Ignore external changes

---

## 11. Terraform Remote Backend Configuration

### S3 Backend Example
```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

---

## 12. Terraform Variables and Outputs

### Variable Types
- string
- number
- bool
- list
- map
- object

### Variable Precedence (lowest to highest)
1. Default values
2. Environment variables
3. terraform.tfvars
4. *.auto.tfvars
5. -var and -var-file

---

## 13. Terraform Data Sources

### Use Case
Reference existing resources not managed by Terraform

### Example
```hcl
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]
  
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}
```

---

## 14. Terraform Provisioners

### Types
- local-exec: Run command on local machine
- remote-exec: Run command on remote resource

### Best Practice
Use provisioners as last resort. Prefer:
- User data scripts
- Configuration management tools (Ansible, Chef)

---

## 15. Terraform Best Practices

1. Use remote state with locking
2. Use modules for reusability
3. Use workspaces for environments
4. Version lock providers
5. Use .tfvars for environment-specific values
6. Implement CI/CD for Terraform
7. Use terraform fmt and validate
8. Review plans before apply
