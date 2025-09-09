# Dev Environment Outputs

# EC2 Instance Information
output "ec2_instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.api_server.id
}

output "ec2_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_eip.api_server.public_ip
}

output "ec2_private_ip" {
  description = "Private IP address of the EC2 instance"
  value       = aws_instance.api_server.private_ip
}

output "ec2_public_dns" {
  description = "Public DNS name of the EC2 instance"
  value       = aws_instance.api_server.public_dns
}

# Application URLs
output "application_url" {
  description = "Main application URL"
  value       = var.domain_name != "" ? "https://${var.domain_name}" : "http://${aws_eip.api_server.public_ip}"
}

output "service_urls" {
  description = "Direct URLs to microservices for development"
  value = {
    users_service         = "http://${aws_eip.api_server.public_ip}:8001"
    conversations_service = "http://${aws_eip.api_server.public_ip}:8002"
    messages_service     = "http://${aws_eip.api_server.public_ip}:8003"
    llm_service          = "http://${aws_eip.api_server.public_ip}:8004"
    embeddings_service   = "http://${aws_eip.api_server.public_ip}:8005"
  }
}

# Database Information
output "database_endpoint" {
  description = "RDS instance endpoint"
  value       = module.database.endpoint
}

output "database_port" {
  description = "RDS instance port"
  value       = module.database.port
}

output "database_name" {
  description = "Database name"
  value       = module.database.database_name
}

output "database_username" {
  description = "Database master username"
  value       = module.database.username
}

output "database_connection_string" {
  description = "Database connection string"
  value       = module.database.connection_string
  sensitive   = true
}

# Networking Information
output "vpc_id" {
  description = "ID of the VPC"
  value       = module.networking.vpc_id
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = module.networking.public_subnet_ids
}

output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value       = module.networking.private_subnet_ids
}

# SSH Access Information
output "ssh_command" {
  description = "SSH command to connect to the EC2 instance"
  value       = "ssh -i ~/.ssh/${var.key_pair_name}.pem ec2-user@${aws_eip.api_server.public_ip}"
}

# Cost Tracking
output "estimated_monthly_cost" {
  description = "Estimated monthly cost breakdown"
  value = {
    ec2_instance = "~$8.50 (t3.micro)"
    rds_instance = "~$12.50 (db.t3.micro)"
    eip          = "~$3.65"
    storage      = "~$2.00 (20GB GP3)"
    total        = "~$26.65/month"
  }
}
