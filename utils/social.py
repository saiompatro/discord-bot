"""
Social Features System
Guilds, duels, and trading between players
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, List

GUILD_DB_PATH = "data/guilds.json"

def ensure_guild_db():
    """Create guild database if it doesn't exist"""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(GUILD_DB_PATH):
        with open(GUILD_DB_PATH, 'w') as f:
            json.dump({}, f)

def load_guilds():
    """Load all guilds"""
    ensure_guild_db()
    try:
        with open(GUILD_DB_PATH, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_guilds(data):
    """Save guilds to disk"""
    with open(GUILD_DB_PATH, 'w') as f:
        json.dump(data, f, indent=2)

def create_guild(user_id: int, guild_name: str) -> Optional[Dict]:
    """Create a new guild"""
    guilds = load_guilds()
    
    # Check if guild already exists
    if any(g["name"].lower() == guild_name.lower() for g in guilds.values()):
        return None  # Guild already exists
    
    guild_id = str(len(guilds) + 1)
    
    guild_data = {
        "id": guild_id,
        "name": guild_name,
        "owner_id": user_id,
        "created_at": datetime.now().isoformat(),
        "members": [{
            "user_id": user_id,
            "role": "owner",
            "join_date": datetime.now().isoformat()
        }],
        "treasury": 0,  # Shared money pool
        "level": 1,
        "experience": 0,
        "war_wins": 0,
        "war_losses": 0,
        "perks": []
    }
    
    guilds[guild_id] = guild_data
    save_guilds(guilds)
    
    return guild_data

def get_guild(guild_id: str) -> Optional[Dict]:
    """Get guild data"""
    guilds = load_guilds()
    return guilds.get(guild_id)

def get_player_guild(user_id: int) -> Optional[Dict]:
    """Get guild that player is a member of"""
    guilds = load_guilds()
    
    for guild in guilds.values():
        if any(m["user_id"] == user_id for m in guild["members"]):
            return guild
    
    return None

def join_guild(user_id: int, guild_id: str) -> bool:
    """Add player to guild"""
    guilds = load_guilds()
    
    if guild_id not in guilds:
        return False
    
    guild = guilds[guild_id]
    
    # Check if already member
    if any(m["user_id"] == user_id for m in guild["members"]):
        return False
    
    guild["members"].append({
        "user_id": user_id,
        "role": "member",
        "join_date": datetime.now().isoformat()
    })
    
    save_guilds(guilds)
    return True

def add_to_treasury(guild_id: str, amount: int) -> bool:
    """Add money to guild treasury"""
    guilds = load_guilds()
    
    if guild_id not in guilds:
        return False
    
    guilds[guild_id]["treasury"] += amount
    save_guilds(guilds)
    return True

def duel(challenger_id: int, opponent_id: int) -> Dict:
    """
    Execute a duel between two players
    Winner gets bragging rights and small cash reward
    """
    from utils.economy import get_player, add_money
    
    challenger = get_player(challenger_id)
    opponent = get_player(opponent_id)
    
    if not challenger or not opponent:
        return {"error": "Player not found"}
    
    # Simple duel: higher leadership stat usually wins, but random chance involved
    import random
    
    challenger_power = (challenger["stats"].get("leadership", 2) * 10) + random.randint(1, 20)
    opponent_power = (opponent["stats"].get("leadership", 2) * 10) + random.randint(1, 20)
    
    reward = 500
    
    if challenger_power > opponent_power:
        add_money(challenger_id, reward, source="duel")
        return {
            "winner": challenger["username"],
            "loser": opponent["username"],
            "challenger_power": challenger_power,
            "opponent_power": opponent_power,
            "reward": reward,
            "message": f"🏆 **{challenger['username']}** defeated **{opponent['username']}** in a duel!\nWon ${reward}!"
        }
    else:
        add_money(opponent_id, reward, source="duel")
        return {
            "winner": opponent["username"],
            "loser": challenger["username"],
            "challenger_power": challenger_power,
            "opponent_power": opponent_power,
            "reward": reward,
            "message": f"🏆 **{opponent['username']}** defeated **{challenger['username']}** in a duel!\nWon ${reward}!"
        }

def trade_stocks(user1_id: int, user2_id: int, user1_ticker: str, user1_qty: int, 
                user2_ticker: str, user2_qty: int) -> Dict:
    """
    Execute a stock trade between two players
    Both must agree on exchange rate
    """
    from utils.economy import get_player, update_player
    
    user1 = get_player(user1_id)
    user2 = get_player(user2_id)
    
    if not user1 or not user2:
        return {"error": "Player not found"}
    
    # Check holdings
    u1_portfolio = user1.get("portfolio", {})
    u2_portfolio = user2.get("portfolio", {})
    
    if u1_portfolio.get(user1_ticker, 0) < user1_qty:
        return {"error": f"User 1 doesn't own {user1_qty} shares of {user1_ticker}"}
    
    if u2_portfolio.get(user2_ticker, 0) < user2_qty:
        return {"error": f"User 2 doesn't own {user2_qty} shares of {user2_ticker}"}
    
    # Execute trade
    u1_portfolio[user1_ticker] -= user1_qty
    if u1_portfolio[user1_ticker] == 0:
        del u1_portfolio[user1_ticker]
    
    u2_portfolio[user2_ticker] -= user2_qty
    if u2_portfolio[user2_ticker] == 0:
        del u2_portfolio[user2_ticker]
    
    # Add new holdings
    if user2_ticker not in u1_portfolio:
        u1_portfolio[user2_ticker] = 0
    u1_portfolio[user2_ticker] += user2_qty
    
    if user1_ticker not in u2_portfolio:
        u2_portfolio[user1_ticker] = 0
    u2_portfolio[user1_ticker] += user1_qty
    
    # Save
    update_player(user1_id, {"portfolio": u1_portfolio})
    update_player(user2_id, {"portfolio": u2_portfolio})
    
    return {
        "success": True,
        "message": f"✅ Trade complete!\n{user1['username']}: Gave {user1_qty} {user1_ticker}, Got {user2_qty} {user2_ticker}\n{user2['username']}: Gave {user2_qty} {user2_ticker}, Got {user1_qty} {user1_ticker}"
    }

def transfer_money(sender_id: int, receiver_id: int, amount: int) -> Dict:
    """
    Transfer money from one player to another
    """
    from utils.economy import get_player, remove_money, add_money
    
    sender = get_player(sender_id)
    receiver = get_player(receiver_id)
    
    if not sender or not receiver:
        return {"error": "Player not found"}
    
    if sender["cash"] < amount:
        return {"error": f"Insufficient funds. You have ${sender['cash']}, need ${amount}"}
    
    if amount <= 0:
        return {"error": "Amount must be positive"}
    
    # Execute transfer
    remove_money(sender_id, amount, source="transfer")
    add_money(receiver_id, amount, source="transfer")
    
    return {
        "success": True,
        "message": f"💸 Transferred ${amount} to {receiver['username']}"
    }

def get_guild_leaderboard(sort_by: str = "level") -> List[Dict]:
    """Get guilds ranked by metric"""
    guilds = load_guilds()
    guilds_list = list(guilds.values())
    
    if sort_by == "level":
        guilds_list.sort(key=lambda g: g["level"], reverse=True)
    elif sort_by == "treasury":
        guilds_list.sort(key=lambda g: g["treasury"], reverse=True)
    elif sort_by == "members":
        guilds_list.sort(key=lambda g: len(g["members"]), reverse=True)
    elif sort_by == "wins":
        guilds_list.sort(key=lambda g: g["war_wins"], reverse=True)
    
    return guilds_list[:20]  # Top 20
