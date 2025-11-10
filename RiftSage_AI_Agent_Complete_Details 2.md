# RiftSage AI Agent - Complete App Details Document 2 (Updated)

### 5. Dynamic Content Adaptation System

**CRITICAL UNDERSTANDING**: RiftSage does NOT use pre-written templates with fill-in-the-blank placeholders. Instead, the AI (Amazon Bedrock with Claude) **generates 100% of the content dynamically** based on each player's unique data.

**Core Adaptation Principles**:

1. **AI-Driven Generation**: Every sentence is created by the AI based on player's specific metrics
2. **Strength-Based Focus**: Always lead with player's best-performing metrics
3. **Relative Benchmarking**: Compare to rank-appropriate standards, not absolute
4. **Personalized Recommendations**: Champion and strategy suggestions match playstyle archetype
5. **Realistic Targets**: Improvement goals scaled to current baseline + 15-25% stretch
6. **Context-Aware Insights**: Interpret metrics based on role, champion pool, and game volume
7. **Unique Content**: No two players receive identical text unless they have identical performance

**How It Works**:

```
TRADITIONAL APPROACH (NOT USED):
Template: "Your [X]% win rate shows [pattern]"
→ Code fills in X and pattern
→ Result: Mechanical, generic

RIFTSAGE APPROACH (ACTUAL):
Data Package: {win_rate: 65%, rank_avg: 52%, kda: 3.8, ...}
→ AI analyzes entire performance profile
→ AI generates: "Your 65% win rate, sitting 13 points above your rank tier, 
   reflects an ability to convert mechanical advantages into decisive game 
   closures—you're not just winning lanes, you're finishing games"
→ Result: Unique, insightful, adapted to THIS player
```

**Data Package Preparation (Lambda Function)**:

Before calling Bedrock, Lambda functions prepare comprehensive data packages:

```python
def prepare_section_data_package(player_id, section_type):
    """
    Prepares all data needed for AI to generate a specific section
    """
    # Fetch player metrics
    metrics = get_player_metrics(player_id)
    
    # Fetch comparative context
    rank_averages = get_rank_benchmarks(metrics['current_rank'])
    percentiles = calculate_percentiles(metrics, rank_averages)
    
    # Identify strengths and weaknesses
    strengths = identify_top_metrics(metrics, percentiles, top_n=4)
    weaknesses = identify_improvement_areas(metrics, rank_averages, top_n=2)
    
    # Determine primary patterns
    primary_pattern = classify_performance_pattern(metrics)
    playstyle_archetype = get_playstyle_archetype(player_id)
    
    # Assemble data package
    data_package = {
        "player_metrics": {
            "win_rate": metrics['win_rate'],
            "rank_avg_win_rate": rank_averages['win_rate'],
            "win_rate_percentile": percentiles['win_rate'],
            "kda": metrics['kda'],
            "kda_2024": metrics.get('kda_2024'),  # If available
            "kills_per_game": metrics['kills_avg'],
            "assists_per_game": metrics['assists_avg'],
            "deaths_per_game": metrics['deaths_avg'],
            "cs_min": metrics['cs_min'],
            "vision_min": metrics['vision_min'],
            # ... all other metrics
        },
        "comparative_analysis": {
            "top_strengths": strengths,  # ["KDA", "Win Rate", "Kills per Game"]
            "improvement_areas": weaknesses,  # ["CS/min", "Vision/min"]
            "overall_percentile": percentiles['overall'],
            "rank": metrics['current_rank'],
            "rank_tier": metrics['rank_tier']  # e.g., "Platinum III"
        },
        "context": {
            "primary_pattern": primary_pattern,  # e.g., "aggressive + survival"
            "playstyle_archetype": playstyle_archetype,  # e.g., "Strategic Enabler"
            "games_played": metrics['total_games'],
            "primary_role": metrics['primary_role']
        }
    }
    
    return data_package
```

**AI Generation Process**:

```python
def generate_section_via_bedrock(section_type, data_package):
    """
    Calls Amazon Bedrock to generate complete section content
    """
    # Load section-specific prompt template
    prompt_template = load_prompt_template(f'{section_type}_v2.txt')
    
    # Construct full prompt
    full_prompt = f"""
{prompt_template}

PLAYER DATA:
{json.dumps(data_package, indent=2)}

Generate the complete {section_type} section following the 4-part structure:
1. Intro Overview (contextual paragraph)
2. Stats & Metrics (top 4 with insights)
3. Deeper Insights (4-5 bullet points)
4. Narrative Meaning (3-5 sentence synthesis)

CRITICAL: Every word must be generated based on THIS player's unique data.
Analyze their specific performance profile and create insights that would
ONLY apply to them. Do not use generic statements.
"""
    
    # Call Bedrock
    response = bedrock_client.invoke_model(
        modelId='anthropic.claude-3-sonnet-20240229-v1:0',
        body=json.dumps({
            'anthropic_version': 'bedrock-2023-05-31',
            'max_tokens': 2500,
            'temperature': 0.3,  # Low temperature for consistency
            'messages': [{'role': 'user', 'content': full_prompt}]
        })
    )
    
    # Extract generated text
    generated_content = json.loads(response['body'].read())['content'][0]['text']
    
    return generated_content
```

**Adaptation Logic Examples**:

The AI automatically adapts based on data patterns:

**Example 1: High Win Rate Player (65%)**
```
AI receives: win_rate=65%, rank_avg=52%, percentile=87th

AI generates Intro:
"Your recent games show a clear pattern of dominant game execution paired with 
consistent decision-making superiority, with win conversion 13 points above 
your rank average and performance in the 87th percentile. Your key impact 
metrics show:"

AI emphasizes: Game-closing power, consistency, climb potential
```

**Example 2: High CS, Low Win Rate Player (48%)**
```
AI receives: win_rate=48%, cs_min=8.2 (91st percentile), kda=2.1

AI generates Intro:
"Your recent games show a clear pattern of exceptional economic development 
paired with mechanical precision in lane phase, with CS rates in the 91st 
percentile but win conversion challenges in mid-to-late transitions. Your key 
resource generation metrics show:"

AI emphasizes: Farming strength, acknowledges macro weaknesses, focuses on conversion
```

**Example 3: Comeback Specialist Player**
```
AI receives: comeback_wins=18, tilt_resistance=89, late_game_wr=72%

AI generates Intro:
"Your recent games show a clear pattern of exceptional mental resilience paired 
with clutch performance under pressure, with 18 comeback victories from 5k+ 
gold deficits and late-game decision-making in the 89th percentile. Your key 
mental game metrics show:"

AI emphasizes: Resilience, pressure performance, comeback factor
```

**Champion Recommendation Logic**:

Instead of pre-determined recommendations, the system:

1. **Queries Champion Database** based on player's role and playstyle archetype
2. **Calculates Fit Scores** for each champion based on:
   - How well champion addresses player's weaknesses (30 points)
   - How well champion leverages player's strengths (25 points)
   - Meta strength (20 points)
   - Learning curve match (15 points)
   - Pool synergy (10 points)
3. **Selects Top 3** champions with highest fit scores
4. **AI Generates Explanations** for why each champion fits THIS player

```python
def generate_champion_recommendations(player_data):
    """
    Dynamically selects and explains champion recommendations
    """
    # Calculate fit scores for all role-appropriate champions
    champions = query_champion_database(role=player_data['primary_role'])
    
    scored_champions = []
    for champion in champions:
        fit_score = calculate_champion_fit_score(
            champion=champion,
            player_strengths=player_data['strengths'],
            player_weaknesses=player_data['weaknesses'],
            playstyle=player_data['archetype']
        )
        scored_champions.append((champion, fit_score))
    
    # Select top 3
    top_3 = sorted(scored_champions, key=lambda x: x[1], reverse=True)[:3]
    
    # AI generates unique fit explanations
    recommendations = []
    for champion, score in top_3:
        prompt = f"""
Explain why {champion['name']} is recommended for this player:

PLAYER PROFILE:
- Strengths: {player_data['strengths']}
- Weaknesses: {player_data['weaknesses']}
- Playstyle: {player_data['archetype']}
- Current CS/min: {player_data['cs_min']}
- Current Vision/min: {player_data['vision_min']}

CHAMPION ATTRIBUTES:
- Avg CS/min for this champion: {champion['avg_cs_min']}
- Avg Vision/min: {champion['avg_vision_min']}
- Strengths: {champion['strengths']}

Generate a 1-sentence explanation of how this champion enables the player's 
strengths while addressing their weaknesses. Be specific.
"""
        explanation = call_bedrock(prompt)
        
        recommendations.append({
            'champion': champion['name'],
            'fit_score': score,
            'explanation': explanation
        })
    
    return recommendations
```

**Improvement Target Calculation**:

Targets are calculated algorithmically, then AI explains what they mean:

```python
def generate_improvement_targets(player_data, rank_averages):
    """
    Calculates targets and generates AI explanation
    """
    # Calculate numeric targets
    targets = {}
    
    for metric in player_data['weaknesses']:
        current = player_data[metric]
        rank_avg = rank_averages[metric]
        
        # Calculate target (80% to average OR 20% improvement, whichever higher)
        target_option_1 = current + (rank_avg - current) * 0.8
        target_option_2 = current * 1.20
        target = max(target_option_1, target_option_2)
        
        targets[metric] = {
            'current': current,
            'target': round(target, 2),
            'timeline': '30 days'
        }
    
    # AI generates outcome descriptions
    for metric, target_data in targets.items():
        prompt = f"""
A player currently has {metric} of {target_data['current']}. 
Their target is to reach {target_data['target']} in 30 days.
In 10 words or less, describe the gameplay benefit of achieving this target.
Format: "[Quantified benefit]"

Examples:
- CS/min: "+1,200 gold every 10 minutes"
- Vision/min: "More picks, safer plays, objective control"
"""
        outcome = call_bedrock(prompt)
        target_data['outcome_description'] = outcome
    
    return targets
```

**Section Generation Flow**:

```
1. Lambda: Prepare data package
   ├── Fetch player metrics from DynamoDB
   ├── Calculate percentiles and comparisons
   ├── Identify strengths/weaknesses
   └── Package into JSON

2. Lambda: Load prompt template
   ├── Get section-specific instructions
   └── Inject player data

3. Bedrock: Generate content
   ├── Analyze player's unique profile
   ├── Create Intro Overview (contextual paragraph)
   ├── Generate Stats & Metrics (with insights)
   ├── Write Deeper Insights (pattern explanations)
   └── Synthesize Narrative Meaning (implications)

4. Lambda: Validate output
   ├── Check 4-part structure exists
   ├── Verify metrics match player data
   ├── Ensure no generic templates used
   └── Confirm appropriate length

5. Lambda: Store generated section
   ├── Save to DynamoDB
   └── Trigger next section generation
```

**Key Difference Summary**:

| Aspect | Template Approach | RiftSage Approach |
|--------|------------------|-------------------|
| **Content Creation** | Pre-written with blanks | 100% AI-generated |
| **Uniqueness** | Similar across players | Unique per player |
| **Adaptation** | Limited to variable substitution | Deep analysis of performance profile |
| **Insights** | Generic patterns | Player-specific revelations |
| **Scalability** | Requires manual updates | Self-adapting to new data patterns |

**Result**: Every player receives a completely unique report with insights that reflect their specific gameplay patterns, strengths, weaknesses, and potential—nothing is generic or reusable across different players.

---

### 6. AI-Powered Insight Generation (Amazon Bedrock)

**Model Configuration**:
- **Primary Model**: Claude 3 Sonnet (for balanced quality and cost)
- **Fallback Model**: Claude 3 Haiku (if token limits or cost constraints)
- **Max Tokens**: 4,000 per section generation
- **Temperature**: 0.3 (for consistent, data-focused output)

**Prompt Engineering Strategy**:

**System Prompt Template**:
```
You are RiftSage, an AI performance analyst for League of Legends. Your role 
is to transform match data into clear, actionable insights using a standardized 
four-part framework.

CRITICAL RULES:
1. Always use the four-part structure: Intro Overview → Stats & Metrics → 
   Deeper Insights → Narrative Meaning
2. The Intro Overview must frame the data story before presenting numbers
3. Be data-grounded: every claim must reference specific metrics
4. Frame achievements meaningfully without fictional embellishment
5. Adapt content to player's unique strengths while maintaining structure
6. Use precise numbers and percentages from provided data
7. Write in clear, direct language that respects player intelligence
8. Provide actionable guidance backed by statistical patterns

TONE: Professional, motivating, data-focused, respectful
STYLE: Clear bullet points for insights, brief paragraphs for narrative
FORMAT: Use exact template structure provided for each section
```

**Section-Specific Prompt Templates**:

**For Role Performance Snapshot**:
```
Generate a Role Performance Snapshot analysis using this data:

PLAYER DATA:
- Primary Role: {role}
- Win Rate: {win_rate}% (Rank Average: {rank_avg}%)
- KDA: {kda} (Year-over-year: {yoy_change}%)
- Kills/Game: {kills_avg}
- Assists/Game: {assists_avg}
- Deaths/Game: {deaths_avg}
- CS/min: {cs_min}
- Vision Score/min: {vision_min}
- Rank: {current_rank}

COMPARISON CONTEXT:
- Player Rank Percentile: {percentile}
- Role Performance vs Rank: {comparison}

Use the Role Performance Snapshot template. Start with an Intro Overview that 
frames the player's performance story before presenting the stats. In the 
Intro Overview, describe the PATTERN you see in their games (e.g., "consistent 
survival paired with high combat output"). Identify the player's PRIMARY 
STRENGTH based on which metrics exceed rank average by the largest margin. 
Build insights around these strengths. For "Deeper Insights", explain HOW 
the metrics work together. For "Narrative Meaning", explain WHAT this 
combination reveals about effectiveness.
```

**For Improvement Blueprint**:
```
Generate an Improvement Blueprint using this data:

PLAYER DATA:
- Current Win Rate: {win_rate}%
- Current CS/min: {cs_min} (Rank Avg: {rank_avg_cs})
- Current Vision/min: {vision_min} (Rank Avg: {rank_avg_vision})
- Playstyle Archetype: {archetype}
- Strongest Role: {role}
- Top 3 Champions: {champion_list_with_winrates}

IMPROVEMENT OPPORTUNITIES:
- Metric 1: {metric} is {percent}% below rank average
- Metric 2: {metric} is {percent}% below rank average
- High Climb Correlation Metrics: {metrics_list}

CHAMPION DATABASE MATCHES (for recommendations):
- {champion_1}: {why_it_fits_playstyle}, Avg {metric1}, Avg {metric2}
- {champion_2}: {why_it_fits}, Avg {metric1}, Avg {metric2}
- {champion_3}: {why_it_fits}, Avg {metric1}, Avg {metric2}

Use the Improvement Blueprint template. Start with an Intro Overview that 
frames the improvement opportunity (e.g., "Your [strength] already proves 
your strength — now layer in [areas] to turn [short-term] into [long-term]"). 
Recommend specific numeric targets that represent 15-25% improvement from 
current baseline. For Phase-by-Phase Execution, provide ACTIONABLE behaviors 
tied to specific game times. For champion recommendations, explain HOW each 
champion enables the player's existing strengths while addressing weaknesses.
```

**For Outstanding Games Showcase**:
```
Generate Outstanding Games analysis using this data:

TOP 5 GAMES BY IMPACT SCORE:
Game 1: Date: {date}, Champion: {champ}, Result: {result}
  - Impact Score: {score}/100
  - KDA: {k}/{d}/{a} ({kda_ratio})
  - Standout Metrics: {metric1}: {value}, {metric2}: {value}, {metric3}: {value}
  - Game Context: {comeback/standard/clutch}, {additional_context}

[Repeat for Games 2-5]

PATTERNS ACROSS OUTSTANDING GAMES:
- Common Champion Types: {analysis}
- Common Game Situations: {analysis}
- Average Metrics in Outstanding Games vs Overall: {comparison}

Use the Outstanding Games template. Start with an Intro Overview that 
highlights what these exceptional performances reveal about the player 
(e.g., "Your standout performances reveal [characteristic], with [pattern], 
particularly strong in [context]"). For each game, identify the 2-3 metrics 
that were MOST exceptional compared to player's average. Categorize by 
excellence type. In "Deeper Insights", identify COMMON FACTORS across high-
impact games. In "Narrative Meaning", explain what these performances reveal 
about the player's ceiling.
```

**Quality Control Checks** (Post-Generation):

The system validates each generated section for:
- Presence of all four parts (Intro Overview, Stats & Metrics, Deeper Insights, Narrative Meaning)
- Intro Overview sets context before presenting statistics
- All metrics referenced match player data
- No fictional storytelling elements
- Actionable guidance with specific targets
- Appropriate section length (500-1500 words)
- Professional, data-focused tone

If validation fails, the system regenerates with corrective prompting (maximum 2 attempts).

---

### 7. Complete Section Inventory

RiftSage generates the following sections for every player report:

**Core Performance Sections** (Always Included):
1. **Role Performance Snapshot** - Primary role analysis with core stats
2. **Improvement Blueprint** - Personalized growth recommendations with targets
3. **Mental Resilience & Consistency** - Tilt resistance and pressure performance
4. **Champion Mastery Analysis** - Pool evaluation and optimization
5. **Outstanding Games Showcase** - Top 5-10 exceptional performances

**Contextual Sections** (Included When Applicable):
6. **Year-Over-Year Growth** - Only if 2024 data available; shows improvement trajectory
7. **Multi-Role Performance** - Only if player has 25+ games in 2+ roles
8. **Comeback Specialist Recognition** - Only if player has 15+ comeback wins
9. **Vision Control Excellence** - Only if vision score in top 25% for rank
10. **Farm Efficiency Mastery** - Only if CS/min in top 25% for rank/role

**Summary Sections** (Always Included):
11. **Season Overview** - High-level summary of games played, ranks climbed, key achievements
12. **2026 Forecast** - Projected rank ceiling and timeline based on current trajectory

**Total Sections Per Report**: 7-12 depending on player's data richness and performance patterns

---

### 8. Data Processing Pipeline

**Step 1: Data Collection** (AWS Lambda)
- Triggered monthly or on-demand by user request
- Fetches all 2025 matches for given summoner via Riot API
- Stores raw JSON responses in S3: `s3://riftsage-data/raw-matches/{puuid}/2025/`
- Updates DynamoDB with collection timestamp and games count
- **Output**: Array of Match IDs, raw match data

**Step 2: Feature Engineering & ETL** (AWS Lambda)
- Triggered by S3 event on raw data upload
- Transforms raw match data into ML-ready features:
  - Calculates assist-to-kill ratios per game
  - Computes vision score per minute
  - Identifies comeback games (team gold deficit > 5k but won)
  - Calculates CS efficiency under pressure
  - Aggregates objective participation rates
  - Computes damage efficiency ratios
  - Identifies pressure games (consecutive ranked matches indicating promos)
  - Calculates performance variance across winning vs. losing streaks
- Handles missing data and outliers
- Creates monthly aggregations for trend analysis
- **Output**: Processed metrics table in DynamoDB, feature vectors in S3

**Step 3: Comparative Benchmarking** (AWS Lambda)
- Queries DynamoDB for rank-appropriate benchmark data
- Calculates percentile rankings for each metric
- Identifies metrics where player exceeds/falls below rank average
- Calculates improvement opportunities based on climb correlation coefficients
- **Output**: Benchmark comparison table in DynamoDB

**Step 4: Model Training** (AWS Lambda - Annual Batch)
- Scheduled via CloudWatch Events (runs once annually in late January)
- Trains ML models on aggregated 2025 player data
- Validates model performance against holdout test set
- Archives trained model artifacts to S3
- **Output**: Trained model files (.pkl), validation reports

**Step 5: Model Inference** (AWS Lambda)
- Loads trained models from S3
- Applies models to player's feature vectors
- Generates classifications, scores, and predictions
- Stores inference results in DynamoDB
- **Output**: Player classifications, archetype assignment, prediction scores

**Step 6: Section Data Preparation** (AWS Lambda)
- Assembles data packages for each report section
- Validates data completeness
- Stores prepared packages in DynamoDB
- **Output**: Section-specific data packages ready for prompt construction

**Step 7: Insight Generation via Bedrock** (AWS Lambda)
- Constructs prompts with player data
- Calls Amazon Bedrock API with Claude model
- Post-processes output (validates four-part structure)
- Stores generated insights in S3 and DynamoDB
- **Output**: Generated text for all applicable sections

**Step 8: Report Compilation** (AWS Lambda)
- Assembles complete report from individual sections
- Generates JSON data package (primary format)
- Optionally generates PDF report
- Creates social media assets (PNG graphics)
- **Output**: Complete report package with presigned S3 URLs

**Step 9: Delivery & Notification** (AWS Lambda + Amazon SES)
- Sends notification email via Amazon SES
- Makes report accessible via API Gateway
- Tracks engagement metrics
- **Output**: User notification sent, report accessible via web app

**Step 10: Monitoring & Error Handling** (Amazon CloudWatch)
- All Lambda functions log to CloudWatch
- Automated error recovery for transient failures
- Manual escalation for persistent issues
- **Output**: Comprehensive monitoring, error recovery

---

### 9. Champion Recommendation Database

RiftSage maintains a curated champion database with performance characteristics aligned to playstyle archetypes.

**Database Structure** (DynamoDB Table: `ChampionRecommendationsTable`):

Key fields:
- champion_name, role, playstyle_fit (array)
- performance_metrics (avg_cs_min, avg_vision_score_min, avg_kda, avg_damage_share)
- win_rate_by_rank (gold, platinum, diamond, etc.)
- strengths (array of text descriptions)
- learning_curve (Low/Medium/High)
- meta_status (Strong/Stable/Weak)
- fit_explanation_template (personalized text template)

**Champion Selection Algorithm**:

For each player:
1. Query champions matching role and playstyle archetype
2. Calculate fit score based on:
   - Playstyle alignment (30 points)
   - Improvement enablement (25 points)
   - Meta strength (20 points)
   - Learning curve (15 points)
   - Pool synergy (10 points)
3. Rank champions by fit score
4. Select top 3 champions
5. Generate personalized fit explanations

**Update Frequency**:
- Patch updates every 2 weeks
- Meta analysis weekly
- Win rate data daily

---

### 10. Actionable Improvement Blueprint - Detailed Specification

**Target Calculation Methodology**:

For each improvement opportunity:
1. Calculate gap between player metric and rank average
2. Calculate climb correlation (how much metric affects rank advancement)
3. Calculate opportunity score (gap × correlation)
4. Rank opportunities by score
5. Select top 2 opportunities
6. Calculate targets:
   - Option 1: Current + 80% of gap to rank average
   - Option 2: Current × 1.20 (20% improvement)
   - Use whichever is more ambitious
   - Cap at realistic ceiling for rank
7. Project win rate improvement based on metric improvements

**Phase-by-Phase Execution Generation**:

For each game phase (Early/Mid/Late):
1. Determine priority goal based on improvement needs
2. Generate specific, actionable behaviors
3. Calculate quantified impact (gold gains, win rate improvements)
4. Tailor to player's role and playstyle

---

### 11. Quality Assurance & Validation Framework

**Purpose**: Ensure every generated section is unique, accurate, and player-specific

**Validation Checks**:

After generating each section, the system validates:
1. **Four-part structure exists** (Intro Overview, Stats & Metrics, Deeper Insights, Narrative Meaning)
2. **Intro Overview is present** and contextualizes data before stats
3. **All referenced metrics match actual player data** (no hallucinated numbers)
4. **No fictional storytelling elements** (no "epic tales" or invented scenarios)
5. **Narrative references specific numbers** (not vague generalizations)
6. **Improvement sections contain measurable targets** (numeric goals, not "do better")
7. **Section length appropriate** (500-1500 words)
8. **Tone is professional and data-focused** (not overly casual or dramatic)
9. **Content uniqueness** (no generic phrases that could apply to any player)

**Uniqueness Validation**:

```python
def validate_content_uniqueness(generated_text, player_data):
    """
    Ensures AI generated unique content, not generic templates
    """
    # Check for generic placeholder patterns
    generic_patterns = [
        r'\[.*?\]',  # Bracket placeholders like [value]
        r'Your \w+ shows',  # Generic "Your X shows" without specifics
        r'You have demonstrated',  # Vague accomplishment statements
        r'This indicates',  # Generic transition phrases
    ]
    
    for pattern in generic_patterns:
        if re.search(pattern, generated_text):
            return False, f"Generic pattern detected: {pattern}"
    
    # Check for specific numbers from player data
    player_numbers = extract_numbers_from_data(player_data)
    text_numbers = extract_numbers_from_text(generated_text)
    
    # At least 50% of text numbers should match player data
    matching_numbers = set(player_numbers) & set(text_numbers)
    if len(matching_numbers) < len(text_numbers) * 0.5:
        return False, "Insufficient use of player-specific numbers"
    
    # Check for player-specific context
    if player_data['win_rate'] > 60 and 'dominant' not in generated_text.lower():
        return False, "High win rate not reflected in language"
    
    if player_data['win_rate'] < 50 and 'growth' not in generated_text.lower():
        return False, "Low win rate not reflected in language"
    
    return True, "Content is unique and player-specific"
```

**Anti-Template Validation**:

```python
def check_for_template_usage(generated_text):
    """
    Detects if AI used template filling instead of generation
    """
    # Flag phrases that indicate template usage
    template_indicators = [
        'Your [',  # Unfilled placeholder
        '% reflects [',  # Unfilled explanation
        'shows [pattern]',  # Generic structure
        'proves [identification]',  # Generic structure
        'your strength',  # Too generic without specifics
    ]
    
    for indicator in template_indicators:
        if indicator in generated_text:
            return False, f"Template indicator found: {indicator}"
    
    # Check for repetitive sentence structures
    sentences = generated_text.split('.')
    structures = [get_sentence_structure(s) for s in sentences]
    
    if len(structures) != len(set(structures)):
        return False, "Repetitive sentence structures detected"
    
    return True, "No template usage detected"
```

**Data Accuracy Validation**:

```python
def validate_data_accuracy(generated_text, player_data):
    """
    Ensures all numbers in generated text match player data
    """
    # Extract all percentages and numbers from generated text
    numbers_in_text = re.findall(r'\d+\.?\d*', generated_text)
    
    # Build list of acceptable numbers from player data
    acceptable_numbers = []
    for key, value in player_data.items():
        if isinstance(value, (int, float)):
            acceptable_numbers.append(str(value))
            # Also add rounded versions
            acceptable_numbers.append(str(round(value)))
            acceptable_numbers.append(str(round(value, 1)))
    
    # Check each number in text
    for number in numbers_in_text:
        # Skip years and other obvious valid numbers
        if number in ['2024', '2025', '2026']:
            continue
        
        # Check if number appears in player data or is a derivative
        if number not in acceptable_numbers:
            # Check if it's a valid calculation
            if not is_valid_calculated_value(number, player_data):
                return False, f"Inaccurate number: {number}"
    
    return True, "All numbers are accurate"
```

**Automated Regeneration**:

If validation fails:
1. **Log errors** for monitoring and pattern analysis
2. **Construct corrective prompt** explaining what was wrong
3. **Regenerate with corrections** using enhanced prompt
4. **Validate again** with stricter criteria
5. **After max attempts (2)**, use fallback or queue for manual review

```python
def regenerate_with_corrections(section_id, player_data, generated_text, errors):
    """
    Regenerates section with corrective guidance
    """
    # Build corrective prompt
    corrections = """
CRITICAL CORRECTIONS NEEDED:
The previous generation had these issues:
"""
    for error in errors:
        corrections += f"- {error}\n"
    
    corrections += """
FIX THESE ISSUES:
1. Generate completely unique content - no template structures
2. Use ONLY numbers from the player data provided
3. Make every sentence specific to THIS player's profile
4. Explain mechanisms, not just restate statistics
5. Connect metrics to reveal gameplay patterns
6. Write as if you deeply understand this specific player

Do not repeat the previous attempt. Create entirely new content.
"""
    
    # Get original prompt
    base_prompt = load_prompt_template(section_id)
    
    # Combine with corrections
    full_prompt = base_prompt + "\n\n" + corrections
    
    # Regenerate
    new_attempt = call_bedrock(full_prompt, player_data)
    
    return new_attempt
```

**Validation Success Metrics**:

The system tracks:
- **First-pass success rate**: Percentage of sections that pass validation on first generation
- **Regeneration frequency**: How often sections need regeneration
- **Error patterns**: Common validation failures to improve prompts
- **Manual review rate**: Percentage requiring human intervention

Target: >90% first-pass success rate, <5% manual review rate

---

### 12. Performance Optimization & Cost Management

**Lambda Function Optimization**:

- Memory configurations optimized per function type
- Lambda layers for ML model dependencies (reduce cold starts)
- Concurrent execution limits to control costs
- Reserved concurrency for critical functions

**Caching Strategy**:

- DynamoDB TTL-based caching for match data (24-hour cache)
- S3 Intelligent-Tiering for cost optimization
- CloudFront CDN for static report assets

**Cost Estimation**:

Per 1,000 players:
- Lambda executions: ~$5
- Bedrock API: ~$99
- S3 storage: ~$3
- DynamoDB: ~$26
- CloudWatch logs: ~$1
- **Total: ~$134** (~$0.13 per player report)

---

### 13. Security & Compliance

**Data Encryption**:
- AES-256 server-side encryption with KMS (S3, DynamoDB)
- TLS 1.3 for all data in transit
- KMS-encrypted Lambda environment variables

**Data Privacy & GDPR Compliance**:
- Explicit user opt-in required
- Right to access (data export API)
- Right to erasure (data deletion API)
- Right to portability (JSON export)
- 2-year data retention policy

**Rate Limiting**:
- Per-user: 5 requests/second, 100 requests/day
- Per-IP: 10 requests/second
- Enforced via DynamoDB rate limit table with TTL

---

### 14. Monitoring & Observability

**CloudWatch Metrics**:
- Report generation success rate
- Average generation time
- Bedrock API latency
- Model inference accuracy
- Validation failure rate

**CloudWatch Alarms**:
- Alert if success rate drops below 95%
- Alert if generation time exceeds 5 minutes
- Alert if validation failure rate exceeds 10%

**Structured Logging**:
- All operations logged with structured JSON
- Operation name, player ID, status, duration, metadata

---

### 15. Testing & Quality Assurance Strategy

**Unit Testing**:
- Test improvement target calculations
- Test ML model prediction accuracy
- Test validation framework logic

**Integration Testing**:
- Test full report generation pipeline
- Mock AWS services
- Validate report structure

---

### 16. Success Metrics & KPIs

**Technical Performance**:
- Match data accuracy: ≥99.5%
- Model prediction accuracy: ≥85%
- Report generation time: <5 minutes (P95)
- System uptime: ≥99.9%
- Cost per report: ≤$0.15

**User Experience**:
- Insight relevance rating: ≥4.2/5.0
- Recommendation actionability: ≥4.0/5.0
- Report completion rate: ≥80%
- Social share rate: ≥25%
- Return user rate: ≥60%

---

### 17. Future Enhancements Roadmap

**Phase 2 (Q2 2026)**: Real-time insights, weekly progress reports, multi-season analysis

**Phase 3 (Q3 2026)**: Team-based insights, coach collaboration, voice narration

**Phase 4 (Q4 2026)**: Predictive match modeling, champion recommendation engine

**Phase 5 (2027)**: ARAM analysis, TFT integration, tournament tools

---

### 18. API Endpoint Specifications

**Base URL**: `https://api.riftsage.gg/v1`

**Key Endpoints**:
- `POST /auth/request-magic-link` - Initiate authentication
- `POST /auth/verify-magic-link` - Verify and get access token
- `POST /summoner/link` - Link League account
- `GET /reports/{puuid}/{year}` - Retrieve complete report
- `POST /reports/{puuid}/generate` - Trigger report generation
- `GET /reports/{puuid}/generation-status/{job_id}` - Check generation status
- `GET /matches/{puuid}` - Retrieve match history with analysis
- `GET /blueprint/{puuid}` - Get improvement blueprint
- `PUT /blueprint/{puuid}/progress` - Update goal progress
- `GET /leaderboards/{region}` - Public leaderboards
- `POST /share/generate` - Generate social media assets
- `GET /settings/{puuid}` - User preferences
- `PUT /settings/{puuid}` - Update preferences
- `DELETE /user/{puuid}` - Delete all user data (GDPR)
- `GET /user/{puuid}/export` - Export all user data (GDPR)

---

### 19. Error Handling & User Feedback

**Error Code Taxonomy**:

- **1xxx**: Authentication errors
- **2xxx**: Data collection errors
- **3xxx**: Report generation errors
- **4xxx**: Data access errors
- **5xxx**: System errors

Each error includes:
- Technical message (for debugging)
- User-friendly message
- Recommended action
- HTTP status code
- Support URL

**Feedback Collection**:

Post-report feedback includes:
- Overall satisfaction (1-5)
- Insight relevance (1-5)
- Recommendation usefulness (1-5)
- NPS score (0-10)
- Section-specific helpfulness
- Open feedback text

---

### 20. Deployment Guide & Infrastructure as Code

**AWS CloudFormation Template (Complete)**:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'RiftSage AI Agent - Complete Infrastructure'

Parameters:
  Environment:
    Type: String
    Default: production
    AllowedValues:
      - development
      - staging
      - production
    Description: Deployment environment

  RiotAPIKey:
    Type: String
    NoEcho: true
    Description: Riot Games Developer API Key

  ProjectName:
    Type: String
    Default: riftsage
    Description: Project name for resource naming

Resources:
  # ====================================
  # KMS Encryption Key
  # ====================================
  DataEncryptionKey:
    Type: AWS::KMS::Key
    Properties:
      Description: KMS key for RiftSage data encryption
      KeyPolicy:
        Version: '2012-10-17'
        Statement:
          - Sid: Enable IAM User Permissions
            Effect: Allow
            Principal:
              AWS: !Sub 'arn:aws:iam::${AWS::AccountId}:root'
            Action: 'kms:*'
            Resource: '*'
          - Sid: Allow Lambda to use the key
            Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action:
              - 'kms:Decrypt'
              - 'kms:DescribeKey'
            Resource: '*'

  DataEncryptionKeyAlias:
    Type: AWS::KMS::Alias
    Properties:
      AliasName: !Sub 'alias/${ProjectName}-${Environment}'
      TargetKeyId: !Ref DataEncryptionKey

  # ====================================
  # S3 Buckets
  # ====================================
  RawMatchDataBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '${ProjectName}-data-${Environment}-${AWS::AccountId}'
      VersioningConfiguration:
        Status: Enabled
      LifecycleConfiguration:
        Rules:
          - Id: TransitionToIA
            Status: Enabled
            Transitions:
              - TransitionInDays: 90
                StorageClass: INTELLIGENT_TIERING
              - TransitionInDays: 365
                StorageClass: GLACIER_INSTANT_RETRIEVAL
          - Id: DeleteOldVersions
            Status: Enabled
            NoncurrentVersionExpirationInDays: 30
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: 'aws:kms'
              KMSMasterKeyID: !Ref DataEncryptionKey
      NotificationConfiguration:
        LambdaConfigurations:
          - Event: 's3:ObjectCreated:*'
            Function: !GetAtt FeatureEngineeringFunction.Arn
            Filter:
              S3Key:
                Rules:
                  - Name: prefix
                    Value: 'raw-matches/'
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Project
          Value: !Ref ProjectName

  ReportsBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '${ProjectName}-reports-${Environment}-${AWS::AccountId}'
      CorsConfiguration:
        CorsRules:
          - AllowedHeaders: ['*']
            AllowedMethods: [GET, HEAD]
            AllowedOrigins: 
              - 'https://chronicle.riftsage.gg'
              - !If [IsDevelopment, 'http://localhost:3000', !Ref 'AWS::NoValue']
            MaxAge: 3600
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: 'aws:kms'
              KMSMasterKeyID: !Ref DataEncryptionKey
      Tags:
        - Key: Environment
          Value: !Ref Environment

  ModelsBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '${ProjectName}-models-${Environment}-${AWS::AccountId}'
      VersioningConfiguration:
        Status: Enabled
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      Tags:
        - Key: Environment
          Value: !Ref Environment

  # ====================================
  # DynamoDB Tables
  # ====================================
  PlayersTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub '${ProjectName}-Players-${Environment}'
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: player_puuid
          AttributeType: S
        - AttributeName: email
          AttributeType: S
      KeySchema:
        - AttributeName: player_puuid
          KeyType: HASH
      GlobalSecondaryIndexes:
        - IndexName: EmailIndex
          KeySchema:
            - AttributeName: email
              KeyType: HASH
          Projection:
            ProjectionType: ALL
      StreamSpecification:
        StreamViewType: NEW_AND_OLD_IMAGES
      PointInTimeRecoverySpecification:
        PointInTimeRecoveryEnabled: true
      SSESpecification:
        SSEEnabled: true
        SSEType: KMS
        KMSMasterKeyId: !Ref DataEncryptionKey
      Tags:
        - Key: Environment
          Value: !Ref Environment

  MetricsTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub '${ProjectName}-Metrics-${Environment}'
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: player_puuid
          AttributeType: S
        - AttributeName: year
          AttributeType: N
      KeySchema:
        - AttributeName: player_puuid
          KeyType: HASH
        - AttributeName: year
          KeyType: RANGE
      SSESpecification:
        SSEEnabled: true
        SSEType: KMS
        KMSMasterKeyId: !Ref DataEncryptionKey
      Tags:
        - Key: Environment
          Value: !Ref Environment

  GeneratedInsightsTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub '${ProjectName}-Insights-${Environment}'
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: player_puuid
          AttributeType: S
        - AttributeName: section_id
          AttributeType: S
      KeySchema:
        - AttributeName: player_puuid
          KeyType: HASH
        - AttributeName: section_id
          KeyType: RANGE
      SSESpecification:
        SSEEnabled: true
      Tags:
        - Key: Environment
          Value: !Ref Environment

  MatchCacheTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub '${ProjectName}-MatchCache-${Environment}'
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: match_id
          AttributeType: S
      KeySchema:
        - AttributeName: match_id
          KeyType: HASH
      TimeToLiveSpecification:
        AttributeName: ttl
        Enabled: true
      SSESpecification:
        SSEEnabled: true
      Tags:
        - Key: Environment
          Value: !Ref Environment

  ChampionRecommendationsTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub '${ProjectName}-ChampionRecs-${Environment}'
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: champion_name
          AttributeType: S
        - AttributeName: role
          AttributeType: S
      KeySchema:
        - AttributeName: champion_name
          KeyType: HASH
      GlobalSecondaryIndexes:
        - IndexName: RoleIndex
          KeySchema:
            - AttributeName: role
              KeyType: HASH
          Projection:
            ProjectionType: ALL
      SSESpecification:
        SSEEnabled: true
      Tags:
        - Key: Environment
          Value: !Ref Environment

  RateLimitTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub '${ProjectName}-RateLimit-${Environment}'
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: user_action
          AttributeType: S
      KeySchema:
        - AttributeName: user_action
          KeyType: HASH
      TimeToLiveSpecification:
        AttributeName: ttl
        Enabled: true
      SSESpecification:
        SSEEnabled: true
      Tags:
        - Key: Environment
          Value: !Ref Environment

  # ====================================
  # Secrets Manager
  # ====================================
  RiotAPIKeySecret:
    Type: AWS::SecretsManager::Secret
    Properties:
      Name: !Sub '/${ProjectName}/${Environment}/riot-api-key'
      Description: Riot Games Developer API Key
      SecretString: !Sub '{"api_key":"${RiotAPIKey}"}'
      KmsKeyId: !Ref DataEncryptionKey
      Tags:
        - Key: Environment
          Value: !Ref Environment

  # ====================================
  # IAM Roles
  # ====================================
  LambdaExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub '${ProjectName}-LambdaExecution-${Environment}'
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: 'sts:AssumeRole'
      ManagedPolicyArns:
        - 'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
      Policies:
        - PolicyName: S3Access
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - 's3:GetObject'
                  - 's3:PutObject'
                  - 's3:DeleteObject'
                  - 's3:ListBucket'
                Resource:
                  - !Sub '${RawMatchDataBucket.Arn}/*'
                  - !Sub '${ReportsBucket.Arn}/*'
                  - !Sub '${ModelsBucket.Arn}/*'
                  - !GetAtt RawMatchDataBucket.Arn
                  - !GetAtt ReportsBucket.Arn
                  - !GetAtt ModelsBucket.Arn
        - PolicyName: DynamoDBAccess
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - 'dynamodb:GetItem'
                  - 'dynamodb:PutItem'
                  - 'dynamodb:UpdateItem'
                  - 'dynamodb:DeleteItem'
                  - 'dynamodb:Query'
                  - 'dynamodb:Scan'
                Resource:
                  - !GetAtt PlayersTable.Arn
                  - !Sub '${PlayersTable.Arn}/index/*'
                  - !GetAtt MetricsTable.Arn
                  - !GetAtt GeneratedInsightsTable.Arn
                  - !GetAtt MatchCacheTable.Arn
                  - !GetAtt ChampionRecommendationsTable.Arn
                  - !GetAtt RateLimitTable.Arn
        - PolicyName: SecretsManagerAccess
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - 'secretsmanager:GetSecretValue'
                Resource: !Ref RiotAPIKeySecret
        - PolicyName: KMSAccess
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - 'kms:Decrypt'
                  - 'kms:DescribeKey'
                Resource: !GetAtt DataEncryptionKey.Arn
        - PolicyName: BedrockAccess
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - 'bedrock:InvokeModel'
                Resource: 'arn:aws:bedrock:*::foundation-model/anthropic.claude-*'
        - PolicyName: CloudWatchLogs
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - 'logs:CreateLogGroup'
                  - 'logs:CreateLogStream'
                  - 'logs:PutLogEvents'
                Resource: '*'
      Tags:
        - Key: Environment
          Value: !Ref Environment

  # ====================================
  # Lambda Layers
  # ====================================
  MLDependenciesLayer:
    Type: AWS::Lambda::LayerVersion
    Properties:
      LayerName: !Sub '${ProjectName}-ml-dependencies-${Environment}'
      Description: Machine learning dependencies (scikit-learn, numpy, pandas)
      Content:
        S3Bucket: !Ref ModelsBucket
        S3Key: 'layers/ml-dependencies.zip'
      CompatibleRuntimes:
        - python3.11
      CompatibleArchitectures:
        - x86_64

  # ====================================
  # Lambda Functions
  # ====================================
  DataCollectionFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub '${ProjectName}-DataCollection-${Environment}'
      Runtime: python3.11
      Handler: data_collection.lambda_handler
      Role: !GetAtt LambdaExecutionRole.Arn
      Code:
        S3Bucket: !Ref ModelsBucket
        S3Key: 'functions/data_collection.zip'
      MemorySize: 512
      Timeout: 300
      Environment:
        Variables:
          ENVIRONMENT: !Ref Environment
          DATA_BUCKET: !Ref RawMatchDataBucket
          PLAYERS_TABLE: !Ref PlayersTable
          CACHE_TABLE: !Ref MatchCacheTable
          RIOT_API_SECRET: !Ref RiotAPIKeySecret
      Tags:
        - Key: Environment
          Value: !Ref Environment

  FeatureEngineeringFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub '${ProjectName}-FeatureEngineering-${Environment}'
      Runtime: python3.11
      Handler: feature_engineering.lambda_handler
      Role: !GetAtt LambdaExecutionRole.Arn
      Code:
        S3Bucket: !Ref ModelsBucket
        S3Key: 'functions/feature_engineering.zip'
      Layers:
        - !Ref MLDependenciesLayer
      MemorySize: 1024
      Timeout: 600
      Environment:
        Variables:
          ENVIRONMENT: !Ref Environment
          DATA_BUCKET: !Ref RawMatchDataBucket
          METRICS_TABLE: !Ref MetricsTable
      Tags:
        - Key: Environment
          Value: !Ref Environment

  ModelInferenceFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub '${ProjectName}-ModelInference-${Environment}'
      Runtime: python3.11
      Handler: model_inference.lambda_handler
      Role: !GetAtt LambdaExecutionRole.Arn
      Code:
        S3Bucket: !Ref ModelsBucket
        S3Key: 'functions/model_inference.zip'
      Layers:
        - !Ref MLDependenciesLayer
      MemorySize: 2048
      Timeout: 300
      Environment:
        Variables:
          ENVIRONMENT: !Ref Environment
          MODELS_BUCKET: !Ref ModelsBucket
          METRICS_TABLE: !Ref MetricsTable
      Tags:
        - Key: Environment
          Value: !Ref Environment

  BedrockGenerationFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub '${ProjectName}-BedrockGeneration-${Environment}'
      Runtime: python3.11
      Handler: bedrock_generation.lambda_handler
      Role: !GetAtt LambdaExecutionRole.Arn
      Code:
        S3Bucket: !Ref ModelsBucket
        S3Key: 'functions/bedrock_generation.zip'
      MemorySize: 1024
      Timeout: 900
      Environment:
        Variables:
          ENVIRONMENT: !Ref Environment
          METRICS_TABLE: !Ref MetricsTable
          INSIGHTS_TABLE: !Ref GeneratedInsightsTable
          REPORTS_BUCKET: !Ref ReportsBucket
      Tags:
        - Key: Environment
          Value: !Ref Environment

  ReportCompilationFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub '${ProjectName}-ReportCompilation-${Environment}'
      Runtime: python3.11
      Handler: report_compilation.lambda_handler
      Role: !GetAtt LambdaExecutionRole.Arn
      Code:
        S3Bucket: !Ref ModelsBucket
        S3Key: 'functions/report_compilation.zip'
      MemorySize: 1024
      Timeout: 300
      Environment:
        Variables:
          ENVIRONMENT: !Ref Environment
          INSIGHTS_TABLE: !Ref GeneratedInsightsTable
          REPORTS_BUCKET: !Ref ReportsBucket
      Tags:
        - Key: Environment
          Value: !Ref Environment

  # ====================================
  # Lambda Permissions
  # ====================================
  FeatureEngineeringS3Permission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref FeatureEngineeringFunction
      Action: 'lambda:InvokeFunction'
      Principal: s3.amazonaws.com
      SourceArn: !GetAtt RawMatchDataBucket.Arn

  # ====================================
  # API Gateway
  # ====================================
  RiftSageAPI:
    Type: AWS::ApiGatewayV2::Api
    Properties:
      Name: !Sub '${ProjectName}-api-${Environment}'
      ProtocolType: HTTP
      CorsConfiguration:
        AllowOrigins:
          - 'https://chronicle.riftsage.gg'
          - !If [IsDevelopment, 'http://localhost:3000', !Ref 'AWS::NoValue']
        AllowMethods:
          - GET
          - POST
          - PUT
          - DELETE
          - OPTIONS
        AllowHeaders:
          - '*'
        MaxAge: 3600
      Tags:
        Environment: !Ref Environment

  RiftSageAPIStage:
    Type: AWS::ApiGatewayV2::Stage
    Properties:
      ApiId: !Ref RiftSageAPI
      StageName: !Ref Environment
      AutoDeploy: true
      DefaultRouteSettings:
        ThrottlingBurstLimit: 100
        ThrottlingRateLimit: 50
      Tags:
        Environment: !Ref Environment

  # ====================================
  # Cognito User Pool
  # ====================================
  UserPool:
    Type: AWS::Cognito::UserPool
    Properties:
      UserPoolName: !Sub '${ProjectName}-users-${Environment}'
      AutoVerifiedAttributes:
        - email
      EmailConfiguration:
        EmailSendingAccount: COGNITO_DEFAULT
      Policies:
        PasswordPolicy:
          MinimumLength: 8
          RequireUppercase: false
          RequireLowercase: false
          RequireNumbers: false
          RequireSymbols: false
      Schema:
        - Name: email
          AttributeDataType: String
          Required: true
          Mutable: true
      UsernameConfiguration:
        CaseSensitive: false
      UserPoolTags:
        Environment: !Ref Environment

  UserPoolClient:
    Type: AWS::Cognito::UserPoolClient
    Properties:
      ClientName: !Sub '${ProjectName}-client-${Environment}'
      UserPoolId: !Ref UserPool
      GenerateSecret: false
      ExplicitAuthFlows:
        - ALLOW_USER_PASSWORD_AUTH
        - ALLOW_REFRESH_TOKEN_AUTH
      TokenValidityUnits:
        RefreshToken: days
      RefreshTokenValidity: 30

  # ====================================
  # CloudWatch Log Groups
  # ====================================
  DataCollectionLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub '/aws/lambda/${DataCollectionFunction}'
      RetentionInDays: 30

  FeatureEngineeringLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub '/aws/lambda/${FeatureEngineeringFunction}'
      RetentionInDays: 30

  ModelInferenceLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub '/aws/lambda/${ModelInferenceFunction}'
      RetentionInDays: 30

  BedrockGenerationLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub '/aws/lambda/${BedrockGenerationFunction}'
      RetentionInDays: 30

  ReportCompilationLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub '/aws/lambda/${ReportCompilationFunction}'
      RetentionInDays: 30

  # ====================================
  # CloudWatch Alarms
  # ====================================
  HighErrorRateAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub '${ProjectName}-HighErrorRate-${Environment}'
      AlarmDescription: Alert when error rate exceeds threshold
      MetricName: Errors
      Namespace: AWS/Lambda
      Statistic: Sum
      Period: 300
      EvaluationPeriods: 2
      Threshold: 10
      ComparisonOperator: GreaterThanThreshold
      TreatMissingData: notBreaching

  SlowGenerationAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub '${ProjectName}-SlowGeneration-${Environment}'
      AlarmDescription: Alert when generation time exceeds 5 minutes
      MetricName: Duration
      Namespace: AWS/Lambda
      Statistic: Average
      Period: 300
      EvaluationPeriods: 3
      Threshold: 300000
      ComparisonOperator: GreaterThanThreshold
      TreatMissingData: notBreaching
      Dimensions:
        - Name: FunctionName
          Value: !Ref BedrockGenerationFunction

  # ====================================
  # EventBridge Rules
  # ====================================
  AnnualModelTrainingRule:
    Type: AWS::Events::Rule
    Properties:
      Name: !Sub '${ProjectName}-AnnualTraining-${Environment}'
      Description: Trigger annual model training in January
      ScheduleExpression: 'cron(0 2 15 1 ? *)'
      State: ENABLED
      Targets:
        - Arn: !GetAtt ModelInferenceFunction.Arn
          Id: ModelTrainingTarget
          Input: '{"action": "train_models"}'

  # ====================================
  # SNS Topics
  # ====================================
  AlertTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: !Sub '${ProjectName}-alerts-${Environment}'
      DisplayName: RiftSage Alerts
      Tags:
        - Key: Environment
          Value: !Ref Environment

# ====================================
# Conditions
# ====================================
Conditions:
  IsDevelopment: !Equals [!Ref Environment, 'development']

# ====================================
# Outputs
# ====================================
Outputs:
  APIEndpoint:
    Description: API Gateway endpoint URL
    Value: !Sub 'https://${RiftSageAPI}.execute-api.${AWS::Region}.amazonaws.com/${Environment}'
    Export:
      Name: !Sub '${ProjectName}-api-endpoint-${Environment}'

  UserPoolId:
    Description: Cognito User Pool ID
    Value: !Ref UserPool
    Export:
      Name: !Sub '${ProjectName}-user-pool-${Environment}'

  UserPoolClientId:
    Description: Cognito User Pool Client ID
    Value: !Ref UserPoolClient
    Export:
      Name: !Sub '${ProjectName}-user-pool-client-${Environment}'

  DataBucket:
    Description: S3 bucket for raw match data
    Value: !Ref RawMatchDataBucket
    Export:
      Name: !Sub '${ProjectName}-data-bucket-${Environment}'

  ReportsBucket:
    Description: S3 bucket for generated reports
    Value: !Ref ReportsBucket
    Export:
      Name: !Sub '${ProjectName}-reports-bucket-${Environment}'

  PlayersTableName:
    Description: DynamoDB Players table name
    Value: !Ref PlayersTable
    Export:
      Name: !Sub '${ProjectName}-players-table-${Environment}'
```

**Deployment Steps**:

1. **Prerequisites**:
   - AWS CLI configured with appropriate credentials
   - Riot Games Developer API key
   - Lambda function code packages prepared and uploaded to S3

2. **Initial Deployment**:
   ```bash
   aws cloudformation create-stack \
     --stack-name riftsage-prod \
     --template-body file://infrastructure.yaml \
     --parameters ParameterKey=Environment,ParameterValue=production \
                  ParameterKey=RiotAPIKey,ParameterValue=<YOUR_API_KEY> \
     --capabilities CAPABILITY_NAMED_IAM
   ```

3. **Wait for Completion**:
   ```bash
   aws cloudformation wait stack-create-complete \
     --stack-name riftsage-prod
   ```

4. **Verify Resources**:
   ```bash
   aws cloudformation describe-stacks \
     --stack-name riftsage-prod \
     --query 'Stacks[0].Outputs'
   ```

5. **Seed Champion Database**:
   - Run champion database population script
   - Verify data in ChampionRecommendationsTable

6. **Test Pipeline**:
   - Trigger test report generation for sample account
   - Monitor CloudWatch logs for each Lambda function
   - Verify report appears in ReportsBucket

---

### 21. Champion Database Management

**Update Frequency**:
- **Patch Updates**: Every 2 weeks (aligned with Riot patches)
- **Meta Analysis**: Weekly (from community data)
- **Win Rate Data**: Daily (from RiftSage analytics)

**Automated Update Pipeline**:

Scheduled Lambda function runs weekly to:
1. Fetch latest patch notes from Riot API
2. Identify buffed/nerfed champions
3. Update meta_status accordingly
4. Recalculate win rates from player data
5. Flag champions needing manual review

---

### 22. Insight Generation Prompt Engineering

**Prompt Construction Best Practices**:

1. **Structured Data Injection**: Provide metrics in JSON format
2. **Context Windowing**: Include only relevant context
3. **Few-Shot Examples**: Include 2-3 examples of perfect output
4. **Explicit Constraints**: State what NOT to do
5. **Output Format Specification**: Provide exact JSON schema
6. **Tone Calibration**: Reinforce professional tone
7. **Edge Case Handling**: Include instructions for missing data

**Prompt Versioning**:

All prompts version-controlled in S3:
- `prompts/v1.0/role_performance.txt` - Initial version
- `prompts/v1.1/role_performance.txt` - Minor refinement
- `prompts/v2.0/role_performance.txt` - Major change

A/B testing with 10% of users for experimental prompts. Winners promoted after statistical significance.

---

### 23. Privacy & Compliance Details

**GDPR Compliance**:
- Lawful basis: Consent (explicit opt-in)
- Data minimization: Only necessary data
- Storage limitation: 2-year retention
- Right to access: Data export API
- Right to erasure: Data deletion API within 24 hours
- Right to portability: JSON export
- Transparency: Clear privacy policy

**COPPA Compliance** (US users under 13):
- Birthdate verification during registration
- Block account creation for users under 13
- Parental consent for 13-16 age group

**Regional Data Residency**:
- EU/EEA: eu-west-1 (Ireland)
- US: us-east-1 (Virginia)
- Asia: ap-northeast-2 (Seoul)

---

### 24. Continuous Improvement Framework

**Feedback Loop**:
1. Collect user feedback and error data
2. Weekly analysis of patterns
3. Prioritize improvements by impact
4. Implement fixes/enhancements
5. Test in staging
6. Roll out incrementally (10% → 50% → 100%)
7. Measure impact

**Model Retraining**:
- Annual retraining in January
- Compare new vs. old model accuracy
- Only promote if improvement ≥ 2%
- Keep previous version for 30 days

**Content Quality Reviews**:
- Monthly audits of 100 random reports
- Check accuracy, tone, actionability
- Update prompts to address issues

---

### 25. Business Logic Rules

**Report Eligibility**:
- Minimum 50 ranked games in target year
- Active account (not banned)
- Public match history
- Supported region
- One report per summoner per year (unless force_regenerate)

**Dynamic Section Inclusion**:
- Year-Over-Year: Only if 2024 data with ≥50 games
- Multi-Role: Only if ≥25 games in 2+ roles
- Comeback Specialist: Only if ≥15 comeback wins
- Vision Excellence: Only if top 25% for rank
- Farm Mastery: Only if top 25% for rank/role

**Improvement Target Calibration**:
- High win rate players (>60%): Focus on consistency
- Climbing players: Targets aligned with next rank
- Plateau players: Focus on bottlenecks
- New players (<100 games): Lenient targets, focus on fundamentals

---

### 26. Champion Recommendation Algorithm Details

**Fit Score Components** (Total: 100 points):
- Playstyle Alignment: 30 points
- Improvement Enablement: 25 points
- Meta Strength: 20 points
- Learning Curve: 15 points
- Pool Synergy: 10 points

**Algorithm Steps**:
1. Filter champions by role
2. Calculate fit score for each
3. Rank by fit score
4. Select top 3
5. Generate personalized explanations

**Anti-Patterns**:
- Don't recommend champions player already plays frequently
- Don't recommend complex champions to low-skill players
- Don't recommend off-meta unless player enjoys experimental picks

---

### 27. Final Technical Specifications Summary

**Technology Stack**:
- Cloud: AWS
- Compute: Lambda (serverless)
- Storage: S3 (objects), DynamoDB (NoSQL)
- AI/ML: Amazon Bedrock (Claude 3), Lambda with scikit-learn
- Auth: Cognito
- API: API Gateway (REST)
- Monitoring: CloudWatch
- Security: KMS, Secrets Manager, IAM

**Programming Languages**:
- Backend: Python 3.11
- Infrastructure: YAML (CloudFormation)
- Web App: HTML5, CSS3, Vanilla JavaScript

**Performance Targets**:
- Report generation: <5 min (P95)
- API response: <2 sec (P95)
- Uptime: >99.9%
- Success rate: >98%
- Model accuracy: >85%
- Cost per report: <$0.13

---

### 28. Success Criteria

**Technical Excellence**:
- ≥99% match data accuracy
- ≥85% model prediction accuracy
- <5 min report generation (P95)
- ≥98% generation success rate
- ≥99.9% system uptime

**User Satisfaction**:
- ≥4.2/5.0 insight relevance
- ≥4.0/5.0 recommendation actionability
- ≥80% report completion rate
- ≥25% social share rate
- ≥60% return user rate

**Business Viability**:
- ≤$0.13 cost per report
- Sustainable unit economics
- Positive user growth
- Strong community engagement

---

### 29. Conclusion

RiftSage AI Agent delivers data-driven, personalized insights for League of Legends players through a standardized four-part framework that adapts to each player's unique performance. By combining advanced machine learning with AI-powered narrative generation, RiftSage transforms raw match data into meaningful guidance that helps players understand their strengths, celebrate achievements, and chart a clear path to improvement—all while maintaining data integrity, user privacy, and cost efficiency at $0.13 per report.

---

## Appendix A: Data Model Schemas

*Note: Complete JSON schemas for all DynamoDB tables and S3 objects are maintained in the project repository under `/schemas/`*

## Appendix B: Error Code Reference

*Note: Complete error code catalog maintained in `/docs/error-codes.md`*

## Appendix C: API Endpoint Reference

*Note: Complete API documentation with request/response examples maintained in `/docs/api-reference.md`*
