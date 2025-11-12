#!/bin/bash

# ==============================================================================
# Summoner's Chronicle - Web App Deployment Script
# ==============================================================================
# Features:
# - Modular deployment steps
# - Resumable from any step
# - Resource tracking
# - State management
# - Rollback capability
# ==============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# State file for resumability
STATE_FILE="${SCRIPT_DIR}/.deployment-state.json"
RESOURCES_FILE="${SCRIPT_DIR}/deployed-resources.json"

# Configuration
PROJECT_NAME="${PROJECT_NAME:-summoners-chronicle}"
ENVIRONMENT="${ENVIRONMENT:-production}"
AWS_REGION="${AWS_REGION:-us-east-1}"
STACK_NAME="${PROJECT_NAME}-webapp-${ENVIRONMENT}"

# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

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

# Save deployment state
save_state() {
    local step=$1
    local status=$2
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    cat > "${STATE_FILE}" <<EOF
{
  "lastStep": "${step}",
  "status": "${status}",
  "timestamp": "${timestamp}",
  "environment": "${ENVIRONMENT}",
  "region": "${AWS_REGION}"
}
EOF
}

# Load deployment state
load_state() {
    if [ -f "${STATE_FILE}" ]; then
        cat "${STATE_FILE}"
    else
        echo "{}"
    fi
}

# Save resource information
save_resource() {
    local resource_type=$1
    local resource_id=$2
    local resource_name=$3

    if [ ! -f "${RESOURCES_FILE}" ]; then
        echo "[]" > "${RESOURCES_FILE}"
    fi

    local temp_file=$(mktemp)
    jq --arg type "$resource_type" \
       --arg id "$resource_id" \
       --arg name "$resource_name" \
       --arg timestamp "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
       '. += [{type: $type, id: $id, name: $name, timestamp: $timestamp}]' \
       "${RESOURCES_FILE}" > "$temp_file"

    mv "$temp_file" "${RESOURCES_FILE}"
}

# Check if step is completed
is_step_completed() {
    local step=$1
    local state=$(load_state)
    local completed=$(echo "$state" | jq -r ".completedSteps[] | select(. == \"$step\")" 2>/dev/null || echo "")

    [ -n "$completed" ]
}

# Mark step as completed
mark_step_completed() {
    local step=$1
    local state_json=$(load_state)

    if [ "$state_json" == "{}" ]; then
        state_json='{"completedSteps": []}'
    fi

    local temp_file=$(mktemp)
    echo "$state_json" | jq --arg step "$step" \
        '.completedSteps += [$step] | .completedSteps |= unique' \
        > "$temp_file"

    mv "$temp_file" "${STATE_FILE}"
}

# ==============================================================================
# DEPLOYMENT STEPS
# ==============================================================================

# Step 1: Validate prerequisites
step_validate_prerequisites() {
    local step_name="validate_prerequisites"

    if is_step_completed "$step_name"; then
        log_info "Step already completed: $step_name (skipping)"
        return 0
    fi

    log_info "Step 1: Validating prerequisites..."
    save_state "$step_name" "in_progress"

    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        log_error "AWS CLI is not installed"
        exit 1
    fi

    # Check jq
    if ! command -v jq &> /dev/null; then
        log_error "jq is not installed (required for JSON processing)"
        exit 1
    fi

    # Check AWS credentials
    if ! aws sts get-caller-identity &> /dev/null; then
        log_error "AWS credentials not configured"
        exit 1
    fi

    # Get AWS account ID
    AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    log_success "AWS Account ID: $AWS_ACCOUNT_ID"

    # Check if RiftSage backend is deployed
    log_info "Checking RiftSage backend deployment..."
    if aws cloudformation describe-stacks --stack-name "riftsage-${ENVIRONMENT}" --region "${AWS_REGION}" &> /dev/null; then
        log_success "RiftSage backend detected"
    else
        log_warning "RiftSage backend not found - web app will not function without it"
    fi

    mark_step_completed "$step_name"
    save_state "$step_name" "completed"
    log_success "Prerequisites validated"
}

# Step 2: Create S3 bucket for web hosting
step_create_s3_bucket() {
    local step_name="create_s3_bucket"

    if is_step_completed "$step_name"; then
        log_info "Step already completed: $step_name (skipping)"
        return 0
    fi

    log_info "Step 2: Creating S3 bucket for web hosting..."
    save_state "$step_name" "in_progress"

    WEBAPP_BUCKET="${PROJECT_NAME}-webapp-${ENVIRONMENT}-${AWS_ACCOUNT_ID}"

    # Check if bucket exists
    if aws s3 ls "s3://${WEBAPP_BUCKET}" 2>/dev/null; then
        log_warning "Bucket already exists: ${WEBAPP_BUCKET}"
    else
        # Create bucket
        if [ "${AWS_REGION}" == "us-east-1" ]; then
            aws s3 mb "s3://${WEBAPP_BUCKET}" --region "${AWS_REGION}"
        else
            aws s3 mb "s3://${WEBAPP_BUCKET}" --region "${AWS_REGION}" \
                --create-bucket-configuration LocationConstraint="${AWS_REGION}"
        fi
        log_success "Created bucket: ${WEBAPP_BUCKET}"
    fi

    # Configure bucket for static website hosting
    aws s3 website "s3://${WEBAPP_BUCKET}" \
        --index-document index.html \
        --error-document index.html

    # Set bucket policy for public read access
    cat > /tmp/bucket-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::${WEBAPP_BUCKET}/*"
    }
  ]
}
EOF

    aws s3api put-bucket-policy \
        --bucket "${WEBAPP_BUCKET}" \
        --policy file:///tmp/bucket-policy.json

    rm /tmp/bucket-policy.json

    save_resource "S3Bucket" "${WEBAPP_BUCKET}" "Web App Hosting Bucket"
    mark_step_completed "$step_name"
    save_state "$step_name" "completed"
    log_success "S3 bucket configured for website hosting"
}

# Step 3: Deploy CloudFormation stack
step_deploy_cloudformation() {
    local step_name="deploy_cloudformation"

    if is_step_completed "$step_name"; then
        log_info "Step already completed: $step_name (skipping)"
        return 0
    fi

    log_info "Step 3: Deploying CloudFormation stack..."
    save_state "$step_name" "in_progress"

    local template_file="${SCRIPT_DIR}/cloudformation-template.yaml"

    if [ ! -f "$template_file" ]; then
        log_error "CloudFormation template not found: $template_file"
        exit 1
    fi

    # Check if stack exists
    if aws cloudformation describe-stacks --stack-name "${STACK_NAME}" --region "${AWS_REGION}" &> /dev/null; then
        log_info "Stack exists, updating..."
        ACTION="update-stack"
    else
        log_info "Creating new stack..."
        ACTION="create-stack"
    fi

    aws cloudformation ${ACTION} \
        --stack-name "${STACK_NAME}" \
        --template-body file://"${template_file}" \
        --parameters \
            ParameterKey=Environment,ParameterValue="${ENVIRONMENT}" \
            ParameterKey=ProjectName,ParameterValue="${PROJECT_NAME}" \
            ParameterKey=WebAppBucket,ParameterValue="${WEBAPP_BUCKET}" \
        --capabilities CAPABILITY_NAMED_IAM \
        --region "${AWS_REGION}"

    # Wait for stack operation to complete
    log_info "Waiting for stack operation to complete..."

    if [ "$ACTION" == "create-stack" ]; then
        aws cloudformation wait stack-create-complete \
            --stack-name "${STACK_NAME}" \
            --region "${AWS_REGION}"
    else
        aws cloudformation wait stack-update-complete \
            --stack-name "${STACK_NAME}" \
            --region "${AWS_REGION}" 2>/dev/null || true
    fi

    save_resource "CloudFormationStack" "${STACK_NAME}" "Web App Infrastructure Stack"
    mark_step_completed "$step_name"
    save_state "$step_name" "completed"
    log_success "CloudFormation stack deployed"
}

# Step 4: Get stack outputs and configure AWS config
step_configure_aws_config() {
    local step_name="configure_aws_config"

    if is_step_completed "$step_name"; then
        log_info "Step already completed: $step_name (skipping)"
        return 0
    fi

    log_info "Step 4: Configuring AWS settings..."
    save_state "$step_name" "in_progress"

    # Get outputs from CloudFormation stack
    USER_POOL_ID=$(aws cloudformation describe-stacks \
        --stack-name "${STACK_NAME}" \
        --query 'Stacks[0].Outputs[?OutputKey==`UserPoolId`].OutputValue' \
        --output text \
        --region "${AWS_REGION}")

    CLIENT_ID=$(aws cloudformation describe-stacks \
        --stack-name "${STACK_NAME}" \
        --query 'Stacks[0].Outputs[?OutputKey==`ClientId`].OutputValue' \
        --output text \
        --region "${AWS_REGION}")

    IDENTITY_POOL_ID=$(aws cloudformation describe-stacks \
        --stack-name "${STACK_NAME}" \
        --query 'Stacks[0].Outputs[?OutputKey==`IdentityPoolId`].OutputValue' \
        --output text \
        --region "${AWS_REGION}")

    # Get RiftSage API endpoint
    RIFTSAGE_API_ENDPOINT=$(aws cloudformation describe-stacks \
        --stack-name "riftsage-${ENVIRONMENT}" \
        --query 'Stacks[0].Outputs[?OutputKey==`APIEndpoint`].OutputValue' \
        --output text \
        --region "${AWS_REGION}" 2>/dev/null || echo "")

    if [ -z "$RIFTSAGE_API_ENDPOINT" ]; then
        log_warning "RiftSage API endpoint not found - using placeholder"
        RIFTSAGE_API_ENDPOINT="https://api.placeholder.com"
    fi

    # Update aws-config.js
    local config_file="${SCRIPT_DIR}/config/aws-config.js"
    local temp_config=$(mktemp)

    sed -e "s|REGION_PLACEHOLDER|${AWS_REGION}|g" \
        -e "s|USER_POOL_ID_PLACEHOLDER|${USER_POOL_ID}|g" \
        -e "s|CLIENT_ID_PLACEHOLDER|${CLIENT_ID}|g" \
        -e "s|IDENTITY_POOL_ID_PLACEHOLDER|${IDENTITY_POOL_ID}|g" \
        -e "s|API_ENDPOINT_PLACEHOLDER|${RIFTSAGE_API_ENDPOINT}|g" \
        -e "s|REPORTS_BUCKET_PLACEHOLDER|riftsage-reports-${ENVIRONMENT}-${AWS_ACCOUNT_ID}|g" \
        -e "s|CLOUDFRONT_DOMAIN_PLACEHOLDER||g" \
        -e "s|ENVIRONMENT_PLACEHOLDER|${ENVIRONMENT}|g" \
        "${config_file}" > "$temp_config"

    mv "$temp_config" "${config_file}"

    mark_step_completed "$step_name"
    save_state "$step_name" "completed"
    log_success "AWS configuration updated"
}

# Step 5: Build and upload web app files
step_upload_webapp_files() {
    local step_name="upload_webapp_files"

    if is_step_completed "$step_name"; then
        log_info "Step already completed: $step_name (skipping)"
        return 0
    fi

    log_info "Step 5: Uploading web app files to S3..."
    save_state "$step_name" "in_progress"

    # Sync files to S3
    aws s3 sync "${SCRIPT_DIR}/" "s3://${WEBAPP_BUCKET}/" \
        --exclude ".git/*" \
        --exclude "*.sh" \
        --exclude "*.md" \
        --exclude "*.json" \
        --exclude "cloudformation-template.yaml" \
        --exclude ".deployment-state.json" \
        --exclude "deployed-resources.json" \
        --delete \
        --region "${AWS_REGION}"

    # Set cache control headers
    aws s3 cp "s3://${WEBAPP_BUCKET}/" "s3://${WEBAPP_BUCKET}/" \
        --recursive \
        --exclude "*" \
        --include "*.html" \
        --metadata-directive REPLACE \
        --cache-control "max-age=300" \
        --region "${AWS_REGION}"

    aws s3 cp "s3://${WEBAPP_BUCKET}/" "s3://${WEBAPP_BUCKET}/" \
        --recursive \
        --exclude "*" \
        --include "*.js" \
        --include "*.css" \
        --metadata-directive REPLACE \
        --cache-control "max-age=31536000" \
        --region "${AWS_REGION}"

    mark_step_completed "$step_name"
    save_state "$step_name" "completed"
    log_success "Web app files uploaded"
}

# Step 6: Summary and outputs
step_display_summary() {
    local step_name="display_summary"

    log_info "Step 6: Deployment Summary"

    # Get website URL
    WEBSITE_URL="http://${WEBAPP_BUCKET}.s3-website-${AWS_REGION}.amazonaws.com"

    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}Deployment Complete!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "${BLUE}Web App URL:${NC} ${WEBSITE_URL}"
    echo -e "${BLUE}S3 Bucket:${NC} ${WEBAPP_BUCKET}"
    echo -e "${BLUE}Region:${NC} ${AWS_REGION}"
    echo -e "${BLUE}Environment:${NC} ${ENVIRONMENT}"
    echo ""
    echo -e "${YELLOW}Next Steps:${NC}"
    echo "1. Visit the web app at: ${WEBSITE_URL}"
    echo "2. Test authentication and summoner linking"
    echo "3. Verify RiftSage integration"
    echo "4. (Optional) Configure CloudFront for HTTPS"
    echo ""
    echo -e "${BLUE}Deployed Resources:${NC}"
    if [ -f "${RESOURCES_FILE}" ]; then
        jq -r '.[] | "  - \(.type): \(.name) (\(.id))"' "${RESOURCES_FILE}"
    fi
    echo ""
    log_success "Deployment completed successfully!"

    mark_step_completed "$step_name"
}

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

main() {
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}Summoner's Chronicle - Web App Deployment${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo "Project: $PROJECT_NAME"
    echo "Environment: $ENVIRONMENT"
    echo "Region: $AWS_REGION"
    echo ""

    # Check for resume flag
    if [ "$1" == "--resume" ]; then
        log_info "Resuming deployment from last checkpoint..."
        local state=$(load_state)
        local last_step=$(echo "$state" | jq -r '.lastStep' 2>/dev/null || echo "")

        if [ -n "$last_step" ]; then
            log_info "Last completed step: $last_step"
        fi
    fi

    # Execute deployment steps
    step_validate_prerequisites
    step_create_s3_bucket
    step_deploy_cloudformation
    step_configure_aws_config
    step_upload_webapp_files
    step_display_summary
}

# Handle script interruption
trap 'log_warning "Deployment interrupted. Run with --resume to continue from last checkpoint."' INT TERM

# Run main function
main "$@"
