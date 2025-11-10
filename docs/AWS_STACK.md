# RiftSage AWS Stack - Complete Resource List and Costs

This document provides a comprehensive list of all AWS resources created by the RiftSage AI Agent infrastructure, along with their costs and purposes.

## Resource Summary

| Category | Count | Monthly Cost (Idle) | Monthly Cost (Active) |
|----------|-------|---------------------|----------------------|
| Lambda Functions | 6 | $0 | $5-50 |
| DynamoDB Tables | 6 | $0 | $10-40 |
| S3 Buckets | 3 | $0.50-2 | $3-10 |
| KMS Keys | 1 | $1 | $1 |
| Cognito User Pool | 1 | $0 | $0-5 |
| API Gateway | 1 | $0 | $3.50-10 |
| CloudWatch | Multiple | $1-3 | $3-10 |
| Secrets Manager | 1 | $0.40 | $0.40 |
| **Total** | **19+** | **~$3** | **~$30-130** |

*Active costs assume 1,000 reports generated per month*

## Detailed Resource Breakdown

### 1. Lambda Functions (6 total)

#### riftsage-DataCollection-{Environment}
- **Purpose**: Fetches match data from Riot Games API
- **Memory**: 512 MB
- **Timeout**: 5 minutes
- **Triggers**: Manual invocation, API Gateway
- **Cost When Idle**: $0
- **Cost When Active**: ~$1 per 1,000 invocations
- **Monthly Cost (1K reports)**: $1

#### riftsage-FeatureEngineering-{Environment}
- **Purpose**: Transforms raw match data into ML features
- **Memory**: 1024 MB
- **Timeout**: 10 minutes
- **Triggers**: S3 event (new match data), Manual
- **Cost When Idle**: $0
- **Cost When Active**: ~$2 per 1,000 invocations
- **Monthly Cost (1K reports)**: $2

#### riftsage-ModelInference-{Environment}
- **Purpose**: Applies ML models for player classification
- **Memory**: 2048 MB
- **Timeout**: 5 minutes
- **Triggers**: Manual invocation, EventBridge (annual training)
- **Cost When Idle**: $0
- **Cost When Active**: ~$3 per 1,000 invocations
- **Monthly Cost (1K reports)**: $3

#### riftsage-BedrockGeneration-{Environment}
- **Purpose**: Generates AI insights using Amazon Bedrock
- **Memory**: 1024 MB
- **Timeout**: 15 minutes
- **Triggers**: Manual invocation
- **Cost When Idle**: $0
- **Cost When Active**: $1 Lambda + $99 Bedrock per 1,000 invocations
- **Monthly Cost (1K reports)**: $100
- **Note**: This is the most expensive component due to Bedrock usage

#### riftsage-ReportCompilation-{Environment}
- **Purpose**: Assembles sections into complete reports
- **Memory**: 1024 MB
- **Timeout**: 5 minutes
- **Triggers**: Manual invocation
- **Cost When Idle**: $0
- **Cost When Active**: ~$1 per 1,000 invocations
- **Monthly Cost (1K reports)**: $1

#### riftsage-ResourceManager-{Environment}
- **Purpose**: Monitors and manages resource usage for cost optimization
- **Memory**: 256 MB
- **Timeout**: 1 minute
- **Triggers**: EventBridge (every 15 minutes)
- **Cost When Idle**: $0.05 (monitoring only)
- **Cost When Active**: $0.10
- **Monthly Cost**: $0.10
- **Note**: Runs continuously but has minimal cost

### 2. DynamoDB Tables (6 total)

All tables use **PAY_PER_REQUEST** billing mode, which means:
- $0 cost when no requests
- $1.25 per million read requests
- $1.25 per million write requests

#### riftsage-Players-{Environment}
- **Purpose**: Stores player account information
- **Partition Key**: player_puuid (String)
- **GSI**: EmailIndex
- **Point-in-Time Recovery**: Enabled
- **Encryption**: KMS
- **Cost When Idle**: $0
- **Monthly Cost (1K reports)**: ~$5

#### riftsage-Metrics-{Environment}
- **Purpose**: Stores calculated player metrics
- **Partition Key**: player_puuid (String)
- **Sort Key**: year (Number)
- **Encryption**: KMS
- **Cost When Idle**: $0
- **Monthly Cost (1K reports)**: ~$10

#### riftsage-Insights-{Environment}
- **Purpose**: Stores AI-generated insight sections
- **Partition Key**: player_puuid (String)
- **Sort Key**: section_id (String)
- **Encryption**: Standard
- **Cost When Idle**: $0
- **Monthly Cost (1K reports)**: ~$15

#### riftsage-MatchCache-{Environment}
- **Purpose**: Caches match data to reduce API calls
- **Partition Key**: match_id (String)
- **TTL**: Enabled (24 hours)
- **Encryption**: Standard
- **Cost When Idle**: $0
- **Monthly Cost (1K reports)**: ~$5

#### riftsage-ChampionRecs-{Environment}
- **Purpose**: Stores champion recommendation data
- **Partition Key**: champion_name (String)
- **GSI**: RoleIndex
- **Encryption**: Standard
- **Cost When Idle**: $0
- **Monthly Cost (1K reports)**: <$1

#### riftsage-RateLimit-{Environment}
- **Purpose**: Tracks API rate limits
- **Partition Key**: user_action (String)
- **TTL**: Enabled (2 minutes)
- **Encryption**: Standard
- **Cost When Idle**: $0
- **Monthly Cost (1K reports)**: <$1

#### riftsage-ResourceState-{Environment}
- **Purpose**: Tracks resource activity for auto-shutdown
- **Partition Key**: resource_id (String)
- **Encryption**: Standard
- **Cost When Idle**: $0
- **Monthly Cost**: <$0.10

### 3. S3 Buckets (3 total)

#### riftsage-data-{Environment}-{AccountId}
- **Purpose**: Stores raw match data from Riot API
- **Lifecycle**:
  - 90 days → Intelligent Tiering
  - 365 days → Glacier Instant Retrieval
- **Versioning**: Enabled
- **Encryption**: KMS
- **Cost When Idle**: ~$0.50/month (existing data)
- **Monthly Cost (1K reports)**: ~$3 (storage + retrieval)

#### riftsage-reports-{Environment}-{AccountId}
- **Purpose**: Stores generated player reports (JSON, MD, PDF)
- **CORS**: Enabled for web access
- **Encryption**: KMS
- **Cost When Idle**: ~$0.50/month
- **Monthly Cost (1K reports)**: ~$2

#### riftsage-models-{Environment}-{AccountId}
- **Purpose**: Stores ML model artifacts and Lambda code
- **Versioning**: Enabled
- **Encryption**: Standard
- **Cost When Idle**: ~$0.20/month
- **Monthly Cost**: ~$0.50

### 4. KMS Keys (1)

#### riftsage-{Environment}
- **Purpose**: Encryption key for data at rest
- **Usage**: DynamoDB, S3, Secrets Manager
- **Cost**: $1/month flat
- **Note**: Single key used across all services

### 5. Cognito (1 User Pool)

#### riftsage-users-{Environment}
- **Purpose**: User authentication
- **Features**: Email verification, magic links
- **Cost When Idle**: $0
- **Cost When Active**: Free for first 50,000 MAUs
- **Monthly Cost**: $0-5 (depends on users)

### 6. API Gateway (1)

#### riftsage-api-{Environment}
- **Type**: HTTP API
- **Purpose**: REST API endpoints
- **Throttling**: 100 burst, 50 steady
- **CORS**: Enabled
- **Cost When Idle**: $0
- **Monthly Cost (1K reports)**: ~$3.50
  - $1.00 per million requests
  - First 1 million free tier (new accounts)

### 7. Secrets Manager (1)

#### /{ProjectName}/{Environment}/riot-api-key
- **Purpose**: Securely stores Riot API key
- **Encryption**: KMS
- **Cost**: $0.40/month per secret
- **Monthly Cost**: $0.40 (flat)

### 8. CloudWatch Resources

#### Log Groups (6)
One per Lambda function:
- /aws/lambda/riftsage-DataCollection-{Environment}
- /aws/lambda/riftsage-FeatureEngineering-{Environment}
- /aws/lambda/riftsage-ModelInference-{Environment}
- /aws/lambda/riftsage-BedrockGeneration-{Environment}
- /aws/lambda/riftsage-ReportCompilation-{Environment}
- /aws/lambda/riftsage-ResourceManager-{Environment}

**Retention**: 30 days
**Cost When Idle**: ~$1/month (ResourceManager logs only)
**Monthly Cost (1K reports)**: ~$5

#### CloudWatch Alarms (2)
- HighErrorRateAlarm
- SlowGenerationAlarm

**Cost**: $0.10/alarm/month
**Monthly Cost**: $0.20

#### CloudWatch Metrics
**Cost**: First 10 custom metrics free, then $0.30/metric/month

### 9. EventBridge Rules (2)

#### AnnualModelTrainingRule
- **Schedule**: cron(0 2 15 1 ? *) - January 15 at 2 AM
- **Purpose**: Trigger annual ML model retraining
- **Cost**: Free (included in Lambda costs)

#### ResourceMonitoringRule
- **Schedule**: rate(15 minutes)
- **Purpose**: Monitor resources for auto-shutdown
- **Cost**: Free (included in Lambda costs)

### 10. SNS Topics (1)

#### riftsage-alerts-{Environment}
- **Purpose**: System alerts and notifications
- **Cost**: Free tier covers typical usage
- **Monthly Cost**: $0-1

## Total Cost Breakdown

### Idle State (No Reports Generated)
```
S3 Storage:           $1.20
CloudWatch Logs:      $1.00
KMS:                  $1.00
Secrets Manager:      $0.40
Resource Manager:     $0.10
SNS:                  $0.00
DynamoDB:             $0.00
Lambda:               $0.00
API Gateway:          $0.00
------------------------
TOTAL:               ~$3.70/month
```

### Active State (1,000 Reports/Month)
```
Lambda Compute:       $8.00
Bedrock (Claude):     $99.00
DynamoDB:             $26.00
S3 Storage/Transfer:  $5.00
API Gateway:          $3.50
CloudWatch:           $5.00
KMS:                  $1.00
Secrets Manager:      $0.40
SNS:                  $0.50
------------------------
TOTAL:               ~$148/month
Cost per report:      $0.148
```

### Cost Optimization Features

1. **Serverless Architecture**: Pay only for actual usage
2. **DynamoDB On-Demand**: Zero cost when idle
3. **S3 Intelligent Tiering**: Automatic cost optimization
4. **Lambda Reserved Concurrency**: Prevents runaway costs
5. **Resource Manager**: Tracks usage patterns
6. **TTL on Cache Tables**: Automatic cleanup
7. **CloudWatch Log Retention**: 30 days to control costs

### Scaling Considerations

**At 10,000 reports/month:**
- Total: ~$1,400/month
- Cost per report: $0.14

**At 100,000 reports/month:**
- Total: ~$13,500/month
- Cost per report: $0.135
- Bedrock dominates costs (~73%)

### Cost Reduction Strategies

1. **Use Bedrock Haiku**: Reduce AI costs by 60% with lower-tier model
2. **Batch Processing**: Process multiple reports together
3. **Caching**: Aggressive caching of champion data and benchmarks
4. **Reserved Capacity**: For predictable, high-volume usage
5. **S3 Lifecycle Policies**: Already implemented
6. **CloudWatch Log Filtering**: Reduce log ingestion

## Resource Tags

All resources are tagged with:
- `Environment`: development | staging | production
- `Project`: riftsage
- `ManagedBy`: CloudFormation

## Cleanup/Teardown

To remove all resources:

```bash
aws cloudformation delete-stack --stack-name riftsage-production

# Wait for deletion
aws cloudformation wait stack-delete-complete --stack-name riftsage-production

# Manually delete S3 buckets (must be empty first)
aws s3 rb s3://riftsage-data-production-{AccountId} --force
aws s3 rb s3://riftsage-reports-production-{AccountId} --force
aws s3 rb s3://riftsage-models-production-{AccountId} --force
```

**Cost After Teardown**: $0 (except for S3 data if retained)

## Monitoring Costs

**View current month costs:**
```bash
aws ce get-cost-and-usage \
  --time-period Start=2025-01-01,End=2025-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --filter file://cost-filter.json
```

**Set up billing alerts:**
1. AWS Console → Billing → Budgets
2. Create budget with threshold (e.g., $200/month)
3. Configure SNS notifications

## Support

For questions about AWS resources or costs:
- Check AWS Cost Explorer
- Review CloudWatch metrics
- Contact AWS Support
