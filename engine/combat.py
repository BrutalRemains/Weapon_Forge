import random
import time


class Combat:
    def __init__(self, player, npc):
        self.player = player # player and npc object
        self.npc = npc
        self.player_meter = 0  # meter is an under the hood mechanic based on the speed of the weapon. 
        self.npc_meter = 0

        self.miss_counter = 0 # counter hidden mechanic that will force something to happen if a stalemate happens
        self.player_damage_dealt = 0
        self.npc_damage_dealt = 0
    
    def resolve_attack(self, attacker, defender):
        weapon = attacker.weapon
        # Convert accuracy/weight into a % based hit chance (percentage)
        # Map base to percent: 50% + base * 6 (adjust multiplier as needed)
        
        base = weapon.accuracy - weapon.weight
        hit_chance = 50 + base * 6
        hit_chance = max(25, min(95, hit_chance)) #25% chance to hit is the bare minimum no matter what. Even at 25, stalemates can occur and created a negative experience

        hit = random.random() < (hit_chance / 100.0)
        if hit:
            self.miss_counter = 0 #resets to 0 if someone hits
            base_damage = weapon.total_damage
            enchant_bonus = weapon.power
            total_damage = base_damage + enchant_bonus

            defender.take_damage(total_damage)
            print(f"{attacker.name} strikes with their {attacker.weapon.core['name']}")
            print(f"{attacker.name}'s attack does {total_damage} damage")

            if weapon.status_effect != "none": # effect application inn combat
                effect_chance = 20 # status chance

                if random.random() < (effect_chance / 100):
                    print(f"This attack applied {weapon.status_effect} to the target")
                    attacker.apply_status(defender, weapon.status_effect)

            if attacker == self.player:
                self.player_damage_dealt += total_damage
            else:
                self.npc_damage_dealt += total_damage # for tracking total dammge over the duel. Mainly used for losing side, since health is static
        else:
            self.miss_counter += 1
            print(f"{self.miss_flavor(attacker)}")
    
    def simulate_duel(self):    
        while self.player.is_alive() and self.npc.is_alive():
            if self.player.is_stunned():
                self.player_meter = 0 # if player is affected by stun, their meter resets to 0
            else:    
                self.player_meter += self.player.weapon.speed # the mechanic which determines taking a turn
            
            if self.npc.is_stunned():
                self.npc_meter = 0
            else:
                self.npc_meter += self.npc.weapon.speed

            if self.player_meter >= self.player.meter_threshold:
                self.resolve_attack(self.player, self.npc)
                print()  
                self.npc.tick_status()  # apply status effects to the defender after attack
                self.player_meter = self.player_meter % self.player.meter_threshold 
                time.sleep(1.4)
            
            # Check for stalemate after each attack
            if self.miss_counter >= 5:
                return self.stalemate_machina()

            if self.npc.is_alive() and self.npc_meter >= self.npc.meter_threshold:
                self.resolve_attack(self.npc, self.player)
                print()  # blank line before status effects
                self.player.tick_status()  # apply status effects to the defender after attack
                self.npc_meter = self.npc_meter % self.npc.meter_threshold
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
    
    def miss_flavor(self, attacker):
        if attacker == self.npc: #third person
            if attacker.weapon.assign_weight() == "light" and attacker.weapon.type == "melee":
                return (f"{attacker.name} strikes swiftly, but catches air!")
            elif attacker.weapon.assign_weight() == "normal" and attacker.weapon.type == "melee":
                return (f"{attacker.name} swings their {attacker.weapon.name} and misses!")
            elif attacker.weapon.assign_weight() == "heavy" and attacker.weapon.type == "melee":
                return (f"{attacker.name} lunges with a lumbering blow, leaving enough time for you to get out of the way")
            elif attacker.weapon.type == "ranged":
                return (f"{attacker.name}'s shot whizzes past!")
            elif attacker.weapon.assign_weight() == "heavy" and attacker.weapon.type == "thrown":
                return (f"With a laboring toss, {attacker.name} is just off the mark!")
            elif attacker.weapon.assign_weight() == "normal" and attacker.weapon.type == "thrown":
                return (f"{attacker.name}'s throw is just wayward!")
            elif attacker.weapon.assign_weight() == "light" and attacker.weapon.type == "thrown":
                return (f"With a toss too swift for their own good, the throw misses the target completely!")
        
        if attacker == self.player:
            if attacker.weapon.assign_weight() == "light" and attacker.weapon.type == "melee":
                return (f"You strike swiftly, but catch air!")
            elif attacker.weapon.assign_weight() == "normal" and attacker.weapon.type == "melee":
                return (f"You swing your {attacker.weapon.name} and miss!")
            elif attacker.weapon.assign_weight() == "heavy" and attacker.weapon.type == "melee":
                return (f"You lunge with a lumbering blow, leaving enough time for you to get out of the way")
            elif attacker.weapon.type == "ranged":
                return (f"Your shot whizzes past, your accuracy just off!")
            elif attacker.weapon.assign_weight() == "heavy" and attacker.weapon.type == "thrown":
                return (f"With a laboring toss, you are just off the mark!")
            elif attacker.weapon.assign_weight() == "normal" and attacker.weapon.type == "thrown":
                return (f"Your throw is just wayward!")
            elif attacker.weapon.assign_weight() == "light" and attacker.weapon.type == "thrown":
                return (f"With a toss too swift for your own good, your throw misses the target completely!")


