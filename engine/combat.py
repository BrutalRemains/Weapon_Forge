import random
import time


class Combat:
    def __init__(self, player, npc):
        self.player = player # player and npc object
        self.npc = npc
        self.player_meter = 0  # meter is an under the hood mechanic based on the speed of the weapon. 
        self.npc_meter = 0

        self.miss_counter = 0 # counter hidden mechanic that will force something to happen if a stalemate happens
        self.player_damage_dealt = 0
        self.npc_damage_dealt = 0
    
    def resolve_attack(self, attacker, defender):
        events = []
        weapon = attacker.weapon
        # Convert accuracy/weight into a % based hit chance (percentage)
        # Map base to percent: 50% + base * 6 (adjust multiplier as needed)
        
        base = weapon.accuracy - weapon.weight
        hit_chance = 50 + base * 6
        hit_chance = max(25, min(95, hit_chance)) #25% chance to hit is the bare minimum no matter what. Even at 25, stalemates can occur and created a negative experience

        hit = random.random() < (hit_chance / 100.0)
        if hit:
            self.miss_counter = 0 #resets to 0 if someone hits
            base_damage = weapon.total_damage
            enchant_bonus = weapon.power
            total_damage = base_damage + enchant_bonus

            defender.take_damage(total_damage)
            events.append({
                "type": "hit",
                "attacker": attacker,
                "flavor": self.hit_flavor(attacker, defender),
                "damage": total_damage
            })

            if weapon.status_effect != "none": # effect application inn combat
                effect_chance = 20 # status chance

                if random.random() < (effect_chance / 100):                    
                    attacker.apply_status(defender, weapon.status_effect)
                    
                    events.append({
                    "type": "status_applied",
                    "effect": weapon.status_effect,
                    "target_name": defender.name,
                    })

            if attacker == self.player:
                self.player_damage_dealt += total_damage
            else:
                self.npc_damage_dealt += total_damage # for tracking total dammge over the duel. Mainly used for losing side, since health is static
        else:
            self.miss_counter += 1
            events.append({
                "type": "miss",
                "attacker": attacker,
                "flavor": self.miss_flavor(attacker),
            })
        return events
    # simulate_duel exists for maintaining cli compatibility
    def simulate_duel(self):    
        while self.player.is_alive() and self.npc.is_alive():
            if self.player.is_stunned():
                self.player_meter = 0 # if player is affected by stun, their meter resets to 0
            else:    
                self.player_meter += self.player.weapon.speed # the mechanic which determines taking a turn
            
            if self.npc.is_stunned():
                self.npc_meter = 0
            else:
                self.npc_meter += self.npc.weapon.speed

            # player hits
            if self.player_meter >= self.player.meter_threshold:
                evs = self.resolve_attack(self.player, self.npc)
                print()                
                for ev in evs:
                    t = ev.get("type")
                    if t == "hit":
                        print(ev.get("flavor", "A hit lands!"))
                        dmg = ev.get("damage", 0)
                        print(f"It deals {dmg} damage!")
                    elif t == "miss":
                        print(ev.get("flavor", "An attack misses."))
                    elif t == "status_applied":
                        eff = ev.get("effect")
                        tgt = ev.get("target_name") 
                    elif t == "info":
                        print(ev.get("msg", "Info"))
                    else:
                        print(ev)
                
                msgs = self.npc.tick_status() or []
                for m in msgs:
                    print(m)
                
                self.player_meter = self.player_meter % self.player.meter_threshold 
                input(f"Current Health: {self.player.health} (enter)")
            

            # npc hits
            if self.npc_meter >= self.npc.meter_threshold:
                evs = self.resolve_attack(self.npc, self.player)
                print()                
                for ev in evs:
                    t = ev.get("type")
                    if t == "hit":
                        print(ev.get("flavor", "A hit lands!"))
                        dmg = ev.get("damage", 0)
                        print(f"It deals {dmg} damage!")
                    elif t == "miss":
                        print(ev.get("flavor", "An attack misses."))
                    elif t == "status_applied":
                        eff = ev.get("effect")
                        tgt = ev.get("target_name") or (ev.get("target").name if ev.get("target") else 'Target')
                        print(f"{tgt} is afflicted with {eff}!")
                    elif t == "info":
                        print(ev.get("msg", "Info"))
                    else:
                        print(ev)
                
                msgs = self.player.tick_status() or []
                for m in msgs:
                    print(m)
                
                self.npc_meter = self.npc_meter % self.npc.meter_threshold 
                input(f"Current Health: {self.player.health} (enter)")
            
            # Check for stalemate after each attack
            if self.miss_counter >= 6:
                return self.stalemate_machina()
            
        winner = self.player if self.player.is_alive() else self.npc
        return winner
    
    def step(self):
        # an essential refactor of simulate duel that using no blocking. it returns a list of events from the duel

        events = []
        # normal meter advance, keeping stun in mind
        if self.player.is_stunned():
            self.player_meter = 0 # if player is affected by stun, their meter resets to 0
        else:    
            self.player_meter += self.player.weapon.speed # the mechanic which determines taking a turn
            
        if self.npc.is_stunned():
            self.npc_meter = 0
        else:
            self.npc_meter += self.npc.weapon.speed
        
        # player attack
        if self.player_meter >= self.player.meter_threshold and self.player.is_alive() and self.npc.is_alive():
            evs = self.resolve_attack(self.player,self.npc) #now resolve attacks returns events list, which we capture here
            events.extend(evs)

            # apply defender status ticks
            msgs = self.npc.tick_status()
            for m in msgs:
                events.append({"type": "info", "msg": m})
            
            self.player_meter %= self.player.meter_threshold
        
        # stalemate machina check
        if self.miss_counter >= 5:
            winner = random.choice([self.player, self.npc])
            loser = self.npc if winner == self.player else self.player
            events.append[{"type": "info", "msg": "The Great Smith grows impatient with this foolish display!"}]
            events.append[{"type": "stalemate", "winner": winner}]
            events.append[{"type": "info", "msg": f"{winner.name} seizes the moment of divine intervention!"}]
            events.append[{"type": "info", "msg": f"{winner.name} strikes {loser.name} down with their {winner.weapon.core['name']}!"}]
            self.miss_counter = 0
            return events
        
        # NPC attack
        if self.npc_meter >= self.player.meter_threshold and self.player.is_alive() and self.npc.is_alive():
            evs = self.resolve_attack(self.npc,self.player) #now resolve attacks returns events list, which we capture here
            events.extend(evs)

            # apply defender status ticks
            msgs = self.player.tick_status()
            for m in msgs:
                events.append({"type": "info", "msg": m})
            
            self.npc_meter %= self.npc.meter_threshold
        
        # we do this again because now each thing is happening "ahead of time"
        if self.miss_counter >= 5:
            winner = random.choice([self.player, self.npc])
            loser = self.npc if winner == self.player else self.player
            events.append[{"type": "info", "msg": "The Great Smith grows impatient with this foolish display!"}]
            events.append[{"type": "stalemate", "winner": winner}]
            events.append[{"type": "info", "msg": f"{winner.name} seizes the moment of divine intervention!"}]
            events.append[{"type": "info", "msg": f"{winner.name} strikes {loser.name} down with their {winner.weapon.core['name']}!"}]
            self.miss_counter = 0
            
        return events
            


    def stalemate_machina(self):
        if self.miss_counter >= 5:
            print("The Great Smith grows impatient with this foolish display!\n")
            input()
            combatants = [self.player, self.npc]
            winner = random.choice(combatants)
            loser = self.npc if winner == self.player else self.player
            
            print(f"{winner.name} seizes the moment of divine intervention!")
            input()
            print(f"{winner.name} strikes {loser.name} down with their {winner.weapon.core['name']}!\n")
            loser.take_damage(loser.health)  # kill the loser
            return winner
    
    def miss_flavor(self, attacker):
        if attacker == self.npc: # third person perspective
            if attacker.weapon.assign_weight() == "light" and attacker.weapon.type == "Melee":
                return (f"{attacker.name} strikes swiftly, but catches air!")
            elif attacker.weapon.assign_weight() == "normal" and attacker.weapon.type == "Melee":
                return (f"{attacker.name} swings their {attacker.weapon.core['name']} and misses!")
            elif attacker.weapon.assign_weight() == "heavy" and attacker.weapon.type == "Melee":
                return (f"{attacker.name} lunges with a lumbering blow, leaving enough time for you to get out of the way")
            elif attacker.weapon.type == "Ranged":
                return (f"{attacker.name}'s shot whizzes past!")
            elif attacker.weapon.assign_weight() == "heavy" and attacker.weapon.type == "Thrown":
                return (f"With a laboring toss, {attacker.name} is just off the mark!")
            elif attacker.weapon.assign_weight() == "normal" and attacker.weapon.type == "Thrown":
                return (f"{attacker.name}'s throw is just wayward!")
            elif attacker.weapon.assign_weight() == "light" and attacker.weapon.type == "Thrown":
                return (f"With a toss too swift for their own good, the throw misses the target completely!")
        
        if attacker == self.player: # first person
            if attacker.weapon.assign_weight() == "light" and attacker.weapon.type == "Melee":
                return (f"You strike swiftly, but catch air!")
            elif attacker.weapon.assign_weight() == "normal" and attacker.weapon.type == "Melee":
                return (f"You swing your {attacker.weapon.core['name']} and miss!")
            elif attacker.weapon.assign_weight() == "heavy" and attacker.weapon.type == "Melee":
                return (f"You lunge with a lumbering blow, leaving enough time for you to get out of the way")
            elif attacker.weapon.type == "Ranged":
                return (f"Your shot whizzes past, your accuracy just off!")
            elif attacker.weapon.assign_weight() == "heavy" and attacker.weapon.type == "Thrown":
                return (f"With a laboring toss, you are just off the mark!")
            elif attacker.weapon.assign_weight() == "normal" and attacker.weapon.type == "Thrown":
                return (f"Your throw is just wayward!")
            elif attacker.weapon.assign_weight() == "light" and attacker.weapon.type == "Thrown":
                return (f"With a toss too swift for your own good, your throw misses the target completely!")


        return "The action is too fast to describe, the attack misses!" # fallback in case of error occurring, a miss statement always happens
    
    def hit_flavor(self, attacker, defender):
        if attacker == self.npc: #
            if attacker.weapon.assign_weight() == "light" and attacker.weapon.type == "Melee":
                return (f"{attacker.name} strikes swiftly, and registers a hit!")
            elif attacker.weapon.assign_weight() == "normal" and attacker.weapon.type == "Melee":
                hits =  [(f"{attacker.name} swings their {attacker.weapon.core['name']} and knicks you in the gut!"),
                         (f"{attacker.name} is accurate with their {attacker.weapon.core['name']}, and clocks you!")]
                return random.choice(hits) # example of scalability 
            elif attacker.weapon.assign_weight() == "heavy" and attacker.weapon.type == "Melee":
                return (f"{attacker.name} lunges with a lumbering blow, landing a powerful hit. You see stars!")
            elif attacker.weapon.type == "Ranged":
                return (f"{attacker.name}'s shot is on target, piercing you in the chest!")
            elif attacker.weapon.assign_weight() == "heavy" and attacker.weapon.type == "Thrown":
                return (f"With a laboring toss, {attacker.name} is on the mark, thats a hit!")
            elif attacker.weapon.assign_weight() == "normal" and attacker.weapon.type == "Thrown":
                return (f"{attacker.name}'s throw is just accurate enough to hit you! Ouch!")
            elif attacker.weapon.assign_weight() == "light" and attacker.weapon.type == "Thrown":
                return (f"With a toss so swift you never saw it coming, it strikes before you know it!")
            else:
                return (f"{attacker.name} strikes with their {attacker.weapon.core['name']['name']}")
        if attacker == self.player:
            if attacker.weapon.assign_weight() == "light" and attacker.weapon.type == "Melee":
                return (f"You strike swiftly, and register a hit!")
            elif attacker.weapon.assign_weight() == "normal" and attacker.weapon.type == "Melee":
                hits =  [(f"You swings your {attacker.weapon.core['name']} and knick {defender.name} in the gut!"),
                         (f"You're accurate with your {attacker.weapon.core['name']}, and clocks {defender.name}!")]
                return random.choice(hits)  
            elif attacker.weapon.assign_weight() == "heavy" and attacker.weapon.type == "Melee":
                return (f"You lunge with a lumbering blow, and land a powerful hit!")
            elif attacker.weapon.type == "Ranged":
                return (f"Your shot is on target, piercing {defender.name} in the chest!")
            elif attacker.weapon.assign_weight() == "heavy" and attacker.weapon.type == "Thrown":
                return (f"With a laboring toss, you're on the mark, thats a hit!")
            elif attacker.weapon.assign_weight() == "normal" and attacker.weapon.type == "Thrown":
                return (f"Your throw is just accurate enough to hit {defender.name}! Ouch!")
            elif attacker.weapon.assign_weight() == "light" and attacker.weapon.type == "Thrown":
                return (f"With a super swift toss, your throw strikes {defender.name} before they ever saw it coming!")
            else:
                return print(f"You strike with your {attacker.weapon.core['name']['name']}")