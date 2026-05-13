# Task Manager CI/CD with AWS

## Project Overview

This project demonstrates a complete end-to-end CI/CD pipeline for deploying a **Task Manager web application** built with Python Flask on AWS using GitHub Actions, Docker, Terraform, and Ansible. The application allows users to create, view, edit, complete, and delete tasks with a modern web interface.

It's designed to showcase DevOps skills for professional resumes and interviews, featuring a realistic web application with database persistence, proper UI/UX, and production-ready deployment.

## Architecture

The pipeline automates the following flow:

1. **Code Push**: Developer pushes code to GitHub main branch
2. **CI Build**: GitHub Actions builds and pushes Docker image to Docker Hub
3. **Infrastructure Provisioning**: Terraform creates AWS resources (VPC, EC2, ALB)
4. **Configuration Management**: Ansible installs Docker and deploys the container on EC2
5. **Deployment**: Task Manager application is accessible via ALB DNS

### Application Features:
- **Task CRUD Operations**: Create, read, update, delete tasks
- **Task Status Management**: Mark tasks as complete/incomplete
- **Database Persistence**: SQLite database for data storage
- **Responsive UI**: Bootstrap-based modern web interface
- **Form Validation**: WTForms for secure form handling
- **Flash Messages**: User feedback for all operations

### AWS Resources Created:
- VPC with public subnet
- EC2 instance (Amazon Linux 2023) - login as `ec2-user`
- Application Load Balancer
- Security groups
- Target group and listener

## Local Development Setup

### Quick Start (Automated)
1. **Windows Command Prompt:**
   ```cmd
   cd d:\DevOps\DevOpsCopilotProject
   run_local.bat
   ```

2. **PowerShell:**
   ```powershell
   cd d:\DevOps\DevOpsCopilotProject
   .\run_local.ps1
   ```

### Manual Setup
1. **Check Environment:**
   ```bash
   cd d:\DevOps\DevOpsCopilotProject\app
   python check_setup.py
   ```

2. **Create Virtual Environment:**
   ```bash
   python -m venv venv
   # Windows: venv\Scripts\activate
   # Linux/Mac: source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r app/requirements.txt
   ```

4. **Run Application:**
   ```bash
   cd app
   python app.py
   ```

5. **Access Application:**
   - Open browser: `http://localhost:5000`
   - Test all features: Add, edit, complete, delete tasks

### Docker Setup
```bash
# Build and run with Docker
docker build -f docker/Dockerfile -t taskmanager-local .
docker run -p 5000:5000 taskmanager-local
```

### Troubleshooting
- **Python not found:** Install Python 3.9+ from python.org
- **Pip issues:** Update pip with `python -m pip install --upgrade pip`
- **Port 5000 busy:** Change port in app.py or stop other services
- **Permission errors:** Run terminal as administrator or use different directory

## STEP-BY-STEP SETUP AND EXECUTION GUIDE

### 1. Prerequisites Setup

#### AWS Account Setup
1. Go to https://aws.amazon.com/ and create a free account
2. Complete account verification and enable billing
3. Note your account ID for future reference

#### IAM User Creation
1. Log into AWS Console → IAM → Users → Create user
2. User name: `taskmanager-cicd-user`
3. Select "Access key - Programmatic access"
4. Attach existing policies:
   - `AmazonEC2FullAccess`
   - `AmazonVPCFullAccess`
   - `IAMFullAccess`
5. Create user and **SAVE** the Access Key ID and Secret Access Key (you won't see them again!)

#### Tools Installation
Install these tools on your local machine:

**Windows (using Chocolatey or manual):**
```powershell
# AWS CLI
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi

# Terraform
choco install terraform

# Ansible
pip install ansible

# Docker Desktop
# Download from https://www.docker.com/products/docker-desktop

# Python 3.9+
# Download from https://www.python.org/

# Git
choco install git
```

**Verify installations:**
```bash
aws --version
terraform --version
ansible --version
docker --version
python --version
git --version
```

### 2. GitHub Setup

#### Create Repository
1. Go to https://github.com → New repository
2. Repository name: `taskmanager-aws-cicd-demo`
3. Make it **public** (required for Docker Hub integration)
4. **DO NOT** initialize with README (we have our own)
5. Create repository

#### Clone and Push Code
```bash
cd d:\DevOps
git clone https://github.com/yourusername/taskmanager-aws-cicd-demo.git
cd taskmanager-aws-cicd-demo
# Copy all files from DevOpsCopilotProject to this directory
copy-item ..\DevOpsCopilotProject\* . -recurse -force
git add .
git commit -m "Initial commit: Task Manager CI/CD pipeline"
git push origin main
```

### 3. Secrets & Variables Setup

In your GitHub repository:
1. Go to Settings → Secrets and variables → Actions
2. Add these **Repository secrets**:

| Secret Name | Value |
|-------------|-------|
| `AWS_ACCESS_KEY_ID` | Your AWS access key from IAM user |
| `AWS_SECRET_ACCESS_KEY` | Your AWS secret key from IAM user |
| `DOCKER_USERNAME` | Your Docker Hub username |
| `DOCKER_PASSWORD` | Your Docker Hub password or access token |
| `SSH_PRIVATE_KEY` | Contents of your private SSH key file (see SSH setup below) |
| `KEY_NAME` | `taskmanager-app-key` (name of your EC2 key pair) |

### 4. SSH Key Pair Setup

This is critical for the CI/CD pipeline to connect to your EC2 instance. Follow these steps carefully.

#### Step 4.1: Generate SSH Key Pair Locally

1. Open Git Bash or Windows PowerShell
2. Run the following commands:

```bash
# Create .ssh directory if it doesn't exist
mkdir -p ~/.ssh

# Generate RSA key pair (2048-bit recommended)
ssh-keygen -t rsa -b 2048 -f ~/.ssh/taskmanager-app-key -N ""

# Verify the key was created
ls -la ~/.ssh/taskmanager-app-key*
```

This creates:
- `~/.ssh/taskmanager-app-key` (private key)
- `~/.ssh/taskmanager-app-key.pub` (public key)

#### Step 4.2: Import Public Key to AWS EC2

1. Open AWS Console → EC2 → Key Pairs
2. Click "Import key pair"
3. Name: `taskmanager-app-key` (must match exactly)
4. Open the public key file and copy its contents:

```bash
cat ~/.ssh/taskmanager-app-key.pub
```

5. Paste the entire public key content (starts with `ssh-rsa`, ends with your username)
6. Click "Import key pair"

#### Step 4.3: Verify Key Pair in AWS

- Go back to EC2 → Key Pairs
- Confirm `taskmanager-app-key` appears in the list
- Note: The key pair must be in the same AWS region as your Terraform deployment (default: `us-east-1`)

#### Step 4.4: Set Up GitHub Secrets

1. Go to your GitHub repository → Settings → Secrets and variables → Actions
2. Add these secrets:

| Secret Name | Value |
|-------------|-------|
| `SSH_PRIVATE_KEY` | Contents of `~/.ssh/taskmanager-app-key` (private key file) |
| `KEY_NAME` | `taskmanager-app-key` |

**Important:** For `SSH_PRIVATE_KEY`:
- Open the private key file: `cat ~/.ssh/taskmanager-app-key`
- Copy the entire content including `-----BEGIN OPENSSH PRIVATE KEY-----` and `-----END OPENSSH PRIVATE KEY-----`
- Paste exactly into the GitHub secret (no extra spaces or line breaks)

#### Step 4.5: Test SSH Connection Locally (Optional but Recommended)

After Terraform creates the EC2 instance, test the connection:

```bash
# Get the EC2 public IP from Terraform outputs or AWS Console
# Replace <EC2_PUBLIC_IP> with actual IP

ssh -i ~/.ssh/taskmanager-app-key -o StrictHostKeyChecking=no ec2-user@<EC2_PUBLIC_IP>

# If successful, you should see:
# Warning: Permanently added '<EC2_PUBLIC_IP>' (EC2) to the list of known hosts.
# [ec2-user@ip-xxx-xx-xx-xxx ~]$
```

#### Step 4.6: Troubleshooting SSH Issues

**Error: "Load key ... error in libcrypto"**
- The private key file is corrupted or has wrong format
- Regenerate the key pair and re-import to AWS
- Update GitHub secret with new private key content

**Error: "Permission denied (publickey)"**
- Key pair name mismatch: Ensure EC2 instance uses `taskmanager-app-key`
- Wrong private key in GitHub secret: Verify the secret contains the exact private key content
- Region mismatch: Key pair and instance must be in same region

**Error: "Connection refused"**
- Security group doesn't allow SSH: Ensure port 22 is open from 0.0.0.0/0
- Instance not running: Check EC2 instance state in AWS Console

**To verify key fingerprints:**
```bash
# Local private key fingerprint
ssh-keygen -lf ~/.ssh/taskmanager-app-key

# Should match the public key fingerprint in AWS Console
```

**If you need to recreate the key pair:**
```bash
# Delete old key pair from AWS Console
# Delete local keys: rm ~/.ssh/taskmanager-app-key*
# Repeat steps 4.1-4.4
# Update Terraform and redeploy
```

### 4.7 Verify Key Pair, GitHub Secret, and Rebuild EC2 Instance

#### Verify the EC2 instance key pair name
1. Open AWS Console → EC2 → Instances
2. Select the instance provisioned by Terraform
3. In the Description panel, check `Key pair name`
4. Confirm it exactly matches `taskmanager-app-key`

#### Verify the GitHub secret
1. Open GitHub repository → Settings → Secrets and variables → Actions
2. Confirm `KEY_NAME` is `taskmanager-app-key`
3. Confirm `SSH_PRIVATE_KEY` contains the full private key content from `~/.ssh/taskmanager-app-key`

To verify locally:
```bash
ssh-keygen -y -f ~/.ssh/taskmanager-app-key
```
If this command prints a public key, the file is valid.

#### Rebuild the instance correctly with Terraform
If the running EC2 instance is using the wrong key pair, destroy and recreate it:

```bash
cd terraform
terraform init
terraform destroy -auto-approve -var="key_name=taskmanager-app-key"
terraform apply -auto-approve -var="key_name=taskmanager-app-key"
```

If you want to preserve state, ensure the same `KEY_NAME` secret is set and the same AWS region is used by both GitHub Actions and Terraform.

### 5. Docker Hub Setup

1. Go to https://hub.docker.com/ and create account if needed
2. Create new repository: `taskmanager-app`
3. Make it **public**
4. The pipeline will automatically push images here

### 6. Terraform Backend Setup

For this demo, we're using local state (no remote backend needed). In production, you'd configure S3 backend.

### 7. End-to-End Execution

#### Step 1: Local Testing (Optional but Recommended)
```bash
cd d:\DevOps\DevOpsCopilotProject

# Option 1: Use the automated setup script (Recommended)
# For Windows Command Prompt:
run_local.bat

# For PowerShell:
.\run_local.ps1

# Option 2: Manual setup
cd app
python check_setup.py  # Verify environment
python app.py

# Visit http://localhost:5000 to access the Task Manager
# You can add, edit, complete, and delete tasks

# Option 3: Test with Docker
cd ..
docker build -f docker/Dockerfile -t test-taskmanager .
docker run -p 5000:5000 test-taskmanager
```

#### Step 2: Trigger the Pipeline
1. Make sure all secrets are set in GitHub
2. Push any change to `main` branch, or manually trigger workflow:
   - Go to Actions tab in GitHub
   - Click the workflow
   - Click "Run workflow"

#### Step 3: Monitor Pipeline Execution
Watch the GitHub Actions logs. The pipeline will:
1. **Build Job (~2-3 minutes)**:
   - Checkout code ✓
   - Build Docker image ✓
   - Push to Docker Hub ✓

2. **Deploy Job (~10-15 minutes)**:
   - Configure AWS credentials ✓
   - Terraform init/plan/apply (creates infrastructure) ✓
   - Extract outputs (ALB DNS, EC2 IP) ✓
   - Setup Ansible inventory ✓
   - Run Ansible playbook (install Docker, deploy app) ✓
   - Output public URL ✓

#### Step 4: Verify Deployment
- In the pipeline output, find: `Application deployed at: http://<alb-dns>`
- Visit that URL in your browser to access the Task Manager application
- Test the application:
  - View the task dashboard
  - Add a new task using the "Add Task" button
  - Edit existing tasks
  - Mark tasks as complete/incomplete
  - Delete tasks
- API endpoints still available:
  - `http://<alb-dns>/health` → `{"status": "healthy", "service": "Task Manager API"}`
  - `http://<alb-dns>/version` → `{"version": "1.0.0", "service": "Task Manager"}`

### 8. Troubleshooting Guide

#### Common Errors & Fixes:

**1. AWS Credentials Error**
```
Error: Unable to locate credentials
```
- Check secrets are set correctly in GitHub
- Verify IAM user permissions
- Regenerate AWS keys if needed

**2. Docker Push Fails**
```
denied: access forbidden
```
- Verify DOCKER_USERNAME and DOCKER_PASSWORD
- Check if Docker Hub repo exists and is public
- Try creating a new access token in Docker Hub

**3. Terraform Apply Fails**
```
Error: creating EC2 Instance: InsufficientInstanceCapacity
```
- Change region in `terraform/variables.tf` to `us-east-1` if needed
- Check AWS limits in EC2 console

**4. SSH Connection Issues**
```
Failed to connect to the host via ssh
```
- Verify KEY_NAME secret matches your EC2 key pair name
- Check SSH_PRIVATE_KEY is the full private key content
- Ensure EC2 security group allows SSH (22) from 0.0.0.0/0

**5. Ansible Playbook Fails**
```
docker: command not found
```
- SSH into EC2: `ssh -i ~/.ssh/taskmanager-app-key ec2-user@<ec2-ip>`
- Check if Docker installed: `docker --version`
- Manual fix: `sudo yum update -y && sudo yum install -y docker`

#### Debugging Steps:
1. Check GitHub Actions detailed logs
2. SSH into EC2 instance using the IP from Terraform outputs
3. View application logs: `docker logs flask-app`
4. Check EC2 system logs in AWS Console
5. Clean up and retry: `terraform destroy`

#### Cost Management:
- Monitor costs in AWS Billing console
- Destroy resources when done: `terraform destroy`
- t2.micro costs ~$8/month if left running

## CI/CD Flow Explanation

1. **Build Job**: Checks out code, builds Docker image, pushes to Docker Hub
2. **Deploy Job**:
   - Configures AWS credentials
   - Runs Terraform to provision infrastructure
   - Extracts ALB DNS and EC2 IP from Terraform outputs
   - Sets up Ansible inventory with EC2 IP
   - Runs Ansible playbook to deploy the application
   - Outputs the public URL

## Security Notes

- In production, restrict SSH access to specific IPs
- Use private Docker repositories
- Implement proper IAM roles instead of access keys
- Add monitoring and logging

## Destroy Infrastructure Pipeline

This repository now includes a second GitHub Actions workflow named `Destroy Infrastructure` that removes all Terraform-managed AWS resources created by the deploy pipeline.

### How to run it
1. Go to your repository `Actions` tab in GitHub.
2. Select the `Destroy Infrastructure` workflow.
3. Click `Run workflow` and choose the branch to use.
4. The workflow will:
   - checkout code
   - authenticate to AWS using `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
   - initialize Terraform in `./terraform`
   - run `terraform destroy -auto-approve`

### Required secrets
Make sure these repository secrets are set:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `KEY_NAME`

> The destroy workflow uses the same Terraform configuration and S3 backend as the deploy workflow, so it will remove the exact infrastructure previously provisioned.

## Sample Repository Link

https://github.com/yourusername/taskmanager-aws-cicd-demo

Replace `yourusername` with your actual GitHub username.