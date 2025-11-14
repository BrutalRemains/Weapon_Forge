import random
import math
class StatusEffect:
    def __init__(self, name, duration=1):
        self.name = name
        self.duration = duration
    
    def apply(self, target):
        pass

    def tick(self, target):
        self.duration -= 1
        return self.duration <= 0 # this will return true when expired; useful for adjustments
    
class Burn(StatusEffect):
    def __init__(self, source):
        super().__init__(name="burn", duration=1)
        self.source = source # player or npc class

    def apply(self, target):
        burn_damage = math.ceil(self.source.weapon.total_damage * 0.2)
        target.take_damage(burn_damage)
        print(f"{target.name} suffers {burn_damage} burn damage!")

    def tick(self, target):
        return super().tick(target)

class Bleed(StatusEffect):
    def __init__(self, source):
        super().__init__(name="bleed", duration=random.randint(3,5))
        self.source = source

    def tick(self, target):
        bleed_damage = math.ceil(self.source.weapon.total_damage * 0.05)
        target.take_damage(bleed_damage)
        print(f"{target.name} suffers {bleed_damage} bleed damage!")
        return super().tick(target)

class Stun(StatusEffect):
    def __init__(self, source):
        super().__init__(name="stun", duration=random.randint(1,3))
        self.source = source

class Chill(StatusEffect):
    def __init__(self, source):
        super().__init__(name="chill", duration=2)
        self.source = source

    def apply(self, target):
        target.meter_threshold += 5

    def tick(self,target):
        expired = super().tick(target)
        if expired:
            target.meter_threshold -= 5
          # print(f"{target.name} shakes off the chill!")
        return expired
