#!/usr/bin/env python3
"""
RiftSage AI Agent - Champion Database Seeder
Populates the ChampionRecommendationsTable with champion data
"""

import json
import boto3
import argparse
from typing import Dict, List

# Sample champion data
CHAMPION_DATA = [
    {
        "champion_name": "Ashe",
        "role": "ADC",
        "playstyle_fit": ["Strategic Enabler", "Team-Oriented Support"],
        "avg_cs_min": 7.8,
        "avg_vision_min": 0.92,
        "avg_kda": 3.2,
        "avg_damage_share": 0.28,
        "win_rate_by_rank": {
            "gold": 52.1,
            "platinum": 53.2,
            "diamond": 51.8,
            "master": 50.5
        },
        "strengths": [
            "Global vision with Hawkshot (E)",
            "High range for safe farming",
            "Strong pick potential with Crystal Arrow (R)"
        ],
        "learning_curve": "Low",
        "meta_status": "Stable",
        "fit_explanation_template": "Global vision and arrows turn positioning into team-wide picks and control"
    },
    {
        "champion_name": "Jinx",
        "role": "ADC",
        "playstyle_fit": ["Mechanical Carry", "Late-Game Scaler"],
        "avg_cs_min": 8.4,
        "avg_vision_min": 0.78,
        "avg_kda": 3.8,
        "avg_damage_share": 0.32,
        "win_rate_by_rank": {
            "gold": 53.5,
            "platinum": 52.8,
            "diamond": 51.2,
            "master": 49.8
        },
        "strengths": [
            "Rocket waveclear for efficient farming",
            "Hyperscaling into late game",
            "Reset potential in teamfights"
        ],
        "learning_curve": "Medium",
        "meta_status": "Strong",
        "fit_explanation_template": "Rockets clear waves fast for more gold and items, scaling into late-game power"
    },
    {
        "champion_name": "Sivir",
        "role": "ADC",
        "playstyle_fit": ["Balanced All-Rounder"],
        "avg_cs_min": 8.7,
        "avg_vision_min": 0.81,
        "avg_kda": 3.1,
        "avg_damage_share": 0.29,
        "win_rate_by_rank": {
            "gold": 51.8,
            "platinum": 52.5,
            "diamond": 52.2,
            "master": 51.0
        },
        "strengths": [
            "Spell shield for safety",
            "Superior waveclear",
            "Utility ultimate for team mobility"
        ],
        "learning_curve": "Low",
        "meta_status": "Stable",
        "fit_explanation_template": "Spell shield blocks danger while waveclear keeps you rich and safe"
    },
    {
        "champion_name": "Leona",
        "role": "SUPPORT",
        "playstyle_fit": ["Aggressive Playmaker", "Team-Oriented Support"],
        "avg_cs_min": 0.5,
        "avg_vision_min": 1.2,
        "avg_kda": 2.8,
        "avg_damage_share": 0.08,
        "win_rate_by_rank": {
            "gold": 52.5,
            "platinum": 53.1,
            "diamond": 51.9,
            "master": 50.2
        },
        "strengths": [
            "High engage potential",
            "Tanky with aftershock",
            "Strong all-in combos"
        ],
        "learning_curve": "Medium",
        "meta_status": "Strong",
        "fit_explanation_template": "Engage tools create picks while tankiness keeps you alive to enable team"
    },
    {
        "champion_name": "Thresh",
        "role": "SUPPORT",
        "playstyle_fit": ["Strategic Enabler", "Mechanical Carry"],
        "avg_cs_min": 0.6,
        "avg_vision_min": 1.3,
        "avg_kda": 3.2,
        "avg_damage_share": 0.09,
        "win_rate_by_rank": {
            "gold": 50.8,
            "platinum": 51.5,
            "diamond": 52.3,
            "master": 53.1
        },
        "strengths": [
            "Versatile hook engage",
            "Lantern for saves and playmaking",
            "High skill expression"
        ],
        "learning_curve": "High",
        "meta_status": "Stable",
        "fit_explanation_template": "Hook creates picks, lantern saves teammates, high skill ceiling rewards practice"
    }
]


def seed_champion_database(environment: str, region: str):
    """Seed the champion recommendations table"""

    table_name = f"riftsage-ChampionRecs-{environment}"

    print(f"Seeding champion database: {table_name}")
    print(f"Region: {region}")

    # Initialize DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(table_name)

    # Insert champions
    success_count = 0
    error_count = 0

    for champion in CHAMPION_DATA:
        try:
            table.put_item(Item=champion)
            print(f"✓ Added {champion['champion_name']} ({champion['role']})")
            success_count += 1
        except Exception as e:
            print(f"✗ Error adding {champion['champion_name']}: {str(e)}")
            error_count += 1

    print(f"\nSeeding complete:")
    print(f"  Success: {success_count}")
    print(f"  Errors: {error_count}")

    return success_count, error_count


def main():
    parser = argparse.ArgumentParser(description='Seed RiftSage champion database')
    parser.add_argument('--environment', default='production', choices=['development', 'staging', 'production'])
    parser.add_argument('--region', default='us-east-1')

    args = parser.parse_args()

    seed_champion_database(args.environment, args.region)


if __name__ == '__main__':
    main()
