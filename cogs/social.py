"""
Achievements & Social Commands Cog
/achievements, /guild, /duel, /transfer, /trade
"""

import discord
from discord.ext import commands
from discord import app_commands
from utils.economy import get_player, player_exists
from utils.achievements import ACHIEVEMENTS, check_achievement_progress, unlock_achievement
from utils.social import (
    create_guild, get_guild, get_player_guild, join_guild, 
    duel, transfer_money, trade_stocks, get_guild_leaderboard
)

class AchievementsSocialCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="achievements", description="View your achievements")
    @app_commands.describe(filter="Filter by rarity (all, common, uncommon, rare, epic, legendary)")
    async def achievements(self, interaction: discord.Interaction, filter: str = "all"):
        """View achievements"""
        user_id = interaction.user.id
        
        if not player_exists(user_id):
            embed = discord.Embed(
                title="❌ No Account",
                description="Use `/setup` to create an account!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        player = get_player(user_id)
        unlocked = set(player.get("achievements", []))
        
        # Filter achievements
        achievements_to_show = []
        for ach_id, ach_data in ACHIEVEMENTS.items():
            if filter != "all" and ach_data["rarity"] != filter:
                continue
            achievements_to_show.append((ach_id, ach_data, ach_id in unlocked))
        
        embed = discord.Embed(
            title=f"🏆 {interaction.user.name}'s Achievements",
            description=f"Unlocked: {len(unlocked)}/{len(ACHIEVEMENTS)}",
            color=discord.Color.gold()
        )
        
        # Show unlocked vs locked
        unlocked_text = ""
        locked_text = ""
        
        for ach_id, ach_data, is_unlocked in achievements_to_show[:15]:  # Show first 15
            progress = check_achievement_progress(user_id, ach_id)
            icon = ach_data.get('icon', '🏆')
            if is_unlocked:
                unlocked_text += f"{icon} **{ach_data['name']}** - {ach_data['description']}\n"
            else:
                prog = progress.get("progress", 0)
                locked_text += f"🔒 {ach_data['name']} ({prog}%) - {ach_data['points']} pts\n"
        
        if unlocked_text:
            embed.add_field(name="✅ Unlocked", value=unlocked_text, inline=False)
        if locked_text:
            embed.add_field(name="🔒 In Progress", value=locked_text, inline=False)
        
        embed.set_footer(text=f"Total Achievements: {len(ACHIEVEMENTS)} | Use filter: all/common/uncommon/rare/epic/legendary")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="guild", description="Guild management")
    @app_commands.describe(
        action="Action (create, info, members, leaderboard)",
        name="Guild name (for create)"
    )
    async def guild(self, interaction: discord.Interaction, action: str = "info", name: str = None):
        """Manage guilds"""
        user_id = interaction.user.id
        
        if not player_exists(user_id):
            embed = discord.Embed(
                title="❌ No Account",
                description="Use `/setup` to create an account!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        player = get_player(user_id)
        
        if action == "create":
            if not name:
                await interaction.response.send_message("❌ Guild name required!")
                return
            
            guild = create_guild(user_id, name)
            if not guild:
                await interaction.response.send_message("❌ Guild with that name already exists!")
                return
            
            embed = discord.Embed(
                title=f"✅ Guild Created: {name}",
                description=f"You are the owner!",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed)
        
        elif action == "info":
            user_guild = get_player_guild(user_id)
            if not user_guild:
                embed = discord.Embed(
                    title="❌ Not in a Guild",
                    description="Create or join a guild!",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed)
                return
            
            embed = discord.Embed(
                title=f"⚔️ {user_guild['name']}",
                color=discord.Color.blue()
            )
            
            embed.add_field(name="Owner", value=f"<@{user_guild['owner_id']}>", inline=True)
            embed.add_field(name="Level", value=user_guild["level"], inline=True)
            embed.add_field(name="Members", value=len(user_guild["members"]), inline=True)
            
            embed.add_field(name="Treasury", value=f"💰 ${user_guild['treasury']:,}", inline=True)
            embed.add_field(name="War Record", value=f"🏆 {user_guild['war_wins']}-{user_guild['war_losses']}", inline=True)
            
            await interaction.response.send_message(embed=embed)
        
        elif action == "members":
            user_guild = get_player_guild(user_id)
            if not user_guild:
                await interaction.response.send_message("❌ Not in a guild!")
                return
            
            embed = discord.Embed(
                title=f"⚔️ {user_guild['name']} - Members",
                color=discord.Color.blue()
            )
            
            members_text = ""
            for member in user_guild["members"][:20]:  # Show first 20
                members_text += f"• <@{member['user_id']}> ({member['role'].upper()})\n"
            
            embed.description = members_text
            await interaction.response.send_message(embed=embed)
        
        elif action == "leaderboard":
            guilds = get_guild_leaderboard("level")
            
            embed = discord.Embed(
                title="⚔️ Guild Leaderboard",
                color=discord.Color.gold()
            )
            
            leaderboard_text = ""
            for i, guild in enumerate(guilds[:10], 1):
                leaderboard_text += f"#{i} **{guild['name']}** - Level {guild['level']}, {len(guild['members'])} members\n"
            
            embed.description = leaderboard_text
            await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="duel", description="Challenge another player to a duel")
    @app_commands.describe(opponent="Player to duel")
    async def duel_command(self, interaction: discord.Interaction, opponent: discord.User):
        """Start a duel"""
        user_id = interaction.user.id
        opponent_id = opponent.id
        
        if not player_exists(user_id):
            await interaction.response.send_message("❌ Create an account first!")
            return
        
        if not player_exists(opponent_id):
            await interaction.response.send_message("❌ Opponent doesn't have an account!")
            return
        
        if user_id == opponent_id:
            await interaction.response.send_message("❌ You can't duel yourself!")
            return
        
        result = duel(user_id, opponent_id)
        
        embed = discord.Embed(
            title="⚔️ DUEL RESULT",
            description=result["message"],
            color=discord.Color.red()
        )
        
        embed.add_field(name=result["loser"], value=f"Power: {result['opponent_power' if result['winner'] != result['loser'] else 'challenger_power']}")
        embed.add_field(name=result["winner"], value=f"Power: {result['challenger_power' if result['winner'] != 'loser' else 'opponent_power']}")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="transfer", description="Send money to another player")
    @app_commands.describe(
        recipient="Player to send money to",
        amount="Amount to send"
    )
    async def transfer(self, interaction: discord.Interaction, recipient: discord.User, amount: int):
        """Transfer money"""
        user_id = interaction.user.id
        recipient_id = recipient.id
        
        if not player_exists(user_id):
            await interaction.response.send_message("❌ Create an account first!")
            return
        
        if not player_exists(recipient_id):
            await interaction.response.send_message("❌ Recipient doesn't have an account!")
            return
        
        result = transfer_money(user_id, recipient_id, amount)
        
        if "error" in result:
            embed = discord.Embed(
                title="❌ Transfer Failed",
                description=result["error"],
                color=discord.Color.red()
            )
        else:
            embed = discord.Embed(
                title="✅ Transfer Sent",
                description=result["message"],
                color=discord.Color.green()
            )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="trade", description="Trade stocks with another player")
    @app_commands.describe(
        player="Player to trade with",
        you_give="Ticker and quantity you give (e.g., APPL:5)",
        you_get="Ticker and quantity you get (e.g., MSFT:3)"
    )
    async def trade(self, interaction: discord.Interaction, player: discord.User, you_give: str, you_get: str):
        """Trade stocks"""
        user_id = interaction.user.id
        other_id = player.id
        
        if not player_exists(user_id):
            await interaction.response.send_message("❌ Create an account first!")
            return
        
        # Parse trade strings
        try:
            give_ticker, give_qty = you_give.split(":")
            get_ticker, get_qty = you_get.split(":")
            give_qty, get_qty = int(give_qty), int(get_qty)
        except:
            await interaction.response.send_message("❌ Invalid format! Use TICKER:qty")
            return
        
        result = trade_stocks(user_id, other_id, give_ticker.upper(), give_qty, get_ticker.upper(), get_qty)
        
        if "error" in result:
            embed = discord.Embed(
                title="❌ Trade Failed",
                description=result["error"],
                color=discord.Color.red()
            )
        else:
            embed = discord.Embed(
                title="✅ Trade Complete",
                description=result["message"],
                color=discord.Color.green()
            )
        
        await interaction.response.send_message(embed=embed)

# Setup function
async def setup(bot):
    await bot.add_cog(AchievementsSocialCommands(bot))
