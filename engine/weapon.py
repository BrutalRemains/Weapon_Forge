import random
import json

# cores are the weapon bases, organized by a list of dictionaries
with open("databases/weapon_cores.json", "r") as file:
    cores = json.load(file)

# attachments will be rolled onto every weapon, adding either damage or accuracy or removing them. some will be melee only and some will be ranged only# some will be melee only and some will be ranged only
with open("databases/attachments.json", "r") as file:
    attachments = json.load(file)

# grips will affect a greater "chance to hit" ratio
with open("databases/grips.json", "r") as file:
    grips = json.load(file)

# enchants will simply be added stats
with open("databases/enchants.json", "r") as file:
    enchants = json.load(file)

class Weapon:
    def __init__(self, core, attachment, grip, enchant):
        self.core = core
        self.attachment = attachment
        self.grip = grip
        self.enchant = enchant
        self.type = core["type"]

        # derived stats
        self.total_damage = core["base_damage"] + attachment["bonus_damage"]
        self.speed = core["speed"]
        self.accuracy = attachment["accuracy"] + grip["stability"] - grip["bounce"]
        self.element = enchant["element"]
        self.power = enchant["power"]
        self.status_effect = enchant["status_effect"]
        self.weight = core["weight"] + attachment["weight"]

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
        
    def assign_weight(self):
        if self.weight <= 1:
            return "light"
        elif self.weight >= 2 and self.weight <= 4:
            return "normal"
        elif self.weight >= 5 and self.weight <= 7:
            return "heavy"
    
    def attachment_flavor(self):
        # attachments that are universal should behave differently depending on the weapon type
        if self.attachment["name"] == "none":
            return "."
        
        if self.attachment["name"] == "Spike" and self.core["type"] == "Ranged":
            return f", its accompanying projectiles laden with spikes."
        
        a_an_plural = ""
        # english important
        if self.attachment['name'][0] == "A" or self.attachment['name'][0] == "E" or self.attachment['name'][0] == "I" or self.attachment['name'][0] == "O" or self.attachment['name'][0] == "U": 
            a_an_plural = f"an {self.attachment['name'].lower()}." 
        elif self.attachment['name'][-1] == "s" or self.attachment['name'] == "Barbed Wire":
            a_an_plural = f"{self.attachment['name'].lower()}."
        else:
            a_an_plural = f"a {self.attachment['name'].lower()}."
        
        return f" attached with {a_an_plural}"

    def description(self, perspective="npc"):
        #adjustment for no attachment
        attachment_text = self.attachment_flavor()

        enchant_text = (f"It is {self.enchant['name'].lower()} enchanted.\n"
                        if self.enchant['name'] != "none" else "")
        
        a_or_an = ""
        if self.core['name'][0] == "A" or self.core['name'][0] == "E" or self.core['name'][0] == "I" or self.core['name'][0] == "O" or self.core['name'][0] == "U":
            a_or_an = f"an {self.core['name'].lower()}{attachment_text}"
        else:
            a_or_an = f"a {self.core['name'].lower()}{attachment_text}"

        if perspective == "player":   
            return(f"You wield {a_or_an}\n"
            f"Running your fingers across the base, you notice it has as {self.grip['name'].lower()} grip.\n"
            f"You close your eyes, channel your inner conciousness and attune to the weapon.\n" 
            f"{enchant_text}"
            f"It could be considered {self.assess_strength} and {self.assess_accuracy}.")
        
        if perspective == "npc":
            return f"They appear to wield {a_or_an}\n"

        if perspective == "hof": #hall of fame
            return f"Weapon: {self.core["name"]}, {self.grip['name']} grip,{attachment_text} {enchant_text}"


def generate_weapon():
    core = random.choice(cores)
    valid_attachments = [a for a in attachments if (a["type"] == core["type"] or a["type"] == "Universal") and not (core.get("subtype") == "crude" and a.get("subtype") == "not crude")] # matches attachments to its appropriate possible type, excludes not_crude for crude weapons
    attachment = random.choice(valid_attachments)
    grip = random.choice(grips)
    enchant = random.choice(enchants)
    return Weapon(core, attachment, grip, enchant)
    
