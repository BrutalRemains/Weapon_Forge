from weapon import Weapon, generate_weapon

class Player:
    def __init__(self, name, weapon):
        self.name = name
        self.weapon = weapon
        self.health = 100 # default

    def weapon_description(self):
        return self.weapon.description("player")