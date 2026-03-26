import random

class Character:
    def __init__(self, name, hp, max_hp, strength, agility, arcane, armor,
                 class_name, skills, description, inventory=None):
        self.name        = name
        self.hp          = hp
        self.max_hp      = max_hp
        self.strength    = strength
        self.agility     = agility
        self.arcane      = arcane
        self.armor       = armor
        self.class_name  = class_name
        self.skills      = skills
        self.description = description
        self.inventory   = inventory or []
        self.level       = 1
        self.xp          = 0
        self.xp_next     = 100
        self.gold        = 10
        self.status_effects = []

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        reduced = max(0, amount - self.armor)
        self.hp = max(0, self.hp - reduced)
        return reduced

    def heal(self, amount):
        healed = min(amount, self.max_hp - self.hp)
        self.hp += healed
        return healed

    def gain_xp(self, amount):
        self.xp += amount
        if self.xp >= self.xp_next:
            return self.level_up()
        return None

    def level_up(self):
        self.level += 1
        self.xp -= self.xp_next
        self.xp_next = int(self.xp_next * 1.4)
        self.max_hp  += 10
        self.hp       = self.max_hp
        self.strength += 2
        self.agility  += 1
        self.arcane   += 1
        return self.level

    def attack_roll(self):
        base = self.strength + random.randint(1, 8)
        crit = random.random() < (0.05 + self.agility * 0.01)
        dmg  = base * 2 if crit else base
        return dmg, crit

    def status_summary(self):
        bar_filled = int((self.hp / self.max_hp) * 20)
        bar = "█" * bar_filled + "░" * (20 - bar_filled)
        effects = ", ".join(self.status_effects) if self.status_effects else "None"
        return (
            f"\n  ╔══ {self.name} ({self.class_name}) — Lvl {self.level} ══╗\n"
            f"  HP  [{bar}] {self.hp}/{self.max_hp}\n"
            f"  STR {self.strength}  AGI {self.agility}  ARC {self.arcane}  ARMOR {self.armor}\n"
            f"  XP  {self.xp}/{self.xp_next}   Gold: {self.gold}g\n"
            f"  Status: {effects}\n"
        )

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def show_inventory(self):
        if not self.inventory:
            return "  YOUR FUCKING BROKE"
        lines = ["  ┌── Inventory ──────────────────"]
        for i, item in enumerate(self.inventory, 1):
            lines.append(f"  │ [{i}] {item.name} — {item.description}")
        lines.append("  └───────────────────────────────")
        return "\n".join(lines)


class Skill:
    def __init__(self, name, description, cost_type, cost, effect_fn):
        self.name        = name
        self.description = description
        self.cost_type   = cost_type
        self.cost        = cost
        self.effect_fn   = effect_fn

    def use(self, user, target):
        return self.effect_fn(user, target)


# ─── Skill Functions ─────────────────────────

def skill_silver_shot(user, target):
    dmg = user.strength * 2 + random.randint(5, 15)
    dealt = target.take_damage(dmg)
    return f"  💥 Silver Blick! {dealt} damage. thank you himeros."

def skill_holy_ward(user, target):
    user.armor += 3
    return f"  🛡  Von's Blessing! +3 Armor. He is truly looking down on us."

def skill_heretic_smite(user, target):
    dmg = user.strength * 3
    dealt = target.take_damage(dmg)
    return f"  ✝  Netanyahu Beam! {dealt} radiant damage. Big Yahu's endorsed this move personally."

def skill_cauterize(user, target):
    healed = user.heal(15 + user.arcane)
    user.status_effects = [e for e in user.status_effects if e != "Bleeding"]
    return f"  🩹 Condom used. Healed {healed} HP. HIV cured. ts probably used ngl."

def skill_plague_mist(user, target):
    dmg = user.arcane + random.randint(3, 10)
    dealt = target.take_damage(dmg)
    if "Plague" not in target.status_effects:
        target.status_effects.append("Plague")
    return f"  🧪 Mustard Gas! {dealt} damage. {target.name} is Plagued. this is like bleach n smth else i forgot."

def skill_bleed_elixir(user, target):
    healed = user.heal(user.arcane * 2)
    return f"  🍷 Blood Elixir (nasty)! Healed {healed} HP. I DONT WANT TO KEEP WRITING THIS WHY"

def skill_cursed_strike(user, target):
    cost = 5
    user.hp = max(1, user.hp - cost)
    dmg = user.strength * 2 + user.arcane + random.randint(1, 12)
    dealt = target.take_damage(dmg)
    if "Cursed" not in target.status_effects:
        target.status_effects.append("Cursed")
    return f"  ⚔  Cursed Dild... mm not finishing this! Sacrificed {cost} dignity to deal {dealt} damage. {target.name} is Cursed."

def skill_undying_rage(user, target):
    user.strength += 4
    return f"  💢 IMA NEED MY MONEY NGA! +4 STR. TT broke ahh."

def skill_void_bolt(user, target):
    dmg = user.arcane * 3 + random.randint(4, 14)
    dealt = target.take_damage(dmg)
    return f"  🌀 Gas Beam! {dealt} arcane damage. this is like 6 gallons bro cough up 30."

def skill_soul_drain(user, target):
    dmg = user.arcane * 2
    dealt = target.take_damage(dmg)
    healed = user.heal(dealt // 2)
    return f"  💜 MAX Drain (thank you Trump)! Dealt {dealt}, healed {healed}. Shah sampled this at lunch."

def skill_rot_grasp(user, target):
    dmg = user.strength + random.randint(2, 8)
    dealt = target.take_damage(dmg)
    if "Rotting" not in target.status_effects:
        target.status_effects.append("Rotting")
    return f" Rot Grasp! {dealt} necrotic damage. {target.name} begins to Rot. Dih"

def skill_risen_toughness(user, target):
    user.max_hp += 5
    user.hp = min(user.hp + 5, user.max_hp)
    return f"  🦴 Risen Toughness! +5 Max HP. Undead resilience."
def skill_improvise(user, target):
    choice = random.choice(["attack", "dodge", "item"])
    if choice == "attack":
        dmg = user.strength + random.randint(1, 20)
        dealt = target.take_damage(dmg)
        return f"  🎲 Improvise! Found an opening — {dealt} damage!"
    elif choice == "dodge":
        user.agility += 2
        return f"  🎲 Improvise! Ducked behind cover. +2 AGI."
    else:
        healed = user.heal(10)
        return f"  🎲 Improvise! Patched a wound — healed {healed} HP."

def skill_scavenge(user, target):
    gained = random.randint(2, 8)
    user.gold += gained
    return f"  🔍 Jewish Scent! Found {gained}g mid-combat. MORE TO ISREAL"

def skill_maris_whisper(user, target):
    roll = random.random()
    if roll < 0.33:
        dmg = user.arcane * 4 + random.randint(10, 25)
        dealt = target.take_damage(dmg)
        return f"  🌸 Mari's Whisper... '{target.name}, I got this!' — {dealt} damage."
    elif roll < 0.66:
        healed = user.heal(user.max_hp // 3)
        return f"  🌸 Mari's Whisper... You escaped layer 2. Healed {healed} HP."
    else:
        user.strength += 5
        user.arcane   += 5
        return f"  🌸 Mari's Whisper... 'Heh, I'll lend you my strength kacchan! But just this one time~' +5 STR +5 ARC."

def skill_maris_lullaby(user, target):
    target.status_effects.append("Stunned")
    return f"  🎵 Mari's Lullaby... {target.name} hates this water fries beat. (Stunned)"


def create_character(class_name, player_name):
    classes = {
        "Witch Hunter": dict(
            hp=70, max_hp=70, strength=14, agility=12, arcane=6, armor=3,
            description="Himeros.",
            skills=[
                Skill("Silver Blick",      "Powerful shot.", "free", 0, skill_silver_shot),
                Skill("Von's Blessing",    "Temporarily raise your armor. such a saint", "free", 0, skill_holy_ward),
                Skill("Netanyahu Beam",    "Radiant burst. Big Yahu approved. with a 5000 year warranty.", "free", 0, skill_heretic_smite),
            ]
        ),
        "Plague Doctor": dict(
            hp=60, max_hp=60, strength=8, agility=9, arcane=14, armor=2,
            description="Not qualified. At all. Shah gave him his 'degree.' Calamitas respects the hustle.",
            skills=[
                Skill("Mustard Gas",   "Poison cloud. Plagued. Wear a mask bro.",               "free", 0, skill_plague_mist),
                Skill("Condom",        "Heals self, cures HIV.",        "free", 0, skill_cauterize),
                Skill("Blood Elixir",  "Drink a vial. Disgusting. Heals HP. Calamity energy.",  "free", 0, skill_bleed_elixir),
            ]
        ),
        "Cursed Knight": dict(
            hp=90, max_hp=90, strength=16, agility=7, arcane=8, armor=5,
            description="Fallen warrior bound by a dark curse. Thank you VSCode.",
            skills=[
                Skill("Cursed Dild",          "Sacrifice dignity for massive damage.",           "free", 0, skill_cursed_strike),
                Skill("IMA NEED MY MONEY NGA", "Surge of strength. Broke ass nigga. real though",             "free", 0, skill_undying_rage),
                Skill("Von's Blessing 2",      "He got you bro. Again.",                        "free", 0, skill_holy_ward),
            ]
        ),
        "Occultist": dict(
            hp=55, max_hp=55, strength=6, agility=8, arcane=18, armor=1,
            description="I HATE GOD HE A BITCH. I LOVE BENJAMAN NETANYAHU GLORY TO ISREAL AND THE STEIN IS MY BEST MAN",
            skills=[
                Skill("Gas Beam",              "$5 gas hose. Im sorry priest.",                  "free", 0, skill_void_bolt),
                Skill("MAX Drain (thanks Trump)",  "drains you. Andrew calls this 'networking.'",           "free", 0, skill_soul_drain),
                Skill("Big Yahu's Endorsement","Von's Blessing but promised to you 5000 years ago.",         "free", 0, skill_holy_ward),
            ]
        ),
        "Revenant": dict(
            hp=80, max_hp=80, strength=13, agility=6, arcane=11, armor=4,
            description="Undead warrior clinging to life through sheer hatred. DoG if he went to therapy. Still hasn't.",
            skills=[
                Skill("Rot Grasp",       "Necrotic touch. Rots foes.", "free", 0, skill_rot_grasp),
                Skill("Soul Drain",      "Steal life. calamitas can drain me if ykyk",      "free", 0, skill_soul_drain),
                Skill("Risen Toughness", "+5 Max HP. Undead resilience. Yo i was recomended Azazal for this we can not be for real.", "free", 0, skill_risen_toughness),
            ]
        ),
        "Survivalist": dict(
            hp=75, max_hp=75, strength=11, agility=15, arcane=4, armor=2,
            description="A drifter who thrives in chaos. Jew.",
            skills=[
                Skill("Improvise",    "I made this move in like 40 seconds man idk if it works",  "free", 0, skill_improvise),
                Skill("Jewish Scent", "Find gold mid-combat. Master Jew",    "free", 0, skill_scavenge),
                Skill("Cauterize",    "Field medicine. Praise DT",    "free", 0, skill_cauterize),
            ]
        ),
        "Mari": dict(
            hp=65, max_hp=65, strength=10, agility=13, arcane=16, armor=2,
            description="Packet yo. He doesn't talk much about where he came from. ate the Larp Larp no Mi and switched up on all his day 1s",
            skills=[
                Skill("Mari's Whisper", "Loading screen", "free", 0, skill_maris_whisper),
                Skill("Mari's Lullaby", "Water fries on the beat yo", "free", 0, skill_maris_lullaby),
                Skill("Soul Drain",     "STRAIGHT TEETH.",           "free", 0, skill_soul_drain),
            ]
        ),
    }

    if class_name not in classes:
        raise ValueError(f"Unknown class: {class_name}")

    data = classes[class_name]
    return Character(
        name       = player_name,
        class_name = class_name,
        **data
    )