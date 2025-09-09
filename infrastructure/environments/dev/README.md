# Career Advisor - Dev Environment

This directory contains the Terraform configuration for deploying the Career Advisor microservices to a development environment on AWS.

## Architecture

The dev environment uses a **cost-optimized single-instance architecture**:

- **EC2 Instance**: Single `t3.micro` instance running all microservices via Docker Compose
- **Database**: RDS PostgreSQL `db.t3.micro` with pgvector extension
- **Networking**: Simple VPC with public subnets (no NAT Gateway for cost savings)
- **Load Balancing**: Nginx reverse proxy on the EC2 instance
- **Estimated Cost**: ~$27/month

## Quick Start

### Prerequisites

1. **AWS CLI** configured with appropriate credentials
2. **Terraform** >= 1.5.0 installed
3. **SSH Key Pair** created in your AWS region

### Deployment Steps

1. **Configure your environment**:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your values
   ```

2. **Deploy the infrastructure**:
   ```bash
   ./deploy.sh
   ```

3. **Wait for initialization** (5-10 minutes for services to start)

4. **Access your services**:
   ```bash
   # Get the public IP
   terraform output ec2_public_ip
   
   # SSH into the instance
   ssh -i ~/.ssh/YOUR_KEY.pem ec2-user@$(terraform output -raw ec2_public_ip)
   
   # Check service status
   sudo systemctl status career-advisor
   sudo docker-compose -f /opt/career-advisor/microservices/docker-services.yml ps
   ```

## Configuration

### Required Variables

Edit `terraform.tfvars` with these required values:

```hcl
# Project Configuration
project_name = "career-advisor"
environment  = "dev"
owner        = "your-name"

# AWS Configuration
aws_region = "us-west-2"

# EC2 Configuration
key_pair_name = "your-key-pair"  # Must exist in AWS

# Database Configuration
database_password = "your-secure-password"

# GitHub Repository
github_repo_url = "https://github.com/yourusername/CareerAdvisor.git"
```

### Optional Variables

```hcl
# Custom domain (requires Route53 hosted zone)
domain_name     = "yourdomain.com"
route53_zone_id = "Z1234567890ABC"

# Security (restrict access)
allowed_ssh_cidrs     = ["YOUR_IP/32"]
allowed_service_cidrs = ["YOUR_IP/32"]
```

## Service Access

After deployment, your services will be available at:

- **Main Application**: `http://PUBLIC_IP` (via Nginx)
- **Users Service**: `http://PUBLIC_IP:8001`
- **Conversations Service**: `http://PUBLIC_IP:8002`
- **Messages Service**: `http://PUBLIC_IP:8003`
- **LLM Service**: `http://PUBLIC_IP:8004`
- **Embeddings Service**: `http://PUBLIC_IP:8005`

## Management Commands

### Deployment Script Options

```bash
# Full deployment
./deploy.sh

# Show deployment plan only
./deploy.sh plan

# Show current outputs
./deploy.sh output

# Destroy infrastructure
./deploy.sh destroy
```

### Manual Terraform Commands

```bash
# Initialize
terraform init

# Plan changes
terraform plan

# Apply changes
terraform apply

# Show outputs
terraform output

# Destroy everything
terraform destroy
```

## Monitoring and Troubleshooting

### Check Service Status

```bash
# SSH into the instance
ssh -i ~/.ssh/YOUR_KEY.pem ec2-user@$(terraform output -raw ec2_public_ip)

# Check systemd service
sudo systemctl status career-advisor
sudo journalctl -u career-advisor -f

# Check Docker containers
sudo docker-compose -f /opt/career-advisor/microservices/docker-services.yml ps
sudo docker-compose -f /opt/career-advisor/microservices/docker-services.yml logs -f

# Check Nginx
sudo systemctl status nginx
sudo tail -f /var/log/nginx/access.log
```

### Database Access

```bash
# Get database connection info
terraform output database_connection_string

# Connect to database (from EC2 instance)
psql "$(terraform output -raw database_connection_string)"

# Test pgvector extension
psql -c "CREATE EXTENSION IF NOT EXISTS vector;" "$(terraform output -raw database_connection_string)"
```

### Common Issues

1. **Services not starting**: Check Docker logs and ensure database is accessible
2. **Database connection failed**: Verify security groups and RDS endpoint
3. **SSH access denied**: Check key pair name and security group rules
4. **High costs**: Ensure you're using t3.micro instances and destroy when not needed

## Cost Management

### Estimated Monthly Costs

- EC2 t3.micro: ~$8.50
- RDS db.t3.micro: ~$12.50
- Elastic IP: ~$3.65
- Storage (20GB): ~$2.00
- **Total**: ~$27/month

### Cost Optimization Tips

1. **Stop when not in use**: Stop EC2 instance to save compute costs
2. **Use free tier**: First 12 months get 750 hours free for t3.micro
3. **Monitor usage**: Set up billing alerts in AWS
4. **Clean up**: Run `./deploy.sh destroy` when done

### Stopping/Starting Services

```bash
# Stop EC2 instance (saves money)
aws ec2 stop-instances --instance-ids $(terraform output -raw ec2_instance_id)

# Start EC2 instance
aws ec2 start-instances --instance-ids $(terraform output -raw ec2_instance_id)

# Note: Public IP will change unless you have Elastic IP (included in this config)
```

## Security Considerations

### Production Readiness Checklist

- [ ] Restrict SSH access to specific IPs
- [ ] Use AWS Secrets Manager for database passwords
- [ ] Enable RDS encryption and backups
- [ ] Set up CloudWatch monitoring and alerts
- [ ] Configure proper IAM roles and policies
- [ ] Enable VPC Flow Logs
- [ ] Set up SSL/TLS certificates

### Current Security Features

- ✅ Encrypted EBS volumes
- ✅ VPC with security groups
- ✅ Database in private subnets
- ✅ Configurable access restrictions
- ⚠️ Services on public subnet (for cost optimization)

## Upgrading to Production

When ready for production, consider:

1. **Multi-AZ deployment** for high availability
2. **Application Load Balancer** instead of single instance
3. **Auto Scaling Groups** for scalability
4. **RDS Multi-AZ** for database redundancy
5. **CloudFront CDN** for static assets
6. **AWS Certificate Manager** for SSL/TLS
7. **EKS or Fargate** for container orchestration

## Support

For issues or questions:

1. Check the troubleshooting section above
2. Review Terraform and Docker logs
3. Verify AWS service limits and quotas
4. Ensure all prerequisites are met

## Cleanup

**Important**: Always destroy resources when done to avoid charges:

```bash
./deploy.sh destroy
```

This will remove all AWS resources created by this configuration.
