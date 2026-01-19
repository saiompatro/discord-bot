# Game Balance & Economy Analysis

## Economy Overview

### Three Income Streams
1. **Jobs** - Steady income with cooldowns (main income)
2. **Casino** - High variance, negative EV (entertainment)
3. **Stocks** - Long-term wealth building (speculative)

### Three Spending Options
1. **Casino Games** - Risk/entertainment
2. **Stock Purchases** - Investment
3. **Guild Treasury** - Cooperative spending (coming soon)

---

## Job System Balance

### Expected Earnings by Tier

| Tier | Level | Min Payout | Max Payout | Cooldown | Hourly Rate* |
|------|-------|-----------|-----------|----------|------------|
| 1 | 1-9 | $50 | $150 | 30s | $600-1800/hr |
| 2 | 10-29 | $200 | $500 | 60s | $720-1800/hr |
| 3 | 30-59 | $800 | $2000 | 120s | $2400-6000/hr |
| 4 | 60+ | $5000 | $15000 | 300s | $6000-18000/hr |

*Assumes perfect execution with no rest

### Current Jobs
```
Tier 1:
- Street Vendor ($50-150, no stat scaling)
- Cashier ($60-180, slight intellect boost)
- Lifeguard ($75-200, strength bonus)
- Waiter ($100-250, humour bonus)
- Tutor ($80-220, intellect bonus)

Tier 2:
- Data Analyst ($200-500, intellect scaling)
- Sales Rep ($250-600, leadership scaling)
- Fitness Coach ($300-700, strength scaling)
- Graphic Designer ($200-550, humour scaling)
- Accountant ($250-650, intellect scaling)

Tier 3:
- Manager ($800-2000, leadership scaling)
- Consultant ($1000-2500, intellect scaling)
- Trainer ($900-2200, strength scaling)
- Creative Director ($850-2100, humour scaling)
- Financial Advisor ($1100-2600, intellect scaling)

Tier 4:
- CEO ($8000-15000, leadership scaling)
- Venture Capitalist ($9000-18000, intellect scaling)
- CFO ($7000-16000, intellect+leadership)
- CTO ($8500-17000, intellect+strength)
- COO ($8000-15000, leadership+humour)
```

### Leveling Progression

| Level | XP Required | Cumulative | Jobs to Reach |
|-------|------------|-----------|--------------|
| 1 | - | 0 | 0 |
| 5 | 500 | 500 | 50 |
| 10 | 1000 | 1500 | 100 |
| 20 | 3000 | 7500 | 250 |
| 30 | 5000 | 18000 | 500 |
| 50 | 12000 | 65000 | 1500 |
| 100 | 50000 | 450000 | 5000+ |

**Analysis**: Level 10 takes ~2-3 hours of consistent work

### Job Success Rate

Base formula:
```
success_rate = base_rate + (player_stat / 5) * 0.15 + random(-0.05, 0.05)
```

Example (Intellect job, max intellect):
```
success_rate = 0.80 + (5 / 5) * 0.15 + random
            = 0.80 + 0.15 + random
            = 0.95 + random (94-96% chance)
```

---

## Casino Balance

### House Edge by Game

| Game | House Edge | Mechanics | Player RTP |
|------|-----------|-----------|-----------|
| Coin Flip | 2% | 50/50 odds | 98% |
| Slots | 10% | 5-symbol, 100 combos | 90% |
| Blackjack | 3.5% | Hit/Stand, dealer rules | 96.5% |
| Roulette | 2.7% | 37 numbers (EU wheel) | 97.3% |
| Dice | 4% | Higher/Lower/7 | 96% |

### Tilt Protection
- Activates after 5 consecutive losses
- 10-minute cooldown for casino
- Prevents bad luck spiral
- Encourages session breaks

### Betting Limits
```python
MIN_BET = 10    # Minimum $10
MAX_BET = 5000  # Maximum $5000
```

### Expected Loss Over Time

Over 1000 bets of $100 each ($100k wagered):
```
Coin Flip: -$2,000 (2%)
Slots: -$10,000 (10%)
Blackjack: -$3,500 (3.5%)
Roulette: -$2,700 (2.7%)
Dice: -$4,000 (4%)
```

### VIP Tiers
```python
TIER_BRONZE = {"threshold": 1000, "bonus": 1.01}   # 1% bonus
TIER_SILVER = {"threshold": 10000, "bonus": 1.02}  # 2% bonus
TIER_GOLD = {"threshold": 100000, "bonus": 1.03}   # 3% bonus
```

---

## Stock Market Balance

### 20 Stocks Available

| Ticker | Sector | Starting Price | Volatility | Type |
|--------|--------|----------------|-----------|------|
| APPL | Tech | $150 | 12% | Growth |
| MSFT | Tech | $300 | 8% | Stable |
| GOOG | Tech | $2500 | 10% | Growth |
| AMZN | Tech | $3200 | 14% | Growth |
| TSLA | Tech | $800 | 20% | Volatile |
| JPM | Finance | $150 | 6% | Stable |
| GS | Finance | $350 | 8% | Stable |
| WFC | Finance | $45 | 7% | Stable |
| BRK.B | Finance | $340 | 4% | Very Stable |
| COIN | Crypto | $80 | 35% | Highly Volatile |
| RIOT | Crypto | $12 | 25% | Volatile |
| MSTR | Crypto | $400 | 30% | Volatile |
| XLU | Energy | $65 | 5% | Stable |
| CVX | Energy | $160 | 8% | Stable |
| XOM | Energy | $110 | 7% | Stable |
| NEE | Energy | $80 | 6% | Stable |
| MSFT | Healthcare | $400 | 9% | Growth |
| JNJ | Healthcare | $160 | 6% | Stable |
| UNH | Healthcare | $475 | 7% | Stable |
| PFE | Healthcare | $50 | 8% | Stable |

### Price Movement Algorithm
```python
change = random.gauss(0, volatility)
new_price = old_price * (1 + change)
```

Example: APPL with 12% volatility
```
Standard move per day: ±2-3%
Possible range: -36% to +36% (3 sigma)
```

### Expected Returns
```
Tech stocks: 20-40% annually
Finance stocks: 5-15% annually
Crypto stocks: ±50-100% annually
```

---

## Starting Character Balance

| Character | Starting Cash | Starting Bank | Bias | Status |
|-----------|---------------|---------------|------|--------|
| Dave | $2000 | $8000 | Finance | Balanced |
| Judy | $1500 | $4500 | Office | Budget |
| Emily | $3000 | $15000 | Tech | Wealthy |
| Marcus | $5000 | $70000 | Executive | Very Wealthy |
| Patricia | $1200 | $2800 | Service | Very Poor |
| Robert | $2500 | $12000 | Sales | Wealthy |
| Sarah | $1800 | $5500 | Education | Budget |
| James | $3500 | $20000 | Finance | Wealthy |
| Maria | $2200 | $8000 | Service | Balanced |
| William | $2000 | $10000 | Management | Balanced |

**Analysis**: Character choice gives 1.2x to 5x starting wealth variation

---

## Economy Stability Checks

### Money Sink (Where Money Goes)
1. Casino losses (negative EV)
2. Guild wars (rewards from treasury)
3. Stock pump-and-dump (speculation)

### Money Faucet (Where Money Comes From)
1. **Jobs** (primary) - ~70% of income
2. **Daily login bonus** - ~5% of income
3. **Stock profits** (if lucky) - ~10% of income
4. **Duels** (win $500) - ~5% of income
5. **Achievements** (future) - ~10% of income

### Targeted Daily Active Player Income
```
Tier 1 player (new): $5,000-8,000/day (grinding)
Tier 2 player (level 20-30): $8,000-15,000/day
Tier 3 player (level 40-50): $20,000-40,000/day
Tier 4 player (level 60+): $40,000-100,000/day
```

### Leaderboard Dynamics
```
Top 1% should have: $1,000,000+ net worth
Top 10% should have: $100,000+ net worth
Top 50% should have: $10,000+ net worth
Average player: $5,000-50,000 net worth
```

---

## Balance Tuning Guide

### If Economy is Inflating (Money Too Easy)
1. Reduce job payouts by 20%
2. Increase casino house edge by 1%
3. Increase stock volatility
4. Add more money sinks (guild wars, gambling)

### If Economy is Stagnant (Hard to Earn)
1. Increase job payouts by 20%
2. Reduce casino house edge by 1%
3. Add daily bonuses
4. Reduce leveling requirements

### If Jobs Feel Grindy
1. Reduce cooldowns by 20%
2. Increase payouts by 10%
3. Reduce min level for tier 2+ jobs

### If Casino Feels Unfair
1. Reduce house edge
2. Increase max bet limit
3. Reduce tilt protection cooldown

### If Stocks are Boring
1. Increase volatility (more dramatic swings)
2. Add pump-and-dump events
3. Add stock news (coming soon)

---

## Achievements Balance

### 60+ Achievements Across Categories

| Category | Count | Difficulty | Reward |
|----------|-------|----------|---------|
| Getting Started | 5 | Easy (1-5 min) | 10-50 pts |
| Grinding | 8 | Medium (1-10 hrs) | 50-300 pts |
| Casino | 10 | Hard (10+ hrs) | 100-500 pts |
| Stocks | 8 | Medium (1-30 days) | 100-500 pts |
| Wealth | 8 | Hard (100+ hrs) | 200-500 pts |
| Leveling | 5 | Very Hard (500+ hrs) | 300-500 pts |
| Social | 8 | Medium (varies) | 50-300 pts |
| Prestige | 8 | Very Hard (1000+ hrs) | 500 pts |

---

## Future Balance Considerations

### Planned Features
- Guild wars (requires treasury management)
- Achievement rewards (cosmetics/boosts)
- Prestige system (reset for points)
- Trading bots (NPC wealth sources)
- Market events (crashes/booms)
- Character evolution (new tiers)

### Data Collection Points
- Average playtime per session
- Average money earned per player per day
- Casino win rate vs house edge
- Stock portfolio performance
- Achievement unlock rates
- Guild participation rates

---

## Quick Balance Reference

| Metric | Current | Ideal Target |
|--------|---------|--------------|
| New player level 1→5 time | 1 hour | 30 min - 1 hour |
| New player level 1→10 time | 2 hours | 2-3 hours |
| Daily grind earnings | $10-20k | Varies by level |
| Casino house edge | 2-10% | 2-5% |
| Stock returns (annual) | -50% to +100% | -30% to +80% |
| Leaderboard diversity | Varies | Top 10% in 1000 hrs |

---

**Last Updated**: Session 1  
**Version**: 1.0 MVP  
**Status**: Ready for testing with real players
