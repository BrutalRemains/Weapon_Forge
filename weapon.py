import random

# cores are the weapon bases, organized by a list of dictionaries
cores = [{"name": "Sword", "type":"Melee", "base_damage": 6, "speed": 4}, 
         {"name": "Bow", "type":"Ranged", "base_damage": 6, "speed": 4},
         {"name": "Hammer", "type":"Melee", "base_damage": 10, "speed": 2},
         {"name": "Rifle", "type":"Ranged", "base_damage": 10, "speed": 2},
         {"name": "Dagger", "type":"Melee", "base_damage": 4, "speed": 6},
         {"name": "Pistol", "type":"Ranged", "base_damage": 4, "speed": 6}]

# attachments will be rolled onto every weapon, adding either damage or accuracy or removing them. some will be melee only and some will be ranged only# some will be melee only and some will be ranged only
attachments = [{"name": "Bayonet", "bonus_damage": 2, "accuracy": 0, "weight": 1, "type":"ranged"},
               {"name": "Scope", "bonus_damage": 0, "accuracy": 3, "weight": 1, "type":"ranged"},
               {"name": "Spike", "bonus_damage": 3, "accuracy": -1, "weight": 2, "type":"universal"},
               {"name": "Axe Head", "bonus_damage": 6, "accuracy": -3, "weight": 4, "type":"melee"},
               {"name": "Barbed Wire", "bonus_damage": 4, "accuracy": -2, "weight": 2, "type":"melee"},
               {"name": "none", "bonus_damage": 0, "accuracy": 0, "weight": 0, "type":"universal"}]

# grips will affect a greater "chance to hit" ratio
grips = [{"name": "Leather", "stability": 3, "bounce": -1},
         {"name": "Lead", "stability": 5, "bounce": 0},
         {"name": "Wooden", "stability": 4, "bounce": -2},
         {"name": "Construction Paper", "stability": 0, "bounce": 7}]

# enchants will simply be added stats
enchants = [{"name": "Flame", "element": "fire", "power": 3, "status_effect": "burn"},
            {"name": "Frost", "element": "ice", "power": 2, "status_effect": "chill"},
            {"name": "Lightning", "element": "electric", "power": 4, "status_effect": "stun"},
            {"name": "Blood", "element": "bleed", "power": 4, "status_effect": "bleed"},
            {"name": "none", "element": "none", "power": 0, "status_effect": "none"},]

class Weapon:
    def __init__(self, core, attachment, grip, enchant):
        self.core = core
        self.attachment = attachment
        self.grip = grip
        self.enchant = enchant

        # derived stats
        self.total_damage = core["base_damage"] + attachment["bonus_damage"]
        self.speed = core["speed"]
        self.accuracy = attachment["accuracy"] + grip["stability"] - grip["bounce"]
        self.element = enchant["element"]
        self.power = enchant["power"]
        self.status_effect = enchant["status_effect"]

        self.assess_strength = self.assign_strength()
        self.assess_accuracy = self.assign_accuracy()

    def assign_strength(self):
        if self.total_damage >= 10:
            return "strong"
        elif self.total_damage >= 6 and self.total_damage < 10:
            return "average"
        else:
            return "weak"
    def assign_accuracy(self):
        if self.accuracy >= 7:
            return "accurate"
        elif self.accuracy >= 3 and self.accuracy < 7:
            return "averagely accurate"
        else:
            return "inaccurate"    
    
    def attachment_flavor(self):
        # attachments that are universal should behave differently depending on the weapon type
        if self.attachment["name"] == "none":
            return "."
        
        if self.attachment["name"] == "Spike" and self.core["type"] == "Ranged":
            return f", its accompanying projectiles laden with spikes."
        return f" attached with a {self.attachment['name'].lower()}."

    def description(self, perspective="npc"):
        #adjustment for no attachment
        attachment_text = self.attachment_flavor()

        enchant_text = (f"It is {self.enchant['name'].lower()} enchanted.\n"
                        if self.enchant['name'] != "none" else "")
        
        if perspective == "player":
            return(f"You wield a {self.core['name'].lower()}{attachment_text}\n"
            f"Running your fingers across the grip, you notice its wrapped in {self.grip['name'].lower()}.\n"
            f"You close your eyes, channel your inner conciousness and attune to the weapon.\n" 
            f"{enchant_text}"
            f"It could be considered {self.assess_strength} and {self.assess_accuracy}.")
        
        if perspective == "npc":
            return f"They appear to wield a {self.core['name'].lower()}{attachment_text}\n"



def generate_weapon():
    core = random.choice(cores)
    valid_attachments = [a for a in attachments if a["type"] == core["type"] or a["type"] ==  "universal"] 
    attachment = random.choice(valid_attachments)
    grip = random.choice(grips)
    enchant = random.choice(enchants)
    return Weapon(core, attachment, grip, enchant)
    
