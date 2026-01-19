#!/usr/bin/env python3
"""
Test script to verify character assignment system works correctly
Run this before deploying to test character tracking
"""

import json
import os
import sys

# Test paths
CHARS_USED_PATH = "data/characters_used.json"
PLAYERS_PATH = "data/players.json"

def test_character_system():
    """Test the character assignment system"""
    
    print("🧪 Testing Character Assignment System")
    print("=" * 50)
    
    # Test 1: Check if files exist
    print("\n✓ Test 1: File creation")
    if os.path.exists(CHARS_USED_PATH):
        print(f"  ✅ {CHARS_USED_PATH} exists")
    else:
        print(f"  ⚠️  {CHARS_USED_PATH} not yet created (will be created on first setup)")
    
    if os.path.exists(PLAYERS_PATH):
        print(f"  ✅ {PLAYERS_PATH} exists")
    else:
        print(f"  ⚠️  {PLAYERS_PATH} not yet created (will be created on first account)")
    
    # Test 2: Check imports
    print("\n✓ Test 2: Module imports")
    try:
        from utils.economy import (
            get_available_character, 
            mark_character_used,
            load_used_characters,
            save_used_characters
        )
        print("  ✅ All functions imported successfully")
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        return False
    
    # Test 3: Test get_available_character
    print("\n✓ Test 3: Get available character")
    try:
        char = get_available_character()
        if char:
            print(f"  ✅ Got available character: {char}")
        else:
            print(f"  ⚠️  No available characters (all 30 assigned)")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 4: Test character marking
    print("\n✓ Test 4: Mark character as used")
    try:
        test_char = "TestCharacter"
        mark_character_used(test_char)
        used = load_used_characters()
        if test_char in used:
            print(f"  ✅ Character '{test_char}' marked as used")
        else:
            print(f"  ❌ Character not marked")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 5: Verify no duplicates
    print("\n✓ Test 5: Check for duplicate assignments")
    try:
        used = load_used_characters()
        if len(used) == len(set(used)):
            print(f"  ✅ No duplicate characters ({len(used)} unique)")
        else:
            duplicates = [char for char in used if used.count(char) > 1]
            print(f"  ❌ Found duplicates: {duplicates}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 6: Verify account creation format
    print("\n✓ Test 6: Check account structure")
    if os.path.exists(PLAYERS_PATH):
        try:
            with open(PLAYERS_PATH, 'r') as f:
                players = json.load(f)
            
            if players:
                first_player_id = list(players.keys())[0]
                player = players[first_player_id]
                
                required_fields = ['character', 'username', 'cash', 'bank_balance', 'stats']
                missing = [field for field in required_fields if field not in player]
                
                if not missing:
                    print(f"  ✅ Player structure valid")
                    print(f"     Character: {player['character']}")
                    print(f"     Cash: ${player['cash']:,}")
                else:
                    print(f"  ❌ Missing fields: {missing}")
                    return False
        except Exception as e:
            print(f"  ❌ Error reading players: {e}")
            return False
    else:
        print("  ⚠️  No players yet (create one with /setup first)")
    
    print("\n" + "=" * 50)
    print("✅ All tests passed!")
    print("\nNow test in Discord:")
    print("  1. Run /setup (should get random character)")
    print("  2. Run /profile (verify character assigned)")
    print("  3. Have another user run /setup (different character)")
    print("  4. Check characters_used.json has both characters")
    
    return True

if __name__ == "__main__":
    success = test_character_system()
    sys.exit(0 if success else 1)
