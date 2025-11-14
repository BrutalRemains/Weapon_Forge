"""
Test script to test combat with specific, non-random weapons.
"""
from weapon import Weapon
from player import Player
from npc import NPC
from combat import Combat

# Create a bleed weapon manually
bleed_core = {"name": "Sword", "type": "Melee", "base_damage": 6, "speed": 4, "weight": 1}
bleed_attachment = {"name": "Barbed Wire", "bonus_damage": 4, "accuracy": -2, "weight": 2, "type": "melee"}
bleed_grip = {"name": "Lead", "stability": 5, "bounce": 0}
bleed_enchant = {"name": "Blood", "element": "bleed", "power": 4, "status_effect": "bleed"}

bleed_weapon = Weapon(bleed_core, bleed_attachment, bleed_grip, bleed_enchant)

# Create a stun weapon manually
stun_core = {"name": "Sword", "type": "Melee", "base_damage": 6, "speed": 4, "weight": 1}
stun_attachment = {"name": "Spike", "bonus_damage": 3, "accuracy": -1, "weight": 2, "type": "universal"}
stun_grip = {"name": "Lead", "stability": 5, "bounce": 0}
stun_enchant = {"name": "Flame", "element": "fire", "power": 3, "status_effect": "burn"}

stun_weapon = Weapon(stun_core, stun_attachment, stun_grip, stun_enchant)

# Create test combatants
player = Player("TestPlayer", bleed_weapon)
npc = NPC("TestNPC", "Warrior", "Human", stun_weapon)

print("=" * 50)
print("TEST COMBAT: Bleed vs Stun")
print("=" * 50)
print(f"\nPlayer weapon: {bleed_weapon.core['name']} with {bleed_enchant['name']} enchant (bleed)")
print(f"  Total damage: {bleed_weapon.total_damage}")
print(f"  Accuracy: {bleed_weapon.accuracy}")
print(f"\nNPC weapon: {stun_weapon.core['name']} with {stun_enchant['name']} enchant (stun)")
print(f"  Total damage: {stun_weapon.total_damage}")
print(f"  Accuracy: {stun_weapon.accuracy}")
print("\n" + "=" * 50 + "\n")

# Run combat
combat = Combat(player, npc)
winner = combat.simulate_duel()

print("\n" + "=" * 50)
print(f"WINNER: {winner.name}")
print("=" * 50)
