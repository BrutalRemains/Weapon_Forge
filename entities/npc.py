import json
import random
from engine.weapon import *
from engine.statuseffect import *
from entities.player import Player

# names npc's could have
with open("databases/names.json", "r") as file:
    names = json.load(file)

# what type the npc can be, does not affect game stats
with open("databases/roles.json", "r") as file:
    roles = json.load(file)

# what race the npc can be, does not affect game stats
with open("databases/races.json", "r") as file:
    races = json.load(file)

class NPC(Player):
    def __init__(self, name, weapon, role, race):
        super().__init__(name, weapon)
        self.role = role  
        self.race = race

    def description(self):        
        weapon_text = self.weapon.description("npc")
        return (f"\n{self.name} the {self.race} {self.role} appears before you!\n"
                f"{weapon_text}\n")


def generate_npc():
    name = random.choice(names)
    role = random.choice(roles)
    race = random.choice(races)
    weapon = generate_weapon()
    return NPC(name, weapon, role, race)