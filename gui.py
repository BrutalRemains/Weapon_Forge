import tkinter as tk
from tkinter import ttk
from engine.combat import Combat
from engine.weapon import *
from engine.endless import hall_of_fame, hof, load_hall_of_fame
from entities.npc import generate_npc
from entities.player import Player

TICK_MS = 200 # auto tick

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weapon Forge")
        self.geometry("800x480")

        top = ttk.Frame(self)
        top.pack(side="top", fill="x", padx=8, pady=6)

        # names at the top
        self.player_name_label = ttk.Label(top, text="Player: -")
        self.player_name_label.pack(side="left", padx = (0,20))

        self.npc_name_label = ttk.Label(top, text="Opponent: -")
        self.npc_name_label.pack(side="left")

        # health bars in the middle
        middle = ttk.Frame(self)
        middle.pack(side="top", fill="x", padx=8, pady=6)

        # player health bar
        player_health_frame = ttk.Frame(middle)
        player_health_frame.pack(side="left", fill="x", expand=True, padx=8)
        ttk.Label(player_health_frame, text="Player Health").pack(anchor="w")
        self.player_hp = ttk.Progressbar(player_health_frame, orient="horizontal", length=300, mode="determinate")
        self.player_hp.pack(fill="x")
        self.player_status_lbl = ttk.Label(player_health_frame, text="")
        self.player_status_lbl.pack(anchor="w")

        # npc health bar
        npc_health_frame = ttk.Frame(middle)
        npc_health_frame.pack(side="left", fill="x", expand=True, padx=8)
        ttk.Label(npc_health_frame, text="Opponent Health").pack(anchor="w")
        self.npc_hp = ttk.Progressbar(npc_health_frame, orient="horizontal", length=300, mode="determinate")
        self.npc_hp.pack(fill="x")
        self.npc_status_lbl = ttk.Label(npc_health_frame, text="")
        self.npc_status_lbl.pack(anchor="w")

        # Combat log, the action
        log_frame = ttk.Frame(self)
        log_frame.pack(side="top", fill="both", expand=True, padx=8, pady=6)
        self.log = tk.Text(log_frame, height = 12, wrap="word", state="disabled")
        self.log.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(log_frame, command=self.log.yview)
        scrollbar.pack(side="right", fill="y")
        self.log.configure(yscrollcommand=scrollbar.set)

        # Player controls
        ctrl = ttk.Frame(self)
        ctrl.pack(side="bottom", fill="x", padx=8, pady=6)
        self.new_btn = ttk.Button(ctrl, text="New Run", command=self.new_duel)
        self.new_btn.pack(side="left", padx=4)
        self.step_btn = ttk.Button(ctrl, text="Step", command=self.do_step, state="disabled")
        self.step_btn.pack(side="left", padx=4)
        self.auto_btn = ttk.Button(ctrl, text="Auto: Off", command=self.toggle_auto, state="disabled")
        self.auto_btn.pack(side="left", padx=4)
        self.stop_btn = ttk.Button(ctrl, text="Stop Auto", command=self.stop_auto, state="disabled")
        self.stop_btn.pack(side="left", padx=4)

        # hall of fame button
        self.hof_btn = ttk.Button(ctrl, text="Hall of Fame", command=self.show_hall_of_fame)
        self.hof_btn.pack(side="left", padx=4)

        self.combat = None
        self.player = None
        self.kill_count = 0
        self.npc = None
        self.auto_running = False
        self.auto_job = None

    
    # this will be used to "create" the events as they happen. All the events happen in combat.step() and will then be appended to a viewable log
    def append_log(self,text):
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")
    
    def set_health_bars(self):
        if self.player:
            max_hp = 50
            self.player_hp["maximum"] = max_hp
            self.player_hp["value"] = self.player.health
            self.player_name_label.config(text=f"Player:  {self.player.name}")
        if self.npc:
            max_hp = 50
            self.npc_hp["maximum"] = max_hp
            self.npc_hp["value"] = self.npc.health
            self.npc_name_label.config(text=f"Opponent:  {self.npc.name} the {self.npc.race} {self.npc.role}")

    def new_duel(self):
        self.stop_auto()

        name_window = tk.Toplevel(self)
        name_window.title("Enter Your Name")
        name_window.geometry("300x100")
        name_window.transient(self)
        name_window.grab_set()

        ttk.Label(name_window, text="Enter your name: ").pack(pady=1)
        name_entry = ttk.Entry(name_window, width=30)
        name_entry.pack(pady=5)
        name_entry.focus()

        player_name = None
        
        def confirm_name():
            nonlocal player_name
            name = name_entry.get().strip()
            if len(name) > 0 and len(name) < 20:
                player_name = name
                name_window.destroy()
            else:
                pass
        
        ttk.Button(name_window, text="Start Duel", command=confirm_name).pack(pady=5)
        name_entry.bind("<Return>", lambda e: confirm_name())

        self.wait_window(name_window)

        if player_name is None:
            return

        # ensures the log is fresh
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")        

        #initialize the members of the duel
        self.player = Player(player_name, generate_weapon())
        self.npc = generate_npc()
        self.combat = Combat(self.player, self.npc)
       
        # disables new run button while one is ocurring, and is re-enabled in end control
        self.new_btn.config(state="disabled")
        self.step_btn.config(state="Normal")
        
        # Beginning run flavor text
        self.append_log("You were brought here to the Weapon Forge as a test subject.")
        self.append_log(f"\nThe Great Smith has given you the following name: {self.player.name}")
        self.append_log("\nPrepare to test a Weapon of the Forge!")
        self.append_log("A fight to the death, by the way!\n")
        self.append_log("--- Your Weapon ---")
        self.append_log(self.player.weapon_description())
        self.append_log("\n--- Your Opponent ---")
        self.append_log(self.npc.description())


        # setting up controls, initializing auto then disabling itt
        self.step_btn.config(state="normal")
        self.auto_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.auto_running = False
        self.auto_btn.config(state="Auto: Off")



        self.append_log(f"New duel: {self.player.name} vs {self.npc.name}")
        self.set_health_bars()

   # the reason combat now returns lists of dictionaries the way that does: a concept present throughout the core of this program
    def process_events(self,events):
        if not events:
            return
        for ev in events:
            etype = ev.get("type")
            if etype == "hit":
                self.append_log(ev.get("flavor"))
                self.append_log("")
            elif etype == "miss":
                self.append_log(ev.get("flavor"))
                self.append_log("")
            elif etype == "status_applied":                
                tgt = ev.get('target_name')
                eff = ev.get('effect')
                self.append_log(f"{tgt} is afflicted with {eff}!")
            elif etype == "info":
                self.append_log(ev.get("msg", "Info"))
            elif etype == "stalemate":
                winner = ev.get("winner")
                self.append_log(f"Stalemate! {winner.name} wins!")
            else:
                self.append_log(str(ev))
        self.set_health_bars()


    # these next steps are for controlling combat flow from a user perspective
    # auto on vs off is as it sounds, obviously combat will be easier to follow with it off
    def do_step(self):
        if not self.combat:
            return
        events = self.combat.step()
        
        if not events and self.player.is_alive() and self.npc.is_alive():
            self.after(10, self.do_step)
            return
        self.process_events(events)
        if not self.player.is_alive() or not self.npc.is_alive():
            self._check_end()

    def toggle_auto(self):
        if not self.combat:
            return
        if self.auto_running:
            self.stop_auto()
            return
        self.auto_running = True
        self.auto_btn.config(text="Auto: On")
        self.stop_btn.config(state="normal")
        self._auto_tick()
    
    def _auto_tick(self):
        if not self.auto_running:
            return
        self.do_step()
        if self.auto_running:
            self.auto_job = self.after(TICK_MS, self._auto_tick)
    
    def stop_auto(self): # the inversion of toggle on
        self.auto_running = False
        self.auto_btn.config(text="Auto: Off")
        self.stop_btn.config(state="disabled")
        if self.auto_job:
            self.after_cancel(self.auto_job)
            self.auto_job = None
    
    def _check_end(self):
        if not self.combat:
            return
        if not self.player.is_alive() and self.kill_count >= 1:
            self.append_log(f"You have fallen after {self.kill_count} kills")
            self.append_log("The Great Smith turns away")
            entry = {
                "name": self.player.name,
                "weapon": self.player.weapon.description("hof"),
                "kill_count": self.kill_count
             }
            hall_of_fame.append(entry)
            hof(hall_of_fame)
            self._end_controls()
        elif not self.player.is_alive() and self.kill_count < 1:
            self.append_log("You have fallen")
            self.append_log("The Great Smith turns away")
            self.append_log("Disgusting")
            self._end_controls()
            
        elif not self.npc.is_alive():
            self.kill_count += 1
            self.append_log(f"{self.npc.name} is defeated! Wins: {self.kill_count}")
            self.player.reset()
            self.npc = generate_npc()
            self.combat = Combat(self.player, self.npc)
            self.append_log("\n--- Your Next Opponent ---")
            self.append_log(self.npc.description())
            self.set_health_bars()

    def _end_controls(self):
        self.auto_running = False
        self.auto_btn.config(text="Auto: Off", state="disabled")
        self.stop_btn.config(state="disabled")
        self.step_btn.config(state="disabled")
        self.new_btn.config(state="normal") #re-enable new run
    
    def show_hall_of_fame(self):
        hof_entries = load_hall_of_fame()

        hof_window = tk.Toplevel(self)
        hof_window.title("Hall of Fame")
        hof_window.geometry("600x400")
        hof_window.transient(self)

        text = tk.Text(hof_window, wrap="word", padx=10, pady=10)
        text.pack(fill="both", expand=True)

        if not hof_entries:
            text.insert("1.0", "No entries in the Hall of Fame yet.\n\nFight bravely to earn your place!")
        else:
            text.insert("1.0", "=== HALL OF FAME ===\n\n")
            for i, entry in enumerate(hof_entries, 1):
                name = entry.get("name")
                kills = entry.get("kill_count")
                weapon = entry.get("weapon")
                text.insert("end", f"{i}. {name}\n")
                text.insert("end", f"   Kills: {kills}\n")
                text.insert("end", f"   Weapon: {weapon}\n\n")

        text.config(state="disabled")

        ttk.Button(hof_window, text="Close", command=hof_window.destroy).pack(pady=10)



if __name__ == "__main__":
    app = GUI()
    app.mainloop()