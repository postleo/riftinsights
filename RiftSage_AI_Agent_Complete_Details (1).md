# RiftSage AI Agent - Complete App Details Document (Updated)

## Executive Summary

RiftSage is an AI-powered agent that leverages AWS AI services and the League of Legends Developer API to deliver personalized, data-driven end-of-year insights for League of Legends players. Using machine learning models trained on match data, RiftSage uncovers performance patterns, identifies growth opportunities, and provides clear, actionable recommendations that help players understand their true value and improve their gameplay. The agent delivers insights through a standardized three-tier framework that adapts dynamically to each player's unique performance data.

---

## Product Overview

### Core Purpose
Transform raw match data into meaningful insights that help players understand their performance patterns, recognize growth opportunities, and receive practical guidance—all delivered in a clear, engaging style that respects data integrity while providing narrative meaning.

### Value Proposition
- **Data-Driven Clarity**: Reveals performance patterns with statistical backing
- **Meaningful Insights**: Transforms numbers into understanding without fictional embellishment
- **Actionable Guidance**: Specific, measurable recommendations based on analysis
- **Adaptive Framework**: Standardized structure that personalizes to each player's strengths
- **Professional Presentation**: Delivers insights through Summoner's Chronicle web app

### Target Audience
- **Primary**: League of Legends players (16-28 years old) who play 50+ ranked games annually
- **Secondary**: Casual players seeking to understand their impact and improve
- **Psychographics**: Players who value clear insights, practical advice, and measurable growth

---

## Product Features & Capabilities

### 1. Intelligent Data Collection & Processing

**Match Data Ingestion**
- Connects to Riot Games Developer API via summoner ID and region
- Retrieves comprehensive match history for 2025 season
- Collects data points including:
  - Champion selections and role distribution
  - KDA across all matches
  - Vision scores and ward placement patterns
  - Objective participation
  - Gold earned and CS efficiency
  - Damage dealt vs. damage taken ratios
  - Game duration and outcome
  - Team composition and matchups
  - Comeback scenarios
  - Critical game moments
  - CS per minute tracking
  - Gold differential analysis
  - Ward placement timing and locations
  - Teamfight positioning data

**Data Storage & Management**
- AWS S3 for raw match data storage
- DynamoDB for player profiles and processed metrics
- Automated data pipeline via AWS Lambda
- Rate limit management (respecting Riot's API limits)
- Historical data retention for year-over-year comparisons

---

### 2. Advanced Analytics & Pattern Recognition

**Machine Learning Models via AWS Lambda**

**Model 1: Performance Pattern Analyzer**
- **Algorithm**: K-Means Clustering with 3 clusters
- **Training Data**: Historical match data with performance characteristics
- **Features Used**:
  - Assist-to-kill ratio
  - Deaths in losses vs. team average
  - Vision score relative to role
  - Objective participation rate
  - Team fight presence percentage
  - CS efficiency metrics
  - Gold differential contribution
- **Output**: Classification of high-impact games, performance consistency levels, player archetype identification
- **Adaptation Logic**: Identifies player's strongest performance dimensions and emphasizes those in output

**Model 2: Mental Resilience Calculator**
- **Algorithm**: Random Forest Classifier
- **Training Data**: Performance metrics correlated with comeback scenarios and pressure situations
- **Features Used**:
  - Performance variance after team deaths
  - KDA improvement in deficit situations
  - Consistency across losing streaks
  - Pressure game performance (promos, series)
  - Tilt recovery patterns
- **Output**: Resilience score (0-100), tilt resistance rating, consistency grade
- **Adaptation Logic**: Calibrates score relative to rank tier and game volume

**Model 3: Growth Trajectory Analyzer**
- **Algorithm**: Time Series Analysis (LSTM Neural Network)
- **Training Data**: Month-over-month performance metrics across player base
- **Features Used**:
  - Rolling 30-day averages for core metrics
  - Champion mastery progression curves
  - Role adaptation patterns over time
  - Meta adaptation speed
  - Improvement velocity calculations
- **Output**: Predicted improvement areas, skill progression forecasts, plateau identification, acceleration metrics
- **Adaptation Logic**: Projects personalized growth targets based on historical improvement rate

**Model 4: Play Style Profiler**
- **Algorithm**: Principal Component Analysis (PCA) + K-Means Clustering
- **Training Data**: Comprehensive gameplay patterns across 100,000+ players
- **Features Used**:
  - Aggression index (early game activity, first blood participation)
  - Teamwork orientation (assists, objective focus, sacrifice plays)
  - Mechanical execution (CS efficiency, damage optimization)
  - Strategic positioning (deaths, vision control, map awareness)
- **Output**: Playstyle archetype (e.g., "Strategic Enabler", "Mechanical Carry", "Late-Game Scaler"), archetype-specific recommendations
- **Adaptation Logic**: Matches player to closest archetype cluster, identifies archetype-specific improvement paths

---

### 3. Comprehensive Metric Tracking (25+ Measurements)

**Core Performance Metrics**
1. **Win Rate**: Overall and role-specific win percentages
2. **KDA Ratio**: Kills/Deaths/Assists performance index
3. **Kills per Game**: Average champion eliminations
4. **Assists per Game**: Team contribution through assists
5. **Deaths per Game**: Survival and positioning metric
6. **CS per Minute**: Farming efficiency across game phases
7. **Vision Score per Minute**: Vision control effectiveness
8. **Gold per Minute**: Economic efficiency

**Macro Game Intelligence**
9. **Objective Participation Rate**: Dragon/Baron/Herald presence vs. team
10. **Map Pressure Creation**: Solo pressure while team secures objectives
11. **Vision Efficiency Score**: Ward placements leading to successful plays
12. **Rotation Timing**: Response speed to map state changes
13. **Side Lane Farm Efficiency**: Gold collection from side lanes post-laning

**Performance Under Pressure**
14. **Comeback Contribution**: Performance improvement in gold-deficit games
15. **Late Game Decision Making**: Success rate in 35+ minute matches
16. **Teamfight Positioning**: Damage dealt/taken ratio in major engagements
17. **Clutch Moment Success**: Performance in critical game-deciding moments
18. **Pressure Game Performance**: Stats in promos and ranked series

**Mental Resilience Indicators**
19. **Tilt Resistance Score**: Consistency after negative events (0-100 scale)
20. **Adaptability Index**: Improvement against counter-matchups over time
21. **Consistency Rating**: Standard deviation of performance metrics
22. **Streak Recovery**: Performance bounce-back after losing streaks

**Skill Expression Metrics**
23. **CS Efficiency Under Pressure**: Farming accuracy when harassed
24. **Damage Optimization**: Damage dealt while maintaining survival
25. **Positioning Intelligence**: Safety index during high-pressure moments
26. **Resource Management**: Mana/energy efficiency in extended engagements

**Team Synergy Metrics**
27. **Follow-up Success Rate**: Team capitalize rate on player initiations
28. **Enablement Factor**: Teammates' performance correlation with player
29. **Sacrifice Play Value**: Deaths directly leading to objectives/advantages
30. **Communication Proxy**: Win rate in coordinated plays vs. solo queue

**Champion & Role Mastery**
31. **Champion Pool Depth**: Number of champions with 55%+ win rate
32. **Role Flexibility**: Performance variance across multiple positions
33. **Meta Adaptation Speed**: Performance with newly buffed/nerfed champions
34. **Signature Champion Mastery**: Win rate on most-played champions

**Comparative Benchmarks**
35. **Rank Percentile**: Performance vs. same-rank players
36. **Role Percentile**: Performance vs. same-role players
37. **Improvement Velocity**: Growth rate vs. player base average

---

### 4. Standardized Output Framework (Three-Tier Structure with Intro Overview)

**CRITICAL UNDERSTANDING ABOUT CONTENT GENERATION**:

RiftSage does NOT use pre-written templates. The structures shown below are **instructions for the AI** on how to analyze data and what to generate. Think of them as a recipe, not a menu - the AI follows the recipe but creates unique dishes for each player.

**What the AI receives**: Player metrics, benchmarks, patterns
**What the AI generates**: 100% unique content analyzing that specific player
**What users see**: Insights that could ONLY apply to them

---

RiftSage delivers all insights using a consistent four-part framework that adapts content to each player's unique data while maintaining structural consistency.

#### **Framework Overview**

Every section follows this structure:
0. **Intro Overview**: Contextual introduction paragraph that frames the data story
1. **Stats & Metrics**: Quantitative data with one-line key insights
2. **Deeper Insights**: Pattern explanations in clear bullet points
3. **Narrative Meaning**: Brief contextual statement (3-5 sentences) explaining significance

**The structure stays the same, but the content is 100% unique per player.**

#### **Section 1: Role Performance Snapshot**

**Purpose**: Establish player's primary role strength and core statistics

**Adaptation Logic**:
- Identifies player's highest win rate role as primary focus
- Selects top 4 metrics that best represent player's strengths
- Compares to rank-appropriate benchmarks
- Calculates year-over-year improvements if historical data available

**AI Generation Instructions (NOT a Fill-in Template)**:

**IMPORTANT**: The structure below is NOT a template with placeholders to fill. It is a set of instructions that tells the AI **how to analyze the data and what to generate**. The AI creates every word dynamically based on the player's unique performance profile.

```
PROMPT TO AI:

Generate a Role Performance Snapshot using this structure:

PART 1 - INTRO OVERVIEW:
Analyze the player's data and write 2-3 sentences that:
- Identify their PRIMARY performance pattern (e.g., "aggressive combat + survival discipline")
- Mention their SECONDARY characteristic (e.g., "year-over-year improvement")
- Reference a specific trend (e.g., "consistent kill participation above rank average")
- End with: "Your key [category] ratios show:"

PART 2 - STATS & METRICS:
Present their top 4 performing metrics (based on percentiles) with format:
- Metric Name: [Exact Value] ([Contextual insight in 5-8 words])
- Use their actual numbers from the data
- Choose metrics where they exceed rank average most

PART 3 - DEEPER INSIGHTS:
Write 4-5 bullet points that explain:
- What their win rate REVEALS about gameplay approach (not just "it's high")
- What their KDA MEANS in terms of actual behavior (e.g., "extracting four impacts per death")
- How other metrics CONNECT to create success patterns
- Use specific numbers from their data
- Each bullet should explain a mechanism, not just restate a stat

PART 4 - NARRATIVE MEANING:
Write 3-5 sentences that:
- Synthesize what the COMBINATION of metrics reveals
- Explain WHY this approach is effective for this player
- Connect to their rank and potential
- Reference at least 3 specific numbers
- Avoid generic statements that could apply to any player

CRITICAL RULES:
- Every sentence must be unique to THIS player's data
- Do not use generic templates or fill-in-the-blank structures
- Adapt insights to their specific strengths/weaknesses
- Make connections between metrics that reveal gameplay patterns
- Write as if you deeply understand THIS player's unique playstyle
```

**Data Provided to AI**:
```json
{
  "player_metrics": {
    "win_rate": 65.0,
    "rank_avg_win_rate": 52.0,
    "win_rate_percentile": 87,
    "kda": 3.8,
    "kda_2024": 2.2,
    "kills_per_game": 7.2,
    "assists_per_game": 6.8,
    "deaths_per_game": 3.5,
    "cs_min": 6.8,
    "vision_min": 0.6
  },
  "comparative_analysis": {
    "top_strengths": ["KDA", "Win Rate", "Kills per Game", "Assists per Game"],
    "improvement_areas": ["CS/min", "Vision Score/min"],
    "overall_percentile": 84
  },
  "context": {
    "primary_pattern": "aggressive_combat_with_survival",
    "playstyle_archetype": "Strategic Enabler",
    "rank": "Platinum III"
  }
}
```

**Example with Real Data**:

```
INTRO OVERVIEW:
Your recent games show a clear pattern of consistent survival paired with high 
combat output, with increases in teamfight presence and significant alignment 
for late-game scaling achievement. Your key survival and impact ratios show:

STATS & METRICS:
- Win Rate: 65% (13% above Platinum average)
- KDA Ratio: 3.8 (71% improvement from 2024)
- Kills per Game: 7.2 (Consistent aggressive impact)
- Assists per Game: 6.8 (Strong team contribution)

DEEPER INSIGHTS (What the Numbers Build On - Pattern Insights):
• Your 65% win rate reflects strong game-closing power — more than half your 
  games end in victory, creating a solid base for rank growth
• Your 3.8 KDA ratio means you stay in the fight longer, turning each life 
  into nearly four impacts
• Your 7.2 kills per game show you consistently find and finish targets
• Your 6.8 assists per game prove you're not just carrying — you're 
  connecting with teammates to close fights
• Low death count opens the door to repeated plays — high kills and assists 
  flow from sharp positioning and timing

NARRATIVE MEANING (Core Data Pattern):
Your 65% win rate on ADC combined with 3.8 KDA demonstrates mastery of 
aggressive positioning while maintaining survival. This balance between impact 
and safety turns teamfights into your strength zone. The combination of 7.2 
kills and 6.8 assists shows you're executing both solo plays and team 
coordination. Adding CS/min and vision score/min to this foundation will 
expand your already strong results into even more consistent climbing power.
```

#### **Section 2: Upgraded Path / Improvement Blueprint**

**Purpose**: Provide actionable, data-driven improvement recommendations

**Adaptation Logic**:
- Identifies 2-3 metrics where player is below rank average
- Selects improvement areas with highest climb correlation
- Recommends 3 champions that align with player's playstyle + address weaknesses
- Provides phase-by-phase targets based on player's current baseline
- Sets 30-day measurable targets scaled to player's current performance

**AI Generation Instructions (NOT a Fill-in Template)**:

```
PROMPT TO AI:

Generate an Improvement Blueprint using this structure:

PART 1 - INTRO OVERVIEW:
Write 2-3 sentences that:
- Acknowledge their primary strength first
- Identify the 2 specific areas for improvement
- Frame improvement as building on existing success
- Use language like "layer in X and Y to turn [short-term] into [long-term]"
- End with: "The goal: make your [strength] work harder by [what improvements enable]"

PART 2 - STATS & METRICS (Current Baseline):
Restate the opportunity in 1-2 sentences, then present their current state

PART 3 - DEEPER INSIGHTS (Data Alignment for Growth):
Write 2-3 bullet points explaining:
- HOW the improvement metrics extend their current impact
- WHY their existing pattern needs these additions
- WHAT enabling factors these improvements provide

PART 4 - RECOMMENDED CHAMPION POOL:
Generate a table with 3 champions that:
- Match their playstyle archetype
- Address their weakness metrics
- Leverage their strength metrics
- Include specific numbers (win rate, CS/min potential, vision support)
- For each champion, write a unique 15-20 word explanation of fit

PART 5 - PHASE-BY-PHASE EXECUTION:
Create a table with 3 game phases showing:
- Specific, measurable priority goals
- Actionable behaviors tied to exact game times
- Quantified benefits (gold gains, percentage improvements)
- Tailored to their role and weaknesses

PART 6 - 30-DAY MEASURABLE TARGETS:
Create a table showing:
- Current value for each improvement metric
- Target value (calculated as current × 1.20 or 80% to rank average)
- Gameplay outcome description
- Projected win rate improvement

PART 7 - NARRATIVE MEANING:
Write 3-4 sentences that:
- Synthesize how current strengths + improvements = superior performance
- Reference specific metrics and their compounding effect
- End with an aspirational but achievable outcome
- Be specific to this player's situation

CRITICAL RULES:
- Champion recommendations must be dynamically selected from database
- Phase-by-phase actions must be specific to their role and weaknesses
- Targets must be calculated, not guessed
- Every word unique to this player's profile
```

**Data Provided to AI**:
```json
{
  "player_metrics": {
    "win_rate": 65.0,
    "cs_min": 6.8,
    "rank_avg_cs_min": 7.8,
    "vision_min": 0.6,
    "rank_avg_vision_min": 0.85,
    "kda": 3.8,
    "primary_role": "ADC"
  },
  "improvement_opportunities": [
    {
      "metric": "cs_min",
      "current": 6.8,
      "rank_avg": 7.8,
      "gap": 1.0,
      "target": 8.0,
      "climb_correlation": 0.42
    },
    {
      "metric": "vision_min",
      "current": 0.6,
      "rank_avg": 0.85,
      "gap": 0.25,
      "target": 0.8,
      "climb_correlation": 0.38
    }
  ],
  "champion_recommendations": [
    {
      "champion": "Ashe",
      "win_rate_pattern": "53%+ in similar play",
      "cs_min_potential": 7.8,
      "vision_support": 0.92,
      "fit_score": 87,
      "strengths": ["Global vision (E)", "High range", "Catch potential"]
    },
    {
      "champion": "Jinx",
      "win_rate_pattern": "52%+ in scaling games",
      "cs_min_potential": 8.4,
      "vision_support": 0.78,
      "fit_score": 85,
      "strengths": ["Rocket waveclear", "Hyperscaling", "Reset potential"]
    },
    {
      "champion": "Sivir",
      "win_rate_pattern": "52%+ in farm-heavy lanes",
      "cs_min_potential": 8.7,
      "vision_support": 0.81,
      "fit_score": 82,
      "strengths": ["Spell shield safety", "Waveclear", "Utility ultimate"]
    }
  ],
  "playstyle_archetype": "Strategic Enabler"
}
```

**Example with Real Data**:

```
INTRO OVERVIEW:
Your 65% win rate already proves your strength — now layer in farm efficiency 
and vision control to turn short-term wins into long-term climbing consistency. 
The goal: make your positioning work harder by giving it more gold and map 
control to work with.

STATS & METRICS (Current Baseline):
Your 65% win rate already proves your strength — now layer in farm efficiency 
and vision control to turn short-term wins into long-term climbing consistency.

DEEPER INSIGHTS (Data Alignment for Growth):
Games where you secure 8+ CS/min and 0.8+ vision/min extend your impact 
beyond teamfights — they keep you ahead in gold and map awareness. Your 
current pattern (high KDA + kills) thrives when you have items and safety. 
Farm and vision deliver both.

RECOMMENDED CHAMPION POOL:

| Champion | Win Rate Pattern | CS/min Potential | Vision Support | Fit for Your Playstyle |
|----------|------------------|------------------|----------------|------------------------|
| Ashe | 53%+ in similar play | 7.8 | 0.92 | Global vision (E) and arrows turn your positioning into team-wide picks and control |
| Jinx | 52%+ in scaling games | 8.4 | 0.78 | Rockets clear waves fast — more gold, more items, more late-game power |
| Sivir | 52%+ in farm-heavy lanes | 8.7 | 0.81 | Spell shield blocks danger; waveclear keeps you rich and safe |

PHASE-BY-PHASE EXECUTION (15-Min Win Focus):

| Game Phase | Priority Goal | Core Action | Gold & Impact Gain |
|------------|---------------|-------------|---------------------|
| 0–10 min (Laning) | 7.5+ CS/min | Freeze near tower or mirror-push; fight only at power spikes (lvl 2/6) with support | +1,000 gold — same as one extra kill, but guaranteed |
| 10–20 min (Mid) | Vision + Side Farm | Place 2 control wards per recall; farm side lanes after T1 falls | +15% gold lead; forces enemies to react to you |
| 20+ min (Late) | Teamfight Control | Stay backline, use utility to start fights. Split only with teleport up | Turns your 65% late-game strength into 67-70% consistent wins |

30-DAY MEASURABLE TARGETS:

| Metric | Your Current Base | Week 4 Target | Growth Outcome |
|--------|-------------------|---------------|----------------|
| CS/min | 6.8 | 8.0+ | +1,200 gold every 10 minutes |
| Vision Score/min | 0.6 | 0.8+ | More picks, safer plays, objective control |
| Win Rate (next 50 games) | 65% | 67-70% | Smoother, faster climb with more consistency |

NARRATIVE MEANING (Final Pattern Insight):
Your 3.8 KDA and 65% win rate are already elite performance markers. Adding 
8 CS/min and 0.8 vision/min means every fight starts with you ahead in items 
and information. Your positioning becomes unstoppable when backed by gold 
advantage and vision control. The combination transforms your already strong 
teamfighting into a comprehensive climbing engine. The nexus becomes routine.
```

#### **Section 3: Mental Resilience & Consistency**

**Purpose**: Highlight psychological strengths and tilt management

**Adaptation Logic**:
- Calculates tilt resistance score from performance variance
- Identifies comeback game performance patterns
- Measures consistency across different game states
- Compares pressure game performance to average games

**Output Template**:

```
INTRO OVERVIEW:
Your mental game shows [primary resilience characteristic] across [context - 
e.g., "difficult match situations", "comeback scenarios"], with [specific 
pattern observed]. Your consistency and pressure performance metrics reveal:

STATS & METRICS:
- Tilt Resistance Score: [0-100 value] ([grade: Low/Medium/High/Elite])
- Consistency Rating: [Value] ([interpretation])
- Comeback Game Win Rate: [%] ([comparison to overall win rate])
- Pressure Performance: [%] in promos/series ([comparison])

DEEPER INSIGHTS (Pattern Identification):
• Your [tilt resistance score] indicates [pattern explanation]
• Performance in [X] comeback games shows [specific behavior pattern]
• [Consistency metric] reveals [what this says about playstyle]
• [Additional pattern from mental game analysis]

NARRATIVE MEANING:
[3-4 sentences explaining player's mental game strengths, how it contributes 
to their success, and what this predicts for future performance improvement.]
```

#### **Section 4: Champion Mastery Analysis**

**Purpose**: Identify champion pool strengths and optimization opportunities

**Adaptation Logic**:
- Ranks champions by win rate and games played
- Identifies champion pool depth (number of champions with 55%+ win rate)
- Analyzes performance by champion class/role
- Recommends pool expansion or specialization based on data

**Output Template**:

```
INTRO OVERVIEW:
Your champion pool demonstrates [primary mastery characteristic] with 
[specific pattern - e.g., "strong specialization", "versatile flexibility"], 
showing [notable trend]. Your champion performance breakdown reveals:

STATS & METRICS (Champion Performance):
- Most Played Champion: [Champion] ([games played], [win rate]%)
- Champion Pool Depth: [X] champions with 55%+ win rate
- Highest Win Rate: [Champion] ([win rate]% over [X] games)
- Role Distribution: [Primary role %], [Secondary role %]

DEEPER INSIGHTS (Champion Analysis):
• Your [X]% win rate on [champion] demonstrates [mastery aspect]
• Champion pool shows preference for [archetype/playstyle]
• [Performance pattern across champion types]
• [Meta adaptation or champion mastery trend]

RECOMMENDED POOL ACTIONS:
[Bullet points with specific recommendations]
• Specialize: [Champion(s)] — your [metric] excels here
• Expand: [Champion(s)] — fills gaps in your pool while matching playstyle
• Practice: [Champion(s)] — high potential based on your strengths

NARRATIVE MEANING:
[3-4 sentences synthesizing champion mastery patterns, what it reveals about 
player skill expression, and strategic recommendations for pool optimization.]
```

#### **Section 5: Outstanding Games Showcase**

**Purpose**: Celebrate exceptional performances with data backing

**Adaptation Logic**:
- Identifies top 10 games by impact score (weighted formula of KDA, objective participation, comeback factor, vision score)
- Categorizes games by type (comeback, carry performance, team enablement, clutch moment)
- Provides context for why each game was exceptional

**Output Template**:

```
INTRO OVERVIEW:
Your standout performances throughout the year reveal [primary excellence 
characteristic], with [specific pattern - e.g., "exceptional clutch factor", 
"consistent high-impact play"], particularly strong in [context]. Your 
exceptional game metrics show:

STATS & METRICS (Top Performance Games):
- Games Analyzed: [Total games]
- Outstanding Impact Games: [Number] ([% of total])
- Highest Impact Score: [Value] ([date, champion, outcome])
- Most Common Excellence Type: [Category]

GAME HIGHLIGHTS (Top 5 by Impact Score):

[For each game, provide:]

Game #[X] - [Date] - [Champion] - [Outcome]
• Impact Score: [Value]/100
• KDA: [K/D/A] ([KDA ratio])
• [2-3 standout metrics specific to why this game was exceptional]
• Excellence Category: [Comeback/Carry/Enabler/Clutch]
• Key Moment: [Brief 1-sentence description of pivotal play]

DEEPER INSIGHTS (What Made These Special):
• [Pattern across outstanding games]
• [Common factors in highest-impact performances]
• [What triggers peak performance for this player]

NARRATIVE MEANING:
[3-4 sentences explaining what these outstanding games reveal about player's 
ceiling, clutch factor, and potential for high-level performance. Connects to 
improvement recommendations.]
```

#### **Section 6: Year-Over-Year Growth (If Applicable)**

**Purpose**: Show measurable improvement trajectory

**Adaptation Logic**:
- Only included if player has 2024 data available
- Calculates percentage improvements across all key metrics
- Identifies breakthrough moments and acceleration periods
- Projects continued growth trajectory

**Output Template**:

```
INTRO OVERVIEW:
Your growth trajectory from 2024 to 2025 demonstrates [primary improvement 
characteristic], with [specific achievements - e.g., "consistent skill 
acceleration", "breakthrough performance gains"], particularly in [strongest 
growth area]. Your year-over-year progress shows:

STATS & METRICS (Year-Over-Year Comparison):
- Rank Improvement: [2024 rank] → [2025 rank] ([X] divisions)
- Win Rate Change: [2024 %] → [2025 %] ([+/-X]% improvement)
- KDA Improvement: [2024 KDA] → [2025 KDA] ([+X]% growth)
- [Top 2-3 metrics with largest improvements]

DEEPER INSIGHTS (Growth Patterns):
• [Largest area of improvement and what enabled it]
• [Skill development trajectory observation]
• [Acceleration periods identified - months of fastest growth]
• [Plateau periods and what changed to break through]

GROWTH TRAJECTORY PROJECTION:
If current improvement rate continues:
• Estimated 2026 Rank: [Projection based on trend]
• Key Metrics to Reach Target: [Specific numbers needed]
• Timeline to Next Rank: [Estimated months based on LP gain rate]

NARRATIVE MEANING:
[3-4 sentences celebrating tangible growth, explaining what the trajectory 
reveals about player's learning curve, and forecasting realistic future 
achievement with continued dedication.]
```

---

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
