from engine.weapon import *
from engine.combat import Combat
from entities.npc import generate_npc
from entities.player import Player
from engine.combat import Combat
from engine.endless import *
import time

def main_menu():
    run = True
    while run:
        print("Welcome to the WEAPON FORGE where you will do battle for the Great Smith!\n")
        print("------MAIN MENU------")
        print("1. Start Game")
        print("2. About")
        print("3. Hall of Fame")
        print("4. Quit")
        choice = input("\nPlease choose an option!: ")
        
        if choice == "1":
            run_game()
        elif choice == "2":
            print("credits")
        elif choice == "3":
            show_hall_of_fame()
        elif choice == "4" or "q".lower():
            print("The Great Smith will continue to forge away...")
            run = False
        elif choice == "":
            pass
        else:
            print("invalid choice")

def run_game():
    print("\nYou were brought here, to the Weapon Forge as a test subject for the Great Smith, and his creations.")

    player_name = input("\nThe Great Smith has given you the following designation: ")
    player = Player(player_name, generate_weapon())   
    npc = generate_npc()

    print(f"{player.name}! Prepare to test a Weapon of the Forge!\n")
    time.sleep(1.4)
    print("Oh! In a fight to the death by the way!\n")
    time.sleep(2)
    print("---------------------------------------\n")
    
    print(player.weapon_description())
    input("\nPress ENTER to inspect your opponent! \n")
    print(npc.description())
    input(f"Press ENTER to draw your {player.weapon.core['name']}...")

    print("\n------FIGHT TO THE DEATH------\n")
    
    combat = Combat(player, npc)
    winner = combat.simulate_duel()

    input(f"Press ENTER...")
    if winner  == player:
        print("------WINNER------\n")
        print("You have proven yourself worthy of the forge!\n")
        input("ENTER")
        endless_duels(player, hall_of_fame)
    else:
        print("------LOSER------")
        time.sleep(1.5)
        print("The Great Smith turns away.")
        time.sleep(1.5)
        print("Disgusting.\n")
    input("Press ENTER to see duel summary...")

    print("\n------Duel Summary------")
    print(f"{player.name} dealt {combat.player_damage_dealt} total damage!")
    print(f"{npc.name} dealt {combat.npc_damage_dealt} total damage!")
    time.sleep(2)


def main():
    main_menu()

if __name__ == "__main__":
    main()
