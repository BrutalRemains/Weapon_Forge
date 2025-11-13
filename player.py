from weapon import Weapon, generate_weapon

class Player:
    def __init__(self, name, weapon):
        self.name = name
        self.weapon = weapon
        self.health = 50 # default
    
    def is_alive(self):
        return self.health > 0
    
    def take_damage(self, damage):
        self.health = max(self.health - damage, 0)

    def attack(self, target):
        damage = self.weapon.total_damage()
        target.take_damage(damage)

    def weapon_description(self):
        return f"{self.weapon.description('player')}"