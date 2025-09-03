#!/bin/bash

# Career Advisor Dev Environment Deployment Script
# This script deploys the development environment to AWS using Terraform

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="career-advisor"
ENVIRONMENT="dev"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if Terraform is installed
    if ! command -v terraform &> /dev/null; then
        log_error "Terraform is not installed. Please install Terraform first."
        exit 1
    fi
    
    # Check if AWS CLI is installed
    if ! command -v aws &> /dev/null; then
        log_error "AWS CLI is not installed. Please install AWS CLI first."
        exit 1
    fi
    
    # Check if AWS credentials are configured
    if ! aws sts get-caller-identity &> /dev/null; then
        log_error "AWS credentials are not configured. Please run 'aws configure' first."
        exit 1
    fi
    
    # Check if terraform.tfvars exists
    if [ ! -f "$SCRIPT_DIR/terraform.tfvars" ]; then
        log_error "terraform.tfvars not found. Please copy terraform.tfvars.example to terraform.tfvars and update with your values."
        exit 1
    fi
    
    log_success "All prerequisites met!"
}

estimate_costs() {
    log_info "Estimated monthly costs for dev environment:"
    echo "  • EC2 t3.micro instance: ~$8.50"
    echo "  • RDS db.t3.micro instance: ~$12.50"
    echo "  • Elastic IP: ~$3.65"
    echo "  • Storage (20GB GP3): ~$2.00"
    echo "  • Data transfer: ~$1.00"
    echo "  ─────────────────────────────"
    echo "  • Total estimated: ~$27.65/month"
    echo ""
    log_warning "Actual costs may vary based on usage and AWS pricing changes."
}

init_terraform() {
    log_info "Initializing Terraform..."
    cd "$SCRIPT_DIR"
    terraform init
    log_success "Terraform initialized!"
}

validate_terraform() {
    log_info "Validating Terraform configuration..."
    terraform validate
    log_success "Terraform configuration is valid!"
}

plan_deployment() {
    log_info "Creating deployment plan..."
    terraform plan -out=tfplan
    log_success "Deployment plan created!"
}

apply_deployment() {
    log_info "Applying deployment..."
    terraform apply tfplan
    log_success "Deployment completed!"
}

show_outputs() {
    log_info "Deployment outputs:"
    terraform output
}

cleanup_plan() {
    if [ -f "tfplan" ]; then
        rm tfplan
        log_info "Cleaned up temporary plan file"
    fi
}

show_next_steps() {
    echo ""
    log_info "Next steps:"
    echo "1. Wait 5-10 minutes for the EC2 instance to fully initialize"
    echo "2. Check the application status:"
    echo "   ssh -i ~/.ssh/YOUR_KEY.pem ec2-user@\$(terraform output -raw ec2_public_ip)"
    echo "   sudo systemctl status career-advisor"
    echo "3. View application logs:"
    echo "   sudo journalctl -u career-advisor -f"
    echo "4. Access your services:"
    terraform output service_urls
    echo ""
    log_warning "Remember to destroy resources when done: terraform destroy"
}

# Main deployment flow
main() {
    echo "========================================"
    echo "Career Advisor Dev Environment Deployment"
    echo "========================================"
    echo ""
    
    check_prerequisites
    estimate_costs
    
    # Confirm deployment
    read -p "Do you want to proceed with the deployment? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Deployment cancelled."
        exit 0
    fi
    
    # Execute deployment steps
    init_terraform
    validate_terraform
    plan_deployment
    
    # Final confirmation before applying
    echo ""
    log_warning "About to create AWS resources. This will incur costs!"
    read -p "Continue with deployment? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        cleanup_plan
        log_info "Deployment cancelled."
        exit 0
    fi
    
    apply_deployment
    show_outputs
    cleanup_plan
    show_next_steps
    
    log_success "Dev environment deployment completed successfully!"
}

# Handle script arguments
case "${1:-}" in
    "destroy")
        log_warning "Destroying dev environment..."
        cd "$SCRIPT_DIR"
        terraform destroy
        log_success "Dev environment destroyed!"
        ;;
    "plan")
        check_prerequisites
        init_terraform
        validate_terraform
        plan_deployment
        cleanup_plan
        ;;
    "output")
        cd "$SCRIPT_DIR"
        show_outputs
        ;;
    "")
        main
        ;;
    *)
        echo "Usage: $0 [plan|destroy|output]"
        echo "  plan    - Show deployment plan without applying"
        echo "  destroy - Destroy the deployed infrastructure"
        echo "  output  - Show deployment outputs"
        echo "  (no args) - Full deployment"
        exit 1
        ;;
esac
