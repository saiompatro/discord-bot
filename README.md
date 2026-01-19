# Game of Wall Street (GWS) - Discord Bot

A comprehensive economy game Discord bot with stock trading, job grinding, casino gambling, and character progression.

## Features

### ✅ Implemented
- **30+ Unique Characters** with different stats and starting money
- **Account System** with leveling and progression
- **Job Grinding System** - 20 different jobs across 4 tiers (Street Vendor → CEO)
- **Casino Games** - Coinflip, Slots, Blackjack, Roulette, Dice Roll
- **Stock Market** - 20 stocks with realistic price movements
- **Economy** - Cash, bank balance, net worth tracking
- **Leaderboards** - Rank by net worth, level, casino winnings, job earnings
- **60+ Achievements** - Unlock rewards for milestones
- **Social Features** - Guilds, duels, player trading, money transfers
- **Help Menu** - Built-in command documentation

### 🎮 Commands

#### Account Commands
- `/setup` - Create account and select character
- `/profile` - View complete profile with stats
- `/balance` - Quick balance check
- `/daily` - Claim daily login bonus
- `/leaderboard [sort_by] [limit]` - View top players
- `/help` - Command documentation

#### Job Commands
- `/work [job_id]` - Work a job
- `/work_list` - See available jobs for your level
- `/work_info [job]` - Detailed job information

#### Casino Commands
- `/casino` - View casino overview
- `/casino_play [game] [bet] [choice]` - Play a casino game
- `/casino_stats` - View your gambling statistics

#### Stock Commands
- `/stocks` - Market overview
- `/stocks_info [ticker]` - Stock details
- `/stocks_buy [ticker] [quantity]` - Buy stock
- `/stocks_sell [ticker] [quantity]` - Sell stock
- `/stocks_portfolio` - View your holdings
- `/stocks_sectors` - Sector performance

#### Achievement Commands
- `/achievements [filter]` - View your achievements (all/common/uncommon/rare/epic/legendary)

#### Social Commands
- `/guild [action] [name]` - Guild management (create/info/members/leaderboard)
- `/duel [@opponent]` - Challenge player to duel
- `/transfer [@player] [amount]` - Send money to player
- `/trade [@player] [give] [get]` - Trade stocks (format: APPL:5 for 5 shares)

## Installation

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Set Up Environment Variables**
Create a `.env` file in the root directory:
```
DISCORD_TOKEN=your_bot_token_here
```

3. **Run the Bot**
```bash
python main.py
```

## Project Structure

```
discord bot/
├── main.py                 # Bot entry point
├── requirements.txt        # Dependencies
├── .env                   # Environment variables (create this)
├── cogs/                  # Command handlers
│   ├── account.py         # Account commands
│   ├── jobs.py            # Job commands
│   ├── casino.py          # Casino commands
│   └── stocks.py          # Stock commands
├── data/                  # Static data
│   ├── characters.py      # 30+ character definitions
│   └── players.json       # Player data (auto-generated)
├── utils/                 # Utility modules
│   ├── economy.py         # Economy and player management
│   ├── jobs.py            # Job system
│   ├── casino.py          # Casino games
│   └── stocks.py          # Stock market
└── assets/                # Images and assets (future)
```

## Character System

Each character has:
- **Stats**: Intellect, Humour, Strength, Leadership, Mental Health, Wealth (1-5 stars each)
- **Starting Money**: Based on character tier
- **Job Bonuses**: Increased payout for certain job types
- **Bio**: Unique background story

**Example Characters:**
- Dave: JP Morgan Broker (Finance expert, low mental health)
- Judy: Citadel Receptionist (Ambitious, low starting funds)
- Emily: Stanford Graduate (Highly ambitious, narcissistic)
- Marcus: Self-Made CEO (Wealthy, excellent leader)
- Patricia: Night Shift Janitor (Lower tier, grinding story)

## Game Mechanics

### Leveling
- **Levels 1-100** - Unlock new jobs at key milestones
- **XP Earned** - Jobs, casino wins, stock trading, achievements
- **Prestige** - Optional reset at level 50 for cosmetics

### Economy
- **Jobs** - Primary income source, stat-dependent payouts
- **Casino** - Risk/reward gambling with house edge
- **Stocks** - Long-term wealth building
- **Daily Bonus** - Login rewards with streak bonuses

### Job System
Jobs have:
- Cooldown (30s - 12min depending on tier)
- Payout range (base earnings)
- Success rate (affected by player stats)
- Stat scaling (bonuses for high relevant stats)
- Critical chance (5% for 2x payout)

**Tiers:**
1. Tier 1 (Levels 1-15): Street Vendor, Dog Walker, etc.
2. Tier 2 (Levels 15-35): Retail Manager, Consultant, etc.
3. Tier 3 (Levels 35-60): Lawyer, Real Estate Agent, etc.
4. Tier 4 (Levels 60+): CEO, Hedge Fund Trader, VC, etc.

### Casino Games

| Game | Min Bet | Max Bet | House Edge | Notes |
|------|---------|---------|-----------|-------|
| Coinflip | $5 | $10,000 | 2% | Simple 50/50 |
| Slots | $5 | $5,000 | 10% | High variance |
| Blackjack | $20 | $10,000 | 3.5% | Skill element |
| Roulette | $10 | $15,000 | 2.7% | Multiple bet types |
| Dice Roll | $5 | $8,000 | 4% | Higher/Lower |

**Features:**
- Tilt protection (5 consecutive losses = 10min cooldown)
- VIP tiers (cosmetic/progression based)
- Loyalty points (1 per $100 wagered)
- Win streaks (bonus to next bet)

### Stock Market

**20 Stocks** across multiple sectors:
- Technology (APPL, MSFT, GOOG, TSLA, etc.)
- Finance (JPM, GS, BRK)
- Semiconductors (AMD, NVDA)
- Cryptocurrency (COIN, RIOT) - High volatility
- Entertainment (NFLX, SPOT)

**Features:**
- Realistic price movements based on volatility
- Sector performance tracking
- Portfolio management
- Buy/Sell mechanics with pricing
- Price history tracking

## Data Persistence

All player data is stored in `data/players.json` and auto-saved after every transaction.

Stock data is in `data/stocks.json` and updates periodically.

## Future Features (Not Yet Implemented)

- ⏳ **Guild System** - Guilds, team competitions, shared treasury
- ⏳ **PvP Duels** - Head-to-head competitions
- ⏳ **Trading** - Direct peer-to-peer item/stock trading
- ⏳ **Achievements** - 60+ achievement system
- ⏳ **Items/Cosmetics** - Collectibles and customization
- ⏳ **Character Portraits** - Visual representations (waiting for user assets)
- ⏳ **Web Dashboard** - Real-time stats and leaderboards
- ⏳ **Events** - Special market events, news, crashes
- ⏳ **Loans System** - Borrowing money with interest

## Configuration

### Adding New Characters

Edit `data/characters.py` and add to `CHARACTERS` dict:

```python
"NewChar": {
    "title": "Job Title",
    "background": "Character description",
    "stats": {"intellect": 3, "humour": 4, "strength": 2, "leadership": 3, "mental_health": 3, "wealth": 2},
    "starting_cash": 5000,
    "starting_bank": 10000,
    "job_bonuses": {"job_id": 1.15},
    "bio_emoji": "🎭"
}
```

### Adding New Jobs

Edit `utils/jobs.py` and add to `JOBS` dict:

```python
"job_id": {
    "name": "Job Name",
    "tier": 3,
    "min_level": 35,
    "cooldown": 240,
    "payout_min": 500,
    "payout_max": 1500,
    "base_success_rate": 0.85,
    "stat_scaling": {"intellect": 0.6, "leadership": 0.4},
    "description": "Job description",
    "emoji": "💼"
}
```

## Economy Balance

- **Daily Cap**: Players can't earn unlimited money (daily earning limits)
- **Deflation**: Bank interest (3-5% annually) absorbs excess cash
- **Inflation Control**: Prices scale with economy
- **Rich Player Content**: CEO jobs and high-tier activities for wealthy players
- **Catch-Up Mechanics**: New players get doubled rewards first 3 days

## Troubleshooting

**Bot Won't Start**
- Check DISCORD_TOKEN in .env file
- Verify discord.py is installed: `pip install discord.py`

**Commands Not Appearing**
- Restart the bot (may take 1-2 min to sync commands)
- Check bot has proper permissions in the server

**Economy Issues**
- Delete `data/players.json` to reset (will lose all accounts!)
- Check `discord.log` for detailed errors

## Support & Contributing

This is a work in progress. Future features will be added based on user feedback.

**Planned Additions:**
1. Character portraits (waiting for user assets)
2. Guild system (2 weeks)
3. Advanced trading (1 week)
4. Web dashboard (2-3 weeks)
5. Mobile app (future consideration)

---

**Made for Discord**  
Game of Wall Street © 2025
#   d i s c o r d - b o t  
 #   d i s c o r d - b o t  
 #   d i s c o r d - b o t  
 