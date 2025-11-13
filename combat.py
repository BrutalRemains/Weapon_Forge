import random
import time

class Combat:
    def __init__(self, player, npc):
        self.player = player # player and npc object
        self.npc = npc
        self.player_meter = 0  # meter is an under the hood mechanic based on the speed of the weapon. 
        self.npc_meter = 0
        self.meter_threshold = 10 # once this threshold is hit, player or npc will get an extra turn.

        self.miss_counter = 0 # counter hidden mechanic that will force something to happen if a stalemate happens
    # def attack_miss_flavor(self, attacker):
    #     if self.attacker.weapon.assign_weight() == "light":
    #         return "{attacker.name} "
    
    def resolve_attack(self, attacker, defender):
        weapon = attacker.weapon
        # Convert accuracy/weight into a predictable hit chance (percentage)
        # base = weapon.accuracy - weapon.weight  (can be negative)
        # Map base to percent: 50% + base * 6 (adjust multiplier as needed)
        # Clamp so nothing is 0% or 100% (keep between 5% and 95%)
        base = weapon.accuracy - weapon.weight
        hit_chance = 50 + base * 6
        hit_chance = max(25, min(95, hit_chance))

        hit = random.random() < (hit_chance / 100.0)

        if hit:
            self.miss_counter = 0
            base_damage = weapon.total_damage
            enchant_bonus = weapon.power
            total_damage = base_damage + enchant_bonus

            defender.take_damage(total_damage)
            print(f"{attacker.name} strikes with their {attacker.weapon.core['name']}")
            print(f"{attacker.name}'s attack does {total_damage} damage")

            if weapon.status_effect != "none":
                effect_chance = 20 # status chance

                if random.random() < (effect_chance / 100):
                    # attacker.apply_status(defender)
                    print(f"This attack applied {weapon.status_effect} to the target")
            print()  # blank line after complete attack
        else:
            self.miss_counter += 1
            print(f"{attacker.name} strikes with their {attacker.weapon.core['name']}")
            print(f"{attacker.name}'s attack misses")
            print()  # blank line after complete attack
    
    def simulate_duel(self):    
        while self.player.is_alive() and self.npc.is_alive():
            self.player_meter += self.player.weapon.speed
            self.npc_meter += self.npc.weapon.speed

            if self.player_meter >= self.meter_threshold:
                self.resolve_attack(self.player, self.npc)
                self.player_meter = self.player_meter % self.meter_threshold 
                time.sleep(1.4)
            
            # Check for stalemate after each attack
            if self.miss_counter >= 5:
                return self.stalemate_machina()

            if self.npc.is_alive() and self.npc_meter >= self.meter_threshold:
                self.resolve_attack(self.npc, self.player)
                self.npc_meter = self.npc_meter % self.meter_threshold
                time.sleep(1.4)
            
            # Check for stalemate after each attack
            if self.miss_counter >= 6:
                return self.stalemate_machina()
            
        winner = self.player if self.player.is_alive() else self.npc
        return winner

    def stalemate_machina(self):
        if self.miss_counter >= 5:
            print("The Great Smith grows impatient with this foolish display!\n")
            time.sleep(1.4)
            combatants = [self.player, self.npc]
            winner = random.choice(combatants)
            loser = self.npc if winner == self.player else self.player
            
            print(f"{winner.name} seizes the moment of divine intervention!")
            time.sleep(1.4)
            print(f"{winner.name} strikes {loser.name} down with their {winner.weapon.core['name']}!\n")
            loser.take_damage(loser.health)  # kill the loser
            return winner