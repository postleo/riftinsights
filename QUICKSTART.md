# RiftSage AI Agent - Quick Start Guide

This guide will get you up and running with RiftSage in under 10 minutes.

## Prerequisites

- AWS Account
- Riot Games Developer API Key ([Get one here](https://developer.riotgames.com/))
- AWS CLI installed and configured
- Python 3.11+

## 5-Minute Setup

### Step 1: Set Your API Key
```bash
export RIOT_API_KEY='RGAPI-your-key-here'
```

### Step 2: Deploy to AWS
```bash
chmod +x deployment/deploy.sh
./deployment/deploy.sh
```

The script will:
- ✓ Create all AWS resources
- ✓ Package and deploy Lambda functions
- ✓ Seed champion database
- ✓ Output your API endpoint

**Expected time**: 5-7 minutes

### Step 3: Test with a Sample Player

```python
import boto3
import json

lambda_client = boto3.client('lambda')

# Replace with a real player PUUID from Riot API
player_puuid = 'your-player-puuid-here'

# Full pipeline
functions = [
    ('riftsage-DataCollection-production', {'player_puuid': player_puuid, 'region': 'na1', 'year': 2025}),
    ('riftsage-FeatureEngineering-production', {'player_puuid': player_puuid, 'year': 2025}),
    ('riftsage-ModelInference-production', {'player_puuid': player_puuid, 'year': 2025}),
    ('riftsage-BedrockGeneration-production', {'player_puuid': player_puuid, 'year': 2025, 'generate_all': True}),
    ('riftsage-ReportCompilation-production', {'player_puuid': player_puuid, 'year': 2025})
]

for func_name, payload in functions:
    print(f"Invoking {func_name}...")
    response = lambda_client.invoke(
        FunctionName=func_name,
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    result = json.loads(response['Payload'].read())
    print(f"Status: {result.get('statusCode', 'N/A')}")
    print()

print("Report generation complete!")
```

## Auto-Shutdown Feature

RiftSage automatically minimizes costs when not in use:

- **Idle costs**: ~$3/month (just storage and monitoring)
- **Active costs**: ~$0.13 per report
- **No manual management needed**

Check system status:
```bash
aws lambda invoke \
  --function-name riftsage-ResourceManager-production \
  --payload '{"action": "get_status"}' \
  status.json && cat status.json
```

## View Your First Report

After running the pipeline, get the report URL:
```python
result = json.loads(response['Payload'].read())
report_url = result['body']['s3_results']['urls']['json']
print(f"Report available at: {report_url}")
```

## Monitoring

View logs in real-time:
```bash
aws logs tail /aws/lambda/riftsage-DataCollection-production --follow
```

Check costs:
```bash
aws lambda invoke \
  --function-name riftsage-ResourceManager-production \
  --payload '{"action": "get_costs"}' \
  costs.json && cat costs.json
```

## Common Issues

### "RIOT_API_KEY not set"
```bash
export RIOT_API_KEY='your-key-here'
```

### "Access Denied" errors
Ensure your AWS credentials have CloudFormation, Lambda, S3, DynamoDB, and Bedrock permissions.

### "Bedrock not available"
Enable Amazon Bedrock in your AWS account:
1. Go to AWS Console → Bedrock
2. Request access to Claude models
3. Wait for approval (usually instant)

## Next Steps

1. **Customize Configuration**: Edit `config/config.yaml`
2. **Add More Champions**: Update `database_seeds/seed_champions.py`
3. **Modify Prompts**: Edit templates in `prompt_templates/`
4. **Build Frontend**: Use the API endpoint from deployment output

## Cost Optimization

Your deployment is already optimized:
- ✓ Serverless (scales to zero)
- ✓ DynamoDB On-Demand billing
- ✓ S3 Intelligent Tiering
- ✓ Automatic resource monitoring

Typical costs:
- Idle: $3/month
- 100 reports: $16/month
- 1,000 reports: $148/month

## Support

- **Documentation**: See `docs/` folder
- **AWS Resources**: Check `docs/AWS_STACK.md`
- **Issues**: Open a GitHub issue

## Clean Up

To remove all resources and stop all charges:
```bash
aws cloudformation delete-stack --stack-name riftsage-production

# Wait for completion
aws cloudformation wait stack-delete-complete --stack-name riftsage-production
```

---

**You're ready to go!** 🎮

Generate your first League of Legends performance report and start providing AI-powered insights to players.
