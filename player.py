from weapon import Weapon, generate_weapon

class Player:
    def __init__(self, name, weapon):
        self.name = name
        self.weapon = weapon
        self.health = 50 # default
        self.status = None # whether a status effect is applied
    
    def is_alive(self):
        return self.health > 0
    
    def take_damage(self, damage):
        self.health = max(self.health - damage, 0)

    def attack(self, target):
        damage = self.weapon.total_damage()
        target.take_damage(damage)

    def weapon_description(self):
        return f"{self.weapon.description('player')}"
    
    def apply_status(self, target, effect):
        target.take_status(effect)
    
    def take_status(self, target, effect):
        self.status = effect

        if self.status == "burn":
            burn_damage = int(self.weapon.total_damage * 0.2)
            self.take_damage(burn_damage)

        if self.status == "bleed":
            bleed_damage = int(self.weapon.total_damage * 0.05)
            self.take_damage(bleed_damage)