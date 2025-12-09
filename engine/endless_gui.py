from engine.endless import *
from engine.combat import Combat

# a new gui version of endless and hof to maintain complete funtionality of cli version

def endless_duels_gui(player, hall_of_fame):
    player.reset()
    kill_count = 1
    events = []

    while player.is_alive():
        npc = generate_npc()
        events.append({"type": "info", "msg": f"The Great Smith presents {npc.name} the {npc.race}{npc.role}"})
        combat = Combat(player, npc)

        while player.is_alive() and npc.is_alive():
            evs = combat.step() or []
            events.extend(evs)

            if not player.is_alive() or not npc.is_alive():
                break

        winner = player if player.is_alive() else npc

        if winner == player:
            kill_count += 1
            events.append({"type": "duel_result", "winner": player.name})
            player.reset()
        else:
            events.append({"type": "duel_result", "loser": player.name})
            hof_entry = {
                "name": player.name,
                "weapon": player.weapon.description("hof"),
                "kill_count": kill_count
            }
            hall_of_fame.append(hof_entry)
            events.append({"type": "hof_entry", "entry": hof_entry })
            break
    return events

def show_hof_gui():
    hof = load_hall_of_fame()
    events = []

    if not hof:
        events.append({"type": "info", "msg": "No entries in the hall of fame" })
        return events
    
    entries = []
    for i, entry in enumerate(hof):
        entries.append({
            "index": i,
            "name": entry.get("name"),
            "kill_count": entry.get("kill_count"),
            "weapon": entry.get("weapon"),
        })

    events.append({"type":"hall_entries", "entries": entries})
    return events