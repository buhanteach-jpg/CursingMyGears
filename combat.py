import random
import time

def slow_print(text, delay=0.025):
    """I LOVE NIKOLA TESLA"""
    for line in text.split("\n"):
        print(line)
        time.sleep(delay)

def apply_status_effects(character):
    """Tick status effects at start of turn. Returns list of messages."""
    messages = []
    for effect in list(character.status_effects):
        if effect == "Bleeding":
            dmg = random.randint(2, 5)
            character.hp = max(0, character.hp - dmg)
            messages.append(f"  🩸 {character.name} bleeds for {dmg} damage.")
        elif effect == "Plague":
            dmg = random.randint(3, 7)
            character.hp = max(0, character.hp - dmg)
            messages.append(f"  🧪 Plague wracks {character.name} for {dmg} damage.")
        elif effect == "Rotting":
            character.armor = max(0, character.armor - 1)
            messages.append(f"  🪦 {character.name}'s flesh rots — armor reduced.")
        elif effect == "Cursed":
            pass  
        elif effect == "Stunned":
            messages.append(f"  💫 {character.name} is Stunned and loses their turn!")
    return messages

def combat(player, enemy):
    """
    Full turn-based combat loop.
    Returns "win", "flee", or "dead".
    """
    slow_print(f"\n  ═══════════════════════════════════════")
    slow_print(f"  ⚔  ENCOUNTER: {enemy.name}")
    slow_print(f"  \"{enemy.description}\"")
    slow_print(f"  ═══════════════════════════════════════\n")


    player_armor_start = player.armor

    round_num = 0
    while player.is_alive() and enemy.is_alive():
        round_num += 1
        slow_print(f"\n  ── Round {round_num} ──────────────────────────────")
        slow_print(f"  {player.name} HP: {player.hp}/{player.max_hp}  │  "
                   f"{enemy.name} [{enemy.hp_bar()}] {enemy.hp}/{enemy.max_hp}")

        for msg in apply_status_effects(player):
            slow_print(msg)
        if not player.is_alive():
            break

        for msg in apply_status_effects(enemy):
            slow_print(msg)
        if not enemy.is_alive():
            break

        player_stunned = "Stunned" in player.status_effects
        if player_stunned:
            player.status_effects.remove("Stunned")
            slow_print(f"  💫 You shake off the stun — but lose this turn.")
        else:
            action = player_turn(player, enemy)
            if action == "flee":
                flee_chance = 0.40 + player.agility * 0.02
                if random.random() < flee_chance:
                    slow_print(f"\n  🏃 NIGERUNDAYO!")
                    player.armor = player_armor_start
                    return "flee"
                else:
                    slow_print(f"  ✗ No escape! {enemy.name} cock blocks you")

            if not enemy.is_alive():
                break

        enemy_stunned = "Stunned" in enemy.status_effects
        if enemy_stunned:
            enemy.status_effects.remove("Stunned")
            slow_print(f"  💫 {enemy.name} is stunned — loses their turn.")
        else:
            raw_dmg  = enemy.attack()
            dealt    = player.take_damage(raw_dmg)
            slow_print(f"\n  👹 {enemy.name} attacks! Deals {dealt} damage.")

            special_msg = enemy.use_special(player)
            if special_msg:
                slow_print(special_msg)

    player.armor = player_armor_start

    if not player.is_alive():
        slow_print(f"\n  ╔══════════════════════════════╗")
        slow_print(f"  ║   YOU HAVE FALLEN...         ║")
        slow_print(f"  ╚══════════════════════════════╝")
        return "dead"

    slow_print(f"\n  ✦ Victory! {enemy.name} is slain.")
    xp_gained   = enemy.xp_reward
    gold_gained = enemy.gold_reward
    player.gold += gold_gained
    slow_print(f"  +{xp_gained} XP   +{gold_gained} gold")

    new_level = player.gain_xp(xp_gained)
    if new_level:
        slow_print(f"\n  ★ LEVEL UP! You are now level {new_level}!")
        slow_print(f"  Max HP +10, STR +2, AGI +1, ARC +1. Fully healed.")

    player.status_effects = [e for e in player.status_effects if e != "Stunned"]

    return "win"


def player_turn(player, enemy):
    """Show player action menu and resolve choice. Returns action string."""
    print()
    print("  What do you do?")
    print("  [1] Attack")
    if player.skills:
        for i, skill in enumerate(player.skills, 2):
            print(f"  [{i}] {skill.name} — {skill.description}")
    item_offset = len(player.skills) + 2
    usable_items = [it for it in player.inventory if it.item_type in ("consumable",)]
    if usable_items:
        print(f"  [{item_offset}] Use Item")
    print(f"  [F] Flee")

    while True:
        choice = input("\n  > ").strip().upper()

        if choice == "1":
            dmg, crit = player.attack_roll()
            dealt = enemy.take_damage(dmg)
            crit_text = " ★ CRITICAL HIT!" if crit else ""
            slow_print(f"  ⚔  You strike {enemy.name} for {dealt} damage.{crit_text}")
            return "attack"

        for idx, skill in enumerate(player.skills, 2):
            if choice == str(idx):
                result = skill.use(player, enemy)
                slow_print(result)
                return "skill"

        if choice == str(item_offset) and usable_items:
            result = use_item_menu(player, usable_items)
            slow_print(result)
            return "item"

        if choice == "F":
            return "flee"

        print("  ✗ Invalid choice.")


def use_item_menu(player, usable_items):
    print("\n  ── Items ───────────────────────")
    for i, item in enumerate(usable_items, 1):
        print(f"  [{i}] {item.name} — {item.description}")
    print("  [0] Cancel")

    while True:
        choice = input("\n  > ").strip()
        if choice == "0":
            return "  You decide to save your supplies."
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(usable_items):
                item = usable_items[idx]
                player.inventory.remove(item)
                return item.use(player)
        except ValueError:
            pass
        print("  ✗ Invalid choice.")
