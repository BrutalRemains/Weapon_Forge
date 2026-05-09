# **Weapon Forge**
Welcome to **Weapon Forge**! Weapon Forge is a text-based rouguelike game where you will randomly a roll weapon, from **over 25,280** possible combinations, and then battle through waves of procedularly generated enemies!
Thats right! Bring your Kitchen Knife wrapped in barbed wire to a fight with a Sniper Rifle wielding Elven Farmer, a Skeleton Soldier mastered in the use of shurikens! **There are over 67,200 potential enemies**

**Weapon Forge** was designed with a few important things in mind: _modularity_, _flavor_, _replayability_, but overall and most important to showcase a _scalable_ _python_ _structure_

## Gameplay:
You are a warrior, chosen by the Great Smith, armed with weapons forged with a randomized combination of weapon cores(the base), attachments, grips, and enchants, for the purpose of testing said weapons.
Your goal is to **win** and _maybe_ etch your name into the Great Smith's "Hall of Fame"

**Weapons**: As mentioned weapons are a combination of several different parts, offering totally different variations for stats and flavor. You're sure to encounter some wacky and fun combos!
**Turn-Based Combat**: Combat is turn-based, with a unique turn mechanic rewarding the speed of your weapon with more turns. Make no mistake however; you are here to test weapons, not armor!
**Status Effects**: Weapons enchanted with status effects can inflict different ailments: burn, bleed, stun and chill, each having a different effect!
**Hall of Fame**: Those with the gumption to uh, not die, in their first match will have potential eligibilty to enter the hall of fame! The more you kill the higher you could rise
**Rogue-like Replaybility**: When you die, the Great Smith has determined you and your weapon _unworthy_ and you will both be scrapped. You will have to try again with a brand new weapon!

## Technical
This project relies on purely python. It uses no external libraries of any kind, and utilizes only knoweldge specifically offered in all Boot.dev courses in the "Backend Development Path" prior to the "First Personal Project". I wanted to demonstrate, mostly to myself, a firm grasp of what I had learned.

Working on this project was **really** fun. I wanted to focus heavily on modularity, and tried to design things in a way that you could add and remove essentially infinitely to this game. Not only that, but because its modularity, even though there are **1.6 billion** possible unique match-ups, it keeps a really, really low runtime.

As for the architecture around the generation of weapons and NPC's, I use all json files that allow for _very_ easy expansion. With some damage, accuracy, etc. number rebalancing done by ai, I could easily add enough data to these jsons to be bring weapon combinations and npc combinations to the millions, which would bring unique matchups to quadrillions or more, but I wanted to ensure I used my time for coding and design.

Apart from all else, every run is designed to be completely self-contained, with the hall of fame also writing to a json file so that it may remain persistent between sessions.

## INSTALLATION INSTRUCTIONS

### CLI: 
git clone https://github.com/kristiansroberts/Weapon_Forge

cd Weapon_Forge

python3 main.py


## Author

### Kristian Roberts(Brutal Remains)

I am a backend developer in training, focused on building my fundamental grasp on modular and scalable design!
