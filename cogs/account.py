"""
Core Account Commands Cog
/profile, /balance, /help, /daily, /setup
"""

import discord
from discord.ext import commands
from discord import app_commands
from utils.economy import (
    create_player, get_player, player_exists, get_net_worth,
    get_player_stats_summary, claim_daily_bonus, get_leaderboard,
    get_available_character, mark_character_used
)
from data.characters import get_all_characters, get_character
import random

class AccountCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="setup", description="Create your Game of Wall Street account")
    async def setup(self, interaction: discord.Interaction):
        """Setup command - creates new player account with random character"""
        user_id = interaction.user.id
        
        if player_exists(user_id):
            embed = discord.Embed(
                title="❌ Account Already Exists",
                description="You already have a Game of Wall Street account!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        # Get available character (random assignment, no duplicates)
        available_char = get_available_character()
        
        if not available_char:
            embed = discord.Embed(
                title="❌ No Characters Available",
                description="All 30 characters have been assigned! The game is full.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        # Get character details
        char = get_character(available_char)
        
        # Create player with randomly assigned character
        player = create_player(
            user_id,
            interaction.user.name,
            available_char,
            char['starting_cash'],
            char['starting_bank'],
            char['stats']
        )
        
        if not player:
            embed = discord.Embed(
                title="❌ Account Creation Failed",
                description="An error occurred while creating your account.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        # Mark character as used
        mark_character_used(available_char)
        
        # Show confirmation with assigned character
        embed = discord.Embed(
            title="🎮 Welcome to Game of Wall Street!",
            description=f"Your character has been randomly assigned!",
            color=discord.Color.gold()
        )
        
        stats_str = f"💡 Intellect: {char['stats']['intellect']}⭐\n😄 Humour: {char['stats']['humour']}⭐\n💪 Strength: {char['stats']['strength']}⭐\n👔 Leadership: {char['stats']['leadership']}⭐\n🧠 Mental Health: {char['stats']['mental_health']}⭐\n💰 Wealth: {char['stats']['wealth']}⭐"
        
        embed.add_field(
            name=f"{char['bio_emoji']} {available_char}",
            value=char['title'],
            inline=False
        )
        
        embed.add_field(
            name="📊 Your Stats",
            value=stats_str,
            inline=False
        )
        
        embed.add_field(
            name="💰 Starting Money",
            value=f"Cash: ${char['starting_cash']:,}\nBank: ${char['starting_bank']:,}",
            inline=False
        )
        
        embed.add_field(
            name="📖 Background",
            value=char['background'],
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="profile", description="View your player profile")
    async def profile(self, interaction: discord.Interaction):
        """View player profile"""
        user_id = interaction.user.id
        
        if not player_exists(user_id):
            embed = discord.Embed(
                title="❌ No Account Found",
                description="Use `/setup` to create an account!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        stats = get_player_stats_summary(user_id)
        player = get_player(user_id)
        
        embed = discord.Embed(
            title=f"💼 {stats['username']}'s Profile",
            description=f"**{player['character_title']}** (Character: {stats['character']})",
            color=discord.Color.blurple()
        )
        
        embed.add_field(name="Level", value=f"🎯 {stats['level']}", inline=True)
        embed.add_field(name="XP", value=f"📊 {stats['experience']:,}", inline=True)
        embed.add_field(name="Reputation", value=f"⭐ {stats['reputation']}", inline=True)
        
        embed.add_field(name="Cash", value=f"💵 ${stats['cash']:,}", inline=True)
        embed.add_field(name="Bank", value=f"🏦 ${stats['bank']:,}", inline=True)
        embed.add_field(name="Net Worth", value=f"💰 ${stats['net_worth']:,}", inline=True)
        
        # Stats as stars
        stats_text = ""
        for stat_name, stat_value in stats['stats'].items():
            stars = "⭐" * stat_value + "☆" * (5 - stat_value)
            stat_display = stat_name.replace("_", " ").title()
            stats_text += f"**{stat_display}**: {stars} ({stat_value}/5)\n"
        
        embed.add_field(name="📈 Character Stats", value=stats_text, inline=False)
        
        embed.add_field(name="Job Streak", value=f"🔥 {stats['job_streak']}", inline=True)
        embed.add_field(name="Login Streak", value=f"📅 {stats['login_streak']}", inline=True)
        
        embed.set_footer(text=f"Account created {player['created_at'][:10]}")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="balance", description="Check your current balance")
    async def balance(self, interaction: discord.Interaction):
        """Quick balance check"""
        user_id = interaction.user.id
        
        if not player_exists(user_id):
            embed = discord.Embed(
                title="❌ No Account Found",
                description="Use `/setup` to create an account!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        player = get_player(user_id)
        
        embed = discord.Embed(
            title=f"💵 {interaction.user.name}'s Balance",
            color=discord.Color.green()
        )
        
        embed.add_field(name="Cash", value=f"💵 ${player['cash']:,}", inline=True)
        embed.add_field(name="Bank", value=f"🏦 ${player['bank_balance']:,}", inline=True)
        embed.add_field(name="Net Worth", value=f"💰 ${get_net_worth(user_id):,}", inline=True)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="daily", description="Claim your daily login bonus")
    async def daily(self, interaction: discord.Interaction):
        """Claim daily bonus"""
        user_id = interaction.user.id
        
        if not player_exists(user_id):
            embed = discord.Embed(
                title="❌ No Account Found",
                description="Use `/setup` to create an account!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        result = claim_daily_bonus(user_id)
        
        if result["claimed"]:
            embed = discord.Embed(
                title="✅ Daily Bonus Claimed!",
                description=f"You earned **${result['bonus']}**!",
                color=discord.Color.gold()
            )
            embed.add_field(name="Streak", value=f"🔥 {result['new_streak']} days")
            embed.add_field(name="Next Bonus", value=result['next_claim'][:10])
        else:
            embed = discord.Embed(
                title="❌ Already Claimed Today",
                description=f"You already claimed today! Try again tomorrow.",
                color=discord.Color.red()
            )
            embed.add_field(name="Next Claim", value=result['next_claim'][:10])
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="leaderboard", description="View top players")
    @app_commands.describe(sort_by="What to sort by", limit="How many to show (max 25)")
    async def leaderboard(self, interaction: discord.Interaction, sort_by: str = "net_worth", limit: int = 10):
        """View leaderboards"""
        
        limit = min(limit, 25)  # Cap at 25
        leaderboard = get_leaderboard(sort_by, limit)
        
        embed = discord.Embed(
            title=f"🏆 {sort_by.replace('_', ' ').title()} Leaderboard",
            color=discord.Color.gold()
        )
        
        if not leaderboard:
            embed.description = "No players yet!"
        else:
            rank_text = ""
            for i, player in enumerate(leaderboard, 1):
                if sort_by == "net_worth":
                    value = f"${get_net_worth(int(player['user_id'])):,}"
                elif sort_by == "level":
                    value = f"Level {player['level']}"
                elif sort_by == "casino_winnings":
                    value = f"${player.get('casino_won', 0):,}"
                elif sort_by == "job_earnings":
                    value = f"${player.get('job_earnings', 0):,}"
                else:
                    value = "N/A"
                
                medal = ["🥇", "🥈", "🥉"][i-1] if i <= 3 else f"#{i}"
                rank_text += f"{medal} **{player['username']}** - {value}\n"
            
            embed.description = rank_text
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="help", description="View available commands")
    async def help_command(self, interaction: discord.Interaction):
        """Show help menu"""
        
        embed = discord.Embed(
            title="📚 Game of Wall Street - Help Menu",
            description="Commands for playing GWS",
            color=discord.Color.blurple()
        )
        
        embed.add_field(
            name="🎮 Getting Started",
            value="/setup - Create your account\n/profile - View your profile\n/balance - Check your balance\n/daily - Claim daily bonus",
            inline=False
        )
        
        embed.add_field(
            name="💼 Jobs & Work",
            value="/work - Work a job\n/work list - See available jobs\n/work info [job] - Job details",
            inline=False
        )
        
        embed.add_field(
            name="🎰 Casino",
            value="/casino - View casino games\n/casino play [game] [bet] - Play a game\n/casino stats - Your casino stats",
            inline=False
        )
        
        embed.add_field(
            name="📈 Stocks",
            value="/stocks - View market overview\n/stocks buy [ticker] [amount] - Buy stock\n/stocks portfolio - View holdings",
            inline=False
        )
        
        embed.add_field(
            name="🏆 Social",
            value="/leaderboard - View rankings\n/achievements - View achievements",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)

# Setup function
async def setup(bot):
    await bot.add_cog(AccountCommands(bot))
