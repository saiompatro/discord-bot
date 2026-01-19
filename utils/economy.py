"""
Economy and user database management system
Handles all player data, transactions, and account management
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import random

# Database file for persistence (using JSON for simplicity)
DB_PATH = "data/players.json"
CHARACTERS_DB_PATH = "data/characters_used.json"

def ensure_db_exists():
    """Create players.json if it doesn't exist"""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, 'w') as f:
            json.dump({}, f)
    if not os.path.exists(CHARACTERS_DB_PATH):
        with open(CHARACTERS_DB_PATH, 'w') as f:
            json.dump([], f)

def load_db():
    """Load all player data from JSON"""
    ensure_db_exists()
    try:
        with open(DB_PATH, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_db(data):
    """Save all player data to JSON"""
    ensure_db_exists()
    with open(DB_PATH, 'w') as f:
        json.dump(data, f, indent=2)

def create_player(user_id: int, username: str, character_name: str, starting_cash: int, starting_bank: int, stats: Dict):
    """Create a new player account"""
    from data.characters import CHARACTERS
    
    db = load_db()
    
    if str(user_id) in db:
        return None  # Player already exists
    
    char = CHARACTERS.get(character_name)
    if not char:
        return None  # Invalid character
    
    player_data = {
        "user_id": user_id,
        "username": username,
        "character": character_name,
        "character_title": char.get("title", ""),
        "created_at": datetime.now().isoformat(),
        "last_active": datetime.now().isoformat(),
        
        # Money
        "cash": starting_cash,
        "bank_balance": starting_bank,
        "total_earned": starting_cash + starting_bank,
        "total_spent": 0,
        
        # Leveling
        "level": 1,
        "experience": 0,
        "prestige": 0,
        "reputation": 100,
        
        # Stats (1-5 stars)
        "stats": {
            "intellect": stats.get("intellect", 2),
            "humour": stats.get("humour", 2),
            "strength": stats.get("strength", 2),
            "leadership": stats.get("leadership", 2),
            "mental_health": stats.get("mental_health", 2),
            "wealth": stats.get("wealth", 2),
        },
        
        # Streaks
        "job_streak": 0,
        "login_streak": 1,
        "casino_win_streak": 0,
        "casino_loss_streak": 0,
        
        # Cooldowns
        "job_cooldown": 0,
        "casino_cooldown": 0,
        "last_daily_claim": datetime.now().isoformat(),
        
        # Job data
        "jobs_completed": 0,
        "job_earnings": 0,
        "current_job": None,
        
        # Casino data
        "casino_wagered": 0,
        "casino_won": 0,
        "casino_lost": 0,
        "casino_vip_tier": "None",
        "loyalty_points": 0,
        
        # Stock data
        "portfolio": {},  # {ticker: quantity}
        "short_positions": {},  # {ticker: {quantity, price}}
        "stock_earnings": 0,
        
        # Achievements
        "achievements": [],
        
        # Items/Inventory
        "inventory": {},
    }
    
    db[str(user_id)] = player_data
    save_db(db)
    return player_data

def get_player(user_id: int) -> Optional[Dict]:
    """Get player data by user_id"""
    db = load_db()
    return db.get(str(user_id))

def player_exists(user_id: int) -> bool:
    """Check if player exists"""
    db = load_db()
    return str(user_id) in db

def update_player(user_id: int, updates: Dict) -> bool:
    """Update player data"""
    db = load_db()
    if str(user_id) not in db:
        return False
    
    db[str(user_id)].update(updates)
    db[str(user_id)]["last_active"] = datetime.now().isoformat()
    save_db(db)
    return True

def add_money(user_id: int, amount: int, source: str = "unknown") -> bool:
    """Add money to player's cash"""
    db = load_db()
    if str(user_id) not in db:
        return False
    
    player = db[str(user_id)]
    player["cash"] += amount
    player["total_earned"] += amount
    
    if source == "job":
        player["job_earnings"] += amount
    elif source == "casino":
        player["casino_won"] += amount
    elif source == "stock":
        player["stock_earnings"] += amount
    
    save_db(db)
    return True

def remove_money(user_id: int, amount: int, source: str = "unknown") -> bool:
    """Remove money from player's cash"""
    db = load_db()
    if str(user_id) not in db:
        return False
    
    player = db[str(user_id)]
    if player["cash"] < amount:
        return False  # Insufficient funds
    
    player["cash"] -= amount
    player["total_spent"] += amount
    
    if source == "casino":
        player["casino_lost"] += amount
        player["casino_wagered"] += amount
    elif source == "gambling":
        player["casino_wagered"] += amount
    
    save_db(db)
    return True

def get_net_worth(user_id: int) -> int:
    """Get player's total net worth"""
    player = get_player(user_id)
    if not player:
        return 0
    
    cash = player.get("cash", 0)
    bank = player.get("bank_balance", 0)
    # TODO: Add stock portfolio value when stocks are calculated
    
    return cash + bank

def add_experience(user_id: int, amount: int) -> Dict:
    """Add experience and handle leveling"""
    db = load_db()
    if str(user_id) not in db:
        return {}
    
    player = db[str(user_id)]
    player["experience"] += amount
    
    # Level up calculation: 100 XP for level 1, +50 XP per level
    xp_needed = 100
    level = 1
    total_xp = 0
    
    while total_xp + xp_needed <= player["experience"]:
        total_xp += xp_needed
        level += 1
        xp_needed += 50
    
    old_level = player["level"]
    player["level"] = level
    
    save_db(db)
    
    return {
        "old_level": old_level,
        "new_level": level,
        "leveled_up": level > old_level,
        "current_experience": player["experience"],
        "xp_to_next": xp_needed - (player["experience"] - total_xp)
    }

def get_leaderboard(sort_by: str = "net_worth", limit: int = 10) -> List[Dict]:
    """Get top players by various metrics"""
    db = load_db()
    
    players_list = list(db.values())
    
    if sort_by == "net_worth":
        players_list.sort(key=lambda p: p.get("cash", 0) + p.get("bank_balance", 0), reverse=True)
    elif sort_by == "level":
        players_list.sort(key=lambda p: p.get("level", 1), reverse=True)
    elif sort_by == "casino_winnings":
        players_list.sort(key=lambda p: p.get("casino_won", 0), reverse=True)
    elif sort_by == "job_earnings":
        players_list.sort(key=lambda p: p.get("job_earnings", 0), reverse=True)
    elif sort_by == "reputation":
        players_list.sort(key=lambda p: p.get("reputation", 0), reverse=True)
    
    return players_list[:limit]

def claim_daily_bonus(user_id: int) -> Optional[Dict]:
    """Claim daily login bonus"""
    player = get_player(user_id)
    if not player:
        return None
    
    last_claim = datetime.fromisoformat(player["last_daily_claim"])
    now = datetime.now()
    
    # Check if enough time has passed
    if now - last_claim < timedelta(hours=20):
        return {
            "claimed": False,
            "reason": "Already claimed today",
            "next_claim": (last_claim + timedelta(hours=24)).isoformat()
        }
    
    # Calculate bonus based on streak
    streak = player.get("login_streak", 1)
    bonus = 50 + (streak * 5)
    bonus = min(bonus, 500)  # Cap at 500
    
    # Award bonus
    add_money(user_id, bonus, source="daily")
    
    # Update streaks and times
    update_player(user_id, {
        "login_streak": streak + 1 if now - last_claim < timedelta(hours=48) else 1,
        "last_daily_claim": now.isoformat()
    })
    
    return {
        "claimed": True,
        "bonus": bonus,
        "new_streak": player.get("login_streak", 1) + 1,
        "next_claim": (now + timedelta(hours=24)).isoformat()
    }

def get_player_stats_summary(user_id: int) -> Optional[Dict]:
    """Get comprehensive player stats summary"""
    player = get_player(user_id)
    if not player:
        return None
    
    return {
        "username": player["username"],
        "character": player["character"],
        "level": player["level"],
        "experience": player["experience"],
        "cash": player["cash"],
        "bank": player["bank_balance"],
        "net_worth": get_net_worth(user_id),
        "stats": player["stats"],
        "reputation": player["reputation"],
        "job_streak": player["job_streak"],
        "login_streak": player["login_streak"],
    }
def load_used_characters():
    """Load list of used characters"""
    ensure_db_exists()
    try:
        with open(CHARACTERS_DB_PATH, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_used_characters(characters: List[str]):
    """Save list of used characters"""
    ensure_db_exists()
    with open(CHARACTERS_DB_PATH, 'w') as f:
        json.dump(characters, f, indent=2)

def get_available_character() -> Optional[str]:
    """Get a random available character (not yet assigned)"""
    from data.characters import get_all_characters
    
    all_chars = get_all_characters()
    used_chars = load_used_characters()
    available_chars = [char for char in all_chars if char not in used_chars]
    
    if not available_chars:
        return None
    
    # Return random available character
    return random.choice(available_chars)

def mark_character_used(character_name: str):
    """Mark a character as used (assigned to a player)"""
    used_chars = load_used_characters()
    if character_name not in used_chars:
        used_chars.append(character_name)
        save_used_characters(used_chars)