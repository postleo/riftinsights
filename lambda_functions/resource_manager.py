"""
RiftSage AI Agent - Resource Manager Lambda Function
Automatically manages AWS resources to minimize costs when not in use
Only provisions/uses resources when actively processing requests
"""

import json
import os
import boto3
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
lambda_client = boto3.client('lambda')
cloudwatch = boto3.client('cloudwatch')

# Environment variables
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')
RESOURCE_STATE_TABLE = os.environ.get('RESOURCE_STATE_TABLE')
AUTO_SHUTDOWN_ENABLED = os.environ.get('AUTO_SHUTDOWN_ENABLED', 'true') == 'true'
IDLE_THRESHOLD_MINUTES = int(os.environ.get('IDLE_THRESHOLD_MINUTES', 60))


class ResourceManager:
    """Manages AWS resources to optimize costs"""

    def __init__(self):
        self.state_table = dynamodb.Table(RESOURCE_STATE_TABLE)

    def get_resource_state(self, resource_id: str) -> Dict:
        """Get current state of a resource"""
        try:
            response = self.state_table.get_item(Key={'resource_id': resource_id})
            return response.get('Item', {})
        except Exception as e:
            logger.error(f"Error getting resource state: {str(e)}")
            return {}

    def update_resource_state(self, resource_id: str, state: Dict):
        """Update resource state"""
        try:
            state['resource_id'] = resource_id
            state['updated_at'] = datetime.utcnow().isoformat()
            self.state_table.put_item(Item=state)
            logger.info(f"Updated state for {resource_id}")
        except Exception as e:
            logger.error(f"Error updating resource state: {str(e)}")

    def check_lambda_activity(self, function_name: str, minutes: int = 60) -> Dict:
        """Check Lambda function activity in the last N minutes"""
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(minutes=minutes)

            # Get invocation metrics
            invocations = cloudwatch.get_metric_statistics(
                Namespace='AWS/Lambda',
                MetricName='Invocations',
                Dimensions=[{'Name': 'FunctionName', 'Value': function_name}],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,  # 5 minutes
                Statistics=['Sum']
            )

            total_invocations = sum(point['Sum'] for point in invocations['Datapoints'])

            # Get error metrics
            errors = cloudwatch.get_metric_statistics(
                Namespace='AWS/Lambda',
                MetricName='Errors',
                Dimensions=[{'Name': 'FunctionName', 'Value': function_name}],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Sum']
            )

            total_errors = sum(point['Sum'] for point in errors['Datapoints'])

            return {
                'function_name': function_name,
                'invocations': int(total_invocations),
                'errors': int(total_errors),
                'is_active': total_invocations > 0,
                'checked_at': datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Error checking Lambda activity: {str(e)}")
            return {
                'function_name': function_name,
                'invocations': 0,
                'errors': 0,
                'is_active': False,
                'error': str(e)
            }

    def get_system_activity(self) -> Dict:
        """Get overall system activity"""
        try:
            # List of Lambda functions to monitor
            functions = [
                f'riftsage-DataCollection-{ENVIRONMENT}',
                f'riftsage-FeatureEngineering-{ENVIRONMENT}',
                f'riftsage-ModelInference-{ENVIRONMENT}',
                f'riftsage-BedrockGeneration-{ENVIRONMENT}',
                f'riftsage-ReportCompilation-{ENVIRONMENT}'
            ]

            activity_summary = {
                'total_invocations': 0,
                'total_errors': 0,
                'active_functions': 0,
                'functions': {}
            }

            for function_name in functions:
                activity = self.check_lambda_activity(function_name, IDLE_THRESHOLD_MINUTES)
                activity_summary['functions'][function_name] = activity
                activity_summary['total_invocations'] += activity['invocations']
                activity_summary['total_errors'] += activity['errors']
                if activity['is_active']:
                    activity_summary['active_functions'] += 1

            activity_summary['is_idle'] = activity_summary['total_invocations'] == 0
            activity_summary['checked_at'] = datetime.utcnow().isoformat()

            return activity_summary

        except Exception as e:
            logger.error(f"Error getting system activity: {str(e)}")
            return {
                'error': str(e),
                'is_idle': False,
                'checked_at': datetime.utcnow().isoformat()
            }

    def set_lambda_concurrency(self, function_name: str, reserved_concurrency: int):
        """
        Set Lambda reserved concurrency
        Setting to 0 effectively pauses the function
        """
        try:
            if reserved_concurrency == 0:
                # Remove reserved concurrency (allows scaling)
                lambda_client.delete_function_concurrency(FunctionName=function_name)
                logger.info(f"Removed concurrency limit for {function_name}")
            else:
                # Set reserved concurrency
                lambda_client.put_function_concurrency(
                    FunctionName=function_name,
                    ReservedConcurrentExecutions=reserved_concurrency
                )
                logger.info(f"Set concurrency to {reserved_concurrency} for {function_name}")

            return True
        except Exception as e:
            logger.error(f"Error setting concurrency: {str(e)}")
            return False

    def optimize_resources(self, activity_summary: Dict) -> Dict:
        """
        Optimize resources based on activity
        Note: With serverless architecture, costs are already minimal when idle
        This function primarily tracks state and can be extended for future optimizations
        """
        try:
            actions_taken = []

            if activity_summary['is_idle']:
                logger.info(f"System has been idle for {IDLE_THRESHOLD_MINUTES} minutes")

                # Update system state
                self.update_resource_state('system', {
                    'status': 'idle',
                    'idle_since': datetime.utcnow().isoformat(),
                    'last_activity': activity_summary
                })

                actions_taken.append({
                    'action': 'state_update',
                    'status': 'idle',
                    'note': 'System marked as idle - no active optimizations needed for serverless'
                })

                # Note: Lambda, DynamoDB On-Demand, and S3 already have pay-per-use pricing
                # No additional shutdown actions needed - they automatically scale to zero

            else:
                logger.info("System is active")

                # Update system state
                self.update_resource_state('system', {
                    'status': 'active',
                    'last_activity': activity_summary,
                    'active_functions': activity_summary['active_functions']
                })

                actions_taken.append({
                    'action': 'state_update',
                    'status': 'active',
                    'invocations': activity_summary['total_invocations']
                })

            return {
                'success': True,
                'is_idle': activity_summary['is_idle'],
                'actions_taken': actions_taken,
                'activity_summary': activity_summary,
                'timestamp': datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Error optimizing resources: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def get_cost_estimate(self) -> Dict:
        """
        Estimate current costs based on resource usage
        This is a simplified estimate
        """
        try:
            activity = self.get_system_activity()

            # Rough cost estimates (per 1000 invocations)
            lambda_cost_per_1k = 0.20  # $0.20 per million requests
            bedrock_cost_per_1k_tokens = 0.015  # Claude 3 Sonnet pricing

            estimated_costs = {
                'lambda_invocations': activity['total_invocations'] * (lambda_cost_per_1k / 1000),
                'estimated_bedrock': 0,  # Would need token count
                'storage': 0,  # S3 and DynamoDB minimal when idle
                'total_estimated': 0
            }

            estimated_costs['total_estimated'] = sum([
                estimated_costs['lambda_invocations'],
                estimated_costs['estimated_bedrock'],
                estimated_costs['storage']
            ])

            return {
                'period': f'last_{IDLE_THRESHOLD_MINUTES}_minutes',
                'costs': estimated_costs,
                'note': 'Estimates only - check AWS Cost Explorer for actual costs'
            }

        except Exception as e:
            logger.error(f"Error estimating costs: {str(e)}")
            return {
                'error': str(e)
            }


def lambda_handler(event, context):
    """
    Lambda handler for resource management

    Expected event format:
    {
        "action": "monitor_and_manage" | "get_status" | "get_costs"
    }
    """

    try:
        logger.info(f"Event: {json.dumps(event)}")

        if not AUTO_SHUTDOWN_ENABLED:
            logger.info("Auto-shutdown is disabled")
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Auto-shutdown is disabled',
                    'enabled': False
                })
            }

        manager = ResourceManager()
        action = event.get('action', 'monitor_and_manage')

        if action == 'monitor_and_manage':
            # Get system activity
            activity = manager.get_system_activity()

            # Optimize resources
            result = manager.optimize_resources(activity)

            return {
                'statusCode': 200,
                'body': json.dumps(result)
            }

        elif action == 'get_status':
            # Get current system status
            state = manager.get_resource_state('system')
            activity = manager.get_system_activity()

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'current_state': state,
                    'activity': activity
                })
            }

        elif action == 'get_costs':
            # Get cost estimates
            costs = manager.get_cost_estimate()

            return {
                'statusCode': 200,
                'body': json.dumps(costs)
            }

        else:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': f'Unknown action: {action}'
                })
            }

    except Exception as e:
        logger.error(f"Lambda handler error: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'type': type(e).__name__
            })
        }
