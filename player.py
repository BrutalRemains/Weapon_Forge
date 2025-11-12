from weapon import Weapon, generate_weapon

class Player:
    def __init__(self, name, weapon):
        self.name = name
        self.weapon = weapon
        self.health = 100 # default

    def weapon_description(self):
        return (f"You are {self.name}, a test subject for the the Great Smith\n"
                f"{self.weapon.description("player")}")
    
    def is_alive(self):
        return self.health > 0
    
    def take_damage(self, amount):
        self.health = self.health - amount