import random
from weapon import Weapon, generate_weapon
from statuseffect import *

class Player:
    def __init__(self, name, weapon):
        self.name = name
        self.weapon = weapon
        self.health = 50 # default
        self.status = []
    
    def is_alive(self):
        return self.health > 0
    
    def take_damage(self, damage):
        self.health = max(self.health - damage, 0)

    def attack(self, target):
        damage = self.weapon.total_damage()
        target.take_damage(damage)

    def weapon_description(self):
        return f"{self.weapon.description('player')}"
    
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