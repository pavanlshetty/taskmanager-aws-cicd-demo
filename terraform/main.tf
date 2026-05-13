data "aws_ami" "amazon_linux" {
  most_recent = true

  filter {
    name   = "name"
    values = ["al2023-ami-minimal-*-x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["137112412989"] # Amazon
}

# Get the default VPC
data "aws_vpc" "default" {
  default = true
}

# Create a subnet in the default VPC
resource "aws_subnet" "taskmanager_subnet" {
  vpc_id                  = data.aws_vpc.default.id
  cidr_block              = "172.31.0.0/20"
  availability_zone       = data.aws_availability_zones.available.names[0]
  map_public_ip_on_launch = true

  tags = {
    Name = "taskmanager-subnet"
  }
}

# Get available AZs
data "aws_availability_zones" "available" {
  state = "available"
}

resource "aws_security_group" "ec2_sg" {
  name        = "taskmanager-app-sg"
  description = "Security group for Task Manager EC2"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "taskmanager-app-sg"
  }
}

resource "aws_instance" "app_server" {
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = var.instance_type
  key_name               = var.key_name
  subnet_id              = aws_subnet.taskmanager_subnet.id
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]
  associate_public_ip_address = true

  tags = {
    Name = "TaskManagerAppServer"
  }
}