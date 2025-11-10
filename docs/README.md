# RiftSage AI Agent

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![AWS](https://img.shields.io/badge/AWS-Serverless-orange.svg)

RiftSage is an AI-powered agent that leverages AWS AI services and the League of Legends Developer API to deliver personalized, data-driven end-of-year insights for League of Legends players.

## Features

- **Intelligent Data Collection**: Automated match history retrieval from Riot Games API
- **Advanced Analytics**: 4 ML models for performance pattern analysis
- **AI-Powered Insights**: Amazon Bedrock (Claude AI) generates unique, personalized insights
- **Comprehensive Metrics**: 37+ tracked performance indicators
- **Auto-Scaling**: Serverless architecture that scales to zero when not in use
- **Cost-Optimized**: ~$0.13 per player report with automatic resource management

## Architecture

```
┌─────────────┐
│   Riot API  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────┐
│         Data Collection Lambda          │
│  - Rate limiting                        │
│  - Caching                              │
│  - S3 storage                           │
└──────────┬──────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│      Feature Engineering Lambda         │
│  - Metric calculation                   │
│  - Aggregation                          │
│  - DynamoDB storage                     │
└──────────┬──────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│       Model Inference Lambda            │
│  - Performance patterns                 │
│  - Mental resilience                    │
│  - Growth trajectory                    │
│  - Playstyle classification             │
└──────────┬──────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│      Bedrock Generation Lambda          │
│  - AI-powered insight generation        │
│  - Section-specific prompts             │
│  - Validation                           │
└──────────┬──────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│     Report Compilation Lambda           │
│  - Section assembly                     │
│  - Multi-format output (JSON, MD)       │
│  - S3 storage with presigned URLs       │
└─────────────────────────────────────────┘
```

## Auto-Shutdown & Cost Management

RiftSage includes intelligent resource management:

- **Serverless-First**: Lambda, DynamoDB On-Demand, and S3 automatically scale to zero
- **Activity Monitoring**: Resource Manager Lambda tracks system usage every 15 minutes
- **Idle Detection**: Automatically detects when no reports are being generated
- **Pay-Per-Use**: Only pay for actual compute time and storage used
- **Cost Tracking**: Built-in cost estimation and monitoring

### Resource States

The system operates in two states:

1. **Active**: Processing requests, all resources in use
2. **Idle**: No active requests, minimal costs (storage only)

Resources automatically transition between states based on activity. No manual intervention needed!

## Quick Start

### Prerequisites

- AWS Account with appropriate permissions
- Riot Games Developer API Key
- Python 3.11+
- AWS CLI configured

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/rifts.git
cd rifts
```

2. **Set environment variables**
```bash
export RIOT_API_KEY='your-riot-api-key'
export AWS_REGION='us-east-1'
export ENVIRONMENT='production'
```

3. **Deploy to AWS**
```bash
chmod +x deployment/deploy.sh
./deployment/deploy.sh
```

The deployment script will:
- Create S3 buckets
- Package and upload Lambda functions
- Deploy CloudFormation stack
- Seed champion database
- Provide API endpoint

### Usage

**Generate a report for a player:**

```python
import boto3
import json

lambda_client = boto3.client('lambda')

# Step 1: Collect match data
response = lambda_client.invoke(
    FunctionName='riftsage-DataCollection-production',
    InvocationType='RequestResponse',
    Payload=json.dumps({
        'player_puuid': 'player-puuid-here',
        'region': 'na1',
        'year': 2025
    })
)

# Step 2: Process features
response = lambda_client.invoke(
    FunctionName='riftsage-FeatureEngineering-production',
    InvocationType='RequestResponse',
    Payload=json.dumps({
        'player_puuid': 'player-puuid-here',
        'year': 2025
    })
)

# Step 3: Run ML inference
response = lambda_client.invoke(
    FunctionName='riftsage-ModelInference-production',
    InvocationType='RequestResponse',
    Payload=json.dumps({
        'player_puuid': 'player-puuid-here',
        'year': 2025
    })
)

# Step 4: Generate insights
response = lambda_client.invoke(
    FunctionName='riftsage-BedrockGeneration-production',
    InvocationType='RequestResponse',
    Payload=json.dumps({
        'player_puuid': 'player-puuid-here',
        'year': 2025,
        'generate_all': True
    })
)

# Step 5: Compile report
response = lambda_client.invoke(
    FunctionName='riftsage-ReportCompilation-production',
    InvocationType='RequestResponse',
    Payload=json.dumps({
        'player_puuid': 'player-puuid-here',
        'year': 2025
    })
)

result = json.loads(response['Payload'].read())
print(f"Report URL: {result['s3_results']['urls']['json']}")
```

## Project Structure

```
rifts/
├── lambda_functions/           # Lambda function code
│   ├── data_collection.py
│   ├── feature_engineering.py
│   ├── model_inference.py
│   ├── bedrock_generation.py
│   ├── report_compilation.py
│   └── resource_manager.py
├── config/                     # Configuration files
│   └── config.yaml
├── deployment/                 # Deployment scripts
│   ├── deploy.sh
│   └── requirements.txt
├── docs/                       # Documentation
│   ├── README.md
│   ├── AWS_STACK.md
│   ├── API_REFERENCE.md
│   └── DEVELOPMENT.md
├── infrastructure.yaml         # CloudFormation template
└── database_seeds/            # Database population scripts
```

## Configuration

Edit `config/config.yaml` to customize:

- AWS region
- Auto-shutdown settings
- Bedrock model configuration
- Rate limits
- Caching policies

## Monitoring

View Lambda execution logs:
```bash
aws logs tail /aws/lambda/riftsage-DataCollection-production --follow
```

Check resource state:
```bash
aws lambda invoke \
  --function-name riftsage-ResourceManager-production \
  --payload '{"action": "get_status"}' \
  response.json

cat response.json
```

Get cost estimates:
```bash
aws lambda invoke \
  --function-name riftsage-ResourceManager-production \
  --payload '{"action": "get_costs"}' \
  costs.json

cat costs.json
```

## Testing

Run tests:
```bash
cd tests
pytest -v
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Cost Breakdown

Per 1,000 player reports:

| Service | Cost |
|---------|------|
| Lambda | $5 |
| Bedrock (Claude 3 Sonnet) | $99 |
| S3 | $3 |
| DynamoDB | $26 |
| CloudWatch | $1 |
| **Total** | **$134** (~$0.13/report) |

When idle (no reports):
- S3 storage: ~$0.023/GB/month
- DynamoDB: $0 (on-demand with no requests)
- Lambda: $0 (no invocations)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built on AWS Serverless architecture
- Powered by Amazon Bedrock (Claude AI)
- League of Legends data from Riot Games API

## Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/yourusername/rifts/issues)
- Documentation: See `docs/` folder

---

**Note**: This project is not endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties.
