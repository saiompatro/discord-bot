# Testing & Configuration Guide

## Pre-Launch Testing Checklist

### Setup & Deployment
- [ ] Create Discord bot on Developer Portal
- [ ] Set bot token in `.env` file
- [ ] Invite bot to test server with proper permissions
- [ ] Run `pip install -r requirements.txt`
- [ ] Start bot with `python main.py`
- [ ] Verify "Bot logged in" message appears
- [ ] Check commands sync (should see ~19 commands)

### Core Commands Testing

#### Account Commands
```bash
# Test /setup
/setup                          # Should show character selection
                                # Choose a character
                                # Should create account with starting money

# Test /profile
/profile                        # Should show character, stats, money

# Test /balance
/balance                        # Should match /profile money

# Test /daily
/daily                          # Should give bonus (first time)
/daily                          # Should say already claimed (second time)

# Test /help
/help                           # Should show all command categories

# Test /leaderboard
/leaderboard                    # Should show top 10 by net worth
/leaderboard level 5            # Should show top 5 by level
```

#### Job Commands
```bash
# Test /work_list
/work_list                      # Should show available jobs for level

# Test /work_info
/work_info street_vendor        # Should show job details

# Test /work
/work street_vendor             # Should work job
                                # Check money increased
                                # Check XP increased
                                # Should show cooldown message on repeat
```

#### Casino Commands
```bash
# Test /casino
/casino                         # Should show all available games

# Test /casino_play
/casino_play coinflip 100 heads # Should win or lose
                                # Check balance changed
                                # Should show result

# Test different games
/casino_play slots 50
/casino_play dice 100 higher
/casino_play roulette 75 red
```

#### Stock Commands
```bash
# Test /stocks
/stocks                         # Should show market overview

# Test /stocks_info
/stocks_info APPL               # Should show stock details

# Test /stocks_buy
/stocks_buy APPL 5              # Should buy 5 shares
/stocks_portfolio               # Should show holding

# Test /stocks_sell
/stocks_sell APPL 3             # Should sell 3 shares
```

#### Achievement Commands
```bash
# Test /achievements
/achievements                   # Should show achievements with unlock status
/achievements rare              # Should filter by rarity (common, uncommon, rare, epic, legendary)
                                # Should show progress on locked achievements
```

#### Social/Guild Commands
```bash
# Test /guild
/guild create MyGuild           # Should create guild
/guild info                     # Should show guild info
/guild members                  # Should show guild members
/guild leaderboard              # Should show top guilds by level

# Test /duel
/duel @opponent                 # Should challenge player
                                # Should show winner based on leadership stat
                                # Winner gets $500

# Test /transfer
/transfer @recipient 1000       # Should send money
                                # Check recipient balance increased

# Test /trade
/trade @player APPL:5 MSFT:3    # Should trade 5 APPL for 3 MSFT
                                # Both players need stocks to trade
```

### Balance Testing

#### Economy Balance
```
Check these values make sense:
- Job payouts: $50-$150 (tier 1) to $5000-$15000 (tier 4)
- Casino wins: Payouts should be less than bet when accounting for house edge
- Starting money: Different characters get different amounts
- Level progression: Level 10 should be achievable in 1-2 hours
```

#### Casino House Edge Verification
```
Theory: Over 1000 bets, player should lose:
- Coinflip: -2% (1000 bets = -20 units lost)
- Slots: -10% (very volatile, test with large sample)
- Roulette: -2.7%
- Dice: -4%
```

#### Job Balance
```
Expected:
- Tier 1 jobs: 5 min for $100-200
- Tier 2 jobs: 10 min for $300-700  
- Tier 3 jobs: 20 min for $800-2000
- Tier 4 jobs: 40+ min for $5000-15000
```

### Gameplay Testing

#### Account Progression
```
1. Create account with different characters
   - Check starting money varies
   - Check stats are different
   
2. Work jobs for 1 hour
   - Should earn $5,000-$15,000
   - Should level up 2-3 times
   - Should see job streaks working
   
3. Gamble in casino for 1 hour
   - Should lose money overall (house edge)
   - Check tilt protection works (5 losses)
   
4. Trade stocks for 1 day
   - Buy some stocks
   - Check prices change
   - Sell for profit/loss
```

#### Social Features
```
1. Multiple accounts
   - Create 5+ test accounts
   - Check leaderboard updates
   - Verify no duplicate data
```

### Error Handling Testing

#### Invalid Inputs
```bash
# Try invalid commands
/work invalid_job                # Should say job not found
/casino_play invalid_game 100    # Should error
/stocks_buy INVALID 10           # Should error
/work_info nonexistent           # Should error

# Try edge cases
/work_list                       # Before level requirement met
/casino_play coinflip 1 heads    # Below min bet
/casino_play slots 50000 tails   # Above max bet
/stocks_buy APPL 999999          # Insufficient funds
/stocks_sell AAPL 100            # Don't own stock
```

#### Money Edge Cases
```bash
# Insufficient funds
/casino_play slots 999999        # Should reject

# Overflow checks
/work                            # After 100 consecutive jobs
```

#### Cooldown Testing
```bash
# Jobs should have cooldown
/work street_vendor              # Works
/work street_vendor              # Should say "Cooldown: X seconds"
[Wait 30 seconds]
/work street_vendor              # Should work again

# Casino tilt protection
/casino_play dice 100 higher     # Lose
/casino_play dice 100 higher     # Lose
/casino_play dice 100 higher     # Lose
/casino_play dice 100 higher     # Lose
/casino_play dice 100 higher     # Lose - triggers tilt
/casino_play slots 50            # Should say tilt protection active
```

## Configuration & Tuning

### Adjusting Game Balance

#### Job Payouts (in `utils/jobs.py`)
```python
# If jobs are too rewarding:
"payout_min": 50,
"payout_max": 150,

# Change to lower value
"payout_min": 30,
"payout_max": 100,
```

#### Casino House Edge (in `utils/casino.py`)
```python
# If casino is unfair to players:
super().__init__(house_edge=2)  # Currently 2%

# Change to lower/higher
super().__init__(house_edge=1)  # 1% easier
super().__init__(house_edge=4)  # 4% harder
```

#### Stock Volatility (in `utils/stocks.py`)
```python
# If stocks don't change enough:
"volatility": 0.08,  # ±8% per day

# Change to more/less volatile
"volatility": 0.15,  # ±15% per day (more exciting)
"volatility": 0.03,  # ±3% per day (more stable)
```

#### Level Requirements (in `utils/jobs.py`)
```python
# If tier 4 jobs are too hard to reach:
"min_level": 60,  # Currently 60

# Change to lower
"min_level": 50,  # Easier to reach
```

### Adding New Jobs

```python
# In utils/jobs.py, add to JOBS dict:
"consultant_v2": {
    "name": "Senior Consultant",
    "tier": 4,
    "min_level": 50,
    "cooldown": 300,
    "payout_min": 1500,
    "payout_max": 4000,
    "base_success_rate": 0.85,
    "stat_scaling": {"intellect": 0.7, "leadership": 0.3},
    "description": "Provide high-level consulting",
    "emoji": "💡"
}
```

### Adding New Stocks

```python
# In utils/stocks.py, add to INITIAL_STOCKS:
"EXAMPLE": {
    "name": "Example Corp",
    "sector": "Technology",
    "starting_price": 100.00,
    "volatility": 0.12,
    "description": "Example company"
}
```

### Adding New Characters

```python
# In data/characters.py, add to CHARACTERS:
"NewChar": {
    "title": "Job Title",
    "background": "Character story...",
    "stats": {"intellect": 3, "humour": 4, "strength": 2, "leadership": 3, "mental_health": 3, "wealth": 2},
    "starting_cash": 5000,
    "starting_bank": 10000,
    "job_bonuses": {"job_id": 1.15},
    "bio_emoji": "🎭"
}
```

## Performance Testing

### Load Testing (Multiple Players)
```bash
# Simulate 100+ concurrent players
# Monitor:
- Response times for commands
- Memory usage
- File I/O performance
- Database size growth
```

### Long-Term Testing
```bash
# Run bot for 24+ hours
# Check:
- Memory leaks (memory should stabilize)
- File corruption (players.json should stay valid)
- Command responsiveness (should not degrade)
- Stock price consistency (should not break)
```

## Common Issues & Solutions

### Bot Doesn't Respond to Commands
```
✓ Check bot is online in Discord
✓ Check bot has message permissions
✓ Wait 1-2 minutes for command sync
✓ Restart bot
✓ Check DISCORD_TOKEN in .env
✓ Check code for errors in console
```

### Commands Are Missing
```
✓ Check "Synced X commands" message on startup
✓ Type "/" and wait for list to load
✓ Commands may be hidden if bot lacks permissions
✓ Try restarting bot
```

### Players Can't Create Accounts
```
✓ Check /setup returns character selection
✓ Check players.json is writable
✓ Verify data/ directory exists
✓ Check for errors in discord.log
```

### Economy Seems Imbalanced
```
✓ Adjust payout values in utils/jobs.py
✓ Check casino house edge math
✓ Verify job cooldowns are reasonable
✓ Test with multiple characters
✓ Collect player feedback
```

## Debugging

### Enable Verbose Logging
```python
# In main.py, change logging level:
logger.setLevel(logging.DEBUG)  # More detail
```

### Check Logs
```bash
# View recent errors
tail -f discord.log

# Search for specific error
grep "ERROR" discord.log
```

### Database Inspection
```bash
# View player data
python -c "import json; print(json.dumps(json.load(open('data/players.json')), indent=2))"

# View stock data
python -c "import json; print(json.dumps(json.load(open('data/stocks.json')), indent=2))"
```

---

**Remember**: This is MVP code. Balance values should be tuned based on actual player feedback!
