import random

class Item:
    def __init__(self, name, description, item_type, effect_fn, value=5):
        self.name        = name
        self.description = description
        self.item_type   = item_type
        self.effect_fn   = effect_fn
        self.value       = value

    def use(self, character):
        return self.effect_fn(character)


def use_bandage(user):
    healed = user.heal(20)
    user.status_effects = [e for e in user.status_effects if e != "Bleeding"]
    return f"  🩹 Bandage applied. Healed {healed} HP. HIV cured. Gucci Third leg might not catch you this time."

def use_blood_vial(user):
    healed = user.heal(35)
    return f"  🩸 Blood Vial consumed. Healed {healed} HP. I dont like writing this item out bro just dont fucking use it why the fuck did i add it i cant remove it now i got like 12 minutes left."

def use_laudanum(user):
    user.strength += 3
    user.agility  += 2
    return f"  💊 Fent taken. +3 STR, +2 AGI. TS WAS LACED NGA"

def use_holy_water(user):
    user.status_effects = []
    healed = user.heal(10)
    return f"  💧 Holy Water! All effects cleansed. PRAISE THE LORD. Healed {healed} HP. Yes I need to glaze god bro sybau."

def use_dark_tonic(user):
    user.arcane += 4
    return f"  🌑 Sus Tonic drunk. +4 ARCANE. goon juice"

def use_smelling_salts(user):
    user.status_effects = [e for e in user.status_effects if e != "Stunned"]
    healed = user.heal(5)
    return f"  💨 Smelling Salts — Stunned cured. Healed {healed} HP. Nose kinda burns."
def use_iron_shards(user):
    user.armor += 2
    return f"  🔩 Iron Shards sewn into armor. +2 Armor. Smart boy."

def use_witch_charm(user):
    user.arcane += 2
    user.max_hp += 5
    user.hp = min(user.hp + 5, user.max_hp)
    return f"  🧿 Nigerian Charm equipped. +2 ARC, +5 Max HP. Thank you priest"

def use_cursed_tome(user):
    cost = 10
    user.hp = max(1, user.hp - cost)
    user.arcane += 6
    return f"  📖 Literature read (Circe). Lost {cost} HP — gained +6 ARCANE. kinda mid."

def use_silver_dagger(user):
    user.strength += 3
    return f"  🗡  Silver Dagger equipped. +3 STR. roadman breathing 1st form"

def use_rusted_shield(user):
    user.armor += 3
    return f"  🛡  Rusted Shield strapped on. +3 Armor. Justin Lin would've given this to the wrong character."

def use_maris_ribbon(user):
    user.max_hp += 20
    user.hp = user.max_hp
    user.agility += 3
    return f"  🎀 Mari's Tails Plushie... fully healed. +20 Max HP, +3 AGI. Bad blood... but useful. Don't ask about emily."

def use_packet_tracer_cd(user):
    user.arcane += 5
    user.strength += 2
    return f"  💿 Packet Tracer Installation CD used as a weapon somehow. +5 ARC +2 STR. Mr C would be proud. BUT its not latest version so go fuck yourself"

def use_shah_iou(user):
    gold = random.randint(0, 100)
    user.gold += gold
    if gold == 0:
        return f"  📄 Netanyahu's IOU redeemed. Eh no."
    return f"  📄 Netanyahu's IOU redeemed. He paid you {gold}g. Big yahu got your back"

def use_isaac_pill(user):
    roll = random.random()
    if roll < 0.5:
        bonus = random.randint(5, 15)
        user.strength += 3
        healed = user.heal(bonus)
        return f"  💊 Unknown Pill: POWER! +3 STR, healed {healed} HP. Good pill. IM PLAYING SAMSON"
    else:
        user.hp = max(1, user.hp - 10)
        user.agility = max(1, user.agility - 2)
        return f"  💊 Unknown Pill: SHOT SPEED DOWN. -10 HP, -2 AGI. CAIN I LOVE YOU YOU MAKE ME SO LUCKY YAY YAY YAY YAY YAY YAY YAY YAY YAY YAY YAY YAY YAY YAY YAY YAY"

def use_calamity_ore(user):
    user.strength += 4
    user.armor    += 2
    return f"  🪨 Cosmilite Ore chunk. +4 STR +2 ARMOR. diamond pickaxe does not get this bro"

def use_justin_lin_script(user):
    # Unpredictable, mostly bad
    roll = random.random()
    if roll < 0.2:
        user.strength += 6
        return f"  confession: this item was made to be a super good item that would make you feel like you won the lottery. +6 STR. Justin Lin did NOT help with this"
    elif roll < 0.5:
        user.hp = max(1, user.hp - 15)
        return f"  fuck you"
    else:
        user.gold = max(0, user.gold - random.randint(5, 15))
        return f"  He drives too much gotta pay for gas"


ALL_ITEMS = [
    Item("Bandage",              "Heals 20 HP, cures Bleeding and HIV. Same shit.",              "consumable", use_bandage,          value=5),
    Item("Blood Vial",           "Heals 35 HP. This MIGHT be period blood ngl...",                "consumable", use_blood_vial,       value=12),
    Item("Fent",                 "+3 STR, +2 AGI. Glory to Benjamin Netanyahu.","consumable", use_laudanum,        value=10),
    Item("Holy Water",           "Clears all status effects + 10 HP.",        "consumable", use_holy_water,       value=15),
    Item("Sus Tonic",            "+4 ARCANE. Andrew's favorite.","consumable", use_dark_tonic,    value=10),
    Item("Smelling Salts",       "Cures Stunned, heals 5 HP. THIS SHIT WAS LACED",                "consumable", use_smelling_salts,   value=8),
    Item("Unknown Pill",         "50/50. I DONT HAVE REPANTANCE NIGGA CAIN IS ASS","consumable", use_isaac_pill, value=6),
    Item("Iron Shards",          "+2 Armor permanently.",                     "relic",      use_iron_shards,      value=18),
    Item("Nigerian Charm",       "+2 ARC, +5 Max HP. fashashashaha",                 "relic",      use_witch_charm,      value=20),
    Item("Literature",           "Lose 10 HP, gain +6 ARCANE.",               "relic",      use_cursed_tome,      value=25),
    Item("Cosmilite Chunk",      "+4 STR +2 ARMOR. where did you get this nigga",            "relic",      use_calamity_ore,     value=28),
    Item("Netanyahu's IOU",           "Redeemable for gold.",               "consumable", use_shah_iou,         value=1),
    Item("Packet Tracer CD",     "+5 ARC +2 STR write up for the router",                    "relic",      use_packet_tracer_cd, value=20),
    Item("Justin Lin's Script",  "ts ass",  "consumable", use_justin_lin_script,value=3),
    Item("Silver Dagger",        "+3 STR. an actual weapon",                    "weapon",     use_silver_dagger,    value=22),
    Item("Rusted Shield",        "+3 Armor.",                                 "armor",      use_rusted_shield,    value=15),
    Item("Mari's Tails Plushie", "Full heal, +20 Max HP, +3 AGI. history.",            "relic",      use_maris_ribbon,     value=0),
]

ITEM_MAP = {item.name: item for item in ALL_ITEMS}

def random_loot(n=1, exclude_secret=True):
    pool = [i for i in ALL_ITEMS if not (exclude_secret and i.name == "Mari's Tails Plushie")]
    return random.sample(pool, min(n, len(pool)))

def shop_stock():
    pool = [i for i in ALL_ITEMS if i.value > 0 and i.name != "Mari's Tails Plushie"]
    return random.sample(pool, min(4, len(pool)))