import random

class Enemy:
    def __init__(self, name, hp, strength, armor, xp_reward, gold_reward,
                 description, special_fn=None):
        self.name         = name
        self.hp           = hp
        self.max_hp       = hp
        self.strength     = strength
        self.armor        = armor
        self.xp_reward    = xp_reward
        self.gold_reward  = gold_reward
        self.description  = description
        self.special_fn   = special_fn
        self.status_effects = []

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        reduced = max(0, amount - self.armor)
        self.hp = max(0, self.hp - reduced)
        return reduced

    def attack(self):
        return self.strength + random.randint(1, 8)

    def use_special(self, player):
        if self.special_fn and random.random() < 0.30:
            return self.special_fn(self, player)
        return None

    def hp_bar(self):
        ratio = self.hp / self.max_hp
        filled = int(ratio * 16)
        return "█" * filled + "░" * (16 - filled)


def special_bleed(enemy, player):
    if "Bleeding" not in player.status_effects:
        player.status_effects.append("Bleeding")
        return f"  🩸 {enemy.name} gives you HIV — you are FRIED (bleeding)"
    return None

def special_curse(enemy, player):
    if "Cursed" not in player.status_effects:
        player.status_effects.append("Cursed")
        player.strength = max(1, player.strength - 2)
        return f"  💀 {enemy.name} uses Nigerian voodoo — you are Cursed! (-2 STR)"
    return None

def special_drain(enemy, player):
    drain = random.randint(5, 12)
    player.hp = max(0, player.hp - drain)
    enemy.hp  = min(enemy.max_hp, enemy.hp + drain)
    return f"  🌑 {enemy.name} drains your life force! You lose {drain} somethinh......"

def special_rot(enemy, player):
    if "Rotting" not in player.status_effects:
        player.status_effects.append("Rotting")
        return f"  🪦 {enemy.name}'s touch rots your flesh — Rotting! (like Ty's grades)"
    return None

def special_stun(enemy, player):
    if "Stunned" not in player.status_effects:
        player.status_effects.append("Stunned")
        return f"  💫 {enemy.name} bashes your skull — you got CTE! (Stunned)"
    return None

def special_plague(enemy, player):
    if "Plague" not in player.status_effects:
        player.status_effects.append("Plague")
        return f"  🧪 {enemy.name} coughs on you — Plagued! wear a mask bro."
    return None

def special_enrage(enemy, player):
    enemy.strength += 3
    return f"  😡 {enemy.name} JUST HIT THE JACKPOT!! (+3 STR) HEY HEY HEY HEY HEY"

def special_shah(enemy, player):
    gold_stolen = random.randint(3, 10)
    player.gold = max(0, player.gold - gold_stolen)
    msgs = [
        f"  💸 {enemy.name} asks to borrow {gold_stolen}g. You'll never see it again.",
        f"  📱 {enemy.name} sends a deltarune reference — {gold_stolen}g is spent. Donating to the mentally impaired is good man.",
        f"  🤲 {enemy.name} SHUT UP ABOUT DELTARUNE (-{gold_stolen}g)",
        f"  👟 {enemy.name} dih -{gold_stolen}g.",
        f"  🍔 {enemy.name} idk bruh this the shah event pool. its ALL gold stolen. (-{gold_stolen}g)",
    ]
    return random.choice(msgs)

def special_justin_lin(enemy, player):
    moves = [
        (lambda: setattr(player, 'armor', max(0, player.armor - 2)),
         "  Justin Lin makes a random noise."),
        (lambda: setattr(player, 'hp', max(1, player.hp - 15)),
         "  J Lin fucking falls in front of Mr C."),
        (lambda: player.status_effects.append("Stunned"),
         "  SHUT THE FUCK UP JUSTIN"),
        (lambda: None,
         "  JUSTIN KY- oh its JT. Hi JT!"),
        (lambda: setattr(player, 'agility', max(1, player.agility - 3)),
         "  Js goon bro."),
    ]
    effect_fn, msg = random.choice(moves)
    effect_fn()
    return msg

def special_calamity(enemy, player):
    moves = [
        (lambda: setattr(player, 'hp', max(1, player.hp - 25)),
         "  ☀️  Providence bullet hell. NIGGA YOU SUCK AT DODGING KILL YOURSELF"),
        (lambda: (setattr(player, 'strength', max(1, player.strength - 3)),
                  setattr(player, 'agility',  max(1, player.agility  - 3))),
         "  random named move I fuckinh forgot nigga."),
        (lambda: setattr(player, 'hp', max(1, player.hp - 30)),
         "  🌌 Devourer of Gods laser. -30 HP. why is this in the fucking game?"),
        (lambda: player.status_effects.append("Cursed"),
         "  👁  Im cracking calamitas"),
        (lambda: setattr(player, 'hp', max(1, player.hp - 20)),
         "  🌊 Aquatic Scourge jumps out of nowhere. -20 HP. Wrong biome bro. YOU AINT EVEN IN THE GAME"),
    ]
    effect_fn, msg = random.choice(moves)
    effect_fn()
    return msg

def special_isaac(enemy, player):
    moves = [
        (lambda: setattr(player, 'hp', max(1, player.hp - 20)),
         "  👟 MOM'S FOOT. -20 HP. You know what you did."),
        (lambda: (player.status_effects.append("Stunned"),
                  setattr(player, 'arcane', max(1, player.arcane - 3))),
         "  🌀 Delirium phase shifts. Stunned and confused. -3 ARC. (it's always Delirium)"),
        (lambda: setattr(player, 'hp', max(1, player.hp - 18)),
         "  💙 HUSH fires a laser. -18 HP. This is floor 1. How did Hush get here."),
        (lambda: setattr(player, 'armor', max(0, player.armor - 4)),
         "  idk bruh i js added this move to make the fight more interesting. -4 ARMOR."),
        (lambda: None,
         "  🔑 Satan door rattles. Nothing happens. You need both keys still. Get a real job."),
        (lambda: setattr(player, 'gold', max(0, player.gold - random.randint(5,12))),
         "  🪙 Greed Mode activated. Coins stolen. Everyone hates JEW Mode. JEW JEW JEW JEW JEW"),
        (lambda: player.status_effects.append("Bleeding"),
         "  ✂️  Scissors. ???. You are Bleeding now. 'why the fuck is this in the game sinai?'"),
    ]
    effect_fn, msg = random.choice(moves)
    effect_fn()
    return msg


ENEMY_TIERS = {
    1: [
        lambda: Enemy("Shambling Corpse", hp=30, strength=7, armor=0,
                      xp_reward=25, gold_reward=random.randint(1,4),
                      description="A lurching undead, reeking of first period PE. Probably Shah. Or perhaps Peter.",
                      special_fn=special_rot),
        lambda: Enemy("Plague Rat", hp=20, strength=5, armor=0,
                      xp_reward=15, gold_reward=random.randint(0,2),
                      description="A bloated rat the size of a guppy. Does not have 9 lives. Has maybe 1.5.",
                      special_fn=special_plague),
        lambda: Enemy("Hollow Wraith", hp=25, strength=8, armor=1,
                      xp_reward=20, gold_reward=random.randint(1,3),
                      description="A translucent specter. Less scary than it looks. Red chests are scarier gang.",
                      special_fn=special_drain),
        lambda: Enemy("Feral Cultist", hp=35, strength=9, armor=1,
                      xp_reward=30, gold_reward=random.randint(2,6),
                      description="Satanist. I FUCKING HATE THIS NIG-",
                      special_fn=special_bleed),
        lambda: Enemy("Shah's Cousin", hp=28, strength=6, armor=0,
                      xp_reward=20, gold_reward=0,
                      description="Asks to borrow gold every round. praises Benjamin Netanyahu",
                      special_fn=special_shah),
    ],
    2: [
        lambda: Enemy("Blood Hound", hp=50, strength=12, armor=1,
                      xp_reward=45, gold_reward=random.randint(3,7),
                      description="FETCH ME THEIR SOULS (cutely). That one dog in Undertale MIGHT be stronger than this fraud.",
                      special_fn=special_bleed),
        lambda: Enemy("Grave Witch", hp=45, strength=10, armor=2,
                      xp_reward=50, gold_reward=random.randint(4,8),
                      description="Must be Haitian. Probably sells Nigerian charms on the side.",
                      special_fn=special_curse),
        lambda: Enemy("Rotting Titan", hp=65, strength=14, armor=3,
                      xp_reward=60, gold_reward=random.randint(5,10),
                      description="An enormous undead hulk. Not goonable. Peter would crack though.",
                      special_fn=special_stun),
        lambda: Enemy("Shadow Stalker", hp=40, strength=13, armor=2,
                      xp_reward=55, gold_reward=random.randint(3,8),
                      description="Helps women get home safely at night.",
                      special_fn=special_drain),
        lambda: Enemy("Andrew (Shah's boyfriend)", hp=42, strength=8, armor=0,
                      xp_reward=40, gold_reward=0,
                      description="HE GOT A 59 ON THE 5-6 TEST",
                      special_fn=special_shah),
    ],
    3: [
        lambda: Enemy("Bone Colossus", hp=90, strength=18, armor=5,
                      xp_reward=100, gold_reward=random.randint(8,15),
                      description="A cathedral of fused skeleton. Not as white as Preston",
                      special_fn=special_enrage),
        lambda: Enemy("The Plague Bishop", hp=80, strength=15, armor=4,
                      xp_reward=110, gold_reward=random.randint(10,18),
                      description="He is NOT my bishop. 'This asrial cosplay is shit' THIS NIGGAS LOOTPOOL IS SO ASS I WANTT TO KMS",
                      special_fn=special_plague),
        lambda: Enemy("Voidborn Revenant", hp=85, strength=17, armor=4,
                      xp_reward=115, gold_reward=random.randint(8,16),
                      description="A normal guy with dihpression. Yall thought this was gonna be a cool monster but no fuck you.",
                      special_fn=special_drain),
        lambda: Enemy("Nissan Lin", hp=70, strength=15, armor=3,
                      xp_reward=90, gold_reward=random.randint(6,12),
                      description="Nissan Ultima.",
                      special_fn=special_justin_lin),
    ],
}

BOSSES = [
    lambda: Enemy("The Pale Sovereign", hp=150, strength=22, armor=6,
                  xp_reward=300, gold_reward=50,
                  description="An ancient vampire lord. Not as cool as DIO. Still pretty cool. Would not date his son.",
                  special_fn=special_drain),
    lambda: Enemy("The Wretched God", hp=180, strength=25, armor=5,
                  xp_reward=350, gold_reward=60,
                  description="Mom if she skipped leg day. Providence knockoff. js put the fries in the bag vro",
                  special_fn=special_calamity),
    lambda: Enemy("Magistra of Plagues", hp=140, strength=19, armor=7,
                  xp_reward=320, gold_reward=55,
                  description="The nigga who ate that stupid ass lunch concoction you made in 4th grade. How is he alive?",
                  special_fn=special_plague),
    lambda: Enemy("Peter", hp=1, strength=50, armor=0,
                  xp_reward=67, gold_reward=random.randint(100,150),
                  description="It's a Black man. His name is Peter. He's a bum. Ty's boyfriend",
                  special_fn=special_plague),
    lambda: Enemy("Delirium (Budget Version)", hp=160, strength=20, armor=4,
                  xp_reward=330, gold_reward=55,
                  description="ngl gang I just really want to play this game with the dlcs",
                  special_fn=special_isaac),
    lambda: Enemy("Shah", hp=100, strength=18, armor=3,
                  xp_reward=280, gold_reward=random.randint(40,80),
                  description="cornball",
                  special_fn=special_shah),
    lambda: Enemy("Zoro", hp=170, strength=23, armor=5,
                  xp_reward=340, gold_reward=random.randint(45,65),
                  description="Why is he even here bro. He has nothing to do with this. He just showed up one day.",
                  special_fn=special_calamity),
]


def special_packet_tracer(enemy, player):
    moves = [
        ("opens Packet Tracer", lambda: None,
         "  🖥  Mr C opens Packet Tracer. you lose your will to live. (like starting Calamity Master Death Mode)"),
        ("assigns 12 labs mid-fight", lambda: setattr(player, 'strength', max(1, player.strength - 3)),
         "  📋 12 labs assigned mid-combat. Extension for the 3rd time in a row... (-3 STR)"),
        ("starts yapping", lambda: player.status_effects.append("Stunned"),
         "  🪑 Mr C yaps for 20 minutes about OSPF. (let me watch smash or pass nga) (Stunned)"),
        ("assigns REDUX again", lambda: setattr(player, 'arcane', max(1, player.arcane - 4)),
         "  🧮 REDUX labs. what the fuck are we doing. Your brain melts. (-4 ARC)"),
        ("pulls up a 90-acronym list", lambda: setattr(player, 'agility', max(1, player.agility - 3)),
         "  📊 90 acronyms. Your Getting a 62. (-3 AGI)"),
        ("says 'bad teacher!'", lambda: setattr(player, 'armor', max(0, player.armor - 2)),
         "  🗣  Mr C says 'bad teacher!' The secondhand embarrassment is physical. (-2 ARMOR)"),
        ("says 'who can tell me about...'", lambda: None,
         "  🎤 'Who can tell me about...' shitty charades wont save you this time."),
        ("docks you 70 points", lambda: setattr(player, 'hp', max(1, player.hp - 20)),
         "  📉 Missed ipv6 unicast-routing. Why 70 points? I put Justin Lin's soul on getting a 100'. (-20 HP direct)"),
        ("shows a 2009 lab walkthrough video", lambda: player.status_effects.append("Stunned"),
         "  📺 A 2009 lab walkthrough video plays. You are Stunned by how shit the quality is"),
        ("says it'll be on the test", lambda: setattr(player, 'arcane', max(1, player.arcane - 2)),
         "  📝 'This WILL be on the test.' It was not. (-2 ARC)"),
        ("loses your submission", lambda: setattr(player, 'gold', max(0, player.gold - 8)),
         "  📁 Mr C cannot find your submission. You lose 8g re-submitting on paper."),
    ]
    name, effect_fn, msg = random.choice(moves)
    effect_fn()
    return f"  👨‍🏫 Mr C {name}.\n{msg}"


def get_mr_c():
    return Enemy(
        name        = "Mr C",
        hp          = 999,
        strength    = 50,
        armor       = 20,
        xp_reward   = 10000,
        gold_reward = random.randint(100, 150),
        description = "The big Mr C. He MIGHT digress. He assigns 12 labs. He doesnt like Justin Lin. Yharon respects him.",
        special_fn  = special_packet_tracer,
    )


def get_enemy(floor):
    tier = min(3, max(1, (floor // 3) + 1))
    return random.choice(ENEMY_TIERS[tier])()

def get_boss(floor):
    return random.choice(BOSSES)()