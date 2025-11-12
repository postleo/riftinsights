# Summoner's Chronicle - Web App Deployment Guide

Complete step-by-step guide for deploying the Summoner's Chronicle web application to AWS.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Method 1: Automated Deployment (deploy.sh)](#method-1-automated-deployment-deploysh)
3. [Method 2: Manual Deployment (AWS CloudShell/Google CloudShell)](#method-2-manual-deployment-aws-cloudshellgoogle-cloudshell)
4. [Post-Deployment Configuration](#post-deployment-configuration)
5. [Troubleshooting](#troubleshooting)
6. [Resource Cleanup](#resource-cleanup)

---

## Prerequisites

Before you begin, ensure you have:

1. **AWS Account** with appropriate permissions
   - IAM permissions for S3, CloudFormation, Cognito, CloudWatch
   - Recommended: Administrator access for first-time setup

2. **RiftSage AI Agent** already deployed
   - The web app requires the RiftSage backend to function
   - See `../deployment/deploy.sh` for RiftSage deployment

3. **Basic Tools** (for automated method):
   - AWS CLI installed and configured
   - jq (JSON processor)
   - Bash shell (Linux/Mac or WSL on Windows)

4. **For Manual Method**:
   - Access to AWS CloudShell or Google CloudShell IDE

---

## Method 1: Automated Deployment (deploy.sh)

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/yourusername/rifts.git
cd rifts/web_app
```

### Step 2: Configure AWS Credentials

If not already configured:

```bash
aws configure
```

Enter:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., `us-east-1`)
- Default output format: `json`

### Step 3: Set Environment Variables (Optional)

```bash
export PROJECT_NAME="summoners-chronicle"
export ENVIRONMENT="production"
export AWS_REGION="us-east-1"
```

### Step 4: Run Deployment Script

```bash
chmod +x deploy.sh
./deploy.sh
```

### Step 5: Monitor Deployment

The script will:
- ✅ Validate prerequisites
- ✅ Create S3 bucket for web hosting
- ✅ Deploy CloudFormation stack (Cognito, etc.)
- ✅ Configure AWS settings
- ✅ Upload web app files
- ✅ Display deployment summary

**Deployment Time**: 5-10 minutes

### Step 6: Access Your Web App

After completion, the script will display:
```
Web App URL: http://summoners-chronicle-webapp-production-123456789.s3-website-us-east-1.amazonaws.com
```

Visit this URL to access your deployed web app!

### Resuming Failed Deployments

If deployment fails or is interrupted:

```bash
./deploy.sh --resume
```

The script will automatically resume from the last completed step.

---

## Method 2: Manual Deployment (AWS CloudShell/Google CloudShell)

### Option A: AWS CloudShell

#### Step 1: Access AWS CloudShell

1. Log in to AWS Console
2. Click the CloudShell icon (terminal icon in top navigation)
3. Wait for CloudShell to initialize

#### Step 2: Clone Repository

```bash
git clone https://github.com/yourusername/rifts.git
cd rifts/web_app
```

#### Step 3: Set Variables

```bash
export PROJECT_NAME="summoners-chronicle"
export ENVIRONMENT="production"
export AWS_REGION="us-east-1"
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export WEBAPP_BUCKET="${PROJECT_NAME}-webapp-${ENVIRONMENT}-${AWS_ACCOUNT_ID}"
```

#### Step 4: Create S3 Bucket

```bash
# Create bucket
aws s3 mb "s3://${WEBAPP_BUCKET}" --region "${AWS_REGION}"

# Configure for static website hosting
aws s3 website "s3://${WEBAPP_BUCKET}" \
    --index-document index.html \
    --error-document index.html
```

#### Step 5: Set Bucket Policy

```bash
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
```

#### Step 6: Deploy CloudFormation Stack

```bash
export STACK_NAME="${PROJECT_NAME}-webapp-${ENVIRONMENT}"

aws cloudformation create-stack \
    --stack-name "${STACK_NAME}" \
    --template-body file://cloudformation-template.yaml \
    --parameters \
        ParameterKey=Environment,ParameterValue="${ENVIRONMENT}" \
        ParameterKey=ProjectName,ParameterValue="${PROJECT_NAME}" \
        ParameterKey=WebAppBucket,ParameterValue="${WEBAPP_BUCKET}" \
    --capabilities CAPABILITY_NAMED_IAM \
    --region "${AWS_REGION}"

# Wait for stack creation (5-7 minutes)
aws cloudformation wait stack-create-complete \
    --stack-name "${STACK_NAME}" \
    --region "${AWS_REGION}"

echo "✅ CloudFormation stack created successfully"
```

#### Step 7: Get Stack Outputs

```bash
# Get Cognito User Pool ID
USER_POOL_ID=$(aws cloudformation describe-stacks \
    --stack-name "${STACK_NAME}" \
    --query 'Stacks[0].Outputs[?OutputKey==`UserPoolId`].OutputValue' \
    --output text \
    --region "${AWS_REGION}")

# Get Cognito Client ID
CLIENT_ID=$(aws cloudformation describe-stacks \
    --stack-name "${STACK_NAME}" \
    --query 'Stacks[0].Outputs[?OutputKey==`ClientId`].OutputValue' \
    --output text \
    --region "${AWS_REGION}")

# Get Identity Pool ID
IDENTITY_POOL_ID=$(aws cloudformation describe-stacks \
    --stack-name "${STACK_NAME}" \
    --query 'Stacks[0].Outputs[?OutputKey==`IdentityPoolId`].OutputValue' \
    --output text \
    --region "${AWS_REGION}")

# Get RiftSage API Endpoint
RIFTSAGE_API_ENDPOINT=$(aws cloudformation describe-stacks \
    --stack-name "riftsage-${ENVIRONMENT}" \
    --query 'Stacks[0].Outputs[?OutputKey==`APIEndpoint`].OutputValue' \
    --output text \
    --region "${AWS_REGION}")

echo "User Pool ID: ${USER_POOL_ID}"
echo "Client ID: ${CLIENT_ID}"
echo "Identity Pool ID: ${IDENTITY_POOL_ID}"
echo "API Endpoint: ${RIFTSAGE_API_ENDPOINT}"
```

#### Step 8: Update AWS Configuration

```bash
# Update config/aws-config.js
sed -i "s|REGION_PLACEHOLDER|${AWS_REGION}|g" config/aws-config.js
sed -i "s|USER_POOL_ID_PLACEHOLDER|${USER_POOL_ID}|g" config/aws-config.js
sed -i "s|CLIENT_ID_PLACEHOLDER|${CLIENT_ID}|g" config/aws-config.js
sed -i "s|IDENTITY_POOL_ID_PLACEHOLDER|${IDENTITY_POOL_ID}|g" config/aws-config.js
sed -i "s|API_ENDPOINT_PLACEHOLDER|${RIFTSAGE_API_ENDPOINT}|g" config/aws-config.js
sed -i "s|REPORTS_BUCKET_PLACEHOLDER|riftsage-reports-${ENVIRONMENT}-${AWS_ACCOUNT_ID}|g" config/aws-config.js
sed -i "s|ENVIRONMENT_PLACEHOLDER|${ENVIRONMENT}|g" config/aws-config.js

echo "✅ AWS configuration updated"
```

#### Step 9: Upload Files to S3

```bash
# Sync all files
aws s3 sync . "s3://${WEBAPP_BUCKET}/" \
    --exclude ".git/*" \
    --exclude "*.sh" \
    --exclude "*.md" \
    --exclude "*.json" \
    --exclude "cloudformation-template.yaml" \
    --delete \
    --region "${AWS_REGION}"

echo "✅ Files uploaded to S3"
```

#### Step 10: Set Cache Headers

```bash
# HTML files - 5 minutes cache
aws s3 cp "s3://${WEBAPP_BUCKET}/" "s3://${WEBAPP_BUCKET}/" \
    --recursive \
    --exclude "*" \
    --include "*.html" \
    --metadata-directive REPLACE \
    --cache-control "max-age=300" \
    --region "${AWS_REGION}"

# CSS and JS files - 1 year cache
aws s3 cp "s3://${WEBAPP_BUCKET}/" "s3://${WEBAPP_BUCKET}/" \
    --recursive \
    --exclude "*" \
    --include "*.js" \
    --include "*.css" \
    --metadata-directive REPLACE \
    --cache-control "max-age=31536000" \
    --region "${AWS_REGION}"

echo "✅ Cache headers configured"
```

#### Step 11: Get Web App URL

```bash
WEBSITE_URL="http://${WEBAPP_BUCKET}.s3-website-${AWS_REGION}.amazonaws.com"

echo ""
echo "========================================="
echo "Deployment Complete!"
echo "========================================="
echo ""
echo "Web App URL: ${WEBSITE_URL}"
echo ""
echo "Visit this URL to access your web app!"
```

### Option B: Google CloudShell IDE

The steps are identical to AWS CloudShell, but you need to:

1. Open Google CloudShell IDE
2. Install AWS CLI first:
   ```bash
   curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
   unzip awscliv2.zip
   sudo ./aws/install
   ```

3. Configure AWS credentials:
   ```bash
   aws configure
   ```

4. Follow the same steps as AWS CloudShell (Step 2 onwards)

---

## Post-Deployment Configuration

### 1. Test Authentication

1. Visit your web app URL
2. Click "Get Started"
3. Enter your email address
4. Check your email for the magic link
5. Click the magic link to sign in

### 2. Link Summoner Account

1. After signing in, enter your summoner name
2. Select your region
3. Click "Link Account"
4. Wait for report generation (2-5 minutes)

### 3. Explore Your Chronicle

Navigate through different sections using the pill navigation:
- Overview
- Performance
- Champions
- Team Impact
- Growth
- Achievements
- Future Goals

### 4. (Optional) Configure Custom Domain

To use a custom domain with HTTPS:

1. **Register Domain** (Route 53 or external registrar)
2. **Request SSL Certificate** (AWS Certificate Manager)
3. **Create CloudFront Distribution**:
   ```bash
   # Create CloudFront distribution for HTTPS
   aws cloudfront create-distribution \
       --origin-domain-name "${WEBAPP_BUCKET}.s3-website-${AWS_REGION}.amazonaws.com" \
       --default-root-object index.html
   ```
4. **Update DNS Records** to point to CloudFront
5. **Update Cognito Callback URLs** with new domain

---

## Troubleshooting

### Issue: "Failed to load user data"

**Solution:**
- Check if RiftSage backend is deployed
- Verify API endpoint in `config/aws-config.js`
- Check browser console for errors

### Issue: "Authentication failed"

**Solution:**
- Verify Cognito User Pool is created
- Check callback URLs in Cognito settings
- Ensure email is verified

### Issue: "S3 bucket already exists"

**Solution:**
- Use a different bucket name
- Or delete existing bucket:
  ```bash
  aws s3 rb s3://YOUR-BUCKET-NAME --force
  ```

### Issue: "CloudFormation stack failed"

**Solution:**
- Check CloudFormation events:
  ```bash
  aws cloudformation describe-stack-events \
      --stack-name ${STACK_NAME} \
      --max-items 20
  ```
- Review error messages
- Delete failed stack and retry:
  ```bash
  aws cloudformation delete-stack --stack-name ${STACK_NAME}
  ```

### Issue: "No report data available"

**Solution:**
- Ensure summoner account is linked
- Trigger report generation manually:
  ```bash
  aws lambda invoke \
      --function-name riftsage-DataCollection-production \
      --payload '{"player_puuid":"YOUR_PUUID","region":"na1","year":2025}' \
      response.json
  ```

---

## Resource Cleanup

To delete all deployed resources and stop charges:

### Quick Cleanup

```bash
# Delete CloudFormation stack
aws cloudformation delete-stack \
    --stack-name summoners-chronicle-webapp-production \
    --region us-east-1

# Wait for deletion
aws cloudformation wait stack-delete-complete \
    --stack-name summoners-chronicle-webapp-production \
    --region us-east-1

# Empty and delete S3 bucket
export WEBAPP_BUCKET="summoners-chronicle-webapp-production-YOUR_ACCOUNT_ID"
aws s3 rm "s3://${WEBAPP_BUCKET}" --recursive
aws s3 rb "s3://${WEBAPP_BUCKET}"
```

### Verify Cleanup

```bash
# List remaining resources
aws cloudformation list-stacks \
    --stack-status-filter DELETE_COMPLETE \
    --query 'StackSummaries[?StackName==`summoners-chronicle-webapp-production`]'

# Check S3 buckets
aws s3 ls | grep summoners-chronicle
```

**Cost After Cleanup**: $0 (all resources deleted)

---

## Deployment Summary

### Resources Created

| Resource | Type | Purpose | Cost (Idle) | Cost (Active) |
|----------|------|---------|-------------|---------------|
| S3 Bucket | Storage | Web hosting | $0.50/month | $1-3/month |
| Cognito User Pool | Auth | User management | $0 | $0 (free tier) |
| Cognito Identity Pool | Auth | AWS credentials | $0 | $0 |
| CloudWatch Logs | Monitoring | Application logs | $0.50/month | $1-2/month |
| IAM Roles | Security | Access control | $0 | $0 |

**Total Monthly Cost**: ~$1-2 (idle), ~$4-7 (active with 1,000 users)

### Security Features

- ✅ HTTPS support (via CloudFront)
- ✅ Email verification required
- ✅ JWT token authentication
- ✅ IAM role-based access control
- ✅ S3 bucket policies
- ✅ Cognito security features

---

## Support

For issues or questions:

1. **GitHub Issues**: [Create an issue](https://github.com/yourusername/rifts/issues)
2. **Documentation**: Review `../docs/` folder
3. **AWS Support**: For AWS-specific problems

---

## Next Steps

After successful deployment:

1. ✅ Test all authentication flows
2. ✅ Verify RiftSage integration
3. ✅ Test report generation
4. ✅ Share with beta testers
5. ✅ Monitor CloudWatch logs
6. ✅ Set up billing alerts
7. ✅ (Optional) Configure custom domain
8. ✅ (Optional) Set up CloudFront CDN

**Congratulations! Your Summoner's Chronicle web app is now live! 🎉**
