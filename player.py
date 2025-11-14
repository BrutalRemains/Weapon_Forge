import random
from weapon import Weapon, generate_weapon
from statuseffect import *

class Player:
    def __init__(self, name, weapon):
        self.name = name
        self.weapon = weapon
        self.health = 50 # default
        self.status_effects = []
    
    def is_alive(self):
        return self.health > 0
    
    def take_damage(self, damage):
        self.health = max(self.health - damage, 0)

    def attack(self, target):
        damage = self.weapon.total_damage()
        target.take_damage(damage)

    def weapon_description(self):
        return f"{self.weapon.description('player')}"
    
    def take_status(self, effect_name, source):
        effect_map = {
            "burn": Burn,
            "bleed": Bleed,
            "stun": Stun,
            "chill": Chill
        }

        if effect_name in effect_map:
            effect = effect_map[effect_name](source) # takes the status effect string from the dictionary, builds the associated class: Burn(source)
            effect.apply(self)
            self.status_effects.append(effect)
    
    def apply_status(self, target, status_effect):
        target.take_status(status_effect, self)

    def tick_status(self):
        expired = []
        for effect in self.status_effects:
            if effect.tick(self):
                expired.append(effect)
        for effect in expired:
            print(f"{self.name}'s {effect.name} wore off!")        
            self.status_effects.remove(effect)
