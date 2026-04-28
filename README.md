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
- EC2 instance (Ubuntu)
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

```bash
# Generate SSH key pair
ssh-keygen -t rsa -b 2048 -f ~/.ssh/taskmanager-app-key -N ""

# Import public key to AWS
# Go to EC2 Console → Key Pairs → Import key pair
# Name: taskmanager-app-key
# Paste contents of ~/.ssh/taskmanager-app-key.pub
```

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
- Change region in `terraform/variables.tf` (try us-west-2)
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
- SSH into EC2: `ssh -i ~/.ssh/taskmanager-app-key ubuntu@<ec2-ip>`
- Check if Docker installed: `docker --version`
- Manual fix: `sudo apt update && sudo apt install -y docker.io`

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