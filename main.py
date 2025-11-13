from weapon import generate_weapon 
from npc import generate_npc
from player import Player
from combat import Combat
import time


def start_game():
    print("Welcome to the WEAPON FORGE where you will do battle for the Great Smith!")
    player_name = input("The Great Smith has given you the following designation: ")
    player = Player(player_name, generate_weapon())
    npc = generate_npc()

    print(player.weapon_description())  
    print(npc.description())
    input(f"Press ENTER to draw your {player.weapon.core['name']}...")
    

    combat = Combat(player, npc)
    winner = combat.simulate_duel()

    input(f"Press ENTER...")
    if winner  == player:
        print("You have proven yourself worth of the forge!")
    
    else:
        print("You lose.")
        time.sleep(3)
        print("Disgusting.")




def main():
    start_game()

if __name__ == "__main__":
    main()
