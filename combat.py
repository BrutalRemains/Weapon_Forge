import random

class Commbat:
    def __init__(self, player, npc):
        self.player = player
        self.npc = npc
        self.player_meter = 0
        self.npc_meter = 0

    def resolve_attack(self, attacker, defender):
        weapon = attacker.weapon
        
        # the dice roll here is -3 to 3, the accuracy and weight affecting the overall output of the roll
        roll = weapon.accuracy - weapon.attachment['weight'] + random.randint(-3,3)

        # conditional logic for determining whether there was an actual hit
        if roll >= 5:
            base_damage = weapon.total_damage
            enchant_bonus = weapon.power
            total_damage = base_damage + enchant_bonus

            defender.take_damage(total_damage)
            print(f"{attacker.name} strikes with their {attacker.weapon.core['name']}")
            print(f"The attack does {total_damage}!")

            if weapon.status_effect != "none":
                print(f"The attack appied {weapon.status_effect} to the target!")
        else:
            print(f"The attack misses!")
    
    def simulate_duel(self, attack):
        return False