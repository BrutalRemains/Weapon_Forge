import time
from entities.npc import generate_npc
from engine.combat import Combat
hall_of_fame = []

def endless_duels(player):
    player.reset() #resets player health and status effects to normal

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
        print(f"{player.name} dealt {combat.player_damage_dealt} total damage!")
        print(f"{npc.name} dealt {combat.npc_damage_dealt} total damage!")

        if winner == player:
            kill_count += 1
            print(f"You have won again!")
            time.sleep(1.4)
        else:
            print(f"You, {player.name} have fallen after slaying {kill_count} for the Great Smith")
    
            hall_of_fame_entry = {"Name": player.name,
                                  "Weapon": player.weapon,
                                  "Kill_Count": kill_count}
            hall_of_fame.append(hall_of_fame_entry)
            break