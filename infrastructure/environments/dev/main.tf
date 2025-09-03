terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "terraform"
      Owner       = var.owner
      CostCenter  = "personal"
    }
  }
}

# Data sources
data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Local values
locals {
  availability_zones = slice(data.aws_availability_zones.available.names, 0, 2)
  
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
    Owner       = var.owner
    CostCenter  = "personal"
  }
}

# Networking
module "networking" {
  source = "../../modules/networking"

  project_name       = var.project_name
  environment        = var.environment
  aws_region         = var.aws_region
  vpc_cidr           = var.vpc_cidr
  availability_zones = local.availability_zones

  public_subnet_cidrs   = var.public_subnet_cidrs
  private_subnet_cidrs  = var.private_subnet_cidrs
  database_subnet_cidrs = var.database_subnet_cidrs

  enable_nat_gateway    = false  # Cost optimization for dev
  enable_vpc_endpoints  = false  # Cost optimization for dev

  tags = local.common_tags
}

# Database
module "database" {
  source = "../../modules/database"

  project_name    = var.project_name
  environment     = var.environment
  vpc_id          = module.networking.vpc_id
  subnet_ids      = module.networking.database_subnet_ids
  security_groups = [module.networking.database_security_group_id]

  instance_class    = "db.t3.micro"  # Free tier eligible
  allocated_storage = 20
  multi_az          = false  # Cost optimization for dev
  
  database_name = var.database_name
  username      = var.database_username
  password      = var.database_password

  backup_retention_period = 1  # Minimal backups for dev
  skip_final_snapshot    = true  # Allow easy teardown

  tags = local.common_tags
}

# EC2 Instance
resource "aws_instance" "api_server" {
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = var.instance_type
  key_name              = var.key_pair_name
  vpc_security_group_ids = [aws_security_group.ec2.id]
  subnet_id             = module.networking.public_subnet_ids[0]  # Public subnet for easy access

  user_data = templatefile("${path.module}/user_data.sh", {
    database_url = "postgresql://postgres:${var.database_password}@${module.database.endpoint}:5432/${var.database_name}"
    github_repo  = var.github_repo_url
    branch       = var.github_branch
  })

  root_block_device {
    volume_type = "gp3"
    volume_size = 20
    encrypted   = true
  }

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-${var.environment}-app-server"
  })
}

# Security Group for EC2
resource "aws_security_group" "ec2" {
  name_prefix = "${var.project_name}-${var.environment}-ec2-"
  vpc_id      = module.networking.vpc_id

  # SSH access
  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.allowed_ssh_cidrs
  }

  # HTTP access for services
  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTPS access for services
  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Direct service access for development
  ingress {
    description = "Microservices"
    from_port   = 8001
    to_port     = 8005
    protocol    = "tcp"
    cidr_blocks = var.allowed_service_cidrs
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-${var.environment}-ec2-sg"
  })

  lifecycle {
    create_before_destroy = true
  }
}

# Elastic IP for consistent access
resource "aws_eip" "api_server" {
  instance = aws_instance.api_server.id
  domain   = "vpc"

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-${var.environment}-eip"
  })

  depends_on = [module.networking]
}

# Route53 record (optional)
resource "aws_route53_record" "app" {
  count = var.domain_name != "" ? 1 : 0

  zone_id = var.route53_zone_id
  name    = "${var.domain_name}"
  type    = "A"
  ttl     = 300
  records = [aws_eip.api_server.public_ip]
}
