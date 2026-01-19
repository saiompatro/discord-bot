"""
Stock Market System
Real-time stock trading with price movements
"""

import random
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, List

STOCK_DB_PATH = "data/stocks.json"
MARKET_DB_PATH = "data/market.json"

# Initial stocks
INITIAL_STOCKS = {
    "APPL": {
        "name": "Apple Corp",
        "sector": "Technology",
        "starting_price": 150.00,
        "volatility": 0.08,  # 8% daily volatility
        "description": "Leading tech company"
    },
    "MSFT": {
        "name": "Microsoft Corp",
        "sector": "Technology",
        "starting_price": 330.00,
        "volatility": 0.07,
        "description": "Software and cloud services"
    },
    "GOOG": {
        "name": "Google Corp",
        "sector": "Technology",
        "starting_price": 135.00,
        "volatility": 0.07,
        "description": "Search and advertising giant"
    },
    "TSLA": {
        "name": "Tesla Inc",
        "sector": "Automotive",
        "starting_price": 250.00,
        "volatility": 0.15,  # High volatility
        "description": "Electric vehicles and energy"
    },
    "JPM": {
        "name": "JP Morgan Chase",
        "sector": "Finance",
        "starting_price": 165.00,
        "volatility": 0.06,  # Low volatility
        "description": "Investment banking and finance"
    },
    "GS": {
        "name": "Goldman Sachs",
        "sector": "Finance",
        "starting_price": 380.00,
        "volatility": 0.07,
        "description": "Investment bank"
    },
    "BRK": {
        "name": "Berkshire Hathaway",
        "sector": "Finance",
        "starting_price": 420.00,
        "volatility": 0.05,  # Very low volatility
        "description": "Holding company and investments"
    },
    "AMD": {
        "name": "Advanced Micro Devices",
        "sector": "Semiconductors",
        "starting_price": 165.00,
        "volatility": 0.12,
        "description": "Chip manufacturer"
    },
    "NVDA": {
        "name": "NVIDIA Corp",
        "sector": "Semiconductors",
        "starting_price": 890.00,
        "volatility": 0.14,
        "description": "GPU and AI chips"
    },
    "AMZ": {
        "name": "Amazon Inc",
        "sector": "Technology",
        "starting_price": 168.00,
        "volatility": 0.09,
        "description": "E-commerce and cloud"
    },
    "META": {
        "name": "Meta Platforms",
        "sector": "Technology",
        "starting_price": 450.00,
        "volatility": 0.13,
        "description": "Social media and metaverse"
    },
    "NFLX": {
        "name": "Netflix Inc",
        "sector": "Entertainment",
        "starting_price": 420.00,
        "volatility": 0.11,
        "description": "Streaming entertainment"
    },
    "SPOT": {
        "name": "Spotify",
        "sector": "Entertainment",
        "starting_price": 250.00,
        "volatility": 0.12,
        "description": "Music streaming"
    },
    "UBER": {
        "name": "Uber Technologies",
        "sector": "Transportation",
        "starting_price": 72.00,
        "volatility": 0.10,
        "description": "Ride-sharing and delivery"
    },
    "COIN": {
        "name": "Coinbase",
        "sector": "Cryptocurrency",
        "starting_price": 165.00,
        "volatility": 0.20,  # Very high volatility
        "description": "Crypto exchange"
    },
    "SNAP": {
        "name": "Snap Inc",
        "sector": "Technology",
        "starting_price": 12.50,
        "volatility": 0.14,
        "description": "Social messaging app"
    },
    "PLTR": {
        "name": "Palantir Technologies",
        "sector": "Technology",
        "starting_price": 28.00,
        "volatility": 0.12,
        "description": "Data analytics"
    },
    "RIOT": {
        "name": "Riot Platforms",
        "sector": "Cryptocurrency",
        "starting_price": 15.00,
        "volatility": 0.25,  # Extreme volatility
        "description": "Bitcoin mining"
    },
    "SQ": {
        "name": "Square Inc",
        "sector": "Finance",
        "starting_price": 98.00,
        "volatility": 0.11,
        "description": "Payment processing"
    },
    "RBLX": {
        "name": "Roblox Corp",
        "sector": "Gaming",
        "starting_price": 32.00,
        "volatility": 0.13,
        "description": "Online gaming platform"
    },
}

def ensure_market_db():
    """Create stock database if it doesn't exist"""
    os.makedirs("data", exist_ok=True)
    
    if not os.path.exists(STOCK_DB_PATH):
        stocks = {}
        for ticker, info in INITIAL_STOCKS.items():
            stocks[ticker] = {
                "ticker": ticker,
                "name": info["name"],
                "sector": info["sector"],
                "description": info["description"],
                "current_price": info["starting_price"],
                "previous_price": info["starting_price"],
                "volatility": info["volatility"],
                "last_update": datetime.now().isoformat(),
                "price_history": [info["starting_price"]],
                "buy_orders": 0,
                "sell_orders": 0,
            }
        
        with open(STOCK_DB_PATH, 'w') as f:
            json.dump(stocks, f, indent=2)

def load_stocks():
    """Load stock data"""
    ensure_market_db()
    try:
        with open(STOCK_DB_PATH, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_stocks(stocks):
    """Save stock data"""
    with open(STOCK_DB_PATH, 'w') as f:
        json.dump(stocks, f, indent=2)

def get_stock(ticker: str) -> Optional[Dict]:
    """Get stock data"""
    stocks = load_stocks()
    return stocks.get(ticker.upper())

def get_all_stocks() -> Dict:
    """Get all stocks"""
    return load_stocks()

def update_stock_price(ticker: str):
    """Update stock price with random walk"""
    stocks = load_stocks()
    stock = stocks.get(ticker.upper())
    
    if not stock:
        return
    
    # Random walk: ±volatility%
    change_percent = random.uniform(-stock["volatility"], stock["volatility"])
    price_change = stock["current_price"] * change_percent
    new_price = max(stock["current_price"] + price_change, 1.0)  # Don't go below $1
    
    stock["previous_price"] = stock["current_price"]
    stock["current_price"] = new_price
    stock["last_update"] = datetime.now().isoformat()
    stock["price_history"].append(new_price)
    
    # Keep only last 100 prices
    if len(stock["price_history"]) > 100:
        stock["price_history"] = stock["price_history"][-100:]
    
    save_stocks(stocks)

def update_all_stocks():
    """Update all stock prices"""
    stocks = load_stocks()
    for ticker in stocks.keys():
        update_stock_price(ticker)

def buy_stock(user_id: int, ticker: str, quantity: int) -> Dict:
    """Buy stock shares"""
    from utils.economy import get_player, remove_money, update_player
    
    ticker = ticker.upper()
    stock = get_stock(ticker)
    
    if not stock:
        return {"error": "Stock not found"}
    
    player = get_player(user_id)
    if not player:
        return {"error": "Player not found"}
    
    cost = int(stock["current_price"] * quantity)
    
    if player["cash"] < cost:
        return {"error": f"Insufficient funds. Need ${cost}, have ${player['cash']}"}
    
    # Remove money
    remove_money(user_id, cost, source="stock")
    
    # Add to portfolio
    portfolio = player.get("portfolio", {})
    if ticker in portfolio:
        portfolio[ticker] += quantity
    else:
        portfolio[ticker] = quantity
    
    update_player(user_id, {"portfolio": portfolio})
    
    return {
        "success": True,
        "ticker": ticker,
        "quantity": quantity,
        "price_per_share": stock["current_price"],
        "total_cost": cost,
        "message": f"✅ Bought {quantity} shares of {stock['name']} at ${stock['current_price']:.2f} each for ${cost:,}"
    }

def sell_stock(user_id: int, ticker: str, quantity: int) -> Dict:
    """Sell stock shares"""
    from utils.economy import get_player, add_money, update_player
    
    ticker = ticker.upper()
    stock = get_stock(ticker)
    
    if not stock:
        return {"error": "Stock not found"}
    
    player = get_player(user_id)
    if not player:
        return {"error": "Player not found"}
    
    portfolio = player.get("portfolio", {})
    
    if ticker not in portfolio or portfolio[ticker] < quantity:
        owned = portfolio.get(ticker, 0)
        return {"error": f"You don't own enough shares. You own {owned}, trying to sell {quantity}"}
    
    revenue = int(stock["current_price"] * quantity)
    
    # Remove from portfolio
    portfolio[ticker] -= quantity
    if portfolio[ticker] == 0:
        del portfolio[ticker]
    
    # Add money
    add_money(user_id, revenue, source="stock")
    
    update_player(user_id, {"portfolio": portfolio})
    
    return {
        "success": True,
        "ticker": ticker,
        "quantity": quantity,
        "price_per_share": stock["current_price"],
        "total_revenue": revenue,
        "message": f"✅ Sold {quantity} shares of {stock['name']} at ${stock['current_price']:.2f} each for ${revenue:,}"
    }

def get_portfolio_value(user_id: int) -> int:
    """Get total portfolio value"""
    from utils.economy import get_player
    
    player = get_player(user_id)
    if not player:
        return 0
    
    portfolio = player.get("portfolio", {})
    total = 0
    
    for ticker, quantity in portfolio.items():
        stock = get_stock(ticker)
        if stock:
            total += int(stock["current_price"] * quantity)
    
    return total

def get_portfolio_details(user_id: int) -> Dict:
    """Get detailed portfolio info"""
    from utils.economy import get_player
    
    player = get_player(user_id)
    if not player:
        return {}
    
    portfolio = player.get("portfolio", {})
    details = []
    total_value = 0
    total_cost = 0
    
    for ticker, quantity in portfolio.items():
        stock = get_stock(ticker)
        if stock:
            current_value = int(stock["current_price"] * quantity)
            # We don't track original purchase price in MVP, so assume average
            estimated_cost = current_value
            details.append({
                "ticker": ticker,
                "name": stock["name"],
                "quantity": quantity,
                "price": stock["current_price"],
                "value": current_value
            })
            total_value += current_value
    
    return {
        "holdings": details,
        "total_value": total_value,
        "count": len(details)
    }

def get_sector_performance() -> Dict:
    """Get performance by sector"""
    stocks = load_stocks()
    sectors = {}
    
    for ticker, stock in stocks.items():
        sector = stock["sector"]
        if sector not in sectors:
            sectors[sector] = {
                "stocks": [],
                "avg_change": 0,
                "count": 0
            }
        
        change_percent = ((stock["current_price"] - stock["previous_price"]) / stock["previous_price"] * 100) if stock["previous_price"] > 0 else 0
        sectors[sector]["stocks"].append({"ticker": ticker, "change": change_percent})
        sectors[sector]["count"] += 1
    
    # Calculate averages
    for sector in sectors:
        avg = sum(s["change"] for s in sectors[sector]["stocks"]) / sectors[sector]["count"]
        sectors[sector]["avg_change"] = avg
    
    return sectors
