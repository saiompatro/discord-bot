# Quick Start Guide - Game of Wall Street

## Setup in 5 Minutes

### Step 1: Get Your Bot Token
1. Go to https://discord.com/developers/applications
2. Click "New Application" → Name it "Game of Wall Street"
3. Go to "Bot" tab → Click "Add Bot"
4. Under TOKEN, click "Copy"
5. Paste into `.env` file as `DISCORD_TOKEN=your_token_here`

### Step 2: Bot Permissions
1. Go to OAuth2 → URL Generator
2. Select scopes: `bot`
3. Select permissions:
   - Send Messages
   - Send Messages in Threads
   - Embed Links
   - Attach Files
   - Read Message History
4. Copy the generated URL and open it in browser
5. Select your test server and authorize

### Step 3: Install & Run
```bash
# Install dependencies
pip install -r requirements.txt

# Run the bot
python main.py
```

Look for: `✅ Bot logged in as YourBotName#1234`

### Step 4: First Test
In your Discord server, type:
```
/help
```

You should see the help menu!

## First Player Experience

### 1. Create Account
```
/setup
```
- Choose a character
- Get starting money based on character
- Ready to play!

### 2. Check Profile
```
/profile
```
- See your character
- View your stats
- Check your money

### 3. Earn Money
**Option A: Work a Job**
```
/work_list         # See available jobs
/work street_vendor   # Start working
```
- Every job has a cooldown
- Stats affect payout and success rate
- Better jobs at higher levels

**Option B: Try Casino**
```
/casino            # See games
/casino_play coinflip 100 heads   # Bet $100 on heads
```
- Different games have different house edges
- Luck stat affects odds
- Can win big or lose quick

**Option C: Trade Stocks**
```
/stocks            # Market overview
/stocks_buy APPL 5    # Buy 5 shares of Apple
/stocks_portfolio     # See what you own
```
- Stocks fluctuate in price
- Long-term wealth building
- Sell when price is high!

### 4. Level Up
Doing any activity earns XP:
- Jobs: 10-100 XP
- Casino wins: 5-25 XP  
- Stock trades: 1 XP per $1000 profit
- Achievements: 50-500 XP

New jobs unlock at each level!

## Gameplay Tips

### Early Game (Levels 1-15)
- Focus on jobs (most reliable income)
- Do your daily bonus every day
- Save money for stock investments
- Casino is risky early on

### Mid Game (Levels 15-50)
- Unlock tier 2 and 3 jobs
- Start building stock portfolio
- Use casino for occasional gambling
- Build your reputation

### Late Game (Levels 50+)
- CEO and hedge fund jobs available
- Large casino bets
- Complex stock strategies
- Prestige option at level 50 (resets level for cosmetics)

## Common Issues

**Bot doesn't respond**
- Check it's online in your server
- Make sure it has message permissions
- Try `/help` to test

**Commands don't show up**
- Wait 1-2 minutes for Discord to sync
- Try typing `/` and wait for command list to load
- Restart bot if commands still don't appear

**Can't create account**
- Make sure you're using `/setup` not `/create`
- Each Discord user can only have one account
- Use `/profile` to check existing account

**Lost money/account issue**
- Data is auto-saved to `data/players.json`
- If something went wrong, file won't be deleted
- Contact server admin for help

## Stats Explained

Each character has 6 stats (1-5 stars):

| Stat | Affects | Best For |
|------|---------|----------|
| **Intellect** | Job success, stock trading | Analyst, lawyer jobs |
| **Humour** | Charisma, some job payouts | Sales, entertainment |
| **Strength** | Physical jobs payouts | Construction, security |
| **Leadership** | Management job bonuses | CEO, manager roles |
| **Mental Health** | Stress resistance, streak bonus | Long grinding sessions |
| **Wealth** | Casino odds, luck | Gambling games |

**Strategy**: Different characters excel at different things. Pick one that matches your playstyle!

## Money Management

- **Cash**: Liquid money you carry (used for gambling, job prep)
- **Bank**: Saved money (earning interest, safe from spending)
- **Net Worth**: Cash + Bank + Stock portfolio value

**Tips:**
- Keep emergency fund in bank (2-3 days income)
- Invest excess in stocks
- Don't gamble more than 10% of cash
- Jobs are most stable income

## Next Steps

1. ✅ Create account with `/setup`
2. ✅ Work some jobs with `/work`
3. ✅ Check leaderboards with `/leaderboard`
4. ✅ Try casino (but gamble responsibly!)
5. ✅ Read `/help` for full command list

## Command Cheat Sheet

| What | Command |
|------|---------|
| Create account | `/setup` |
| View profile | `/profile` |
| Check balance | `/balance` |
| Daily bonus | `/daily` |
| Work a job | `/work` |
| See available jobs | `/work_list` |
| Play casino game | `/casino_play` |
| View holdings | `/stocks_portfolio` |
| Buy stock | `/stocks_buy TICKER 5` |
| See leaderboard | `/leaderboard` |
| Get help | `/help` |

## Have Fun! 🎮

This game is designed to be:
- **Engaging**: Multiple paths to make money
- **Strategic**: Choices matter (character, job, investments)
- **Fair**: No pay-to-win (cosmetics only later)
- **Rewarding**: Progress feels meaningful

Good luck on Wall Street! 📈
