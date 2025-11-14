import random
from weapon import *
from statuseffect import *

roles = ["Bandit", "Warrior", "Commoner", "Hunter", "Savage"]
names = ["Moriaty", "Unglaus", "Sable", "Annie", "Leonhart", "Eren", "Hange", "Kazuto", "Lisbeth", "Lochlann"]
races = ["Skeleton", "Human", "Elf", "Dwarf", "Fungaloid", "Squirrelkin"]

class NPC:
    def __init__(self, name, role, race, weapon):
        self.name = name
        self.role = role
        self.race = race
        self.weapon = weapon
        self.health = 100

    def is_alive(self):
        return self.health > 0

    def take_damage(self, amount):
        self.health = self.health - amount

    def attack(self, target):
        damage = self.weapon.total_damage()
        target.take_damage(damage)

    def description(self):        
        weapon_text = self.weapon.description("npc")
        return (f"\n{self.name} the {self.race} {self.role} appears before you!\n"
                f"{weapon_text}\n")

    def take_status(self, status_effect, source):
        status_effects = {
            "burn": Burn,
            "bleed": Bleed,
            #"stun": Stun,
            #"chill": Chill
        }

        if status_effect in status_effects:
            effect = status_effects[status_effect](source)
            effect.apply(self)
            self.status_effects.append(effect)
    
    def apply_status(self, status_effect, target):
        target.take_status(status_effect, self)                
    
def generate_npc():
    name = random.choice(names)
    role = random.choice(roles)
    race = random.choice(races)
    weapon = generate_weapon()
    return NPC(name, role, race, weapon)