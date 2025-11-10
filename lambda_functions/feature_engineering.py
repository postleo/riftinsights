"""
RiftSage AI Agent - Feature Engineering Lambda Function
Transforms raw match data into ML-ready features
"""

import json
import os
import boto3
import logging
from datetime import datetime
from typing import Dict, List, Any
from decimal import Decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# Environment variables
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')
DATA_BUCKET = os.environ.get('DATA_BUCKET')
METRICS_TABLE_NAME = os.environ.get('METRICS_TABLE')


class DecimalEncoder(json.JSONEncoder):
    """Helper class to convert Decimal to float for JSON serialization"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


def calculate_kda(kills: int, deaths: int, assists: int) -> float:
    """Calculate KDA ratio"""
    if deaths == 0:
        return float(kills + assists)
    return round((kills + assists) / deaths, 2)


def calculate_cs_per_min(total_cs: int, game_duration_seconds: int) -> float:
    """Calculate CS per minute"""
    game_minutes = game_duration_seconds / 60
    if game_minutes == 0:
        return 0.0
    return round(total_cs / game_minutes, 2)


def calculate_vision_score_per_min(vision_score: int, game_duration_seconds: int) -> float:
    """Calculate vision score per minute"""
    game_minutes = game_duration_seconds / 60
    if game_minutes == 0:
        return 0.0
    return round(vision_score / game_minutes, 2)


def calculate_gold_per_min(total_gold: int, game_duration_seconds: int) -> float:
    """Calculate gold per minute"""
    game_minutes = game_duration_seconds / 60
    if game_minutes == 0:
        return 0.0
    return round(total_gold / game_minutes, 2)


def calculate_damage_efficiency(damage_dealt: int, damage_taken: int) -> float:
    """Calculate damage efficiency ratio"""
    if damage_taken == 0:
        return float(damage_dealt)
    return round(damage_dealt / damage_taken, 2)


def identify_comeback_game(match_data: Dict, participant_data: Dict) -> bool:
    """
    Identify if this was a comeback game
    (team was down 5k+ gold at 20 min but won)
    """
    try:
        # This would require timeline data - simplified version
        win = participant_data.get('win', False)
        game_duration = match_data['info']['gameDuration']

        # Comeback detection heuristic:
        # If game lasted 35+ minutes and won, likely comeback
        if win and game_duration > 2100:  # 35 minutes
            return True

        return False
    except:
        return False


def determine_primary_role(match_data: Dict, participant_data: Dict) -> str:
    """Determine player's role in the match"""
    try:
        # Try to get from teamPosition first (more accurate)
        position = participant_data.get('teamPosition', '')

        role_map = {
            'TOP': 'TOP',
            'JUNGLE': 'JUNGLE',
            'MIDDLE': 'MID',
            'BOTTOM': 'ADC',
            'UTILITY': 'SUPPORT'
        }

        return role_map.get(position, 'UNKNOWN')
    except:
        return 'UNKNOWN'


def calculate_objective_participation(participant_data: Dict, team_data: Dict) -> float:
    """Calculate objective participation rate"""
    try:
        challenges = participant_data.get('challenges', {})

        # Baron + Dragon + Rift Herald kills
        player_objectives = (
            challenges.get('baronKills', 0) +
            challenges.get('dragonKills', 0) +
            challenges.get('riftHeraldKills', 0)
        )

        # Team objectives
        team_objectives = (
            team_data.get('objectives', {}).get('baron', {}).get('kills', 0) +
            team_data.get('objectives', {}).get('dragon', {}).get('kills', 0) +
            team_data.get('objectives', {}).get('riftHerald', {}).get('kills', 0)
        )

        if team_objectives == 0:
            return 0.0

        return round(player_objectives / team_objectives, 2)
    except:
        return 0.0


def extract_features_from_match(match_data: Dict, player_puuid: str) -> Dict:
    """Extract all features from a single match"""

    try:
        info = match_data['info']
        metadata = match_data['metadata']

        # Find the participant
        participant_data = None
        participant_id = None

        for participant in info['participants']:
            if participant['puuid'] == player_puuid:
                participant_data = participant
                participant_id = participant['participantId']
                break

        if not participant_data:
            raise ValueError("Player not found in match")

        # Find team data
        team_id = participant_data['teamId']
        team_data = None
        for team in info['teams']:
            if team['teamId'] == team_id:
                team_data = team
                break

        # Extract basic stats
        game_duration = info['gameDuration']

        features = {
            # Match metadata
            'match_id': metadata['matchId'],
            'game_creation': info['gameCreation'],
            'game_duration': game_duration,
            'game_mode': info['gameMode'],
            'game_type': info['gameType'],

            # Participant info
            'champion_name': participant_data['championName'],
            'champion_id': participant_data['championId'],
            'role': determine_primary_role(match_data, participant_data),
            'team_position': participant_data.get('teamPosition', ''),

            # Core stats
            'win': participant_data['win'],
            'kills': participant_data['kills'],
            'deaths': participant_data['deaths'],
            'assists': participant_data['assists'],
            'kda': calculate_kda(
                participant_data['kills'],
                participant_data['deaths'],
                participant_data['assists']
            ),

            # Farm
            'total_minions_killed': participant_data['totalMinionsKilled'],
            'neutral_minions_killed': participant_data['neutralMinionsKilled'],
            'total_cs': participant_data['totalMinionsKilled'] + participant_data['neutralMinionsKilled'],
            'cs_per_min': calculate_cs_per_min(
                participant_data['totalMinionsKilled'] + participant_data['neutralMinionsKilled'],
                game_duration
            ),

            # Gold
            'gold_earned': participant_data['goldEarned'],
            'gold_spent': participant_data['goldSpent'],
            'gold_per_min': calculate_gold_per_min(
                participant_data['goldEarned'],
                game_duration
            ),

            # Damage
            'total_damage_dealt': participant_data['totalDamageDealtToChampions'],
            'total_damage_taken': participant_data['totalDamageTaken'],
            'damage_efficiency': calculate_damage_efficiency(
                participant_data['totalDamageDealtToChampions'],
                participant_data['totalDamageTaken']
            ),

            # Vision
            'vision_score': participant_data['visionScore'],
            'vision_score_per_min': calculate_vision_score_per_min(
                participant_data['visionScore'],
                game_duration
            ),
            'wards_placed': participant_data['wardsPlaced'],
            'wards_killed': participant_data['wardsKilled'],
            'control_wards_placed': participant_data.get('detectorWardsPlaced', 0),

            # Objectives
            'turret_kills': participant_data.get('turretKills', 0),
            'inhibitor_kills': participant_data.get('inhibitorKills', 0),
            'objective_participation': calculate_objective_participation(participant_data, team_data),

            # Performance indicators
            'double_kills': participant_data.get('doubleKills', 0),
            'triple_kills': participant_data.get('tripleKills', 0),
            'quadra_kills': participant_data.get('quadraKills', 0),
            'penta_kills': participant_data.get('pentaKills', 0),
            'first_blood': participant_data.get('firstBloodKill', False),

            # Challenges (if available)
            'challenges': participant_data.get('challenges', {}),

            # Special flags
            'is_comeback_game': identify_comeback_game(match_data, participant_data),
            'early_surrender': game_duration < 900,  # Less than 15 minutes
            'late_game': game_duration > 2100,  # More than 35 minutes
        }

        return features

    except Exception as e:
        logger.error(f"Error extracting features: {str(e)}")
        raise


def aggregate_metrics(all_match_features: List[Dict], year: int) -> Dict:
    """Aggregate features across all matches for a player"""

    if not all_match_features:
        return {}

    total_games = len(all_match_features)
    wins = sum(1 for m in all_match_features if m['win'])

    # Aggregate by role
    roles = {}
    for match in all_match_features:
        role = match['role']
        if role not in roles:
            roles[role] = []
        roles[role].append(match)

    # Determine primary role (most games)
    primary_role = max(roles.keys(), key=lambda r: len(roles[r])) if roles else 'UNKNOWN'

    # Calculate averages
    total_kills = sum(m['kills'] for m in all_match_features)
    total_deaths = sum(m['deaths'] for m in all_match_features)
    total_assists = sum(m['assists'] for m in all_match_features)

    aggregated = {
        'year': year,
        'total_games': total_games,
        'wins': wins,
        'losses': total_games - wins,
        'win_rate': round((wins / total_games) * 100, 2) if total_games > 0 else 0,

        # Primary role
        'primary_role': primary_role,
        'role_distribution': {role: len(matches) for role, matches in roles.items()},

        # KDA
        'total_kills': total_kills,
        'total_deaths': total_deaths,
        'total_assists': total_assists,
        'kills_per_game': round(total_kills / total_games, 2),
        'deaths_per_game': round(total_deaths / total_games, 2),
        'assists_per_game': round(total_assists / total_games, 2),
        'kda': calculate_kda(total_kills, total_deaths, total_assists),

        # Average stats
        'avg_cs_per_min': round(sum(m['cs_per_min'] for m in all_match_features) / total_games, 2),
        'avg_gold_per_min': round(sum(m['gold_per_min'] for m in all_match_features) / total_games, 2),
        'avg_vision_score_per_min': round(sum(m['vision_score_per_min'] for m in all_match_features) / total_games, 2),
        'avg_damage_efficiency': round(sum(m['damage_efficiency'] for m in all_match_features) / total_games, 2),
        'avg_objective_participation': round(sum(m['objective_participation'] for m in all_match_features) / total_games, 2),

        # Performance indicators
        'comeback_wins': sum(1 for m in all_match_features if m['is_comeback_game'] and m['win']),
        'late_game_wins': sum(1 for m in all_match_features if m['late_game'] and m['win']),
        'late_game_losses': sum(1 for m in all_match_features if m['late_game'] and not m['win']),

        # Multi-kills
        'total_double_kills': sum(m['double_kills'] for m in all_match_features),
        'total_triple_kills': sum(m['triple_kills'] for m in all_match_features),
        'total_quadra_kills': sum(m['quadra_kills'] for m in all_match_features),
        'total_penta_kills': sum(m['penta_kills'] for m in all_match_features),

        # Champion pool
        'unique_champions': len(set(m['champion_name'] for m in all_match_features)),
        'most_played_champion': max(
            set(m['champion_name'] for m in all_match_features),
            key=lambda c: sum(1 for m in all_match_features if m['champion_name'] == c)
        ),

        # Metadata
        'processed_at': datetime.utcnow().isoformat(),
    }

    return aggregated


def save_metrics_to_dynamodb(player_puuid: str, metrics: Dict):
    """Save aggregated metrics to DynamoDB"""
    try:
        metrics_table = dynamodb.Table(METRICS_TABLE_NAME)

        # Convert floats to Decimal for DynamoDB
        def convert_floats(obj):
            if isinstance(obj, dict):
                return {k: convert_floats(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_floats(item) for item in obj]
            elif isinstance(obj, float):
                return Decimal(str(obj))
            return obj

        metrics_decimal = convert_floats(metrics)

        metrics_table.put_item(
            Item={
                'player_puuid': player_puuid,
                'year': metrics['year'],
                **metrics_decimal
            }
        )

        logger.info(f"Saved metrics for {player_puuid} to DynamoDB")
    except Exception as e:
        logger.error(f"Error saving metrics: {str(e)}")
        raise


def lambda_handler(event, context):
    """
    Lambda handler for feature engineering

    Triggered by S3 event when new match data is uploaded
    OR manually with player_puuid and year

    Event formats:
    1. S3 Event (automatic):
    {
        "Records": [{
            "s3": {
                "bucket": {"name": "..."},
                "object": {"key": "raw-matches/PUUID/2025/match_id.json"}
            }
        }]
    }

    2. Manual trigger:
    {
        "player_puuid": "string",
        "year": 2025
    }
    """

    try:
        logger.info(f"Event: {json.dumps(event, default=str)}")

        # Determine if this is an S3 event or manual trigger
        if 'Records' in event and event['Records']:
            # S3 event - process single match
            record = event['Records'][0]
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']

            logger.info(f"Processing S3 event: {bucket}/{key}")

            # Parse key to extract player_puuid and year
            # Format: raw-matches/PUUID/YEAR/match_id.json
            parts = key.split('/')
            if len(parts) != 4 or parts[0] != 'raw-matches':
                logger.warning(f"Invalid S3 key format: {key}")
                return {'statusCode': 400, 'body': 'Invalid key format'}

            player_puuid = parts[1]
            year = int(parts[2])

            # Get match data from S3
            response = s3_client.get_object(Bucket=bucket, Key=key)
            match_data = json.loads(response['Body'].read())

            # Extract features
            features = extract_features_from_match(match_data, player_puuid)

            logger.info(f"Extracted features for match {features['match_id']}")

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'success': True,
                    'match_id': features['match_id'],
                    'player_puuid': player_puuid
                })
            }

        else:
            # Manual trigger - aggregate all matches
            player_puuid = event.get('player_puuid')
            year = event.get('year', datetime.utcnow().year)

            if not player_puuid:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'player_puuid is required'})
                }

            logger.info(f"Manual trigger: aggregating metrics for {player_puuid}, year {year}")

            # List all match files for this player and year
            prefix = f"raw-matches/{player_puuid}/{year}/"
            response = s3_client.list_objects_v2(Bucket=DATA_BUCKET, Prefix=prefix)

            if 'Contents' not in response:
                logger.warning(f"No matches found for {player_puuid} in {year}")
                return {
                    'statusCode': 404,
                    'body': json.dumps({'error': 'No matches found'})
                }

            # Process each match
            all_match_features = []

            for obj in response['Contents']:
                key = obj['Key']
                if not key.endswith('.json'):
                    continue

                # Get match data
                match_response = s3_client.get_object(Bucket=DATA_BUCKET, Key=key)
                match_data = json.loads(match_response['Body'].read())

                # Extract features
                try:
                    features = extract_features_from_match(match_data, player_puuid)
                    all_match_features.append(features)
                except Exception as e:
                    logger.error(f"Error processing match {key}: {str(e)}")
                    continue

            if not all_match_features:
                return {
                    'statusCode': 500,
                    'body': json.dumps({'error': 'Failed to process any matches'})
                }

            # Aggregate metrics
            aggregated_metrics = aggregate_metrics(all_match_features, year)

            # Save to DynamoDB
            save_metrics_to_dynamodb(player_puuid, aggregated_metrics)

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'success': True,
                    'player_puuid': player_puuid,
                    'year': year,
                    'matches_processed': len(all_match_features),
                    'metrics': aggregated_metrics
                }, cls=DecimalEncoder)
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
