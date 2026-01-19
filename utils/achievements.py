"""
Achievements System
60+ achievements for players to unlock
"""

from typing import Dict, List, Optional
from datetime import datetime

ACHIEVEMENTS = {
    # Getting Started (5)
    "first_account": {
        "name": "First Account",
        "description": "Create your first account",
        "icon": "🎮",
        "points": 10,
        "rarity": "common"
    },
    "first_job": {
        "name": "Hard Worker",
        "description": "Complete your first job",
        "icon": "💼",
        "points": 25,
        "rarity": "common"
    },
    "first_casino": {
        "name": "Lucky Bet",
        "description": "Play your first casino game",
        "icon": "🎰",
        "points": 25,
        "rarity": "common"
    },
    "first_stock": {
        "name": "Stock Trader",
        "description": "Buy your first stock",
        "icon": "📈",
        "points": 25,
        "rarity": "common"
    },
    "level_5": {
        "name": "Rising Star",
        "description": "Reach level 5",
        "icon": "⭐",
        "points": 50,
        "rarity": "common"
    },

    # Grinding (8)
    "jobs_10": {
        "name": "Employed",
        "description": "Complete 10 jobs",
        "icon": "💪",
        "points": 50,
        "rarity": "common"
    },
    "jobs_50": {
        "name": "Workaholic",
        "description": "Complete 50 jobs",
        "icon": "🔥",
        "points": 100,
        "rarity": "uncommon"
    },
    "jobs_100": {
        "name": "Career Focused",
        "description": "Complete 100 jobs",
        "icon": "👔",
        "points": 250,
        "rarity": "uncommon"
    },
    "job_streak_10": {
        "name": "On a Roll",
        "description": "Get 10 job successes in a row",
        "icon": "🔥",
        "points": 150,
        "rarity": "rare"
    },
    "job_streak_25": {
        "name": "Unstoppable",
        "description": "Get 25 consecutive job successes",
        "icon": "💥",
        "points": 300,
        "rarity": "rare"
    },
    "daily_7": {
        "name": "Dedicated",
        "description": "Claim daily bonus 7 days in a row",
        "icon": "📅",
        "points": 100,
        "rarity": "uncommon"
    },
    "daily_30": {
        "name": "Faithful",
        "description": "Claim daily bonus 30 days in a row",
        "icon": "📅",
        "points": 300,
        "rarity": "rare"
    },
    "daily_100": {
        "name": "Forever Loyal",
        "description": "Claim daily bonus 100 days in a row",
        "icon": "👑",
        "points": 500,
        "rarity": "epic"
    },

    # Casino (8)
    "casino_play": {
        "name": "Gambler",
        "description": "Play a casino game",
        "icon": "🎲",
        "points": 25,
        "rarity": "common"
    },
    "casino_win": {
        "name": "Lucky",
        "description": "Win a casino game",
        "icon": "🍀",
        "points": 50,
        "rarity": "common"
    },
    "casino_wins_10": {
        "name": "Hot Streak",
        "description": "Win 10 casino games",
        "icon": "🔥",
        "points": 150,
        "rarity": "uncommon"
    },
    "casino_wins_50": {
        "name": "Casino Expert",
        "description": "Win 50 casino games",
        "icon": "🏆",
        "points": 300,
        "rarity": "rare"
    },
    "casino_jackpot": {
        "name": "JACKPOT!",
        "description": "Hit a casino jackpot",
        "icon": "💎",
        "points": 250,
        "rarity": "epic"
    },
    "casino_1k": {
        "name": "Big Gambler",
        "description": "Win $1,000 in casino games",
        "icon": "💰",
        "points": 100,
        "rarity": "uncommon"
    },
    "casino_10k": {
        "name": "High Roller",
        "description": "Win $10,000 in casino",
        "icon": "💸",
        "points": 250,
        "rarity": "rare"
    },
    "casino_100k": {
        "name": "Casino King",
        "description": "Win $100,000 in casino",
        "icon": "👑",
        "points": 500,
        "rarity": "epic"
    },

    # Stock Market (8)
    "stock_buy": {
        "name": "Stock Buyer",
        "description": "Buy a stock",
        "icon": "📊",
        "points": 25,
        "rarity": "common"
    },
    "stock_sells": {
        "name": "Trader",
        "description": "Sell a stock at profit",
        "icon": "📈",
        "points": 50,
        "rarity": "common"
    },
    "stock_portfolio_1k": {
        "name": "Portfolio Builder",
        "description": "Get $1,000 in stocks",
        "icon": "💼",
        "points": 100,
        "rarity": "uncommon"
    },
    "stock_portfolio_10k": {
        "name": "Investor",
        "description": "Get $10,000 in stocks",
        "icon": "🏦",
        "points": 250,
        "rarity": "rare"
    },
    "stock_portfolio_100k": {
        "name": "Wealthy Investor",
        "description": "Get $100,000 in stocks",
        "icon": "💎",
        "points": 500,
        "rarity": "epic"
    },
    "stock_gains_1k": {
        "name": "Smart Trader",
        "description": "Make $1,000 from stock gains",
        "icon": "📈",
        "points": 150,
        "rarity": "uncommon"
    },
    "stock_gains_10k": {
        "name": "Market Master",
        "description": "Make $10,000 from stocks",
        "icon": "🎯",
        "points": 300,
        "rarity": "rare"
    },
    "stock_gains_100k": {
        "name": "Stock Tycoon",
        "description": "Make $100,000 from stocks",
        "icon": "👑",
        "points": 500,
        "rarity": "epic"
    },

    # Wealth (8)
    "cash_1k": {
        "name": "Savings Start",
        "description": "Have $1,000 in cash",
        "icon": "💵",
        "points": 50,
        "rarity": "common"
    },
    "cash_10k": {
        "name": "Rich",
        "description": "Have $10,000 in cash",
        "icon": "💰",
        "points": 150,
        "rarity": "uncommon"
    },
    "cash_100k": {
        "name": "Very Rich",
        "description": "Have $100,000 in cash",
        "icon": "💸",
        "points": 300,
        "rarity": "rare"
    },
    "cash_1m": {
        "name": "Millionaire",
        "description": "Have $1,000,000 in cash",
        "icon": "💎",
        "points": 500,
        "rarity": "epic"
    },
    "networth_10k": {
        "name": "Growing Wealth",
        "description": "Reach $10,000 net worth",
        "icon": "📈",
        "points": 100,
        "rarity": "uncommon"
    },
    "networth_100k": {
        "name": "Wealthy",
        "description": "Reach $100,000 net worth",
        "icon": "💎",
        "points": 250,
        "rarity": "rare"
    },
    "networth_1m": {
        "name": "Mega Rich",
        "description": "Reach $1,000,000 net worth",
        "icon": "👑",
        "points": 500,
        "rarity": "epic"
    },
    "earned_100k": {
        "name": "Earner",
        "description": "Earn $100,000 total",
        "icon": "💪",
        "points": 250,
        "rarity": "rare"
    },

    # Leveling (6)
    "level_10": {
        "name": "Experienced",
        "description": "Reach level 10",
        "icon": "⭐",
        "points": 100,
        "rarity": "uncommon"
    },
    "level_25": {
        "name": "Seasoned",
        "description": "Reach level 25",
        "icon": "🌟",
        "points": 200,
        "rarity": "uncommon"
    },
    "level_50": {
        "name": "Veteran",
        "description": "Reach level 50",
        "icon": "👑",
        "points": 300,
        "rarity": "rare"
    },
    "level_75": {
        "name": "Legend",
        "description": "Reach level 75",
        "icon": "🏆",
        "points": 400,
        "rarity": "epic"
    },
    "level_100": {
        "name": "Maximum",
        "description": "Reach level 100",
        "icon": "🎯",
        "points": 500,
        "rarity": "legendary"
    },
    "prestige": {
        "name": "Reborn",
        "description": "Use prestige to reset",
        "icon": "✨",
        "points": 250,
        "rarity": "epic"
    },

    # Special (9)
    "leaderboard_1st": {
        "name": "Top Dog",
        "description": "Get #1 on net worth leaderboard",
        "icon": "🥇",
        "points": 500,
        "rarity": "legendary"
    },
    "leaderboard_10": {
        "name": "Top 10",
        "description": "Get top 10 on leaderboard",
        "icon": "🏆",
        "points": 200,
        "rarity": "rare"
    },
    "reputation_500": {
        "name": "Respected",
        "description": "Reach 500 reputation",
        "icon": "⭐",
        "points": 150,
        "rarity": "uncommon"
    },
    "reputation_2000": {
        "name": "Legendary",
        "description": "Reach 2000 reputation",
        "icon": "👑",
        "points": 300,
        "rarity": "rare"
    },
    "all_jobs": {
        "name": "Renaissance Man",
        "description": "Complete every type of job",
        "icon": "🎭",
        "points": 250,
        "rarity": "epic"
    },
    "all_games": {
        "name": "Game Master",
        "description": "Win every casino game",
        "icon": "🎮",
        "points": 250,
        "rarity": "epic"
    },
    "all_sectors": {
        "name": "Sector Expert",
        "description": "Buy stocks from every sector",
        "icon": "📊",
        "points": 200,
        "rarity": "rare"
    },
    "lucky_7": {
        "name": "Lucky Number",
        "description": "Have exactly $7,777 in cash",
        "icon": "7️⃣",
        "points": 100,
        "rarity": "rare"
    },
    "speedrunner": {
        "name": "Speed Racer",
        "description": "Reach level 50 in one week",
        "icon": "🚀",
        "points": 300,
        "rarity": "epic"
    }
}

def get_achievement(achievement_id: str) -> Optional[Dict]:
    """Get achievement data"""
    return ACHIEVEMENTS.get(achievement_id)

def get_all_achievements() -> Dict:
    """Get all achievements"""
    return ACHIEVEMENTS

def check_achievement_progress(user_id: int, achievement_id: str) -> Dict:
    """
    Check if player has earned an achievement
    Returns: {earned: bool, progress: percent}
    """
    from utils.economy import get_player
    
    player = get_player(user_id)
    if not player:
        return {"earned": False, "progress": 0}
    
    achievement = ACHIEVEMENTS.get(achievement_id)
    if not achievement:
        return {"error": "Achievement not found"}
    
    # Check if already earned
    if achievement_id in player.get("achievements", []):
        return {"earned": True, "progress": 100}
    
    # Check progress based on achievement type
    progress = 0
    
    if achievement_id == "first_account":
        progress = 100
    elif achievement_id == "first_job":
        progress = 100 if player.get("jobs_completed", 0) > 0 else 0
    elif achievement_id == "first_casino":
        progress = 100 if player.get("casino_wagered", 0) > 0 else 0
    elif achievement_id == "first_stock":
        progress = 100 if len(player.get("portfolio", {})) > 0 else 0
    elif achievement_id == "level_5":
        progress = min(100, (player.get("level", 1) / 5) * 100)
    
    # Jobs achievements
    elif achievement_id == "jobs_10":
        progress = min(100, (player.get("jobs_completed", 0) / 10) * 100)
    elif achievement_id == "jobs_50":
        progress = min(100, (player.get("jobs_completed", 0) / 50) * 100)
    elif achievement_id == "jobs_100":
        progress = min(100, (player.get("jobs_completed", 0) / 100) * 100)
    elif achievement_id == "job_streak_10":
        progress = min(100, (player.get("job_streak", 0) / 10) * 100)
    elif achievement_id == "job_streak_25":
        progress = min(100, (player.get("job_streak", 0) / 25) * 100)
    
    # Daily achievements
    elif achievement_id == "daily_7":
        progress = min(100, (player.get("login_streak", 1) / 7) * 100)
    elif achievement_id == "daily_30":
        progress = min(100, (player.get("login_streak", 1) / 30) * 100)
    elif achievement_id == "daily_100":
        progress = min(100, (player.get("login_streak", 1) / 100) * 100)
    
    # Wealth achievements
    elif achievement_id == "cash_1k":
        progress = min(100, (player.get("cash", 0) / 1000) * 100)
    elif achievement_id == "cash_10k":
        progress = min(100, (player.get("cash", 0) / 10000) * 100)
    elif achievement_id == "cash_100k":
        progress = min(100, (player.get("cash", 0) / 100000) * 100)
    elif achievement_id == "cash_1m":
        progress = min(100, (player.get("cash", 0) / 1000000) * 100)
    
    # Level achievements
    elif achievement_id == "level_10":
        progress = min(100, (player.get("level", 1) / 10) * 100)
    elif achievement_id == "level_25":
        progress = min(100, (player.get("level", 1) / 25) * 100)
    elif achievement_id == "level_50":
        progress = min(100, (player.get("level", 1) / 50) * 100)
    elif achievement_id == "level_75":
        progress = min(100, (player.get("level", 1) / 75) * 100)
    elif achievement_id == "level_100":
        progress = min(100, (player.get("level", 1) / 100) * 100)
    
    return {"earned": False, "progress": int(progress)}

def unlock_achievement(user_id: int, achievement_id: str) -> bool:
    """Unlock an achievement for a player"""
    from utils.economy import get_player, update_player
    
    player = get_player(user_id)
    if not player:
        return False
    
    # Check if already unlocked
    if achievement_id in player.get("achievements", []):
        return False
    
    # Unlock it
    achievements = player.get("achievements", [])
    achievements.append(achievement_id)
    
    update_player(user_id, {"achievements": achievements})
    return True
