import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Setup logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Bot intents and setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)

# Load cogs
async def load_cogs():
    """Load all command cogs"""
    cogs = [
        'cogs.account',
        'cogs.jobs',
        'cogs.casino',
        'cogs.stocks',
        'cogs.social',
    ]
    
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            logger.info(f"✅ Loaded {cog}")
        except Exception as e:
            logger.error(f"❌ Failed to load {cog}: {e}")

@bot.event
async def on_ready():
    """Bot is ready"""
    logger.info(f"✅ Bot logged in as {bot.user}")
    print(f"✅ Bot logged in as {bot.user}")
    
    try:
        synced = await bot.tree.sync()
        logger.info(f"✅ Synced {len(synced)} command(s)")
        print(f"✅ Synced {len(synced)} command(s)")
    except Exception as e:
        logger.error(f"❌ Failed to sync commands: {e}")

async def main():
    """Main function"""
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())

