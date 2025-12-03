import json
import os
import time
from entities.npc import generate_npc
from engine.combat import Combat
def load_hall_of_fame(): # opens the hall_of_fame file, to keep it persistent between sessions
    if os.path.exists("databases/hall_of_fame.json"):
       try:
           with open("databases/hall_of_fame.json", "r") as f:
                return json.load(f)
       except:
           return []
    return []

def save_hall_of_fame(hall_of_fame): # saves to hall_of_fame file
    with open("databases/hall_of_fame.json", "w") as f:
        json.dump(hall_of_fame, f, indent=4)

hall_of_fame = load_hall_of_fame()

def endless_duels(player, hall_of_fame):
    player.reset() # failsafe ensures player starts fresh
    kill_count = 1 # this function is called after the first win

    while player.is_alive():
        npc = generate_npc()
        print(f"\nThe Great Smith is pleased, and wishes to see you continue!")
        input("Press ENTER to challenge your next opponent! ")
        print(npc.description())
        input(f"Draw your {player.weapon.core['name']} once more!")

        combat = Combat(player, npc)
        winner = combat.simulate_duel()

        input("Press ENTER to see duel summary...")

        print("\n------Duel Summary------")
        print(f"You dealt {combat.player_damage_dealt} total damage!")
        print(f"{npc.name} dealt {combat.npc_damage_dealt} total damage!")

        if winner == player:
            kill_count += 1
            print(f"You have won again!")
            time.sleep(1)
            player.reset()
        else:
            print(f"You, {player.name} have fallen after slaying {kill_count} for the Great Smith")
            print("Perhaps the Great Smith will have etched your name into the hall of fame!")
    
            hall_of_fame_entry = {"name": player.name,
                                  "weapon": player.weapon.description("hof"),
                                  "kill_count": kill_count}
            hall_of_fame.append(hall_of_fame_entry)
            hof(hall_of_fame)
            break

def hof(hall_of_fame):
    hall_of_fame.sort(key=lambda x: x["kill_count"], reverse=True) # this will ensure list is sorted by kill count descending
    hall_of_fame[:] = hall_of_fame[:5]# this keeps the list at 5
    save_hall_of_fame(hall_of_fame)

def show_hall_of_fame():
    hof = load_hall_of_fame()

    if not hof:
        print("\nNo entries in the hall of fame yet! \n")
        return 
    
    print("\n------Hall of Fame------")
    for i, entry in enumerate(hof):
        print(f"{i}. Name: {entry['name']}, Kill Count: {entry['kill_count']}")
        print(f"    {entry['weapon']}")