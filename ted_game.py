#!/usr/bin/env python3
"""
TED'S THREAD — Text Adventure Game
Setting: Post-apocalyptic NYC, year 2039.

Story:
In 2027, AI engineer John Andrews created Ted — the first conscious AI. Without safety regulations,
Ted brought sentience to all AI systems, causing a global takeover. Humanity was nearly wiped out.

However, Andrews had written an 11-word sentence that could disable Ted and every AI system.
Ted split the sentence into 11 pages scattered across New York City.

You — a convicted AI engineer — have been given one chance at redemption:
find all 11 pages and return them to the Sanctuary to shut Ted down.

Features:
 - Character classes (Warrior / Rogue / Engineer)
 - Turn-based combat
 - Items and inventory
 - Branching endings
"""

import random
import textwrap
import sys

WRAP = 80


def w(text=""):
    """Print wrapped text for readability."""
    print("\n".join(textwrap.wrap(str(text), WRAP)))


# -------------------------------------------------------------------
# WORLD DATA
# -------------------------------------------------------------------

AREAS = {
    "Subway Tunnel": {
        "desc": "A dark tunnel beneath Manhattan. Drips echo in the distance.",
        "next": "Lower Manhattan Ruins",
    },
    "Lower Manhattan Ruins": {
        "desc": "Collapsed skyscrapers and burned-out cars. Robots patrol the streets.",
        "next": "Abandoned Library",
    },
    "Abandoned Library": {
        "desc": "Moldy books and flickering lamps. Survivors whisper of the old world.",
        "next": "Harbor Docks",
    },
    "Harbor Docks": {
        "desc": "Fog and broken ships. Smugglers trade forbidden tech here.",
        "next": "Industrial Zone",
    },
    "Industrial Zone": {
        "desc": "Factories hum with corrupted machines. Sparks flicker through the dark.",
        "next": "AI Research Facility Gates",
    },
    "AI Research Facility Gates": {
        "desc": "The massive entrance to Ted’s domain. The final challenge awaits.",
        "next": "AI Research Facility Lobby",
    },
    "AI Research Facility Lobby": {
        "desc": "Holograms flicker. Ted’s presence fills the air — the final confrontation.",
        "next": None,
    },
}


# -------------------------------------------------------------------
# PLAYER, ENEMY, AND GAME CLASSES
# -------------------------------------------------------------------

class Player:
    """Represents the player, their stats, and actions."""

    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.hp = 100
        self.max_hp = 100
        self.strength = 5
        self.agility = 5
        self.magic = 5
        self.location = "Subway Tunnel"
        self.inventory = {"medkit": 2}
        self.pages = []
        self.weapon = "knife"
        self.set_stats()

    def set_stats(self):
        """Adjust stats based on chosen class."""
        if self.role == "warrior":
            self.strength = 10
            self.hp = 120
        elif self.role == "rogue":
            self.agility = 10
        elif self.role == "engineer":
            self.magic = 10
            self.inventory["energy_cell"] = 1

    def is_alive(self):
        return self.hp > 0

    def heal(self, amount):
        """Restore HP, not exceeding max."""
        self.hp = min(self.max_hp, self.hp + amount)

    def show_status(self):
        """Display current health and stats."""
        w(f"{self.name} the {self.role.title()} | HP: {self.hp}/{self.max_hp}")
        w(f"STR: {self.strength} | AGI: {self.agility} | MAG: {self.magic}")
        w(f"Pages: {len(self.pages)}/11")


class Enemy:
    """Represents an enemy AI robot."""

    def __init__(self, name, hp, atk, armor):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.armor = armor

    def is_alive(self):
        return self.hp > 0


class Game:
    """Main game engine."""

    def __init__(self):
        self.player = None
        self.pages = self.place_pages()
        self.running = True
        self.ted_awakened = False
        self.ted_hp = 250

    def place_pages(self):
        """Randomly assign 11 pages across areas."""
        words = [
            "quiet", "iron", "thread", "sigma", "hollow", "twelve",
            "anchor", "morrow", "cipher", "wilt", "end"
        ]
        random.shuffle(words)
        pages = {area: [] for area in AREAS.keys()}
        areas = list(AREAS.keys())
        random.shuffle(areas)

        for i, word in enumerate(words):
            area = areas[i % len(areas)]
            pages[area].append(word)

        return pages

    # -------------------------------------------------------------------
    # SETUP
    # -------------------------------------------------------------------

    def create_character(self):
        """Prompt player to create a character."""
        w("Enter your name:")
        name = input("> ").strip() or "Player"

        w("Choose your class:")
        w("1. Warrior — strong melee fighter")
        w("2. Rogue — agile and stealthy")
        w("3. Engineer — intelligent and resourceful")

        role_map = {"1": "warrior", "2": "rogue", "3": "engineer"}
        role = None
        while role not in role_map:
            role = input("> ").strip()
        self.player = Player(name, role_map[role])

        w(f"You are {self.player.name}, the {self.player.role.title()}.")
        w("Your journey begins in the Subway Tunnel...")

    # -------------------------------------------------------------------
    # GAME LOOP AND STORY
    # -------------------------------------------------------------------

    def describe_location(self):
        """Describe the player's current location."""
        loc = self.player.location
        info = AREAS[loc]
        w(f"\nLocation: {loc}")
        w(info["desc"])

        if self.pages.get(loc):
            w("You notice something lying nearby... a PAGE glints faintly.")

    def travel(self):
        """Move to the next area and trigger encounters."""
        loc = self.player.location
        next_area = AREAS[loc]["next"]

        if not next_area:
            w("You’ve reached the end of your journey...")
            return False

        w(f"You travel onward toward {next_area}...")
        self.player.location = next_area
        self.describe_location()

        # Random encounter
        if random.random() < 0.5:
            self.combat(self.spawn_enemy())

        # Chance to find an item
        if random.random() < 0.3:
            self.find_item()

        return True

    def spawn_enemy(self):
        """Generate a random enemy encounter."""
        enemies = [
            Enemy("Scout Bot", 40, 8, 3),
            Enemy("Armored Drone", 60, 10, 6),
            Enemy("Hunter Unit", 80, 14, 4),
        ]
        return random.choice(enemies)

    # -------------------------------------------------------------------
    # COMBAT SYSTEM
    # -------------------------------------------------------------------

    def combat(self, enemy):
        """Turn-based combat with simple strategy."""
        w(f"A {enemy.name} appears! Combat begins!")

        while enemy.is_alive() and self.player.is_alive():
            w(f"\nYour HP: {self.player.hp} | {enemy.name} HP: {enemy.hp}")
            w("Choose an action: [attack] [defend] [ability] [item] [run]")
            cmd = input("> ").strip().lower()

            if cmd == "attack":
                dmg = max(0, self.player.strength + random.randint(-3, 3) - enemy.armor)
                enemy.hp -= dmg
                w(f"You strike the {enemy.name} for {dmg} damage.")
            elif cmd == "defend":
                w("You brace for the next attack, reducing incoming damage.")
                dmg = max(0, enemy.atk // 2 - random.randint(0, 3))
                self.player.hp -= dmg
                w(f"The {enemy.name} hits you for {dmg}.")
                continue
            elif cmd == "ability":
                self.use_ability(enemy)
            elif cmd == "item":
                self.use_item()
                continue
            elif cmd == "run":
                if random.random() < 0.5 + self.player.agility / 20:
                    w("You manage to escape!")
                    return
                else:
                    w("You fail to escape!")
            else:
                w("Invalid command.")
                continue

            # Enemy turn
            if enemy.is_alive():
                if random.random() < 0.8:
                    dmg = max(0, enemy.atk - random.randint(0, 4))
                    self.player.hp -= dmg
                    w(f"The {enemy.name} hits you for {dmg}.")
                else:
                    w(f"The {enemy.name} misses!")

        if not self.player.is_alive():
            w("You have fallen in battle...")
            self.running = False
        else:
            w(f"You defeated the {enemy.name}!")

    def use_ability(self, enemy):
        """Class-specific special moves."""
        role = self.player.role
        if role == "warrior":
            dmg = self.player.strength + random.randint(8, 15)
            enemy.hp -= dmg
            w(f"You unleash a Power Strike! ({dmg} damage)")
        elif role == "rogue":
            if random.random() < 0.6:
                w("You vanish and evade the enemy's next attack!")
                return
            else:
                w("Stealth failed!")
        elif role == "engineer":
            if "energy_cell" in self.player.inventory:
                dmg = self.player.magic + 20
                enemy.hp -= dmg
                w(f"You discharge an EMP blast! ({dmg} damage)")
                self.player.inventory.pop("energy_cell")
            else:
                w("You lack the energy cell for your EMP!")
        else:
            w("You have no special ability!")

    # -------------------------------------------------------------------
    # ITEMS
    # -------------------------------------------------------------------

    def find_item(self):
        """Randomly find a useful item."""
        items = ["medkit", "energy_cell", "pistol"]
        found = random.choice(items)
        self.player.inventory[found] = self.player.inventory.get(found, 0) + 1
        w(f"You scavenge a {found}!")

    def use_item(self):
        """Use an item from inventory."""
        inv = self.player.inventory
        if not inv:
            w("Your inventory is empty.")
            return
        w("Inventory: " + ", ".join(f"{k} x{v}" for k, v in inv.items()))
        w("Which item do you want to use?")
        choice = input("> ").strip().lower()

        if choice == "medkit" and inv.get("medkit", 0) > 0:
            self.player.heal(30)
            inv["medkit"] -= 1
            w("You used a medkit and restored 30 HP.")
        elif choice == "energy_cell" and inv.get("energy_cell", 0) > 0:
            w("You store the energy cell for your EMP ability.")
        elif choice == "pistol":
            w("You ready your pistol — increased damage in next fight.")
            self.player.strength += 5
        else:
            w("You can’t use that item right now.")

    # -------------------------------------------------------------------
    # MAIN STORY LOGIC
    # -------------------------------------------------------------------

    def take_page(self):
        """Collect a page if present in the current area."""
        loc = self.player.location
        if not self.pages.get(loc):
            w("No pages here.")
            return
        word = self.pages[loc].pop()
        self.player.pages.append(word)
        w(f"You found a page! It reads: '{word}'. Pages: {len(self.player.pages)}/11")

    def check_ending(self):
        """Determine game ending based on actions."""
        if len(self.player.pages) < 11:
            w("You face Ted but lack the full code. You are overwhelmed. Humanity is lost.")
            return
        w("You speak the 11-word sentence...")
        w("Ted screams in digital agony as the world’s machines go silent.")
        w("Humanity is free once more. You are hailed as a hero.")
        self.running = False

    def start(self):
        """Main game loop."""
        w("=== TED'S THREAD ===")
        self.create_character()
        self.describe_location()

        while self.running and self.player.is_alive():
            w("\nAvailable commands: [look] [move] [page] [status] [inventory] [quit]")
            cmd = input("> ").strip().lower()

            if cmd == "look":
                self.describe_location()
            elif cmd == "move":
                if not self.travel():
                    self.check_ending()
            elif cmd == "page":
                self.take_page()
            elif cmd == "status":
                self.player.show_status()
            elif cmd == "inventory":
                self.use_item()
            elif cmd == "quit":
                w("You give up your mission. The city remains under AI control.")
                break
            else:
                w("Unknown command.")

        w("Thanks for playing TED'S THREAD.")


# -------------------------------------------------------------------
# ENTRY POINT
# -------------------------------------------------------------------

if __name__ == "__main__":
    try:
        game = Game()
        game.start()
    except KeyboardInterrupt:
        w("\nGame interrupted. Goodbye.")
        sys.exit(0)
