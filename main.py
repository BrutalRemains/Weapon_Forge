from weapon import generate_weapon 
from npc import generate_npc

def main():
    player_weapon = generate_weapon()
    print(player_weapon.description("player"))
    npc = generate_npc()
    print(npc.description())



if __name__ == "__main__":
    main()
