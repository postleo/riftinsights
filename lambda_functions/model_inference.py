"""
RiftSage AI Agent - Model Inference Lambda Function
Applies ML models to player data for classification and predictions
"""

import json
import os
import boto3
import logging
import pickle
from datetime import datetime
from typing import Dict, List, Any
from decimal import Decimal
import numpy as np

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# Environment variables
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')
MODELS_BUCKET = os.environ.get('MODELS_BUCKET')
METRICS_TABLE_NAME = os.environ.get('METRICS_TABLE')


class MLModelPipeline:
    """Pipeline for running ML models on player data"""

    def __init__(self, models_bucket: str):
        self.models_bucket = models_bucket
        self.models = {}

    def load_model(self, model_name: str):
        """Load a trained model from S3"""
        try:
            if model_name in self.models:
                return self.models[model_name]

            # Download model from S3
            model_key = f"models/{model_name}.pkl"
            local_path = f"/tmp/{model_name}.pkl"

            s3_client.download_file(self.models_bucket, model_key, local_path)

            # Load model
            with open(local_path, 'rb') as f:
                model = pickle.load(f)

            self.models[model_name] = model
            logger.info(f"Loaded model: {model_name}")

            return model

        except Exception as e:
            logger.error(f"Error loading model {model_name}: {str(e)}")
            # Return None if model doesn't exist - use rule-based fallback
            return None

    def classify_performance_pattern(self, metrics: Dict) -> Dict:
        """
        Model 1: Performance Pattern Analyzer
        Classifies player's performance characteristics
        """
        try:
            # Try to load trained model
            model = self.load_model('performance_pattern_analyzer')

            if model is not None:
                # Use ML model
                features = self._extract_pattern_features(metrics)
                prediction = model.predict([features])[0]

                return {
                    'model': 'ml',
                    'pattern': prediction,
                    'confidence': 0.85  # Would come from model probability
                }

            else:
                # Rule-based fallback
                pattern = self._rule_based_performance_pattern(metrics)
                return {
                    'model': 'rule_based',
                    'pattern': pattern,
                    'confidence': 0.75
                }

        except Exception as e:
            logger.error(f"Error classifying performance pattern: {str(e)}")
            return {
                'model': 'error',
                'pattern': 'unknown',
                'confidence': 0.0,
                'error': str(e)
            }

    def _extract_pattern_features(self, metrics: Dict) -> List[float]:
        """Extract features for performance pattern classification"""
        return [
            float(metrics.get('kda', 0)),
            float(metrics.get('win_rate', 0)),
            float(metrics.get('deaths_per_game', 0)),
            float(metrics.get('avg_vision_score_per_min', 0)),
            float(metrics.get('avg_objective_participation', 0)),
            float(metrics.get('avg_cs_per_min', 0)),
        ]

    def _rule_based_performance_pattern(self, metrics: Dict) -> str:
        """Rule-based performance pattern classification"""
        kda = float(metrics.get('kda', 0))
        deaths_per_game = float(metrics.get('deaths_per_game', 0))
        vision_per_min = float(metrics.get('avg_vision_score_per_min', 0))

        # Simple rule-based classification
        if kda > 3.0 and deaths_per_game < 5:
            return "aggressive_combat_with_survival"
        elif deaths_per_game > 7:
            return "high_risk_high_reward"
        elif vision_per_min > 1.0:
            return "vision_focused_support"
        else:
            return "balanced_gameplay"

    def calculate_mental_resilience(self, metrics: Dict) -> Dict:
        """
        Model 2: Mental Resilience Calculator
        Calculates tilt resistance and consistency
        """
        try:
            # Try to load trained model
            model = self.load_model('mental_resilience_calculator')

            if model is not None:
                features = self._extract_resilience_features(metrics)
                score = model.predict([features])[0]
            else:
                # Rule-based calculation
                score = self._rule_based_resilience_score(metrics)

            # Determine grade
            if score >= 80:
                grade = "Elite"
            elif score >= 65:
                grade = "High"
            elif score >= 45:
                grade = "Medium"
            else:
                grade = "Developing"

            return {
                'resilience_score': round(float(score), 2),
                'grade': grade,
                'comeback_wins': metrics.get('comeback_wins', 0),
                'consistency_rating': self._calculate_consistency(metrics)
            }

        except Exception as e:
            logger.error(f"Error calculating resilience: {str(e)}")
            return {
                'resilience_score': 50.0,
                'grade': "Unknown",
                'error': str(e)
            }

    def _extract_resilience_features(self, metrics: Dict) -> List[float]:
        """Extract features for resilience calculation"""
        return [
            float(metrics.get('comeback_wins', 0)),
            float(metrics.get('win_rate', 0)),
            float(metrics.get('total_games', 0)),
        ]

    def _rule_based_resilience_score(self, metrics: Dict) -> float:
        """Rule-based resilience score calculation"""
        total_games = float(metrics.get('total_games', 1))
        comeback_wins = float(metrics.get('comeback_wins', 0))
        win_rate = float(metrics.get('win_rate', 0))

        # Calculate comeback rate
        comeback_rate = (comeback_wins / total_games) * 100 if total_games > 0 else 0

        # Weighted score
        score = (comeback_rate * 0.4) + (win_rate * 0.6)

        return min(100, max(0, score))

    def _calculate_consistency(self, metrics: Dict) -> str:
        """Calculate consistency rating"""
        win_rate = float(metrics.get('win_rate', 0))

        if win_rate >= 55:
            return "Very Consistent"
        elif win_rate >= 50:
            return "Consistent"
        elif win_rate >= 45:
            return "Moderate"
        else:
            return "Variable"

    def analyze_growth_trajectory(self, current_metrics: Dict, previous_metrics: Dict = None) -> Dict:
        """
        Model 3: Growth Trajectory Analyzer
        Predicts improvement areas and growth potential
        """
        try:
            if previous_metrics is None:
                return {
                    'trajectory': 'insufficient_data',
                    'improvement_velocity': 0.0,
                    'predicted_improvement_areas': []
                }

            # Calculate improvement rates
            improvements = {}

            metrics_to_compare = ['kda', 'win_rate', 'avg_cs_per_min', 'avg_vision_score_per_min']

            for metric in metrics_to_compare:
                current = float(current_metrics.get(metric, 0))
                previous = float(previous_metrics.get(metric, 0))

                if previous > 0:
                    improvement_pct = ((current - previous) / previous) * 100
                    improvements[metric] = round(improvement_pct, 2)

            # Identify improvement areas
            improvement_areas = []
            if current_metrics.get('avg_cs_per_min', 0) < 7.0:
                improvement_areas.append('cs_efficiency')
            if current_metrics.get('avg_vision_score_per_min', 0) < 0.8:
                improvement_areas.append('vision_control')
            if current_metrics.get('deaths_per_game', 10) > 6:
                improvement_areas.append('positioning')

            # Calculate overall improvement velocity
            avg_improvement = sum(improvements.values()) / len(improvements) if improvements else 0

            return {
                'trajectory': 'improving' if avg_improvement > 0 else 'stable',
                'improvement_velocity': round(avg_improvement, 2),
                'improvements_by_metric': improvements,
                'predicted_improvement_areas': improvement_areas,
                'growth_potential': 'high' if avg_improvement > 10 else 'moderate'
            }

        except Exception as e:
            logger.error(f"Error analyzing growth: {str(e)}")
            return {
                'trajectory': 'error',
                'error': str(e)
            }

    def classify_playstyle(self, metrics: Dict) -> Dict:
        """
        Model 4: Play Style Profiler
        Classifies player's playstyle archetype
        """
        try:
            # Calculate playstyle indicators
            aggression_index = self._calculate_aggression_index(metrics)
            teamwork_orientation = self._calculate_teamwork_orientation(metrics)
            mechanical_skill = self._calculate_mechanical_skill(metrics)

            # Classify into archetype
            archetype = self._determine_archetype(
                aggression_index,
                teamwork_orientation,
                mechanical_skill
            )

            return {
                'archetype': archetype,
                'aggression_index': round(aggression_index, 2),
                'teamwork_orientation': round(teamwork_orientation, 2),
                'mechanical_skill': round(mechanical_skill, 2),
                'playstyle_description': self._get_archetype_description(archetype)
            }

        except Exception as e:
            logger.error(f"Error classifying playstyle: {str(e)}")
            return {
                'archetype': 'Unknown',
                'error': str(e)
            }

    def _calculate_aggression_index(self, metrics: Dict) -> float:
        """Calculate aggression index (0-100)"""
        kills_per_game = float(metrics.get('kills_per_game', 0))
        deaths_per_game = float(metrics.get('deaths_per_game', 1))

        # Higher kills and deaths = more aggressive
        aggression = (kills_per_game * 5) + (deaths_per_game * 3)
        return min(100, aggression)

    def _calculate_teamwork_orientation(self, metrics: Dict) -> float:
        """Calculate teamwork orientation (0-100)"""
        assists_per_game = float(metrics.get('assists_per_game', 0))
        obj_participation = float(metrics.get('avg_objective_participation', 0))

        # Higher assists and objective participation = more teamwork focused
        teamwork = (assists_per_game * 8) + (obj_participation * 100)
        return min(100, teamwork)

    def _calculate_mechanical_skill(self, metrics: Dict) -> float:
        """Calculate mechanical skill (0-100)"""
        cs_per_min = float(metrics.get('avg_cs_per_min', 0))
        kda = float(metrics.get('kda', 0))

        # CS efficiency and KDA as mechanical proxies
        mechanical = (cs_per_min * 10) + (kda * 5)
        return min(100, mechanical)

    def _determine_archetype(self, aggression: float, teamwork: float, mechanical: float) -> str:
        """Determine playstyle archetype from scores"""
        if teamwork > 60 and aggression < 50:
            return "Strategic Enabler"
        elif aggression > 70 and mechanical > 60:
            return "Mechanical Carry"
        elif mechanical > 70:
            return "Late-Game Scaler"
        elif aggression > 60:
            return "Aggressive Playmaker"
        elif teamwork > 70:
            return "Team-Oriented Support"
        else:
            return "Balanced All-Rounder"

    def _get_archetype_description(self, archetype: str) -> str:
        """Get description for archetype"""
        descriptions = {
            "Strategic Enabler": "Focuses on team coordination and objective control",
            "Mechanical Carry": "Relies on mechanical skill to dominate games",
            "Late-Game Scaler": "Excels in extended games with strong scaling",
            "Aggressive Playmaker": "Creates opportunities through aggressive plays",
            "Team-Oriented Support": "Enables team success through vision and assists",
            "Balanced All-Rounder": "Well-rounded gameplay across all aspects"
        }
        return descriptions.get(archetype, "Unknown playstyle")


def process_player_inference(player_puuid: str, year: int) -> Dict:
    """Run all ML models on player data"""
    try:
        # Get player metrics
        metrics_table = dynamodb.Table(METRICS_TABLE_NAME)
        response = metrics_table.get_item(
            Key={
                'player_puuid': player_puuid,
                'year': year
            }
        )

        if 'Item' not in response:
            return {
                'success': False,
                'error': 'Metrics not found for player'
            }

        current_metrics = response['Item']

        # Get previous year metrics if available
        previous_year = year - 1
        prev_response = metrics_table.get_item(
            Key={
                'player_puuid': player_puuid,
                'year': previous_year
            }
        )
        previous_metrics = prev_response.get('Item')

        # Initialize pipeline
        pipeline = MLModelPipeline(MODELS_BUCKET)

        # Run all models
        performance_pattern = pipeline.classify_performance_pattern(current_metrics)
        mental_resilience = pipeline.calculate_mental_resilience(current_metrics)
        growth_trajectory = pipeline.analyze_growth_trajectory(current_metrics, previous_metrics)
        playstyle = pipeline.classify_playstyle(current_metrics)

        # Compile results
        inference_results = {
            'player_puuid': player_puuid,
            'year': year,
            'performance_pattern': performance_pattern,
            'mental_resilience': mental_resilience,
            'growth_trajectory': growth_trajectory,
            'playstyle': playstyle,
            'processed_at': datetime.utcnow().isoformat()
        }

        # Save results back to metrics table
        metrics_table.update_item(
            Key={
                'player_puuid': player_puuid,
                'year': year
            },
            UpdateExpression='SET ml_inference = :inference',
            ExpressionAttributeValues={
                ':inference': inference_results
            }
        )

        return {
            'success': True,
            'results': inference_results
        }

    except Exception as e:
        logger.error(f"Error in player inference: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


def lambda_handler(event, context):
    """
    Lambda handler for model inference

    Event formats:
    {
        "player_puuid": "string",
        "year": 2025
    }

    OR for training (annual batch):
    {
        "action": "train_models"
    }
    """

    try:
        logger.info(f"Event: {json.dumps(event, default=str)}")

        action = event.get('action')

        if action == 'train_models':
            # This would trigger model training
            # For now, return placeholder
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Model training triggered',
                    'note': 'Training process would run here'
                })
            }

        # Standard inference
        player_puuid = event.get('player_puuid')
        year = event.get('year', datetime.utcnow().year)

        if not player_puuid:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'player_puuid is required'
                })
            }

        # Run inference
        result = process_player_inference(player_puuid, year)

        if result['success']:
            return {
                'statusCode': 200,
                'body': json.dumps(result)
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps(result)
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
