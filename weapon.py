# cores are the weapon bases, organized by a list of dictionaries/
cores = [{"name": "Sword", "type":"Melee", "base_damage": 6, "speed": 4}, 
         {"name": "Bow", "type":"Ranged", "base_damage": 6, "speed": 4},
         {"name": "Hammer", "type":"Melee", "base_damage": 10, "speed": 2},
         {"name": "Rifle", "type":"Ranged", "base_damage": 10, "speed": 2},
         {"name": "Dagger", "type":"Melee", "base_damage": 4, "speed": 6},
         {"name": "Pistol", "type":"Ranged", "base_damage": 4, "speed": 6}]

# attachments will be rolled onto every weapon, adding either damage or accuracy or removing them.
# some will be melee only and some will be ranged only
attachments = [{"name": "Bayonet", "bonus_damage": 2, "accuracy": 0, "weight": 1},
               {"name": "Scope", "bonus_damage": 0, "accuracy": 3, "weight": 1},
               {"name": "Spike", "bonus_damage": 3, "accuracy": -1, "weight": 2},
               {"name": "Axe Head", "bonus_damage": 6, "accuracy": -3, "weight": 4},
               {"name": "Barbed Wire", "bonus_damage":4, "accuracy": -2, "weight": 2}]

# grips will affect a greater "chance to hit" ratio
grips = [{"name": "Leather Wrap", "stability": 3, "bounce": -1},
         {"name": "Lead Wrap", "stability": 5, "bounce": 0},
         {"name": "Wooden", "stability": 4, "bounce": -2},
         {"name": "Construction Paper", "stability": 0, "bounce": -7}]

# enchants will simply be added stats
enchants = [{"name": "Flame", "element": "fire", "power": 3, "status_effect": "burn"},
            {"name": "Frost", "element": "ice", "power": 2, "status_effect": "chill"},
            {"name": "Lightning", "element": "electric", "power": 4, "status_effect": "stun"}]