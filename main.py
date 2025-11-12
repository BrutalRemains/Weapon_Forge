from weapon import generate_weapon 
from npc import generate_npc
from player import Player

def main():
    player = Player(name="Kristian", weapon=generate_weapon())
    print(player.weapon_description())


if __name__ == "__main__":
    main()
