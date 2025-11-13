from weapon import generate_weapon 
from npc import generate_npc
from player import Player
from combat import Combat
import time

def main_menu():
    run = True
    while run:
        print("Welcome to the WEAPON FORGE where you will do battle for the Great Smith!")
        print("------MAIN MENU------\n")
        print("1. Start Game")
        print("2. About")
        print("3. Quit")
        choice = input("\nPlease choose an option!: ")
        
        if choice == "1":
            start_game()
        elif choice == "2":
            print("credits")
        elif choice == "3" or "q".lower():
            print("The Great Smith will continue to forge away...")
            run = False
        else:
            print("invalid choice")

def start_game():
    print("\nYou were brought here, to the Weapon Forge as a test subject for the Great Smith, and his creations.")
    player_name = input("\nThe Great Smith has given you the following designation: ")
    player = Player(player_name, generate_weapon())
    npc = generate_npc()
    print(f"{player.name.capitalize()}! Prepare to test a Weapon of the Forge!\n")
    time.sleep(1.5)
    print("Oh! In a fight to the death by the way!\n")
    time.sleep(1.5)
    print("---------------------------------------\n")
    print(player.weapon_description())  
    print(npc.description())
    input(f"Press ENTER to draw your {player.weapon.core['name']}...")

    print("\n------FIGHT TO THE DEATH------\n")

    combat = Combat(player, npc)
    winner = combat.simulate_duel()

    input(f"Press ENTER...")
    if winner  == player:
        print("------WINNER------\n")
        print("You have proven yourself worthy of the forge!")
    
    else:
        print("You lose.")
        time.sleep(2)
        print("The Great Smith turns away.")
        time.sleep(1.5)
        print("Disgusting.")




def main():
    main_menu()

if __name__ == "__main__":
    main()
