import random
from weapon import *

roles = ["Human Bandit", "Human Warrior", "Human Commoner", "Human Hunter", "Skeleton Warrior", "Skeletal Hunter"]
names = ["Moriaty", "Unglaus", "Sable", "Annie", "Leonhart", "Eren", "Hange", "Kazuto", "Lisbeth", "Lochlann"]

class NPC:
    def __init__(self, name, role, weapon):
        self.name = name
        self.role = role
        self.weapon = weapon

    def description(self):        
        weapon_text = self.weapon.description("npc")
        return (f"\n{self.name} the {self.role.lower()} appears before you!\n"
                f"{weapon_text}\n")
                
    
def generate_npc():
    name = random.choice(names)
    role = random.choice(roles)
    weapon = generate_weapon()
    return NPC(name, role, weapon)