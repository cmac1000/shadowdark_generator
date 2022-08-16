# pylint: disable=too-many-lines, too-many-instance-attributes, too-many-branches, too-many-locals, too-many-statements
"""
Generates a series of markdown-formatted character sheets, suitable
for adventuring using the Shadowdark system.
"""

import itertools
import random
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Iterable, List, Set

DieSpecification = str
Item = str
GearList = List[str]
Spell = str
Talent = str
Language = str


class Race(Enum):
    """
    Valid races for Shadowdark characters
    """

    DWARF = "dwarf"
    HUMAN = "human"
    ELF = "elf"
    HALF_ORC = "half orc"
    GOBLIN = "goblin"
    HALFLING = "halfling"


class CharacterClass(Enum):
    """
    Valid classes for Shadowdark characters
    """

    THIEF = "thief"
    FIGHTER = "fighter"
    CLERIC = "cleric"
    WIZARD = "wizard"
    KNIGHT_OF_ST_YDRIS = "knight of St. Ydris"
    WARLOCK = "warlock"
    WITCH = "witch"


@dataclass
class Character:
    """
    A shadowdark character.
    """

    race: Race
    character_class: CharacterClass
    hit_points: int
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int
    spells: Set[Spell]
    talents: List[Talent]
    languages: Set[Language]
    name: str


HIT_DICE_TABLE: Dict[CharacterClass, DieSpecification] = {
    CharacterClass.THIEF: "1d4",
    CharacterClass.FIGHTER: "1d8",
    CharacterClass.CLERIC: "1d6",
    CharacterClass.WIZARD: "1d4",
    CharacterClass.KNIGHT_OF_ST_YDRIS: "1d6",
    CharacterClass.WARLOCK: "1d6",
    CharacterClass.WITCH: "1d4",
}

STAT_BONUS_TABLE: Dict[int, int] = defaultdict(
    lambda: 4,
    {
        1: -4,
        2: -4,
        3: -4,
        4: -3,
        5: -3,
        6: -2,
        7: -2,
        8: -1,
        9: -1,
        10: 0,
        11: 0,
        12: 1,
        13: 1,
        14: 2,
        15: 2,
        16: 3,
        17: 3,
        18: 4,
    },
)

WEAPON_PREFERENCES = {
    CharacterClass.THIEF: ["shortsword", "dagger", "club"],
    CharacterClass.FIGHTER: ["bastard sword", "longsword", "spear", "dagger", "club"],
    CharacterClass.KNIGHT_OF_ST_YDRIS: [
        "bastard sword",
        "longsword",
        "spear",
        "dagger",
        "club",
    ],
    CharacterClass.CLERIC: ["longsword", "mace", "club"],
    CharacterClass.WIZARD: ["staff", "dagger"],
    CharacterClass.WARLOCK: ["longsword", "mace", "dagger", "club"],
    CharacterClass.WITCH: ["dagger", "staff"],
}

PRICE_TABLE = {
    "shortsword": 7,
    "longsword": 9,
    "bastard sword": 10,
    "greataxe": 10,
    "dagger": 1,
    "mace": 5,
    "club": 0.05,
    "staff": 0.5,
    "spear": 0.5,
}

CLERIC_SPELLS = [
    "cure wounds",
    "light",
    "shield of faith",
    "protection from evil",
    "holy weapon",
]
WIZARD_SPELLS = [
    "alarm",
    "burning hands",
    "charm person",
    "detect magic",
    "feather fall",
    "floating disk",
    "hold portal",
    "light",
    "magic missile",
    "protection from evil",
    "sleep",
]
WITCH_SPELLS = [
    "cauldron",
    "charm person",
    "eyebite",
    "fog",
    "hypnotize",
    "oak, ash, thorn",
    "puppet",
    "shadowdance",
    "willowman",
    "witchlight",
]

GODS = {
    "lawful": ["St. Terragnis", "Madeera the Covenant"],
    "neutral": ["Gede", "Ord"],
}
COMMON_LANGUAGES = [
    "dwarvish",
    "elvish",
    "giant",
    "goblin",
    "merran",
    "orchish",
    "reptilian",
    "sylvan",
    "thanian",
]
RARE_LANGUAGES = ["celestial", "primordial", "diabolic", "draconic"]

MAGIC_ITEMS = [
    "bag of holding",
    "bracers of defense",
    "boots of the cat",
    "braks cube of perfection",
    "cloak of elvenkind",
    "jewel of barbalt",
    "gauntlets of might",
    "kytherian cog",
    "immovable rod",
    "ophidian armor",
    "pearl of power",
    "potion of healing",
    "potion of extirpation",
    "potion of invisibility",
    "scarab of protection",
    "sword of the ancients",
    "shortsword of the thief",
    "staff of healing",
    "true name",
]

NAMES = {
    Race.DWARF: [
        "Hilde",
        "Torbin",
        "Marga",
        "Bruno",
        "Karina",
        "Naugrim",
        "Brenna",
        "Darvin",
        "Elga",
        "Alric",
    ],
    Race.ELF: [
        "Eliara",
        "Ryarn",
        "Sariel",
        "Tirolas",
        "Galira",
        "Varos",
        "Daeniel",
        "Axidor",
        "Hiralia",
        "Cyrwin",
    ],
    Race.GOBLIN: [
        "Iggs",
        "Tark",
        "Nix",
        "Lenk",
        "Roke",
    ],
    Race.HALFLING: [
        "Willow",
        "Benny",
        "Annie",
        "Tucker",
        "Marie",
    ],
    Race.HALF_ORC: [
        "Vara",
        "Gralk",
        "Ranna",
        "Korv",
        "Zasha",
    ],
    Race.HUMAN: [
        "Zali",
        "Bram",
        "Clara",
        "Nattias",
        "Rina",
        "Denton",
        "Mirena",
        "Aran",
        "Morgan",
        "Giralt",
        "Tamra",
        "Oscar",
        "Ishana",
        "Rogar",
        "Jasmin",
        "Tarin",
        "Yuri",
        "Malchor",
        "Lienna",
        "Godfrey",
    ],
}


@dataclass
class CharacterSheet:
    """
    A character sheet, consisting of a character and a set of equipment.
    """

    character: Character
    gear: GearList

    def _format_stat(self, stat: int) -> str:
        bonus = STAT_BONUS_TABLE[stat]
        return f'{stat}{"  " if len(str(stat)) == 1 else " "}{"+" if bonus >= 0 else ""}{bonus}'

    def _format_talents(self, talents: List[Talent]):
        talent_list = "\n".join([f"* {talent}" for talent in sorted(talents)])

        return f"""## Talents

{talent_list}"""

    def _format_languages(self, languages: Iterable[str]) -> str:

        language_list = "\n".join([f"* {language}" for language in sorted(languages)])
        return f"""## Languages

{language_list}"""

    def _format_gear(self, gear: GearList) -> str:

        gear_list = "\n".join([f"* {spell}" for spell in sorted(gear)])
        return f"""## Gear

{gear_list}"""

    def _format_spells(self, spells: Set[Spell]) -> str:
        if not spells:
            return ""
        spell_list = "\n".join([f"* {spell}" for spell in sorted(list(spells))])
        return f"""
## Spells

{spell_list}
"""

    def as_markdown(self) -> str:
        """
        Generates a markdown-formatted character sheet.

        :return: Markdown-formatted character sheet
        """
        return f"""
# {self.character.name}, {self.character.race.value} {self.character.character_class.value}

HP: {self.character.hit_points}

```
STR: {self._format_stat(self.character.strength)}
DEX: {self._format_stat(self.character.dexterity)}
CON: {self._format_stat(self.character.constitution)}
INT: {self._format_stat(self.character.intelligence)}
WIS: {self._format_stat(self.character.wisdom)}
CHA: {self._format_stat(self.character.charisma)}
```

{self._format_languages(self.character.languages)}

{self._format_talents(self.character.talents)}
{self._format_spells(self.character.spells)}
{self._format_gear(self.gear)}
        """


def get_racial_languages(race: Race) -> Set[Language]:
    """
    Determines the starting languages for a character of a given race

    :param: race: the race of the character
    :returns: a set of languages as strings
    """
    languages_by_race = {
        Race.HALFLING: set(["common"]),
        Race.HUMAN: set(["common"]),
        Race.HALF_ORC: set(["common", "orchish"]),
        Race.DWARF: set(["common", "dwarvish"]),
        Race.ELF: set(["common", "elvish", "sylvan"]),
        Race.GOBLIN: set(["common", "goblin"]),
    }
    languages = languages_by_race[race]
    if race is Race.HUMAN:
        languages.add(random.choice(COMMON_LANGUAGES))
    return languages


def roll(specification: DieSpecification, advantage=False, disadvantage=False) -> int:
    """
    Rolls some dice and returns the result

    :param: specification: a die specification such as "1d20" or "1d6"
    :param: advantage: whether to roll with advantage (roll twice and take the higher)
    :param: disadvantage: whether to roll with disadvantage (roll twice and take the lower)
    :returns: an integer, the result of making the rolls and summing them
    """
    assert not (
        advantage and disadvantage
    ), "advantage and disadvantage are mutually exclusive"

    count, die_size = specification.split("d")

    if advantage:
        assert count == "1", "only one die can be rolled with advantage"
        return max(roll(specification) for _ in range(2))

    if disadvantage:
        assert count == "1", "only one die can be rolled with disadvantage"
        return min(roll(specification) for _ in range(2))

    return sum((random.randint(1, int(die_size)) for _ in range(int(count))))


def make_talent_rolls(race: Race) -> List[int]:
    """
    Returns the results of a series of 2d6 rolls, suitable
    for use in determining talents.

    :param: race: necessary because humans get extra starting talents
    :returns: a list of integers, representing results of the rolls
    """
    return [roll("2d6") for _ in range((2 if race is Race.HUMAN else 1))]


def generate_character_sheet() -> CharacterSheet:
    """
    Create a character sheet. This follows the rules of Shadowdark's character
    creation process, and attempts to make a fair, viable, character.

    :returns: a CharacterSheet
    """
    # roll stats - if any under 14, re-roll
    while True:
        strength, dexterity, constitution, intelligence, wisdom, charisma = [
            roll("3d6") for _ in range(6)
        ]
        if any(
            (
                x >= 14
                for x in (
                    strength,
                    dexterity,
                    constitution,
                    wisdom,
                    intelligence,
                    charisma,
                )
            )
        ):
            break

    stats = sorted(
        [
            ("strength", strength),
            ("dexterity", dexterity),
            ("constitution", constitution),
            ("intelligence", intelligence),
            ("wisdom", wisdom),
            ("charisma", charisma),
        ],
        key=lambda x: x[1],
        reverse=True,
    )

    # choose class based on best stat
    best = next(
        (
            s
            for s in stats
            if s[0]
            in (
                "dexterity",
                "wisdom",
                "strength",
                "intelligence",
                "charisma",
            )
        )
    )
    if best[1] < 14:
        character_class = CharacterClass.WARLOCK  # good at nothing, hail mary!
    elif best[0] == "dexterity":
        character_class = CharacterClass.THIEF
    elif best[0] == "wisdom":
        character_class = CharacterClass.CLERIC
    elif best[0] == "strength":
        if charisma >= 14:
            character_class = CharacterClass.KNIGHT_OF_ST_YDRIS
        else:
            character_class = CharacterClass.FIGHTER
    elif best[0] == "intelligence":
        character_class = CharacterClass.WIZARD
    elif best[0] == "charisma":
        character_class = CharacterClass.WITCH

    languages = set()
    talents = []
    gear = []
    weight = 0
    spells = set()
    alignment = random.choice(["lawful", "neutral"])
    advantage_spells = set()

    if character_class == CharacterClass.CLERIC:
        race = random.choice(
            [
                Race.HUMAN,
                Race.DWARF,
            ]
        )
        languages = get_racial_languages(race)
        languages.add(
            random.choice(
                [
                    x
                    for x in [
                        "primordial",
                        "diabolic",
                        "celestial",
                    ]
                    if x not in languages
                ]
            )
        )
        gear.append("holy symbol")
        spells.add("turn undead")
        while len(spells) < 3:
            spells.add(random.choice(CLERIC_SPELLS))
        talents.append(f"worshipper of {random.choice(GODS[alignment])}")

        spellcasting_bonus = 0
        melee_bonus = 0
        for talent_roll in make_talent_rolls(race):
            if talent_roll == 2:
                advantage_spells.add(
                    random.choice([x for x in spells if x not in advantage_spells])
                )
            elif 3 <= talent_roll <= 6:
                melee_bonus += 1
            elif 7 <= talent_roll <= 9:
                spellcasting_bonus += 1
            elif 10 <= talent_roll <= 11:
                if wisdom < 18:
                    wisdom += 2
                else:
                    strength += 2
            elif talent_roll == 12:
                spellcasting_bonus += 1
        if spellcasting_bonus:
            talents.append(f"+{spellcasting_bonus} to cleric spellcasting checks")
        if melee_bonus:
            talents.append(f"+{melee_bonus} to melee attacks")
    elif character_class == CharacterClass.FIGHTER:
        race = random.choice(
            [
                Race.HUMAN,
                Race.HALF_ORC,
                Race.DWARF,
            ]
        )
        languages = get_racial_languages(race)
        talents.append("hauler: add con mod, if positive to gear slots")
        talents.append(
            f"weapon mastery: {'greataxe' if race is Race.DWARF else 'bastard sword'}"
        )
        talents.append("Grit: advantage on strength checks to overcome opposing force")

        melee_and_ranged_bonus = 0
        armor_bonus = 0
        for talent_roll in make_talent_rolls(race):
            if talent_roll == 2:
                if "weapon mastery: longbow" not in talents:
                    talents.append("weapon mastery: longbow")
                else:
                    talents.append("weapon mastery: greatsword")
            elif 3 <= talent_roll <= 6:
                melee_and_ranged_bonus += 1
            elif 7 <= talent_roll <= 9:
                if strength < 18:
                    strength += 2
                elif constitution < 18:
                    constitution += 2
                else:
                    dexterity += 2
            elif 10 <= talent_roll <= 11:
                armor_bonus += 1
            elif talent_roll == 12:
                melee_and_ranged_bonus += 1
        if melee_and_ranged_bonus:
            talents.append(f"+{melee_and_ranged_bonus} to melee and ranged attacks")
        if armor_bonus:
            talents.append(f"+{armor_bonus} AC when wearing plate mail")

    elif character_class == CharacterClass.THIEF:
        talents.append(
            "backstab: on attack against unaware target, add 1+half-level damage dice"
        )
        talents.append("thievery: you always have thieves' tools, no gear slots needed")
        talents.append(
            "trained in climbing, sneaking, hiding, finding/disabling traps, delicate "
            "work like picking pockets and locks (advantage on relevant checks)"
        )
        race = random.choice([Race.HUMAN, Race.GOBLIN, Race.HALFLING])
        languages = get_racial_languages(race)
        melee_and_ranged_bonus = 0
        backstab_bonus = 0

        while True:
            talent_rolls = make_talent_rolls(race)
            if len(talent_rolls) == 1:
                break
            if not all((x == 2 for x in talent_rolls)):
                break

        for talent_roll in talent_rolls:
            if talent_roll == 2:
                talents.append("advantage on initiative rolls")
            elif 3 <= talent_roll <= 5:
                backstab_bonus += 1
            elif 6 <= talent_roll <= 9:
                if dexterity < 18:
                    dexterity += 2
                elif charisma < 18:
                    charisma += 2
                else:
                    constitution += 2
            elif 10 <= talent_roll <= 11:
                melee_and_ranged_bonus += 1
            elif talent_roll == 12:
                melee_and_ranged_bonus += 1
        if melee_and_ranged_bonus:
            talents.append(f"+{melee_and_ranged_bonus} to melee and ranged attacks")
        if backstab_bonus:
            talents.append(f"+{backstab_bonus} to backstab damage dice")

    elif character_class == CharacterClass.WIZARD:
        race = random.choice(
            [
                Race.HUMAN,
                Race.ELF,
            ]
        )
        languages = get_racial_languages(race)
        languages = languages.union(
            set(
                random.choice(
                    list(
                        itertools.combinations(
                            [x for x in COMMON_LANGUAGES if x not in languages], 2
                        )
                    )
                )
            )
        )
        languages = languages.union(
            set(
                random.choice(
                    list(
                        itertools.combinations(
                            [x for x in RARE_LANGUAGES if x not in languages], 2
                        )
                    )
                )
            )
        )
        while len(spells) < 3:
            spells.add(random.choice(WIZARD_SPELLS))

        spellcasting_bonus = 0
        for talent_roll in make_talent_rolls(race):
            if talent_roll == 2:
                weight += 1
                gear.append(random.choice(MAGIC_ITEMS))
            elif (3 <= talent_roll <= 6) or talent_roll == 12:
                if intelligence < 18:
                    intelligence += 2
                else:
                    spellcasting_bonus += 1
            elif 7 <= talent_roll <= 9:
                advantage_spells.add(
                    random.choice([x for x in spells if x not in advantage_spells])
                )
            elif 10 <= talent_roll <= 11:
                spells.add(random.choice([x for x in WIZARD_SPELLS if x not in spells]))
        if spellcasting_bonus:
            talents.append(f"+{spellcasting_bonus} to wizard spellcasting checks")
    elif character_class == CharacterClass.KNIGHT_OF_ST_YDRIS:
        race = random.choice(
            [
                Race.HUMAN,
                Race.HALF_ORC,
                Race.DWARF,
            ]
        )
        languages = get_racial_languages(race)
        languages.add("diabolic")
        demonic_possession_bonus = 1
        spellcasting_bonus = 0
        melee_bonus = 0
        for talent_roll in make_talent_rolls(race):
            if talent_roll in [2, 12]:
                demonic_possession_bonus += 1
            elif 3 <= talent_roll <= 6:
                melee_bonus += 1
            elif 7 <= talent_roll <= 9:
                if strength < 18:
                    strength += 2
                elif constitution < 18:
                    constitution += 2
                else:
                    dexterity += 2
            elif 10 <= talent_roll <= 11:
                if charisma < 18:
                    charisma += 2
                else:
                    spellcasting_bonus += 1
        if spellcasting_bonus:
            talents.append(f"+{spellcasting_bonus} to witch spellcasting checks")
        if melee_bonus:
            talents.append(f"+{melee_bonus} to melee attacks")
        talents.append(
            f"demonic possession: 3/day, gain a {demonic_possession_bonus} "
            + "half-level bonus to damage rolls for 3 rounds"
        )
    elif character_class == CharacterClass.WARLOCK:
        race = random.choice(
            [
                Race.HUMAN,
                Race.HALF_ORC,
                Race.DWARF,
                Race.ELF,
                Race.GOBLIN,
                Race.HALFLING,
            ]
        )
        languages = get_racial_languages(race)
        # this is a complicated damn class
        melee_bonus = 0
        armor_bonus = 0
        if not [
            x for x in [strength, dexterity, intelligence, wisdom, charisma] if x >= 10
        ]:
            # true scrubs serve the slime god
            talents.append("warlock of Mugdulblub")
            hd_bonus = 0
            for talent_roll in make_talent_rolls(race):
                if talent_roll == 2:
                    talents.append(
                        "1/day, turn into a crawling puddle of slime for 3 rounds"
                    )
                elif 3 <= talent_roll <= 7:
                    hd_bonus += 2
                elif (8 <= talent_roll <= 9) or talent_roll == 12:
                    if constitution < 18:
                        constitution += 2
                    else:
                        dexterity += 2
                elif 10 <= talent_roll <= 11:
                    talents.append(
                        f"immune to {random.choice(['cold', 'acid', 'poison'])}"
                    )
            if hd_bonus:
                talents.append(f"Maximize {hd_bonus} hit dice rolls (prior or future)")

        elif best[0] == "strength":
            talents.append("warlock of Almazzat")

            # special-case logic - need to reroll if we get initiative advantage twice
            while True:
                talent_rolls = make_talent_rolls(race)
                if len(talent_rolls) == 1:
                    break
                if not all((x in [10, 11] for x in talent_rolls)):
                    break

            adv_bonus = 0
            for talent_roll in talent_rolls:
                if talent_roll == 2:
                    adv_bonus += 1
                elif 3 <= talent_roll <= 7:
                    melee_bonus += 1
                elif (8 <= talent_roll <= 9) or talent_roll == 12:
                    if strength < 18:
                        strength += 2
                    else:
                        melee_bonus += 1
                elif 10 <= talent_roll <= 11:
                    talents.append("advantage on initiative rolls")
            if adv_bonus:
                talents.append(
                    f"{adv_bonus}/day, gain advantage on melee attacks for 3 rounds"
                )
        elif best[0] == "wisdom":
            talents.append("warlock of Kytheros")

            while True:
                talent_rolls = make_talent_rolls(race)
                if len(talent_rolls) == 1:
                    break
                if not all((x in [10, 11] for x in talent_rolls)):
                    break
            roll_bonus = 0
            for talent_roll in talent_rolls:
                if talent_roll == 2:
                    roll_bonus += 1
                elif 3 <= talent_roll <= 7:
                    armor_bonus += 1
                elif (8 <= talent_roll <= 9) or talent_roll == 12:
                    if wisdom < 18:
                        wisdom += 2
                    elif dexterity < 18:
                        dexterity += 2
                    else:
                        strength += 2
                elif 10 <= talent_roll <= 11:
                    talents.append("3/day, add WIS bonus to any roll")
            if roll_bonus:
                talents.append(f"{roll_bonus}/day, force GM to reroll")
        elif best[0] == "intelligence":
            talents.append("warlock of Shune the Vile")
            xp_bonus = 0
            mind_bonus = 0
            for talent_roll in make_talent_rolls(race):
                if talent_roll == 2:
                    mind_bonus += 1
                elif (3 <= talent_roll <= 7) or talent_roll == 12:
                    spells.add(
                        random.choice([x for x in WIZARD_SPELLS if x not in spells])
                    )
                elif 8 <= talent_roll <= 9:
                    if intelligence < 18:
                        intelligence += 2
                    else:
                        dexterity += 2
                elif 10 <= talent_roll <= 11:
                    xp_bonus += 1
            if xp_bonus:
                talents.append(f"+{xp_bonus} xp on learning a valuable secret")
            if mind_bonus:
                talents.append(
                    f"{mind_bonus}/day, read the mind of a creature you touch for 3 rounds"
                )
        elif best[0] == "dexterity":
            talents.append("warlock of Titania")
            while True:
                talent_rolls = make_talent_rolls(race)
                if len(talent_rolls) == 1:
                    break
                if not all((x in [10, 11] for x in talent_rolls)):
                    break
            range_bonus = 0
            for talent_roll in talent_rolls:
                if talent_roll == 2:
                    talents.append(
                        "1/day, hypnotize a 5 HD or less creature for 3 rounds"
                    )
                elif 3 <= talent_roll <= 7:
                    if "can use a longbow" in talents:
                        range_bonus += 1
                    else:
                        talents.append("can use a longbow")
                elif (8 <= talent_roll <= 9) or talent_roll == 12:
                    if dexterity < 18:
                        dexterity += 2
                    else:
                        charisma += 2
                elif 10 <= talent_roll <= 11:
                    talents.append("hostile spells that target you are hard to cast")
            if range_bonus:
                talents.append(f"+{range_bonus} to ranged attack rolls")
        elif best[0] == "charisma":
            # charisma is not actually valuable here,
            # but with a little self-esteem you avoid the slime god
            talents.append("warlock of The Willowman")
            morale_bonus = 0
            teleport_bonus = 0
            for talent_roll in make_talent_rolls(race):
                if talent_roll == 2:
                    teleport_bonus += 1
                elif 3 <= talent_roll <= 7:
                    melee_bonus += 1
                elif (8 <= talent_roll <= 9) or talent_roll == 12:
                    if strength < 18:
                        strength += 2
                    else:
                        dexterity += 2
                elif 10 <= talent_roll <= 11:
                    morale_bonus += 1
            if teleport_bonus:
                talents.append(
                    f"{teleport_bonus}/day, teleport to a far location you see as your move"
                )
            if morale_bonus:
                talents.append(
                    f"{morale_bonus}/day, force a close being to check morale, even if immune"
                )
        else:
            raise Exception("should not get here")

        if melee_bonus:
            talents.append(f"+{melee_bonus} to melee attacks")
        if armor_bonus:
            talents.append(f"+{armor_bonus} to AC")
    elif character_class == CharacterClass.WITCH:
        race = random.choice(
            [
                Race.HUMAN,
                Race.ELF,
                Race.GOBLIN,
                Race.HALFLING,
            ]
        )
        languages = get_racial_languages(race) | {"diabolic", "primoridal", "sylvan"}
        talents.append(
            "familiar: you have a little buddy, it speaks common and you can cast spells through it"
        )

        while len(spells) < 3:
            spells.add(random.choice(WITCH_SPELLS))

        spellcasting_bonus = 0
        teleport_bonus = 0
        for talent_roll in make_talent_rolls(race):
            if talent_roll == 2:
                teleport_bonus += 1
            elif (3 <= talent_roll <= 7) or talent_roll == 12:
                if charisma < 18:
                    charisma += 2
                else:
                    spellcasting_bonus += 1
            elif 8 <= talent_roll <= 9:
                advantage_spells.add(
                    random.choice([x for x in spells if x not in advantage_spells])
                )
            elif 10 <= talent_roll <= 11:
                spells.add(random.choice([x for x in WITCH_SPELLS if x not in spells]))
        if spellcasting_bonus:
            talents.append(f"+{spellcasting_bonus} to witch spellcasting checks")
        if teleport_bonus:
            talents.append(f"{teleport_bonus}/day teleport to familiar's location")

    for spell in advantage_spells:
        talents.append(f"advantage on casting {spell}")

    # racial bonuses
    if race is Race.ELF:
        if character_class in [CharacterClass.WIZARD, CharacterClass.CLERIC]:
            talents.append("farsight: +1 to spellcasting")
        else:
            talents.append("farsight: +1 to ranged attacks")
    elif race is Race.GOBLIN:
        talents.append("keen senses: can't be surprised")
    elif race is Race.HALFLING:
        talents.append("stealthy: 1/day can become invisible for three rounds")
    elif race is Race.HALF_ORC:
        talents.append("mighty: +1 to melee attack and damage")

    assert len(set(talents)) == len(talents), "duplicate talents"

    gold = float(roll("2d6") * 5)
    gear_slots = max([10, strength]) + (
        STAT_BONUS_TABLE[constitution]
        if character_class is CharacterClass.FIGHTER
        else 0
    )

    # everyone gets a crawling kit if they can afford it
    if gold >= 7:
        gear += [
            "backpack",
            "flint and steel",
            "2x torches",
            "3x rations",
            "10x iron spikes",
            "grappling hook",
            "rope, 60 feet",
        ]
        weight += 7

    # good to have a weapon
    affordable_weapons = [
        x for x in WEAPON_PREFERENCES[character_class] if PRICE_TABLE[x] <= gold
    ]
    assert affordable_weapons, "no affordable weapons"
    if affordable_weapons and weight < gear_slots:
        best_weapon = affordable_weapons[0]
        if best_weapon == "bastard sword" and race is Race.DWARF:
            best_weapon = "greataxe"
        gear += [best_weapon]
        weight += 1
        gold -= PRICE_TABLE[best_weapon]

    # get a shield if plausible
    if (
        character_class
        in (
            CharacterClass.FIGHTER,
            CharacterClass.CLERIC,
            CharacterClass.KNIGHT_OF_ST_YDRIS,
            CharacterClass.WARLOCK,
        )
        and gold >= 10
        and weight < gear_slots
    ):
        gear += ["shield"]
        weight += 1
        gold -= 10

    # get leather armor if plausible
    if (
        character_class
        in (
            CharacterClass.FIGHTER,
            CharacterClass.CLERIC,
            CharacterClass.THIEF,
            CharacterClass.KNIGHT_OF_ST_YDRIS,
            CharacterClass.WARLOCK,
            CharacterClass.WITCH,
        )
        and gold >= 10
        and weight < gear_slots
    ):
        gear += ["leather armor"]
        weight += 1
        gold -= 10

    gear += [f"{gold} gold pieces"]

    talents.append(
        random.choice(
            [
                "urchin: grew up in a bad part of a city",
                "wanted: bounty on you, you have friends",
                "cult initiate: knows grim secrets and rituals",
                "thieves' guild: connections, contacts, debts",
                "banished: cast out for supposed crimes",
                "orphaned: raise by unusual guardian",
                "wizard's apprentice: eye for magic",
                "jeweler: expert in jewelry",
                "herbalist: expert in plants, medicines, poisons",
                "barbarian: once in the horde",
                "mercenary: hired to fight for coin",
                "sailor: good with ships",
                "acolyte: trained in rites and doctrines",
                "soldier: trained in organized army",
                "ranger: good in wilderness",
                "scout: good at stealth, observation, speed",
                "minstrel: traveler, good at song, dance, and comedy",
                "scholar: know ancient history and lore",
                "noble: famous name, noble birth",
                "chirurgeon: know anatomy surgery, and first aid",
            ]
        )
    )

    character = Character(
        race=race,
        character_class=character_class,
        hit_points=roll(HIT_DICE_TABLE[character_class], advantage=(race is Race.DWARF))
        + max(STAT_BONUS_TABLE[constitution], 1),
        strength=strength,
        dexterity=dexterity,
        constitution=constitution,
        wisdom=wisdom,
        intelligence=intelligence,
        charisma=charisma,
        spells=spells,
        talents=talents,
        languages=languages,
        name=random.choice(NAMES[race]),
    )

    return CharacterSheet(character=character, gear=gear)


def generate_party(size=4, unique_classes=True) -> List[CharacterSheet]:
    """
    Create a list of party members

    :param size: number of members of party
    :param unique: False if the party may have multiple members of the same class
    :returns: a list of CharacterSheets
    """
    members: List[CharacterSheet] = []
    while len(members) < size:
        candidate = generate_character_sheet()
        if not unique_classes or candidate.character.character_class not in [
            x.character.character_class for x in members
        ]:
            members.append(candidate)

    return members


print("\n---\n".join(x.as_markdown() for x in generate_party(size=3, unique_classes=False)))
