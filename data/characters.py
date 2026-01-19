"""
Character database for Game of Wall Street
30 unique characters with different backgrounds and stat distributions
"""

CHARACTERS = {
    # Finance Professionals
    "Dave": {
        "title": "Stock Broker",
        "background": "NYU graduate, works at JP Morgan as a stock broker with no personal life",
        "stats": {"intellect": 4, "humour": 1, "strength": 2, "leadership": 3, "mental_health": 1, "wealth": 4},
        "starting_cash": 5000,
        "starting_bank": 10000,
        "job_bonuses": {"stock_broker": 1.15, "analyst": 1.10},
        "bio_emoji": "📈"
    },
    "Judy": {
        "title": "Receptionist",
        "background": "High school dropout working at Citadel reception desk, aspires to break into finance",
        "stats": {"intellect": 2, "humour": 3, "strength": 2, "leadership": 2, "mental_health": 3, "wealth": 1},
        "starting_cash": 1500,
        "starting_bank": 2000,
        "job_bonuses": {"receptionist": 1.20, "assistant": 1.10},
        "bio_emoji": "📞"
    },
    "Emily": {
        "title": "Unemployed Graduate",
        "background": "Stanford graduate aggressively seeking Wall Street position, greedy and narcissistic",
        "stats": {"intellect": 5, "humour": 1, "strength": 1, "leadership": 4, "mental_health": 1, "wealth": 2},
        "starting_cash": 3000,
        "starting_bank": 5000,
        "job_bonuses": {"hedge_fund": 1.12, "vc": 1.15},
        "bio_emoji": "🎓"
    },
    "Marcus": {
        "title": "CEO",
        "background": "Self-made real estate and finance mogul, commanding presence",
        "stats": {"intellect": 4, "humour": 2, "strength": 3, "leadership": 5, "mental_health": 3, "wealth": 5},
        "starting_cash": 25000,
        "starting_bank": 50000,
        "job_bonuses": {"ceo": 1.25, "manager": 1.20},
        "bio_emoji": "👔"
    },
    "Sarah": {
        "title": "Hedge Fund Manager",
        "background": "Aggressive trader with Harvard MBA, thrives on high-stakes deals",
        "stats": {"intellect": 5, "humour": 2, "strength": 2, "leadership": 4, "mental_health": 2, "wealth": 4},
        "starting_cash": 15000,
        "starting_bank": 30000,
        "job_bonuses": {"hedge_fund": 1.20, "trader": 1.18},
        "bio_emoji": "💼"
    },
    "James": {
        "title": "Investment Banker",
        "background": "Goldman Sachs analyst, workaholic with impressive credentials",
        "stats": {"intellect": 4, "humour": 1, "strength": 1, "leadership": 3, "mental_health": 2, "wealth": 4},
        "starting_cash": 12000,
        "starting_bank": 25000,
        "job_bonuses": {"investment_banker": 1.22, "analyst": 1.15},
        "bio_emoji": "💰"
    },
    "Rachel": {
        "title": "VC Partner",
        "background": "Venture capitalist with Stanford pedigree, optimistic about startups",
        "stats": {"intellect": 4, "humour": 3, "strength": 2, "leadership": 4, "mental_health": 4, "wealth": 4},
        "starting_cash": 20000,
        "starting_bank": 40000,
        "job_bonuses": {"vc": 1.18, "manager": 1.12},
        "bio_emoji": "🚀"
    },

    # Service & Entrepreneurial
    "Mike": {
        "title": "Street Vendor",
        "background": "Hustling hot dog cart owner in Financial District with dreams of expansion",
        "stats": {"intellect": 2, "humour": 4, "strength": 4, "leadership": 2, "mental_health": 4, "wealth": 1},
        "starting_cash": 800,
        "starting_bank": 1000,
        "job_bonuses": {"vendor": 1.25, "entrepreneur": 1.10},
        "bio_emoji": "🌭"
    },
    "Lisa": {
        "title": "Gym Owner",
        "background": "Former athlete turned gym owner, physically fit but financially struggling",
        "stats": {"intellect": 2, "humour": 3, "strength": 5, "leadership": 3, "mental_health": 4, "wealth": 2},
        "starting_cash": 2500,
        "starting_bank": 3000,
        "job_bonuses": {"trainer": 1.15, "manager": 1.08},
        "bio_emoji": "💪"
    },
    "David": {
        "title": "Rideshare Driver",
        "background": "Uber/Lyft driver saving money for business school",
        "stats": {"intellect": 3, "humour": 4, "strength": 2, "leadership": 2, "mental_health": 3, "wealth": 1},
        "starting_cash": 1200,
        "starting_bank": 2000,
        "job_bonuses": {"driver": 1.20, "contractor": 1.10},
        "bio_emoji": "🚕"
    },
    "Angela": {
        "title": "Real Estate Agent",
        "background": "Charismatic realtor selling luxury Manhattan apartments",
        "stats": {"intellect": 3, "humour": 4, "strength": 2, "leadership": 4, "mental_health": 4, "wealth": 3},
        "starting_cash": 5000,
        "starting_bank": 8000,
        "job_bonuses": {"realtor": 1.18, "salesman": 1.15},
        "bio_emoji": "🏢"
    },
    "Carlos": {
        "title": "Restaurant Owner",
        "background": "Passionate chef turned restaurateur, living on thin margins",
        "stats": {"intellect": 2, "humour": 4, "strength": 3, "leadership": 3, "mental_health": 3, "wealth": 1},
        "starting_cash": 3000,
        "starting_bank": 5000,
        "job_bonuses": {"entrepreneur": 1.20, "manager": 1.12},
        "bio_emoji": "👨‍🍳"
    },

    # Corporate Ladder
    "Jennifer": {
        "title": "Senior Manager",
        "background": "15-year corporate veteran climbing the ladder at McKinsey",
        "stats": {"intellect": 4, "humour": 2, "strength": 1, "leadership": 5, "mental_health": 2, "wealth": 3},
        "starting_cash": 8000,
        "starting_bank": 15000,
        "job_bonuses": {"manager": 1.18, "consultant": 1.15},
        "bio_emoji": "📊"
    },
    "Robert": {
        "title": "IT Director",
        "background": "Tech-savvy corporate director with comp sci background",
        "stats": {"intellect": 5, "humour": 1, "strength": 1, "leadership": 3, "mental_health": 3, "wealth": 3},
        "starting_cash": 7000,
        "starting_bank": 12000,
        "job_bonuses": {"director": 1.15, "tech": 1.20},
        "bio_emoji": "💻"
    },
    "Michelle": {
        "title": "HR Executive",
        "background": "CIPD-certified HR director at Fortune 500 company",
        "stats": {"intellect": 3, "humour": 3, "strength": 1, "leadership": 4, "mental_health": 4, "wealth": 3},
        "starting_cash": 6500,
        "starting_bank": 11000,
        "job_bonuses": {"hr": 1.12, "manager": 1.10},
        "bio_emoji": "👥"
    },
    "Daniel": {
        "title": "Sales Director",
        "background": "Competitive salesman with trophy case at Morgan Stanley",
        "stats": {"intellect": 3, "humour": 4, "strength": 2, "leadership": 4, "mental_health": 3, "wealth": 4},
        "starting_cash": 9000,
        "starting_bank": 16000,
        "job_bonuses": {"salesman": 1.20, "manager": 1.15},
        "bio_emoji": "🎯"
    },

    # Struggling/Climbing
    "Kevin": {
        "title": "Security Guard",
        "background": "Ex-military security at Wall Street office complex",
        "stats": {"intellect": 2, "humour": 2, "strength": 5, "leadership": 2, "mental_health": 3, "wealth": 1},
        "starting_cash": 1800,
        "starting_bank": 2500,
        "job_bonuses": {"security": 1.15, "manual": 1.10},
        "bio_emoji": "🛡️"
    },
    "Patricia": {
        "title": "Janitor",
        "background": "Night shift janitor at Goldman Sachs, observant and determined",
        "stats": {"intellect": 3, "humour": 3, "strength": 3, "leadership": 1, "mental_health": 3, "wealth": 1},
        "starting_cash": 1000,
        "starting_bank": 1200,
        "job_bonuses": {"manual": 1.20, "services": 1.10},
        "bio_emoji": "🧹"
    },
    "Thomas": {
        "title": "Lawyer",
        "background": "Corporate lawyer at prestigious firm, cynical but skilled",
        "stats": {"intellect": 5, "humour": 2, "strength": 1, "leadership": 3, "mental_health": 2, "wealth": 4},
        "starting_cash": 11000,
        "starting_bank": 22000,
        "job_bonuses": {"lawyer": 1.20, "consultant": 1.12},
        "bio_emoji": "⚖️"
    },
    "Grace": {
        "title": "Data Scientist",
        "background": "MIT grad working in fintech startup on Wall Street",
        "stats": {"intellect": 5, "humour": 1, "strength": 1, "leadership": 2, "mental_health": 3, "wealth": 3},
        "starting_cash": 6000,
        "starting_bank": 10000,
        "job_bonuses": {"analyst": 1.22, "tech": 1.18},
        "bio_emoji": "📈"
    },

    # Miscellaneous Personalities
    "Alexandra": {
        "title": "Influencer/Trader",
        "background": "Social media influencer turned crypto trader, controversial",
        "stats": {"intellect": 2, "humour": 5, "strength": 1, "leadership": 3, "mental_health": 2, "wealth": 2},
        "starting_cash": 4000,
        "starting_bank": 6000,
        "job_bonuses": {"trader": 1.10, "influencer": 1.25},
        "bio_emoji": "📱"
    },
    "Stephen": {
        "title": "Accountant",
        "background": "CPA with OCD tendencies, obsessed with numbers and precision",
        "stats": {"intellect": 4, "humour": 1, "strength": 1, "leadership": 1, "mental_health": 2, "wealth": 2},
        "starting_cash": 4500,
        "starting_bank": 8000,
        "job_bonuses": {"accountant": 1.18, "analyst": 1.12},
        "bio_emoji": "🧮"
    },
    "Natasha": {
        "title": "Consultant",
        "background": "Strategy consultant at Bain, ambitious and conniving",
        "stats": {"intellect": 4, "humour": 2, "strength": 1, "leadership": 4, "mental_health": 2, "wealth": 3},
        "starting_cash": 7500,
        "starting_bank": 13000,
        "job_bonuses": {"consultant": 1.17, "strategist": 1.15},
        "bio_emoji": "🎓"
    },
    "Victor": {
        "title": "Bartender",
        "background": "Charming bartender at Wall Street hotspot, great networker",
        "stats": {"intellect": 3, "humour": 5, "strength": 3, "leadership": 4, "mental_health": 4, "wealth": 1},
        "starting_cash": 2000,
        "starting_bank": 2500,
        "job_bonuses": {"service": 1.20, "networking": 1.15},
        "bio_emoji": "🍸"
    },
    "Sophie": {
        "title": "Marketing Director",
        "background": "Creative marketer at luxury brand, fashion-forward and confident",
        "stats": {"intellect": 3, "humour": 4, "strength": 1, "leadership": 3, "mental_health": 4, "wealth": 2},
        "starting_cash": 5500,
        "starting_bank": 9000,
        "job_bonuses": {"marketing": 1.15, "salesman": 1.12},
        "bio_emoji": "🎨"
    },
    "Andrew": {
        "title": "Personal Trainer",
        "background": "Enthusiastic trainer at expensive Manhattan gym, struggling with finances",
        "stats": {"intellect": 2, "humour": 4, "strength": 5, "leadership": 3, "mental_health": 4, "wealth": 1},
        "starting_cash": 1500,
        "starting_bank": 2000,
        "job_bonuses": {"trainer": 1.18, "services": 1.10},
        "bio_emoji": "🏋️"
    },
    "Diana": {
        "title": "Freelance Writer",
        "background": "Financial journalist covering Wall Street news, sharp analytical mind",
        "stats": {"intellect": 4, "humour": 3, "strength": 1, "leadership": 2, "mental_health": 3, "wealth": 2},
        "starting_cash": 2800,
        "starting_bank": 4500,
        "job_bonuses": {"writer": 1.15, "analyst": 1.12},
        "bio_emoji": "📝"
    },
    "Gregory": {
        "title": "Loan Officer",
        "background": "Career bank employee, helpful but always pushing products",
        "stats": {"intellect": 3, "humour": 2, "strength": 1, "leadership": 3, "mental_health": 3, "wealth": 2},
        "starting_cash": 4000,
        "starting_bank": 7000,
        "job_bonuses": {"banking": 1.15, "services": 1.10},
        "bio_emoji": "🏦"
    },
}

# Helper functions to get character info
def get_character(name: str):
    """Get character data by name"""
    return CHARACTERS.get(name)

def get_all_characters():
    """Get all available characters"""
    return list(CHARACTERS.keys())

def get_character_stats(name: str):
    """Get character stats"""
    char = CHARACTERS.get(name)
    if char:
        return char.get("stats", {})
    return {}

def get_character_starting_money(name: str):
    """Get starting cash and bank for character"""
    char = CHARACTERS.get(name)
    if char:
        return {
            "cash": char.get("starting_cash", 1000),
            "bank": char.get("starting_bank", 2000)
        }
    return {"cash": 1000, "bank": 2000}
