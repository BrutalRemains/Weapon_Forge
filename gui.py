import tkinter as tk
from tkinter import ttk
from engine.combat import Combat
from engine.weapon import *
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
        self.new_btn = ttk.Button(ctrl, text="New Duel", command=self.new_duel)
        self.new_btn.pack(side="left", padx=4)
        self.step_btn = ttk.Button(ctrl, text="Step", command=self.do_step, state="disabled")
        self.step_btn.pack(side="left", padx=4)
        self.auto_btn = ttk.Button(ctrl, text="Auto: Off", command=self.toggle_auto, state="disabled")
        self.auto_btn.pack(side="left", padx=4)
        self.stop_btn = ttk.Button(ctrl, text="Stop Auto", command=self.stop_auto, state="disabled")
        self.stop_btn.pack(side="left", padx=4)

        self.combat = None
        self.player = None
        self.npc = None
        self.auto_running = False
        self.auto_job = None

        def append_log(self,text):
            self.log.configure(state="normal")
            self.log.insert("end", text + "\n")
            self.log.see("end")
            self.log.configure(state="disabled")
        
        def set_health_bars(self):
            if self.player:
                max_hp = self.player.health
                self.player_hp["maximum"] = max_hp
                self.player_hp["value"] = self.player.health
                self.player_name_label.config(text=f"Player:  {self.player.name}")
            if self.npc:
                max_hp = self.npc.health
                self.npc_hp["maximum"] = max_hp
                self.npc_hp["value"] = self.npc.health
                self.npc_name_label.config(text=f"Opponent:  {self.npc.name}")

        def new_duel(self):
            name_window = tk.Toplevel(self)
            name_window.title("Enter Your Name")
            name_window.geometry("300x100")
            name_window.transient(self)
            name_window.grab_set()

            ttk.Label(name_window, text="Enter your name: ").pack(pady=10)
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

            #initialize the members of the duel
            self.player = Player(player_name, generate_weapon())
            self.npc = generate_npc()
            self.combat = Combat(self.player, self.npc)

            # setting up controls, initializing auto then disabling itt
            self.step_btn.config(state="normal")
            self.auto_btn.config(state="normal")
            self.stop_btn.config(state="disabled")
            self.auto_running = False
            self.auto_btn.config(state="Auto: Off")

            # ensures the log is fresh
            self.log.configure(state="normal")
            self.log.delete("1.0", "end")
            self.log.configure(state="disabled")

            self.append_log(f"New duel: {self.player.name} vs {self.npc.name}")
            self.set_health_bars()



if __name__ == "__main__":
    app = GUI()
    app.mainloop()