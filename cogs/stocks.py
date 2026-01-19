"""
Stock Market Commands Cog
/stocks, /stocks buy, /stocks sell, /stocks portfolio
"""

import discord
from discord.ext import commands
from discord import app_commands
from utils.economy import get_player, player_exists
from utils.stocks import (
    get_all_stocks, get_stock, buy_stock, sell_stock,
    get_portfolio_details, get_portfolio_value, get_sector_performance
)

class StockCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="stocks", description="View stock market overview")
    async def stocks_overview(self, interaction: discord.Interaction):
        """Stock market overview"""
        
        all_stocks = get_all_stocks()
        
        if not all_stocks:
            await interaction.response.send_message("No stocks available yet")
            return
        
        embed = discord.Embed(
            title="📈 Stock Market Overview",
            description="Top stocks by sector",
            color=discord.Color.green()
        )
        
        # Show top gainers and losers
        stocks_list = list(all_stocks.values())
        stocks_list.sort(key=lambda s: (s["current_price"] - s["previous_price"]) / s["previous_price"] * 100, reverse=True)
        
        gainers = stocks_list[:5]
        losers = stocks_list[-5:]
        
        gainers_text = ""
        for stock in gainers:
            change = ((stock["current_price"] - stock["previous_price"]) / stock["previous_price"] * 100)
            gainers_text += f"**{stock['ticker']}** ({stock['name']}) - ${stock['current_price']:.2f} {'+' if change > 0 else ''}{change:.2f}%\n"
        
        losers_text = ""
        for stock in losers:
            change = ((stock["current_price"] - stock["previous_price"]) / stock["previous_price"] * 100)
            losers_text += f"**{stock['ticker']}** ({stock['name']}) - ${stock['current_price']:.2f} {'+' if change > 0 else ''}{change:.2f}%\n"
        
        embed.add_field(name="🟢 Top Gainers", value=gainers_text, inline=True)
        embed.add_field(name="🔴 Top Losers", value=losers_text, inline=True)
        
        embed.set_footer(text=f"Use /stocks_info [ticker] for details")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="stocks_info", description="Get detailed info on a stock")
    @app_commands.describe(ticker="Stock ticker symbol (e.g., APPL, MSFT)")
    async def stocks_info(self, interaction: discord.Interaction, ticker: str):
        """Stock detailed info"""
        
        stock = get_stock(ticker)
        
        if not stock:
            embed = discord.Embed(
                title="❌ Stock Not Found",
                description=f"Ticker '{ticker}' does not exist",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        change = stock["current_price"] - stock["previous_price"]
        change_percent = (change / stock["previous_price"] * 100) if stock["previous_price"] > 0 else 0
        
        embed = discord.Embed(
            title=f"{stock['ticker']} - {stock['name']}",
            description=stock["description"],
            color=discord.Color.green() if change > 0 else discord.Color.red()
        )
        
        embed.add_field(name="Current Price", value=f"${stock['current_price']:.2f}", inline=True)
        embed.add_field(name="Previous Price", value=f"${stock['previous_price']:.2f}", inline=True)
        embed.add_field(name="Change", value=f"{change:+.2f} ({change_percent:+.2f}%)", inline=True)
        
        embed.add_field(name="Sector", value=stock["sector"], inline=True)
        embed.add_field(name="Volatility", value=f"{stock['volatility']*100:.1f}%", inline=True)
        
        buy_orders = stock.get("buy_orders", 0)
        sell_orders = stock.get("sell_orders", 0)
        embed.add_field(name="Activity", value=f"Buys: {buy_orders} | Sells: {sell_orders}", inline=True)
        
        embed.set_footer(text="Use /stocks_buy or /stocks_sell to trade")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="stocks_buy", description="Buy stock shares")
    @app_commands.describe(
        ticker="Stock ticker (e.g., APPL)",
        quantity="Number of shares to buy"
    )
    async def stocks_buy(self, interaction: discord.Interaction, ticker: str, quantity: int):
        """Buy stocks"""
        user_id = interaction.user.id
        
        if not player_exists(user_id):
            embed = discord.Embed(
                title="❌ No Account",
                description="Use `/setup` to create an account!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if quantity <= 0:
            await interaction.response.send_message("❌ Quantity must be greater than 0")
            return
        
        result = buy_stock(user_id, ticker, quantity)
        
        if "error" in result:
            embed = discord.Embed(
                title="❌ Purchase Failed",
                description=result["error"],
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        embed = discord.Embed(
            title="✅ Stock Purchased",
            description=result["message"],
            color=discord.Color.green()
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="stocks_sell", description="Sell stock shares")
    @app_commands.describe(
        ticker="Stock ticker (e.g., APPL)",
        quantity="Number of shares to sell"
    )
    async def stocks_sell(self, interaction: discord.Interaction, ticker: str, quantity: int):
        """Sell stocks"""
        user_id = interaction.user.id
        
        if not player_exists(user_id):
            embed = discord.Embed(
                title="❌ No Account",
                description="Use `/setup` to create an account!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if quantity <= 0:
            await interaction.response.send_message("❌ Quantity must be greater than 0")
            return
        
        result = sell_stock(user_id, ticker, quantity)
        
        if "error" in result:
            embed = discord.Embed(
                title="❌ Sale Failed",
                description=result["error"],
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        embed = discord.Embed(
            title="✅ Stock Sold",
            description=result["message"],
            color=discord.Color.green()
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="stocks_portfolio", description="View your stock portfolio")
    async def stocks_portfolio(self, interaction: discord.Interaction):
        """View portfolio"""
        user_id = interaction.user.id
        
        if not player_exists(user_id):
            embed = discord.Embed(
                title="❌ No Account",
                description="Use `/setup` to create an account!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        portfolio = get_portfolio_details(user_id)
        
        embed = discord.Embed(
            title="📊 Your Stock Portfolio",
            color=discord.Color.blue()
        )
        
        if not portfolio.get("holdings"):
            embed.description = "You don't own any stocks yet!"
            await interaction.response.send_message(embed=embed)
            return
        
        holdings_text = ""
        for holding in portfolio["holdings"]:
            holdings_text += f"**{holding['ticker']}** ({holding['name']}) - {holding['quantity']} shares @ ${holding['price']:.2f} = ${holding['value']:,}\n"
        
        embed.add_field(name="Holdings", value=holdings_text, inline=False)
        embed.add_field(name="Total Portfolio Value", value=f"💰 ${portfolio['total_value']:,}")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="stocks_sectors", description="View sector performance")
    async def stocks_sectors(self, interaction: discord.Interaction):
        """View sectors"""
        
        sectors = get_sector_performance()
        
        embed = discord.Embed(
            title="📈 Sector Performance",
            color=discord.Color.blue()
        )
        
        sorted_sectors = sorted(sectors.items(), key=lambda x: x[1]["avg_change"], reverse=True)
        
        for sector_name, data in sorted_sectors:
            change = data["avg_change"]
            emoji = "🟢" if change > 0 else "🔴"
            embed.add_field(
                name=f"{emoji} {sector_name}",
                value=f"{change:+.2f}% avg ({data['count']} stocks)",
                inline=True
            )
        
        await interaction.response.send_message(embed=embed)

# Setup function
async def setup(bot):
    await bot.add_cog(StockCommands(bot))
