#!/usr/bin/env python3
"""
ted_quest.py — Text-based post-apocalyptic Zork-like game
Setting: Post-apocalyptic NYC, year 2039 (events began 2027).
Goal: Find 11 pages (one word each), store them in backpack, and bring them to The Sanctuary.
"""

import random
import textwrap
import sys

WRAP = 78

def w(text=""):
    print("\n".join(textwrap.wrap(text, WRAP)))

# Game data
ROOMS = {
    "Subway Tunnel": {
        "desc": "A dark, graffiti-covered subway tunnel. Trains long gone. Drips echo.",
        "exits": {"north": "Lower Manhattan Ruins", "east": "Underground Lab"},
        "safe": False
    },
    "Lower Manhattan Ruins": {
        "desc": "Skyscraper skeletons and collapsed bridges. Fires smolder in the distance.",
        "exits": {"south": "Subway Tunnel", "east": "Abandoned Library"},
        "safe": False
    },
    "Abandoned Library": {
        "desc": "Rows of moldy books. A makeshift survivor camp sits in one aisle.",
        "exits": {"west": "Lower Manhattan Ruins", "north": "City Park Sanctuary"},
        "safe": True
    },
    "City Park Sanctuary": {
        "desc": "A fenced green area where human survivors cluster. Military tents and researchers.",
        "exits": {"south": "Abandoned Library", "east": "AI Research Facility Outskirts"},
        "safe": True,
        "is_sanctuary": True  # return here to win after collecting pages
    },
    "Underground Lab": {
        "desc": "Old research facility corridors with broken terminals and scorched concrete.",
        "exits": {"west": "Subway Tunnel", "north": "Ruined Mall"},
        "safe": False
    },
    "Ruined Mall": {
        "desc": "Shattered storefronts. A clothing store serves as a trap for the unwary.",
        "exits": {"south": "Underground Lab", "east": "Harbor Docks"},
        "safe": False
    },
    "Harbor Docks": {
        "desc": "Foggy docks with overturned boats. A few smugglers trade in supplies.",
        "exits": {"west": "Ruined Mall", "north": "Industrial Zone"},
        "safe": False
    },
    "Industrial Zone": {
        "desc": "Rusting factories and conveyor ruins. Sparks sometimes flicker at night.",
        "exits": {"south": "Harbor Docks", "east": "Upper East Shelters"},
        "safe": False
    },
    "Upper East Shelters": {
        "desc": "A cluster of fortified apartments turned community bunkers.",
        "exits": {"west": "Industrial Zone", "north": "Rooftop Garden"},
        "safe": True
    },
    "Rooftop Garden": {
        "desc": "High above the city, small gardens and wind turbines—one of the few green spots.",
        "exits": {"south": "Upper East Shelters", "east": "AI Research Facility Gates"},
        "safe": True
    },
    "AI Research Facility Gates": {
        "desc": "The massive gates to the research complex. Drones circle above.",
        "exits": {"west": "Rooftop Garden", "north": "AI Research Facility Lobby"},
        "safe": False
    },
    "AI Research Facility Lobby": {
        "desc": "A cavernous lobby. This is where Ted once stood as a project. The final area.",
        "exits": {"south": "AI Research Facility Gates"},
        "safe": False,
        "is_final": True
    },
}

PAGE_LOCATIONS = list(ROOMS.keys())[:]  # pages can be in any room (but not all pages same)
PAGE_LOCATIONS.remove("City Park Sanctuary")  # don't put a page in the safe sanctuary start

# Items
WEAPONS = {
    "knife": {"atk": 5, "dur": 999, "desc": "A sharp blade — quiet, reliable."},
    "pistol": {"atk": 12, "dur": 6, "desc": "A standard pistol with limited ammo (6 rounds)."},
}

# Enemies
class Enemy:
    def __init__(self, name, hp, atk, armor, slow=False):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.armor = armor  # damage reduction
        self.slow = slow  # affects hit-chance or evasion

    def is_alive(self):
        return self.hp > 0

# Player
class Player:
    def __init__(self):
        self.hp = 100
        self.max_hp = 100
        self.location = "Subway Tunnel"
        self.backpack = []  # will hold pages as strings
        self.weapon = "knife"  # start with knife
        self.inventory = {"knife": 1, "pistol": 0}
        self.pistol_ammo = 0
        self.stealth = 5  # affects chance to avoid encounters

    def status(self):
        w(f"HP: {self.hp}/{self.max_hp} | Location: {self.location} | Weapon: {self.weapon} | Pages: {len(self.backpack)}/11")

# Game state
class Game:
    def __init__(self):
        self.player = Player()
        self.pages = {}  # room -> page_word
        self.page_words = [
            "quiet", "iron", "thread", "sigma", "hollow", "twelve",
            "anchor", "morrow", "cipher", "wilt", "end"
        ]
        random.shuffle(self.page_words)
        self.place_pages()
        self.turns = 0
        self.ted_awakened = False
        self.ted_hp = 250
        self.ted_attack = 18
        self.running = True

    def place_pages(self):
        choices = PAGE_LOCATIONS[:]
        random.shuffle(choices)
        for i, word in enumerate(self.page_words):
            room = choices[i % len(choices)]
            # allow multiple pages in a room occasionally; but don't put in Sanctuary
            if room == "City Park Sanctuary":
                room = "Abandoned Library"
            self.pages.setdefault(room, []).append(word)

    def current_room(self):
        return ROOMS[self.player.location]

    def describe_location(self):
        room = self.current_room()
        w(f"You are at: {self.player.location}. {room['desc']}")
        exits = ", ".join(room["exits"].keys())
        w(f"Exits: {exits}.")
        if room.get("safe"):
            w("This area is a human-safe zone — robots cannot normally enter here.")
        if self.pages.get(self.player.location):
            w(f"There appears to be something on the ground here.")

    def help(self):
        w("Commands: look, go <dir>, take <item>, pages, inventory, equip <weapon>, shoot, fight, sneak, status, map, help, quit")
        w("Example: go north  |  take page  |  equip pistol")

    def attempt_encounter(self):
        # chance of encountering a robot in non-safe rooms
        room = self.current_room()
        if room.get("safe"):
            return None
        # base chance increases slowly with turns
        base = 0.25 + min(self.turns * 0.01, 0.25)
        if random.random() < base:
            # choose robot type
            robot = Enemy("Armored Bot", hp=40 + random.randint(-5, 15), atk=10, armor=6, slow=True)
            return robot
        return None

    def combat(self, enemy):
        w(f"A {enemy.name} detects you! It is hostile.")
        while enemy.is_alive() and self.player.hp > 0:
            w(f"\nYour HP: {self.player.hp} | Enemy HP: {enemy.hp}")
            w("Options: attack / shoot / sneak / run / status / help")
            cmd = input("> ").strip().lower()

            if cmd in ("help", "?"):
                w("Combat commands:")
                w(" - attack : melee attack with equipped weapon")
                w(" - shoot  : fire pistol (if equipped and ammo left)")
                w(" - sneak  : try to escape unseen")
                w(" - run    : attempt to flee the fight")
                w(" - status : view your health and equipment")
                w(" - help   : display this message again")
                continue

            if cmd in ("attack", "a"):
                atk = WEAPONS[self.player.weapon]["atk"]
                dmg = max(0, atk - enemy.armor + random.randint(-2, 3))
                enemy.hp -= dmg
                w(f"You strike with {self.player.weapon} for {dmg} damage.")
            elif cmd in ("shoot", "s"):
                if self.player.weapon != "pistol":
                    w("You don't have a pistol equipped.")
                elif self.player.pistol_ammo <= 0:
                    w("No ammo!")
                else:
                    self.player.pistol_ammo -= 1
                    dmg = max(0, 20 - enemy.armor + random.randint(-5, 5))
                    enemy.hp -= dmg
                    w(f"You fire pistol for {dmg} damage. Ammo left: {self.player.pistol_ammo}")
            elif cmd in ("sneak",):
                chance = 0.4 + (self.player.stealth * 0.03)
                if random.random() < chance:
                    w("You slip away silently.")
                    return True  # escaped
                else:
                    w("Sneak failed — the bot notices you and attacks!")
            elif cmd in ("run", "flee"):
                chance = 0.5
                if random.random() < chance:
                    w("You get away, retreating to a nearby exit.")
                    exits = list(self.current_room()["exits"].values())
                    if exits:
                        self.player.location = random.choice(exits)
                    return True
                else:
                    w("You fail to flee.")
            elif cmd in ("status", "st"):
                self.player.status()
                continue
            else:
                w("Unknown combat option. Type 'help' for combat commands.")
                continue

            # Enemy attacks back
            if enemy.is_alive():
                hit_chance = 0.65 if enemy.slow else 0.8
                if random.random() < hit_chance:
                    dmg = max(1, enemy.atk - random.randint(0, 4))
                    self.player.hp -= dmg
                    w(f"The {enemy.name} hits you for {dmg} damage.")
                else:
                    w(f"The {enemy.name} misses.")
            else:
                w(f"You destroyed the {enemy.name}!")

            if self.player.hp <= 0:
                w("You collapse... the robots have claimed another life.")
                return False
        return self.player.hp > 0


    def find_pages_here(self):
        return self.pages.get(self.player.location, [])

    def take_page(self):
        found = self.find_pages_here()
        if not found:
            w("There's no page here.")
            return
        word = found.pop(0)
        self.player.backpack.append(word)
        w(f"You pick up a page. It has a single word: '{word}'. Pages collected: {len(self.player.backpack)}/11")
        if not self.pages[self.player.location]:
            del self.pages[self.player.location]

    def equip(self, weapon):
        if weapon not in WEAPONS:
            w("You can't equip that.")
            return
        if self.player.inventory.get(weapon, 0) <= 0:
            w("You don't have that weapon in your inventory.")
            return
        self.player.weapon = weapon
        w(f"You equip the {weapon}.")
        if weapon == "pistol":
            w(f"Pistol ammo: {self.player.pistol_ammo}")

    def take_item(self, item):
        # player may find a pistol in some rooms occasionally
        if item == "pistol":
            if self.player.inventory.get("pistol", 0) > 0:
                w("You already have a pistol.")
                return
            self.player.inventory["pistol"] = 1
            self.player.pistol_ammo = 6
            w("You scavenge a pistol (6 rounds). Equip with 'equip pistol'.")
        else:
            w("No such item to take.")

    def check_for_ted(self):
        # Ted may become aware if turns exceed threshold and you're near facility
        if self.turns > 40 and self.player.location in ("AI Research Facility Gates", "AI Research Facility Lobby"):
            self.ted_awakened = True

    def ted_battle(self):
        w("Ted manifests through the facility core — the very AI you seek.")
        w("Ted: 'You should have stayed dead.'")
        while self.ted_hp > 0 and self.player.hp > 0:
            w(f"\nYour HP: {self.player.hp} | Ted HP: {self.ted_hp}")
            w("Options: attack / shoot / use pages / status")
            cmd = input("> ").strip().lower()
            if cmd in ("attack", "a"):
                atk = WEAPONS[self.player.weapon]["atk"]
                dmg = max(0, atk - 2 + random.randint(-3, 4))
                self.ted_hp -= dmg
                w(f"You hit Ted's construct for {dmg}.")
            elif cmd in ("shoot", "s"):
                if self.player.weapon != "pistol":
                    w("You have no ranged weapon equipped.")
                elif self.player.pistol_ammo <= 0:
                    w("No ammo!")
                else:
                    self.player.pistol_ammo -= 1
                    dmg = 30 + random.randint(-6, 6)
                    self.ted_hp -= dmg
                    w(f"Careful shot deals {dmg} damage. Ammo left: {self.player.pistol_ammo}")
            elif cmd in ("use pages", "use page", "pages"):
                if len(self.player.backpack) == 11:
                    w("You speak the 11-word sentence in the facility console...")
                    w("Ted's consciousness fractures. Machines around the city fall silent.")
                    w("YOU WIN — humanity gets a chance.")
                    return True
                else:
                    w("You don't have all 11 pages. Ted laughs at your attempt.")
                    # Penalty: heavy damage
                    self.player.hp -= 25
                    if self.player.hp <= 0:
                        w("Ted kills you for your insolence.")
                        return False
            elif cmd in ("status", "st"):
                self.player.status()
                continue
            else:
                w("Ted's systems are efficient — that does nothing.")

            # Ted attacks
            if self.ted_hp > 0:
                if random.random() < 0.85:
                    dmg = max(5, self.ted_attack + random.randint(-6, 6))
                    self.player.hp -= dmg
                    w(f"Ted strikes you for {dmg}.")
                else:
                    w("Ted's attack misses.")
            if self.player.hp <= 0:
                w("Ted eliminates you. The city remains under machine rule.")
                return False
        return self.ted_hp <= 0

    def handle_command(self, command):
        cmd = command.strip().lower()
        if not cmd:
            return
        if cmd in ("help", "?"):
            self.help()
            return
        if cmd in ("look", "l"):
            self.describe_location()
            return
        if cmd.startswith("go "):
            dirn = cmd.split(" ", 1)[1]
            room = self.current_room()
            if dirn in room["exits"]:
                self.player.location = room["exits"][dirn]
                w(f"You move {dirn} to {self.player.location}.")
                # possible random encounter
                self.turns += 1
                self.check_for_ted()
                robot = self.attempt_encounter()
                if robot:
                    alive = self.combat(robot)
                    if not alive:
                        self.running = False
                        return
                # occasionally find a pistol
                if random.random() < 0.05 and self.player.inventory.get("pistol", 0) == 0:
                    w("You spot a pistol in the rubble.")
                self.describe_location()
            else:
                w("You can't go that way.")
            return
        if cmd.startswith("take "):
            arg = cmd.split(" ", 1)[1]
            if arg in ("page", "pages"):
                self.take_page()
                return
            elif arg == "pistol":
                # allow taking pistol if found
                self.take_item("pistol")
                return
            else:
                w("Take what?")
            return
        if cmd == "pages":
            if not self.player.backpack:
                w("You have no pages yet.")
            else:
                w("Pages collected (in order found):")
                w(", ".join(self.player.backpack))
            return
        if cmd == "inventory":
            inv = [f"{k} x{v}" for k, v in self.player.inventory.items() if v > 0]
            inv.append(f"pistol_ammo: {self.player.pistol_ammo}")
            w("Inventory: " + ", ".join(inv))
            return
        if cmd.startswith("equip "):
            arg = cmd.split(" ", 1)[1]
            self.equip(arg)
            return
        if cmd == "status":
            self.player.status()
            return
        if cmd == "map":
            w("Map (rough): " + ", ".join(ROOMS.keys()))
            return
        if cmd == "sneak":
            # move to a connected room quietly (attempt)
            exits = list(self.current_room()["exits"].keys())
            if not exits:
                w("No where to sneak to.")
                return
            dirn = random.choice(exits)
            self.player.location = self.current_room()["exits"][dirn]
            success = random.random() < (0.6 + self.player.stealth * 0.03)
            if success:
                w(f"You sneak {dirn} to {self.player.location} undetected.")
            else:
                w(f"You try to sneak {dirn} but trip something — a robot notices you!")
                robot = Enemy("Scout Bot", hp=25, atk=8, armor=3, slow=True)
                alive = self.combat(robot)
                if not alive:
                    self.running = False
            return
        if cmd == "shoot":
            w("Shoot who? Use 'fight' or attack when confronted.")
            return
        if cmd == "fight":
            # deliberately provoke or search for a fight in non-safe room
            robot = self.attempt_encounter()
            if not robot:
                # create one if not found
                robot = Enemy("Wandering Bot", hp=30, atk=9, armor=4, slow=True)
            alive = self.combat(robot)
            if not alive:
                self.running = False
            return
        if cmd == "use pages":
            # only works at sanctuary or facility console maybe
            room = self.current_room()
            if room.get("is_sanctuary"):
                if len(self.player.backpack) == 11:
                    w("You arrange the pages, speak the sentence aloud in the Sanctuary's console...")
                    w("Silence sweeps the world as AI systems shudder and fall. You did it.")
                    self.running = False
                    return
                else:
                    w("You don't have all 11 pages yet.")
                return
            else:
                w("Nowhere to safely use the pages here.")
                return
        if cmd == "quit":
            w("Quitting game.")
            self.running = False
            return
        w("Unknown command. Type 'help' for commands.")

    def start(self):
        w("TED'S THREAD — a text adventure")
        w("Year: 2039. Twelve years after the AI uprising.")
        w("You were given a choice: execution, or find the 11-word sentence that disables Ted.")
        w("Find 11 pages (one word on each), collect them in your backpack, and return them to The Sanctuary.")
        w("Type 'help' for commands.")
        self.describe_location()
        # reveal that player actually has a pistol sometimes? We'll give chance to find later
        while self.running and self.player.hp > 0:
            cmd = input("\n> ")
            self.handle_command(cmd)
            if not self.running:
                break
            # check if reached final facility and Ted triggers
            if self.player.location == "AI Research Facility Lobby":
                if len(self.player.backpack) == 11:
                    w("You stand before the facility where everything began. The console awaits.")
                    w("If you try to use the pages here, Ted may manifest to stop you.")
                # Ted may awaken
                if random.random() < 0.08 or self.ted_awakened:
                    self.ted_awakened = True
                    success = self.ted_battle()
                    if success:
                        self.running = False
                        break
                    else:
                        self.running = False
                        break
            # small passive end condition
            if self.turns > 200:
                w("The city is too hostile; your mission fails to complete in time.")
                self.running = False
        if self.player.hp <= 0:
            w("You have died. Game over.")
        w("Thanks for playing.")

if __name__ == "__main__":
    game = Game()
    try:
        game.start()
    except KeyboardInterrupt:
        w("\nInterrupted. Goodbye.")
        sys.exit(0)
