import random
class StatusEffect:
    def __init__(self, duration=1):
        self.duration = duration
    
    def apply(self):
        pass

    def tick(self):
        self.duration -= 1
        return self.duration <= 0
    
class Burn(StatusEffect):
    def __init__(self, source):
        super().__init__(duration=1)
        self.source = source # player or npc class

    def apply(self, target):
        burn_damage = int(self.weapon.total_damage * 0.2)
        target.take_damage(burn_damage)

class Bleed(StatusEffect):
    def __init__(self, source):
        super().__init__(duration=random.randint(1,3))
        self.source = source

    def apply(self, target):
        bleed_damage = int(self.weapon.total_damage * 0.05)
        target.take_damage(bleed_damage)