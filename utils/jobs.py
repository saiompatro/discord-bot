"""
Job/Grinding system for Game of Wall Street
Players can work various Wall Street jobs for income
"""

import random
from datetime import datetime, timedelta
from typing import Dict, Optional, List

JOBS = {
    # Tier 1 (Levels 1-15)
    "street_vendor": {
        "name": "Street Vendor",
        "tier": 1,
        "min_level": 1,
        "cooldown": 30,
        "payout_min": 50,
        "payout_max": 150,
        "base_success_rate": 0.85,
        "stat_scaling": {"humour": 0.5, "strength": 0.3},
        "description": "Sell goods on the street",
        "emoji": "🌭"
    },
    "dog_walker": {
        "name": "Dog Walker",
        "tier": 1,
        "min_level": 1,
        "cooldown": 45,
        "payout_min": 75,
        "payout_max": 200,
        "base_success_rate": 0.85,
        "stat_scaling": {"humour": 0.3, "strength": 0.5},
        "description": "Walk dogs in Central Park",
        "emoji": "🐕"
    },
    "fast_food": {
        "name": "Fast Food Worker",
        "tier": 1,
        "min_level": 1,
        "cooldown": 60,
        "payout_min": 100,
        "payout_max": 250,
        "base_success_rate": 0.85,
        "stat_scaling": {"humour": 0.3, "strength": 0.4},
        "description": "Work at a fast food restaurant",
        "emoji": "🍔"
    },
    "delivery": {
        "name": "Task Delivery",
        "tier": 1,
        "min_level": 1,
        "cooldown": 90,
        "payout_min": 125,
        "payout_max": 300,
        "base_success_rate": 0.85,
        "stat_scaling": {"strength": 0.6, "humour": 0.2},
        "description": "Deliver packages across the city",
        "emoji": "📦"
    },

    # Tier 2 (Levels 15-35)
    "freelancer": {
        "name": "Freelancer",
        "tier": 2,
        "min_level": 15,
        "cooldown": 120,
        "payout_min": 200,
        "payout_max": 500,
        "base_success_rate": 0.85,
        "stat_scaling": {"intellect": 0.5, "humour": 0.3},
        "description": "Do freelance work online",
        "emoji": "💻"
    },
    "retail_manager": {
        "name": "Retail Manager",
        "tier": 2,
        "min_level": 15,
        "cooldown": 180,
        "payout_min": 300,
        "payout_max": 700,
        "base_success_rate": 0.85,
        "stat_scaling": {"leadership": 0.5, "humour": 0.3},
        "description": "Manage a retail store",
        "emoji": "🛍️"
    },
    "security_guard": {
        "name": "Security Guard",
        "tier": 2,
        "min_level": 15,
        "cooldown": 120,
        "payout_min": 250,
        "payout_max": 600,
        "base_success_rate": 0.85,
        "stat_scaling": {"strength": 0.6, "leadership": 0.2},
        "description": "Work as a security guard",
        "emoji": "🛡️"
    },
    "tutor": {
        "name": "Tutor/Coach",
        "tier": 2,
        "min_level": 15,
        "cooldown": 180,
        "payout_min": 350,
        "payout_max": 800,
        "base_success_rate": 0.85,
        "stat_scaling": {"intellect": 0.6, "leadership": 0.3},
        "description": "Tutor or coach students",
        "emoji": "📚"
    },

    # Tier 3 (Levels 35-60)
    "consultant": {
        "name": "Business Consultant",
        "tier": 3,
        "min_level": 35,
        "cooldown": 240,
        "payout_min": 500,
        "payout_max": 1500,
        "base_success_rate": 0.85,
        "stat_scaling": {"intellect": 0.6, "leadership": 0.4},
        "description": "Consult for businesses",
        "emoji": "💼"
    },
    "realtor": {
        "name": "Real Estate Agent",
        "tier": 3,
        "min_level": 35,
        "cooldown": 300,
        "payout_min": 800,
        "payout_max": 2000,
        "base_success_rate": 0.85,
        "stat_scaling": {"leadership": 0.5, "humour": 0.4},
        "description": "Sell real estate properties",
        "emoji": "🏢"
    },
    "lawyer": {
        "name": "Lawyer",
        "tier": 3,
        "min_level": 35,
        "cooldown": 360,
        "payout_min": 1000,
        "payout_max": 2500,
        "base_success_rate": 0.85,
        "stat_scaling": {"intellect": 0.7, "leadership": 0.3},
        "description": "Provide legal services",
        "emoji": "⚖️"
    },
    "analyst": {
        "name": "Data Analyst",
        "tier": 3,
        "min_level": 35,
        "cooldown": 240,
        "payout_min": 700,
        "payout_max": 1800,
        "base_success_rate": 0.85,
        "stat_scaling": {"intellect": 0.8, "humour": 0.1},
        "description": "Analyze data for companies",
        "emoji": "📊"
    },

    # Tier 4 (Levels 60+)
    "ceo": {
        "name": "CEO",
        "tier": 4,
        "min_level": 60,
        "cooldown": 480,
        "payout_min": 2000,
        "payout_max": 5000,
        "base_success_rate": 0.80,
        "stat_scaling": {"leadership": 0.8, "intellect": 0.5},
        "description": "Run a company as CEO",
        "emoji": "👑"
    },
    "investment_manager": {
        "name": "Investment Fund Manager",
        "tier": 4,
        "min_level": 60,
        "cooldown": 600,
        "payout_min": 3000,
        "payout_max": 7500,
        "base_success_rate": 0.80,
        "stat_scaling": {"intellect": 0.7, "wealth": 0.4},
        "description": "Manage an investment fund",
        "emoji": "💰"
    },
    "hedge_fund": {
        "name": "Hedge Fund Trader",
        "tier": 4,
        "min_level": 60,
        "cooldown": 720,
        "payout_min": 4000,
        "payout_max": 10000,
        "base_success_rate": 0.75,
        "stat_scaling": {"intellect": 0.6, "wealth": 0.6},
        "description": "Trade at a hedge fund (high risk)",
        "emoji": "📈"
    },
    "vc": {
        "name": "Venture Capitalist",
        "tier": 4,
        "min_level": 60,
        "cooldown": 720,
        "payout_min": 5000,
        "payout_max": 15000,
        "base_success_rate": 0.80,
        "stat_scaling": {"leadership": 0.6, "intellect": 0.5},
        "description": "Fund startups as a VC",
        "emoji": "🚀"
    },
}

def get_available_jobs(level: int) -> List[str]:
    """Get available jobs for a given level"""
    available = []
    for job_id, job_data in JOBS.items():
        if job_data["min_level"] <= level:
            available.append(job_id)
    return available

def get_job_info(job_id: str) -> Optional[Dict]:
    """Get job information"""
    return JOBS.get(job_id)

def calculate_job_payout(job_id: str, intellect: int, humour: int, strength: int, 
                        leadership: int, mental_health: int, wealth: int) -> Dict:
    """
    Calculate job payout with stat scaling
    Stats are 1-5, we normalize them
    """
    job = JOBS.get(job_id)
    if not job:
        return {"error": "Job not found"}
    
    # Normalize stats (1-5 to 0-1)
    stat_values = {
        "intellect": intellect / 5,
        "humour": humour / 5,
        "strength": strength / 5,
        "leadership": leadership / 5,
        "mental_health": mental_health / 5,
        "wealth": wealth / 5,
    }
    
    # Calculate success rate
    success_rate = job["base_success_rate"]
    for stat_name, scaling in job["stat_scaling"].items():
        success_rate += (stat_values[stat_name] * scaling * 0.15)
    success_rate = min(success_rate, 1.0)  # Cap at 100%
    
    # Determine if job succeeds
    success = random.random() < success_rate
    
    if not success:
        # Failed job
        return {
            "success": False,
            "payout": 0,
            "xp": 5,
            "message": "❌ You failed this job!"
        }
    
    # Calculate payout
    base_payout = random.randint(job["payout_min"], job["payout_max"])
    
    # Apply stat bonuses (can increase payout)
    payout_multiplier = 1.0
    for stat_name, scaling in job["stat_scaling"].items():
        payout_multiplier += (stat_values[stat_name] * scaling * 0.2)
    
    # Random variance (0.8x - 1.2x)
    variance = random.uniform(0.8, 1.2)
    
    # 5% chance of critical success (2x payout)
    if random.random() < 0.05:
        variance = 2.0
    
    final_payout = int(base_payout * payout_multiplier * variance)
    
    # XP calculation
    xp_earned = int((job["payout_max"] - job["payout_min"]) / 25)
    
    return {
        "success": True,
        "payout": final_payout,
        "xp": xp_earned,
        "message": f"✅ Job completed! Earned ${final_payout}",
        "critical": variance == 2.0
    }

def work_job(user_id: int, job_id: str) -> Dict:
    """
    Execute a job for a player
    Returns result dictionary with success/failure info
    """
    from utils.economy import get_player, add_money, add_experience, update_player
    
    player = get_player(user_id)
    if not player:
        return {"error": "Player not found"}
    
    # Check if job exists
    job = get_job_info(job_id)
    if not job:
        return {"error": "Job not found"}
    
    # Check level requirement
    if player["level"] < job["min_level"]:
        return {
            "error": "Job requires level " + str(job["min_level"]),
            "current_level": player["level"]
        }
    
    # Check cooldown
    job_cooldown_key = f"job_{job_id}_cooldown"
    if job_cooldown_key in player:
        cooldown_time = player[job_cooldown_key]
        if datetime.fromisoformat(cooldown_time) > datetime.now():
            remaining = (datetime.fromisoformat(cooldown_time) - datetime.now()).total_seconds()
            return {
                "error": "Job on cooldown",
                "remaining_seconds": int(remaining),
                "job": job_id
            }
    
    # Get stats from player
    stats = player["stats"]
    
    # Calculate payout
    result = calculate_job_payout(
        job_id,
        stats.get("intellect", 2),
        stats.get("humour", 2),
        stats.get("strength", 2),
        stats.get("leadership", 2),
        stats.get("mental_health", 2),
        stats.get("wealth", 2),
    )
    
    if "error" in result:
        return result
    
    # Apply job result
    if result["success"]:
        # Add money
        add_money(user_id, result["payout"], source="job")
        
        # Add experience
        add_experience(user_id, result["xp"])
        
        # Update job stats
        player["jobs_completed"] = player.get("jobs_completed", 0) + 1
        player["job_earnings"] = player.get("job_earnings", 0) + result["payout"]
        player["job_streak"] = player.get("job_streak", 0) + 1
    else:
        # Failed job
        player["job_streak"] = 0
        result["xp"] = 5
        add_experience(user_id, 5)
    
    # Set cooldown
    cooldown_time = datetime.now() + timedelta(seconds=job["cooldown"])
    player[job_cooldown_key] = cooldown_time.isoformat()
    
    update_player(user_id, player)
    
    return result

def get_job_list(level: int) -> str:
    """Generate a formatted list of available jobs"""
    available_jobs = get_available_jobs(level)
    
    if not available_jobs:
        return "No jobs available"
    
    job_list = ""
    for job_id in available_jobs:
        job = get_job_info(job_id)
        pay_range = f"${job['payout_min']}-${job['payout_max']}"
        cooldown_min = job["cooldown"] / 60
        job_list += f"{job['emoji']} **{job['name']}** - {pay_range} ({int(cooldown_min)}m cooldown)\n"
    
    return job_list
