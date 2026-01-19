# Deployment Guide - Game of Wall Street

## Quick Start (5 minutes)

### 1. Create Discord Bot
1. Go to https://discord.com/developers/applications
2. Click "New Application" → Name it "Game of Wall Street"
3. Go to "Bot" tab → Click "Add Bot"
4. Under TOKEN, click "Copy"
5. Create `.env` file in bot directory:
```
DISCORD_TOKEN=your_token_here
```

### 2. Set Bot Permissions
1. In Discord Developer Portal, go to OAuth2 → URL Generator
2. Select scopes: `bot`
3. Select permissions:
   - [x] Send Messages
   - [x] Embed Links
   - [x] Read Message History
   - [x] Use Slash Commands
4. Copy generated URL and open in browser
5. Select server and authorize

### 3. Install & Run
```bash
# Install dependencies
pip install -r requirements.txt

# Run bot
python main.py
```

Expected output:
```
✅ Bot logged in as Game of Wall Street#1234
✅ Synced 23 command(s)
```

## Production Deployment

### Option 1: Local Server (Always-On PC)
```bash
# Install Python 3.8+
# Install dependencies
pip install -r requirements.txt

# Run in background (Windows)
pythonw main.py

# Or use systemd (Linux)
# Create game-of-wall-street.service in /etc/systemd/system/
```

### Option 2: Cloud Hosting (Recommended)

#### Heroku (Free tier available)
```bash
# Login to Heroku
heroku login

# Create Procfile
echo "worker: python main.py" > Procfile

# Deploy
git push heroku main

# Set environment variable
heroku config:set DISCORD_TOKEN=your_token
```

#### Railway.app (Simple)
1. Connect GitHub repository
2. Add DISCORD_TOKEN as environment variable
3. Deploy

#### Google Cloud / AWS / DigitalOcean
- Standard Python app deployment
- Set DISCORD_TOKEN in environment
- Run `python main.py`

### Option 3: Docker
```bash
# Build image
docker build -t game-of-wall-street .

# Run container
docker run -e DISCORD_TOKEN=your_token game-of-wall-street
```

Create `Dockerfile`:
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

## Scaling for Multiple Servers

### Enable Bot in Multiple Servers
1. Generate new invite URL with same permissions
2. Share with server administrators
3. Bot will work across all servers automatically

### Database Migration (When You Have 1000+ Players)
Currently uses JSON files. To migrate to MongoDB:

```python
# In utils/economy.py, replace file operations with:
from pymongo import MongoClient

client = MongoClient("mongodb://...")
db = client["game_of_wall_street"]
players = db["players"]

def get_player(user_id):
    return players.find_one({"_id": user_id})

def update_player(user_id, data):
    players.update_one({"_id": user_id}, {"$set": data})
```

Install: `pip install pymongo`

## Monitoring & Maintenance

### Check Bot Status
```bash
# View logs
tail -f discord.log

# Check if running
ps aux | grep python

# Check memory usage
top
```

### Restart Bot
```bash
# Stop current process
pkill -f main.py

# Start again
python main.py
```

### Backup Data
```bash
# Backup all player data daily
cp -r data/ backups/data_$(date +%Y%m%d)/

# Or use cloud backup service
```

### Performance Monitoring
```bash
# Monitor in real-time
watch -n 1 'wc -l data/*.json'

# Check file sizes
du -sh data/

# Verify JSON validity
python -m json.tool data/players.json > /dev/null
```

## Troubleshooting Deployment

### Bot Not Responding
```
1. Check bot is online in Discord
2. Verify .env file has correct token
3. Check firewall allows Python
4. Restart bot and wait 30 seconds for sync
```

### Commands Not Showing
```
1. Wait 1-2 minutes after startup
2. Check "Synced X commands" in logs
3. Try typing "/" in Discord - should show list
4. Restart bot if needed
```

### Players Can't Create Accounts
```
1. Verify data/ directory exists
2. Check file permissions (chmod 755 data/)
3. Verify players.json is valid JSON
4. Check disk space available
```

### Out of Memory
```
1. Check number of players: wc -l data/players.json
2. Monitor with: top -p $(pgrep -f main.py)
3. If >10000 players, migrate to MongoDB
4. Restart bot to clear memory
```

### Commands Timing Out
```
1. Check if API calls are slow
2. Verify internet connection
3. Check Discord API status: discordstatus.com
4. Increase command timeout if needed
```

## Environment Variables

Create `.env` file:
```
# Required
DISCORD_TOKEN=your_bot_token

# Optional (coming soon)
# DATABASE_URL=mongodb://...
# LOG_LEVEL=INFO
# STOCK_API_KEY=...
```

## Security Best Practices

✅ DO:
- Keep .env file in .gitignore
- Use strong bot token (rotate if leaked)
- Backup data regularly
- Monitor for unusual activity
- Update discord.py regularly (`pip install --upgrade discord.py`)

❌ DON'T:
- Commit .env to GitHub
- Share bot token publicly
- Give admin role to bot in server
- Delete data/ folder in production

## Feature Flags (Enable/Disable Features)

In `main.py`:
```python
# Toggle features
ENABLE_CASINO = True
ENABLE_STOCKS = True
ENABLE_ACHIEVEMENTS = True
ENABLE_SOCIAL = True

# Then check before loading cog:
if ENABLE_CASINO:
    await bot.load_extension('cogs.casino')
```

## Support & Debugging

### Enable Debug Mode
```python
# In main.py
logger.setLevel(logging.DEBUG)
```

### Get Detailed Error Messages
```bash
python -u main.py 2>&1 | tee bot.log
```

### Contact Discord Support
- API Issues: https://discord.com/developers/docs
- Rate Limited? Check docs for limits
- Bot Suspended? Check Terms of Service

---

**Deployment successful when:**
- ✅ Bot appears online in Discord
- ✅ `/help` command works
- ✅ `/setup` shows character selection
- ✅ New players can create accounts
- ✅ Commands respond within 1-3 seconds
