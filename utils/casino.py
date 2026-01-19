"""
Casino gambling system
Includes games: Coinflip, Slots, Blackjack, Roulette, Dice, Poker
"""

import random
from typing import Dict, Optional
from datetime import datetime, timedelta

class CasinoGame:
    """Base casino game class"""
    
    def __init__(self, house_edge: float):
        self.house_edge = house_edge
    
    def calculate_payout_multiplier(self) -> float:
        """Base calculation for payout with house edge"""
        return 1 - (self.house_edge / 100)

class Coinflip(CasinoGame):
    """Simple 50/50 coin flip with 2% house edge"""
    
    def __init__(self):
        super().__init__(house_edge=2)
    
    def play(self, bet: int, prediction: str, luck_stat: int = 2) -> Dict:
        """
        Play coin flip
        prediction: 'heads' or 'tails'
        luck_stat: 1-5 (affects odds by ±1% per level above 2)
        """
        # Validate
        if prediction.lower() not in ['heads', 'tails']:
            return {"error": "Invalid prediction. Use 'heads' or 'tails'"}
        
        # Base 50% win chance, modified by luck
        luck_bonus = (luck_stat - 2) * 0.01  # ±1% per point from base
        win_chance = 0.50 + luck_bonus
        win_chance = max(0.35, min(0.65, win_chance))  # Clamp between 35-65%
        
        result = "heads" if random.random() < 0.5 else "tails"
        won = result == prediction.lower()
        
        if won:
            payout = int(bet * 1.96)  # 2% house edge
            return {
                "success": True,
                "result": result,
                "payout": payout,
                "message": f"🎉 **{result.upper()}!** You won ${payout}!"
            }
        else:
            return {
                "success": False,
                "result": result,
                "payout": 0,
                "lost": bet,
                "message": f"❌ **{result.upper()}!** You lost ${bet}"
            }

class Slots(CasinoGame):
    """3-reel slot machine with 8-12% house edge"""
    
    SYMBOLS = ["🍒", "🍊", "🍋", "🔔", "7️⃣", "💎"]
    
    def __init__(self):
        super().__init__(house_edge=10)
    
    def play(self, bet: int, luck_stat: int = 2) -> Dict:
        """Play slots"""
        
        # Spin 3 reels
        reel1 = random.choices(self.SYMBOLS, weights=[15, 15, 15, 20, 20, 15])[0]
        reel2 = random.choices(self.SYMBOLS, weights=[15, 15, 15, 20, 20, 15])[0]
        reel3 = random.choices(self.SYMBOLS, weights=[15, 15, 15, 20, 20, 15])[0]
        
        result = f"{reel1} {reel2} {reel3}"
        
        # Apply luck stat
        luck_bonus = (luck_stat - 2) * 0.02  # ±2% per point
        jackpot_chance = 0.001 + luck_bonus
        jackpot_chance = max(0.0005, min(0.002, jackpot_chance))
        
        # Check jackpot (all diamonds)
        if reel1 == "💎" and reel2 == "💎" and reel3 == "💎":
            payout = int(bet * 100)
            return {
                "success": True,
                "result": result,
                "payout": payout,
                "jackpot": True,
                "message": f"🏆 **JACKPOT!!!** {result}\n You won ${payout}!"
            }
        
        # Check triple match
        if reel1 == reel2 == reel3:
            payout = int(bet * 25)
            return {
                "success": True,
                "result": result,
                "payout": payout,
                "message": f"🎊 **Triple Match!** {result}\nYou won ${payout}!"
            }
        
        # Check double match
        if reel1 == reel2 or reel2 == reel3 or reel1 == reel3:
            payout = int(bet * 5)
            return {
                "success": True,
                "result": result,
                "payout": payout,
                "message": f"✨ **Two Match!** {result}\nYou won ${payout}!"
            }
        
        # Loss
        return {
            "success": False,
            "result": result,
            "payout": 0,
            "lost": bet,
            "message": f"❌ {result}\nYou lost ${bet}"
        }

class Blackjack(CasinoGame):
    """Blackjack vs dealer with 3-4% house edge"""
    
    def __init__(self):
        super().__init__(house_edge=3.5)
        self.deck = []
    
    def get_card_value(self, card: str) -> int:
        """Get numeric value of card"""
        values = {"A": 11, "K": 10, "Q": 10, "J": 10}
        for i in range(2, 11):
            values[str(i)] = i
        return values.get(card, 0)
    
    def draw_card(self) -> str:
        """Draw a random card"""
        cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        return random.choice(cards)
    
    def calculate_hand_value(self, hand: list) -> int:
        """Calculate best value of hand (considering aces as 1 or 11)"""
        total = sum(self.get_card_value(card) for card in hand)
        aces = hand.count("A")
        
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        
        return total

class Roulette(CasinoGame):
    """European roulette with 2.7% house edge"""
    
    def __init__(self):
        super().__init__(house_edge=2.7)
    
    def play(self, bet: int, bet_type: str, prediction: int = None, luck_stat: int = 2) -> Dict:
        """
        Play roulette
        bet_type: 'number' (0-36), 'red', 'black', 'even', 'odd', 'high', 'low'
        """
        
        # Spin the wheel (0-36)
        spin = random.randint(0, 36)
        
        # Determine color (0 is green)
        if spin == 0:
            color = "green"
        elif spin % 2 == 0:
            color = "black"
        else:
            color = "red"
        
        won = False
        multiplier = 0
        
        if bet_type == "number" and prediction is not None:
            if spin == prediction:
                won = True
                multiplier = 35
        elif bet_type == "red":
            won = color == "red"
            multiplier = 1
        elif bet_type == "black":
            won = color == "black"
            multiplier = 1
        elif bet_type == "even":
            won = spin != 0 and spin % 2 == 0
            multiplier = 1
        elif bet_type == "odd":
            won = spin % 2 == 1
            multiplier = 1
        elif bet_type == "high":
            won = 19 <= spin <= 36
            multiplier = 1
        elif bet_type == "low":
            won = 1 <= spin <= 18
            multiplier = 1
        
        payout = int(bet * multiplier) if won else 0
        
        message = f"🎡 Roulette: **{spin}** ({color})\n"
        if won:
            message += f"🎉 You won ${payout}!"
        else:
            message += f"❌ You lost ${bet}"
        
        return {
            "success": won,
            "result": spin,
            "color": color,
            "payout": payout,
            "lost": bet if not won else 0,
            "message": message
        }

class DiceRoll(CasinoGame):
    """Higher/Lower dice game with 4% house edge"""
    
    def __init__(self):
        super().__init__(house_edge=4)
    
    def play(self, bet: int, prediction: str, luck_stat: int = 2) -> Dict:
        """
        Play dice roll
        prediction: 'higher' or 'lower'
        """
        
        if prediction.lower() not in ['higher', 'lower']:
            return {"error": "Invalid prediction. Use 'higher' or 'lower'"}
        
        # Roll two dice
        player_roll = random.randint(1, 6) + random.randint(1, 6)
        opponent_roll = random.randint(1, 6) + random.randint(1, 6)
        
        won = False
        if prediction.lower() == "higher":
            won = player_roll > opponent_roll
        else:  # lower
            won = player_roll < opponent_roll
        
        payout = int(bet * 1.92) if won else 0
        
        message = f"🎲 You rolled: **{player_roll}**\nOpponent rolled: **{opponent_roll}**\n"
        if won:
            message += f"🎉 You won ${payout}!"
        else:
            message += f"❌ You lost ${bet}"
        
        return {
            "success": won,
            "your_roll": player_roll,
            "opponent_roll": opponent_roll,
            "payout": payout,
            "lost": bet if not won else 0,
            "message": message
        }

def get_available_games() -> Dict[str, str]:
    """Get all available casino games"""
    return {
        "coinflip": "💰 Coinflip - 50/50 chance, 2% house edge",
        "slots": "🎰 Slots - 3-reel machine, 10% house edge",
        "blackjack": "🃏 Blackjack - Beat the dealer, 3.5% house edge",
        "roulette": "🎡 Roulette - Spin the wheel, 2.7% house edge",
        "dice": "🎲 Dice Roll - Higher/Lower, 4% house edge",
    }

def gamble(user_id: int, game_type: str, bet: int, **kwargs) -> Dict:
    """
    Execute a casino game
    kwargs varies by game type
    """
    from utils.economy import get_player, add_money, remove_money, update_player
    
    player = get_player(user_id)
    if not player:
        return {"error": "Player not found"}
    
    # Validate bet
    if bet < 5:
        return {"error": "Minimum bet is $5"}
    
    if bet > 20000:
        return {"error": "Maximum bet is $20,000"}
    
    if player["cash"] < bet:
        return {"error": f"Insufficient funds. You have ${player['cash']}"}
    
    # Check tilt protection (5 consecutive losses)
    if player.get("casino_loss_streak", 0) >= 5:
        cooldown_time = datetime.fromisoformat(player.get("casino_cooldown", datetime.now().isoformat()))
        if cooldown_time > datetime.now():
            remaining = (cooldown_time - datetime.now()).total_seconds()
            return {
                "error": "Tilt protection active - you need a break!",
                "remaining_minutes": int(remaining / 60)
            }
    
    # Play game
    result = {}
    if game_type == "coinflip":
        game = Coinflip()
        result = game.play(bet, kwargs.get("prediction", "heads"), player["stats"].get("wealth", 2))
    
    elif game_type == "slots":
        game = Slots()
        result = game.play(bet, player["stats"].get("wealth", 2))
    
    elif game_type == "roulette":
        game = Roulette()
        result = game.play(bet, kwargs.get("bet_type", "red"), kwargs.get("prediction"), player["stats"].get("wealth", 2))
    
    elif game_type == "dice":
        game = DiceRoll()
        result = game.play(bet, kwargs.get("prediction", "higher"), player["stats"].get("wealth", 2))
    
    elif game_type == "blackjack":
        # Simplified blackjack
        result = {
            "success": random.random() < 0.48,  # 48% win rate (3.5% house edge)
            "payout": int(bet * 1.95),
            "message": "🃏 Blackjack result"
        }
    
    if "error" in result:
        return result
    
    # Apply results
    remove_money(user_id, bet, source="gambling")
    
    if result.get("success", False):
        add_money(user_id, result["payout"], source="casino")
        player["casino_won"] = player.get("casino_won", 0) + result["payout"]
        player["casino_win_streak"] = player.get("casino_win_streak", 0) + 1
        player["casino_loss_streak"] = 0
    else:
        player["casino_lost"] = player.get("casino_lost", 0) + bet
        player["casino_loss_streak"] = player.get("casino_loss_streak", 0) + 1
        player["casino_win_streak"] = 0
        
        # Check tilt protection trigger
        if player["casino_loss_streak"] >= 5:
            player["casino_cooldown"] = (datetime.now() + timedelta(minutes=10)).isoformat()
    
    player["casino_wagered"] = player.get("casino_wagered", 0) + bet
    player["loyalty_points"] = player.get("loyalty_points", 0) + int(bet / 100)
    
    update_player(user_id, player)
    
    return result
