"""
Casino & Gambling Commands Cog
/casino play, /casino stats, /casino leaderboard
"""

import discord
from discord.ext import commands
from discord import app_commands
from utils.economy import get_player, player_exists
from utils.casino import gamble, get_available_games

class CasinoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="casino", description="View casino information")
    async def casino_menu(self, interaction: discord.Interaction):
        """Casino main menu"""
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
        
        embed = discord.Embed(
            title="🎰 Welcome to GWS Casino",
            description="Bet your money in thrilling games!",
            color=discord.Color.purple()
        )
        
        games = get_available_games()
        games_text = ""
        for game_id, game_info in games.items():
            games_text += f"{game_info}\n"
        
        embed.add_field(name="Available Games", value=games_text, inline=False)
        
        embed.add_field(name="Your Balance", value=f"💵 ${player['cash']:,}", inline=True)
        embed.add_field(name="VIP Tier", value=player.get('casino_vip_tier', 'None'), inline=True)
        embed.add_field(name="Loyalty Points", value=f"🎫 {player.get('loyalty_points', 0)}", inline=True)
        
        embed.add_field(
            name="How to Play",
            value="Use `/casino_play [game] [bet] [options]`\nExample: `/casino_play coinflip 100 heads`",
            inline=False
        )
        
        embed.set_footer(text="⚠️ Gamble responsibly! Use /casino_limit to set spending limits.")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="casino_play", description="Play a casino game")
    @app_commands.describe(
        game="Game to play (coinflip, slots, roulette, dice, blackjack)",
        bet="Amount to bet (min $5, max $20,000)",
        choice="Your choice (heads/tails for coinflip, higher/lower for dice, etc)"
    )
    async def casino_play(self, interaction: discord.Interaction, game: str, bet: int, choice: str = None):
        """Play a casino game"""
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
        
        # Gamble
        kwargs = {}
        if choice:
            if game.lower() in ["coinflip", "dice"]:
                kwargs["prediction"] = choice.lower()
            elif game.lower() == "roulette":
                kwargs["bet_type"] = choice.lower()
        
        result = gamble(user_id, game.lower(), bet, **kwargs)
        
        if "error" in result:
            embed = discord.Embed(
                title="❌ Error",
                description=result["error"],
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        # Show result
        embed = discord.Embed(
            title=f"🎰 {game.upper()}",
            description=result.get("message", "Game played!"),
            color=discord.Color.gold() if result.get("success") else discord.Color.red()
        )
        
        if result.get("success"):
            embed.add_field(name="💰 Winnings", value=f"${result['payout']:,}", inline=True)
        else:
            embed.add_field(name="💸 Lost", value=f"${result.get('lost', bet):,}", inline=True)
        
        # Updated stats
        updated_player = get_player(user_id)
        embed.add_field(name="Balance", value=f"${updated_player['cash']:,}", inline=True)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="casino_stats", description="View your casino statistics")
    async def casino_stats(self, interaction: discord.Interaction):
        """View casino stats"""
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
        
        wagered = player.get("casino_wagered", 0)
        won = player.get("casino_won", 0)
        lost = player.get("casino_lost", 0)
        
        embed = discord.Embed(
            title=f"🎰 {interaction.user.name}'s Casino Stats",
            color=discord.Color.purple()
        )
        
        embed.add_field(name="Total Wagered", value=f"💵 ${wagered:,}", inline=True)
        embed.add_field(name="Total Won", value=f"💰 ${won:,}", inline=True)
        embed.add_field(name="Total Lost", value=f"💸 ${lost:,}", inline=True)
        
        if wagered > 0:
            net = won - lost
            embed.add_field(name="Net Result", value=f"{'✅' if net > 0 else '❌'} ${net:,}", inline=True)
            roi = ((net / wagered) * 100)
            embed.add_field(name="ROI", value=f"{roi:.1f}%", inline=True)
        
        embed.add_field(name="VIP Tier", value=player.get("casino_vip_tier", "None"), inline=True)
        embed.add_field(name="Loyalty Points", value=f"🎫 {player.get('loyalty_points', 0)}", inline=True)
        
        embed.add_field(name="Win Streak", value=f"🔥 {player.get('casino_win_streak', 0)}", inline=True)
        embed.add_field(name="Loss Streak", value=f"❄️ {player.get('casino_loss_streak', 0)}", inline=True)
        
        embed.set_footer(text="Play responsibly!")
        
        await interaction.response.send_message(embed=embed)

# Setup function
async def setup(bot):
    await bot.add_cog(CasinoCommands(bot))
