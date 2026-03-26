import random
import os
import time

from characters import create_character
from enemies   import get_enemy, get_boss
from items     import random_loot, shop_stock
from combat    import combat, slow_print

CLASSES = [
    "Witch Hunter",
    "Plague Doctor",
    "Cursed Knight",
    "Occultist",
    "Revenant",
    "Survivalist",
    "??? (unlock with care)",
]

SECRET_UNLOCK = "MARI" 

FLOOR_EVENTS = ["combat", "combat", "combat", "shop", "rest", "loot", "elite"]

TITLE = r"""
  ██████╗██████╗ ██╗███╗   ███╗███████╗ ██████╗ ███╗   ██╗
 ██╔════╝██╔══██╗██║████╗ ████║██╔════╝██╔═══██╗████╗  ██║
 ██║     ██████╔╝██║██╔████╔██║███████╗██║   ██║██╔██╗ ██║
 ██║     ██╔══██╗██║██║╚██╔╝██║╚════██║██║   ██║██║╚██╗██║
 ╚██████╗██║  ██║██║██║ ╚═╝ ██║███████║╚██████╔╝██║ ╚████║
  ╚═════╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝
                    D E P T H S
  ─────────────────────────────────────────────────────────
  A gothic horror roguelike. Every descent will be your last (Yo ts is so not serious).
"""

FLOOR_DESCRIPTIONS = [
    "The cobblestones are slick with old blood.",
    "Torchlight flickers. Something breathes in the dark.",
    "The walls weep black ichor.",
    "Bones crunch beneath your feet.",
    "A distant choir sings hymns in reverse.",
    "The air tastes of sulfur and rot.",
    "You hear your own heartbeat echoed back.",
    "The shadows move before you do.",
    "A child's laughter echoes ahead.",
    "The deeper you go, the warmer it gets.",
    "A note on the wall reads: 'Prepare for acronym test 8'",
    "wtf is this floor made of"
]


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\n  [ Press ENTER to continue ]\n")


class Game:
    def __init__(self):
        self.player = None
        self.floor  = 1
        self.running = True

    # ─────────────────────────────────────────
    #  MAIN LOOP
    # ─────────────────────────────────────────

    def run(self):
        clear()
        slow_print(TITLE, delay=0.005)
        pause()
        self.main_menu()

    def main_menu(self):
        while True:
            clear()
            print("\n  ╔══════════════════════════╗")
            print("  ║  1. New Game             ║")
            print("  ║  2. How to Play          ║")
            print("  ║  3. Quit                 ║")
            print("  ╚══════════════════════════╝\n")
            choice = input("  > ").strip()
            if choice == "1":
                self.new_game()
                if self.running:
                    self.game_loop()
            elif choice == "2":
                self.how_to_play()
            elif choice == "3":
                slow_print("\n  The diharkness welcomes you.\n")
                break

    def how_to_play(self):
        clear()
        slow_print("""
  ── HOW TO PLAY (read ts nga) ─────────────────────────────────────────

  You wild descend through cursed floors, each more dangerous
  than the last. On each floor you will encounter:

    ⚔  Combat    — pokemon style
    💀 Elite     — a harder enemy with better shit
    👑 Boss      — every 5th floor, a politcian waits.
    🛒 Shop      — we know you broke nga 😂
    🔥 Rest Site — fortnite campfire
    📦 Loot      — E Coli or Sacred Heart

  In combat, you may:
    Attack      — standard strike
    Use a Skill — class ability, each unique per class
    Use an Item — consumables from your inventory DONT HOARD
    Flee        — black special

  Status Effects:
    Bleeding  — lose HP each round
    Plague    — lose HP each round (worse no shit)
    Cursed    — -2 STR
    Rotting   — lose 1 Armor per round (ts lwk the worst)
    Stunned   — lose your next turn (cucked)

  Reach floor 10 to face the final boss and escape.
  Or die trying. (dih)

  ────────────────────────────────────────────────────────
""")
        pause()

    # ─────────────────────────────────────────
    #  NEW GAME SETUP
    # ─────────────────────────────────────────

    def new_game(self):
        clear()
        slow_print("\n  ── CHARACTER CREATION ─────────────────────────────\n")
        name = input("  Enter your name, traveller: ").strip()
        if not name:
            name = "Bitch"

        slow_print("\n  Choose your class:\n")
        for i, c in enumerate(CLASSES, 1):
            print(f"    [{i}] {c}")
        print()

        chosen_class = None
        while not chosen_class:
            choice = input("  > ").strip().upper()

            # Secret unlock
            if choice == SECRET_UNLOCK:
                chosen_class = "Mari"
                slow_print("\n  ...the name hangs in the air.")
                slow_print("  A Larper approaches.")
                slow_print("  \"Heh... You called?\" he says nonchalantly.\n")
                time.sleep(1.5)
            else:
                try:
                    idx = int(choice) - 1
                    if 0 <= idx <= 5:
                        chosen_class = CLASSES[idx]
                    elif idx == 6:
                        slow_print("  You don't know the unlock word yet nga.")
                    else:
                        slow_print("  Invalid choice.")
                except (ValueError, IndexError):
                    slow_print("  Invalid choice.")

        self.player = create_character(chosen_class, name)
        slow_print(f"\n  You are {self.player.name}, the {self.player.class_name}.")
        slow_print(f"  \"{self.player.description}\"\n")

        # Starting item
        loot = random_loot(1)
        if loot:
            item = loot[0]
            self.player.add_to_inventory(item)
            slow_print(f"  You begin with: {item.name} — {item.description}")

        self.floor   = 1
        self.running = True
        pause()

    # ─────────────────────────────────────────
    #  GAME LOOP
    # ─────────────────────────────────────────

    def game_loop(self):
        while self.running and self.player.is_alive():
            clear()
            desc = FLOOR_DESCRIPTIONS[(self.floor - 1) % len(FLOOR_DESCRIPTIONS)]
            slow_print(f"\n  ╔══ FLOOR {self.floor} ═══════════════════════════════╗")
            slow_print(f"  ║  {desc:<46}║")
            slow_print(f"  ╚══════════════════════════════════════════════════╝")
            slow_print(self.player.status_summary())

            # Boss floor every 5th
            if self.floor % 5 == 0:
                self.boss_event()
            else:
                event = self.choose_event()
                self.run_event(event)

            if not self.player.is_alive():
                break

            # After event options
            self.between_floors()

        if not self.player.is_alive():
            self.game_over()
        self.running = False

    def choose_event(self):
        weights = {
            "combat": 40,
            "elite":  15,
            "shop":   15,
            "rest":   15,
            "loot":   15,
        }
        events  = list(weights.keys())
        w_vals  = [weights[e] for e in events]
        return random.choices(events, weights=w_vals, k=1)[0]

    def run_event(self, event):
        if event == "combat":
            self.combat_event(elite=False)
        elif event == "elite":
            self.combat_event(elite=True)
        elif event == "shop":
            self.shop_event()
        elif event == "rest":
            self.rest_event()
        elif event == "loot":
            self.loot_event()

    # ─────────────────────────────────────────
    #  EVENTS
    # ─────────────────────────────────────────

    def combat_event(self, elite=False):
        enemy = get_enemy(self.floor)
        if elite:
            enemy.hp       = int(enemy.hp * 1.5)
            enemy.max_hp   = enemy.hp
            enemy.strength = int(enemy.strength * 1.3)
            enemy.xp_reward = int(enemy.xp_reward * 1.5)
            enemy.gold_reward += random.randint(3, 8)
            slow_print(f"\n  ⚠  ELITE ENCOUNTER — {enemy.name} stirs...")
            time.sleep(0.8)

        result = combat(self.player, enemy)

        if result == "dead":
            return
        if result == "win" and elite:
            # Bonus loot from elites
            loot = random_loot(1)
            if loot:
                item = loot[0]
                self.player.add_to_inventory(item)
                slow_print(f"\n  📦 Elite loot: {item.name} — {item.description}")
        pause()

    def boss_event(self):
        boss_intros = [
            "  The floor trembles. A boss approaches.",
            "  The air goes colder.",
            "  Something massive stirs ahead. (dih)",
            "  Good luck.",
            "  The darkness thickens. Even the rats fled this floor.",
        ]
        slow_print(f"\n  ☠  {random.choice(boss_intros)}")
        slow_print(f"  BOSS FLOOR {self.floor}. Go off.\n")
        time.sleep(1)

        from enemies import get_boss
        boss = get_boss(self.floor)
        result = combat(self.player, boss)

        if result == "dead":
            return

        if self.floor >= 10:
            self.victory()
            return

        # Boss loot
        loot = random_loot(2)
        for item in loot:
            self.player.add_to_inventory(item)
            slow_print(f"  📦 Boss loot: {item.name} — {item.description}")
        self.player.gold += 20
        slow_print(f"  💰 +20 gold from the boss's hoard.")
        pause()

    def shop_event(self):
        clear()
        slow_print("\n  🛒 ── THE BONER MERCHANT ────────────────────────────")
        slow_print("  A hunched figure beckons from behind a rotting popeyes sign.")
        slow_print(f"  Your gold: {self.player.gold}g\n")

        stock = shop_stock()
        for i, item in enumerate(stock, 1):
            print(f"  [{i}] {item.name} ({item.value}g) — {item.description}")
        print(f"  [0] Leave\n")

        while True:
            choice = input("  > ").strip()
            if choice == "0":
                slow_print("  \"Come back when you're not a broke ass nga.\"")
                break
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(stock):
                    item = stock[idx]
                    if self.player.gold >= item.value:
                        self.player.gold -= item.value
                        self.player.add_to_inventory(item)
                        slow_print(f"  Purchased: {item.name}. Gold remaining: {self.player.gold}g")
                        stock.pop(idx)
                        if not stock:
                            slow_print("  \"Sold out. Move along bitch.\"")
                            break
                    else:
                        slow_print(f"  ✗ Not enough gold. (Need {item.value}g, have {self.player.gold}g)")
            except (ValueError, IndexError):
                slow_print("  ✗ Invalid choice.")
        pause()

    def rest_event(self):
        clear()
        rest_lines = [
            "  A dying fire.",
            "  A rare moment of quiet. Wonder when MR C will yap again",
            "  A campfire. cant craft at this one bub.",
            "  whats up niggatron",
            "  A warm corner of hell. You take what you can get.",
        ]
        slow_print("\n  🔥 ── REST SITE ─────────────────────────────────────")
        slow_print(f"  {random.choice(rest_lines)}\n")
        heal_amt = int(self.player.max_hp * 0.30)
        healed   = self.player.heal(heal_amt)
        slow_print(f"  You tend your wounds. Healed {healed} HP.")
        slow_print(f"  HP: {self.player.hp}/{self.player.max_hp}")

        # Option to remove a status effect
        if self.player.status_effects:
            slow_print(f"\n  Active effects: {', '.join(self.player.status_effects)}")
            choice = input("  Remove one status effect? [Y/N]: ").strip().upper()
            if choice == "Y":
                removed = self.player.status_effects.pop(0)
                slow_print(f"  {removed} fades in the firelight.")
        pause()

    def loot_event(self):
        clear()
        cache_lines = [
            "  Hidden beneath a loose stone. Good Jew.",
            "  A crate with some shitty designer knock off logo written on it.",
            "  2 gb of RAM. Take what you can get twin",
            "  Someone left their USB here.",
            "  gooning",
        ]
        slow_print("\n  📦 ── ABANDONED CACHE ──────────────────────────────")
        slow_print(f"  {random.choice(cache_lines)}\n")
        n    = random.choice([1, 1, 2])
        loot = random_loot(n)
        for item in loot:
            self.player.add_to_inventory(item)
            slow_print(f"  Found: {item.name} — {item.description}")
        bonus_gold = random.randint(0, 8)
        if bonus_gold:
            self.player.gold += bonus_gold
            slow_print(f"  Found {bonus_gold}g tucked inside.")
        pause()

    # ─────────────────────────────────────────
    #  BETWEEN FLOORS
    # ─────────────────────────────────────────

    def between_floors(self):
        clear()
        slow_print(self.player.status_summary())
        print("  ── What will you do? ───────────────────────────────")
        print("  [1] Descend deeper")
        print("  [2] Check inventory")
        print("  [3] View skills")
        print("  [4] Quit to menu")

        while True:
            choice = input("\n  > ").strip()
            if choice == "1":
                self.floor += 1
                break
            elif choice == "2":
                clear()
                slow_print(self.player.show_inventory())
                print("\n  [U] Use an item  [B] Back")
                sub = input("  > ").strip().upper()
                if sub == "U":
                    usable = [it for it in self.player.inventory if it.item_type == "consumable"]
                    if not usable:
                        slow_print("  No consumable items.")
                    else:
                        for i, it in enumerate(usable, 1):
                            print(f"  [{i}] {it.name}")
                        try:
                            idx = int(input("  > ").strip()) - 1
                            if 0 <= idx < len(usable):
                                item = usable[idx]
                                self.player.inventory.remove(item)
                                slow_print(item.use(self.player))
                        except (ValueError, IndexError):
                            slow_print("  Invalid.")
                pause()
                clear()
                slow_print(self.player.status_summary())
                print("  [1] Descend  [2] Inventory  [3] Skills  [4] Quit")
            elif choice == "3":
                clear()
                slow_print("\n  ── Your Skills ─────────────────────────────────")
                for skill in self.player.skills:
                    slow_print(f"  ✦ {skill.name}: {skill.description}")
                pause()
                clear()
                slow_print(self.player.status_summary())
                print("  [1] Descend  [2] Inventory  [3] Skills  [4] Quit")
            elif choice == "4":
                slow_print("\n  You retreat from the depths... for now.")
                self.running = False
                break

    # ─────────────────────────────────────────
    #  END STATES
    # ─────────────────────────────────────────

    def game_over(self):
        clear()
        slow_print("""
  ╔═══════════════════════════════════════════╗
  ║                                           ║
  ║         Y O U   H A V E   F A L L E N    ║
  ║                                           ║
  ║  yo you suck.                             ║
  ║  Shah said he could've done it.           ║
  ║  He could not have done it.               ║
  ║  Justin Lin is directing your funeral.    ║
  ║   This WILL get a sequel.                 ║
  ╚═══════════════════════════════════════════╝
""", delay=0.04)
        slow_print(f"  You reached Floor {self.floor}.")
        slow_print(f"  Final level: {self.player.level}\n")
        pause()

    def victory(self):
        clear()
        slow_print("""
  ╔═══════════════════════════════════════════╗
  ║                                           ║
  ║    Y O U   E S C A P E D   T H E         ║
  ║    C R I M S O N   D E P T H S           ║
  ║                                           ║
  ║  The light above blinds you.              ║
  ║  You cannot remember what warmth felt     ║
  ║  like. But you are alive.                 ║
  ║  Probably. You could go for popeyes       ║
  ║                                           ║
  ╚═══════════════════════════════════════════╝
""", delay=0.04)
        slow_print(f"  Floors cleared: {self.floor}")
        slow_print(f"  Final level: {self.player.level}")
        slow_print(f"  Gold remaining: {self.player.gold}g\n")
        self.running = False
        pause()