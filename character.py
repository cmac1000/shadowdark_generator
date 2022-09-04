# pylint: disable=too-many-lines, too-many-instance-attributes, too-many-branches, too-many-locals, too-many-statements, too-few-public-methods
"""
Generates a series of markdown-formatted character sheets, suitable
for adventuring using the Shadowdark system.
"""
from __future__ import annotations

import copy
import itertools
import random
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Iterable, List, Optional, Set, Tuple, Type, TypedDict

DieSpecification = str
Item = str
GearList = List[str]
Spell = str
Talent = str
Language = str


class StatArray(TypedDict):
    """
    A dictionary of stats for a character
    """

    dexterity: int
    strength: int
    intelligence: int
    wisdom: int
    charisma: int
    constitution: int


class Bonus(Enum):
    """
    A bonus that can be applied to a character as an integer
    """

    ALMAZZAT_MELEE = "almazzat_melee"
    ARMOR = "armor"
    BACKSTAB = "backstab"
    DEMONIC_POSSESSION = "demonic_possession"
    KYTHEROS_REROLL = "kytheros_reroll"
    MELEE_ATTACK = "melee_attack"
    MUGDULBLUB_HD = "mugdulblub_hd"
    MUGDULBLUB_SLIME = "mugdulblub_slime"
    PLATE_ARMOR = "plate_armor"
    RANGED_ATTACK = "ranged_attack"
    SHUNE_MIND = "shune_mind"
    SHUNE_XP = "shune_xp"
    SPELL_CASTING = "spell_casting"
    TITANIA_HYPNOTIZE = "titania_hypnotize"
    WILLOWMAN_MORALE = "willowman_morale"
    WILLOWMAN_TELEPORT = "willowman_teleport"
    WITCH_TELEPORT = "witch_teleport"


class Feature:
    """
    An attribute that modifies the mechanics of a character
    """


@dataclass
class BonusFeature(Feature):
    """
    A feature that can be acquired multiple times, additively
    """

    bonus: Bonus
    value: int


@dataclass
class ImmunityFeature(Feature):
    """
    Grants immunity from a particular type of damage
    """

    damage_immunity: str


@dataclass
class GearFeature(Feature):
    """
    Grants a piece of equipment
    """

    gear: str
    weight: int


@dataclass
class LanguageFeature(Feature):
    """
    Grants knowledge of a language
    """

    language: Language


@dataclass
class SpellMasteryFeature(Feature):
    """
    Grants mastery of a spell; this gives the character
    advantage on casting that spell.
    """

    spell: Spell


@dataclass
class SpellFeature(Feature):
    """
    Grants knowlege of a spell, and the ability to cast it
    """

    spell: Spell


@dataclass
class MiscellaneousFeature(Feature):
    """
    An unusual feature which is hard to categorize
    """

    name: str


@dataclass
class WeaponMasteryFeature(Feature):
    """
    Grants mastery for a particular type of weapon - this gives
    bonuses to damage for hits made using that weapon type
    """

    weapon: str


@dataclass
class WeaponProficiencyFeature(Feature):
    """
    Grants the ability to use a particular type of weapon
    """

    weapon: str


@dataclass
class StatFeature(Feature):
    """
    Increases a particular character statistic
    """

    stat: str
    value: int


class FeatureContext:
    """
    A container for features accumulated during character generation
    """

    bonuses: Dict[Bonus, int]
    damage_immunities: Set[str]
    gear_weight: int
    gear: GearList
    languages: Set[Language]
    spell_masteries: Set[Spell]
    spells: Set[Spell]
    stats: StatArray
    talents: List[Talent]
    weapon_masteries: Set[str]
    weapon_proficiencies: Set[str]

    def __init__(self, stats: StatArray):
        self.bonuses = defaultdict(int)
        self.damage_immunities = set()
        self.gear = []
        self.gear_weight = 0
        self.languages = set()
        self.spell_masteries = set()
        self.spells = set()
        self.talents = []
        self.weapon_masteries = set()
        self.weapon_proficiencies = set()
        self.stats = copy.deepcopy(stats)

    def apply_feature(self, feature: Feature) -> None:
        """
        Alters the character according to the rules for a particular
        feature
        """

        if isinstance(feature, BonusFeature):
            self.bonuses[feature.bonus] += feature.value
        elif isinstance(feature, ImmunityFeature):
            self.damage_immunities.add(feature.damage_immunity)
        elif isinstance(feature, GearFeature):
            self.gear.append(feature.gear)
            self.gear_weight += feature.weight
        elif isinstance(feature, LanguageFeature):
            self.languages.add(feature.language)
        elif isinstance(feature, SpellMasteryFeature):
            self.spell_masteries.add(feature.spell)
        elif isinstance(feature, SpellFeature):
            self.spells.add(feature.spell)
        elif isinstance(feature, MiscellaneousFeature):
            self.talents.append(feature.name)
        elif isinstance(feature, WeaponMasteryFeature):
            self.weapon_masteries.add(feature.weapon)
        elif isinstance(feature, WeaponProficiencyFeature):
            self.weapon_proficiencies.add(feature.weapon)
        elif isinstance(feature, StatFeature):
            self.stats[feature.stat] += feature.value  # type: ignore


class Race:
    """
    The ancestry or heritage of a character
    """

    @staticmethod
    def get_default_features(character_class: Type[CharacterClass]) -> List[Feature]:
        """
        Returns the list of features shared by all members of this race.
        """
        raise NotImplementedError()


class Human(Race):
    """
    A standard humans, adaptable and common
    """

    name = "Human"
    names = [
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
    ]

    @staticmethod
    def get_default_features(character_class: Type[CharacterClass]) -> List[Feature]:
        return [
            LanguageFeature(language="common"),
            LanguageFeature(language=random.choice(COMMON_LANGUAGES)),
        ]


class Dwarf(Race):
    """
    A stocky, hardy soul
    """

    name = "Dwarf"
    names = [
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
    ]

    @staticmethod
    def get_default_features(character_class: Type[CharacterClass]) -> List[Feature]:
        return [
            LanguageFeature(language="common"),
            LanguageFeature(language="dwarvish"),
            MiscellaneousFeature(name="stout: roll hit dice gains with advantage"),
        ]


class Elf(Race):
    """
    Rare, long-lived, and tall
    """

    name = "Elf"
    names = [
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
    ]

    @staticmethod
    def get_default_features(character_class: Type[CharacterClass]) -> List[Feature]:
        features: List[Feature] = [LanguageFeature("common"), LanguageFeature("elvish")]
        if character_class in [
            Wizard,
            Cleric,
            Witch,
        ]:
            features.append(BonusFeature(Bonus.SPELL_CASTING, 1))
        else:
            features.append(BonusFeature(Bonus.RANGED_ATTACK, 1))

        return features


class HalfOrc(Race):
    """
    A powerful specimen
    """

    name = "Half-Orc"
    names = [
        "Vara",
        "Gralk",
        "Ranna",
        "Korv",
        "Zasha",
    ]

    @staticmethod
    def get_default_features(character_class: Type[CharacterClass]) -> List[Feature]:
        return [
            BonusFeature(Bonus.MELEE_ATTACK, 1),
            LanguageFeature("common"),
            LanguageFeature("orcish"),
        ]


class Goblin(Race):
    """
    Quick, small, and keen
    """

    name = "Goblin"
    names = [
        "Iggs",
        "Tark",
        "Nix",
        "Lenk",
        "Roke",
    ]

    @staticmethod
    def get_default_features(character_class: Type[CharacterClass]) -> List[Feature]:
        return [
            MiscellaneousFeature("keen senses: can't be surprised"),
            LanguageFeature("common"),
            LanguageFeature("goblin"),
        ]


class Halfling(Race):
    """
    Quick, small, and sneaky
    """

    name = "Halfling"
    names = [
        "Willow",
        "Benny",
        "Annie",
        "Tucker",
        "Marie",
    ]

    @staticmethod
    def get_default_features(character_class: Type[CharacterClass]) -> List[Feature]:
        return [
            MiscellaneousFeature(
                "stealthy: 1/day can become invisible for three rounds"
            ),
            LanguageFeature("common"),
        ]


class CharacterClass:
    """
    A character's specialization
    """

    hit_dice: str
    name: str

    @staticmethod
    def choose_race() -> Type[Race]:
        """
        Chooses a race well-suited to this class
        """
        raise NotImplementedError

    @staticmethod
    def get_default_features(race: Type[Race], alignment: str) -> List[Feature]:
        """
        Returns the list of features shared by all class members
        """
        raise NotImplementedError

    @staticmethod
    def requires_reroll(_) -> bool:
        """
        Returns whether or not a character class requires a reroll
        :param: talent_rolls: rolls for talent
        :returns: whether or not the character class requires a reroll
        """
        return False

    @staticmethod
    def get_features_for_roll(
        talent_roll: int, ctx: FeatureContext, race: Race
    ) -> List[Feature]:
        """
        Returns a feature for a character class

        :param: talent_roll: the roll of the talent
        :param: ctx: the context of the character
        :returns: a feature
        """
        raise NotImplementedError


class Cleric(CharacterClass):
    """
    A stalwart channeler of divine magic
    """

    name = "Cleric"
    hit_dice = "1d6"
    weapon_preferences = ["longsword", "mace", "club"]

    @staticmethod
    def choose_race() -> Type[Race]:
        return random.choice([Human, Dwarf])

    @staticmethod
    def get_default_features(race: Type[Race], alignment: str) -> List[Feature]:
        spells: Set[Spell] = set()
        while len(spells) < 3:
            spells.add(random.choice(CLERIC_SPELLS))
        return [
            LanguageFeature(
                language=random.choice(["primordial", "diabolic", "celestial"])
            ),
            GearFeature(gear="holy symbol", weight=0),
            SpellFeature(spell="turn undead"),
            MiscellaneousFeature(
                name=f"worshipper of {random.choice(GODS[alignment])}"
            ),
        ] + [SpellFeature(spell=spell) for spell in spells]

    @staticmethod
    def get_features_for_roll(
        talent_roll: int, ctx: FeatureContext, race: Race
    ) -> List[Feature]:
        """
        Returns a feature for a character class

        :param: talent_roll: the roll of the talent
        :param: ctx: the context of the character
        :returns: a feature
        """
        if talent_roll == 2:
            return [
                SpellMasteryFeature(
                    spell=random.choice(
                        [x for x in ctx.spells if x not in ctx.spell_masteries]
                    )
                )
            ]
        if 3 <= talent_roll <= 6:
            return [BonusFeature(bonus=Bonus.MELEE_ATTACK, value=1)]
        if (7 <= talent_roll <= 9) or talent_roll == 12:
            return [BonusFeature(bonus=Bonus.SPELL_CASTING, value=1)]
        if ctx.stats["wisdom"] < 18:
            return [StatFeature(stat="wisdom", value=2)]
        return [StatFeature(stat="strength", value=2)]


class Fighter(CharacterClass):
    """
    A valiant warrior
    """
    name = "Fighter"
    hit_dice = "1d8"
    weapon_preferences = ["bastard sword", "longsword", "spear", "dagger", "club"]

    @staticmethod
    def choose_race() -> Type[Race]:
        return random.choice(
            [
                Human,
                HalfOrc,
                Dwarf,
            ]
        )

    @staticmethod
    def get_default_features(race: Type[Race], alignment: str) -> List[Feature]:
        return [
            MiscellaneousFeature(name="hauler: add con mod, if positive to gear slots"),
            MiscellaneousFeature(
                name="grit: advantage on strength checks to overcome opposing force"
            ),
            WeaponMasteryFeature(
                weapon="greataxe" if race is Dwarf else "bastard sword"
            ),
        ]

    @staticmethod
    def get_features_for_roll(
        talent_roll: int, ctx: FeatureContext, race: Race
    ) -> List[Feature]:
        """
        Returns a feature for a character class

        :param: talent_roll: the roll of the talent
        :param: ctx: the context of the character
        :returns: a feature
        """
        if talent_roll == 2:
            if "longbow" not in ctx.weapon_masteries:
                return [WeaponMasteryFeature(weapon="longbow")]
            else:
                return [WeaponMasteryFeature(weapon="greatsword")]

        if 3 <= talent_roll <= 6 or talent_roll == 12:
            return [
                BonusFeature(bonus=Bonus.MELEE_ATTACK, value=1),
                BonusFeature(bonus=Bonus.RANGED_ATTACK, value=1),
            ]
        if 7 <= talent_roll <= 9:
            if ctx.stats["strength"] < 18:
                return [StatFeature(stat="strength", value=2)]
            if ctx.stats["constitution"] < 18:
                return [StatFeature(stat="constitution", value=2)]
            else:
                return [StatFeature(stat="dexterity", value=2)]
        return [BonusFeature(bonus=Bonus.PLATE_ARMOR, value=1)]


class Thief(CharacterClass):
    name = "Thief"
    hit_dice = "1d4"
    weapon_preferences = ["shortsword", "dagger", "club"]

    @staticmethod
    def choose_race() -> Type[Race]:
        return random.choice([Human, Goblin, Halfling])

    @staticmethod
    def get_default_features(race: Type[Race], alignment: str) -> List[Feature]:
        return [
            MiscellaneousFeature(name=x)
            for x in [
                "backstab: on attack against unaware target, add 1+half-level damage dice",
                "thievery: you always have thieves' tools, no gear slots needed",
                "trained in climbing, sneaking, hiding, finding/disabling traps, delicate "
                + "work like picking pockets and locks (advantage on relevant checks)",
            ]
        ]

    @staticmethod
    def requires_reroll(talent_rolls: Iterable[int]) -> bool:
        """
        Returns whether or not a character class requires a reroll
        :param: talent_rolls: rolls for talent
        :returns: whether or not the character class requires a reroll
        """
        if len(list(talent_rolls)) == 1:
            return False
        if all((x == 2 for x in talent_rolls)):
            return True
        return False

    @staticmethod
    def get_features_for_roll(
        talent_roll: int, ctx: FeatureContext, race: Race
    ) -> List[Feature]:
        """
        Returns a feature for a character class

        :param: talent_roll: the roll of the talent
        :param: ctx: the context of the character
        :returns: a feature
        """
        if talent_roll == 2:
            return [MiscellaneousFeature(name="advantage on initiative checks")]

        if 3 <= talent_roll <= 5:
            return [
                BonusFeature(bonus=Bonus.BACKSTAB, value=1),
            ]
        if 6 <= talent_roll <= 9:
            if ctx.stats["dexterity"] < 18:
                return [StatFeature(stat="dexterity", value=2)]
            if ctx.stats["charisma"] < 18:
                return [StatFeature(stat="charisma", value=2)]
            else:
                return [StatFeature(stat="constitution", value=2)]
        return [
            BonusFeature(bonus=Bonus.MELEE_ATTACK, value=1),
            BonusFeature(bonus=Bonus.RANGED_ATTACK, value=1),
        ]


class Wizard(CharacterClass):
    name = "Wizard"
    hit_dice = "1d4"
    weapon_preferences = ["staff", "dagger"]

    @staticmethod
    def choose_race() -> Type[Race]:
        return random.choice([Human, Elf])

    @staticmethod
    def get_default_features(race: Type[Race], alignment: str) -> List[Feature]:
        spells: Set[Spell] = set()
        while len(spells) < 3:
            spells.add(random.choice(WIZARD_SPELLS))
        return [SpellFeature(spell) for spell in spells]

    @staticmethod
    def get_features_for_roll(
        talent_roll: int, ctx: FeatureContext, race: Race
    ) -> List[Feature]:
        """
        Returns a feature for a character class

        :param: talent_roll: the roll of the talent
        :param: ctx: the context of the character
        :returns: a feature
        """
        if talent_roll == 2:
            return [GearFeature(gear=random.choice(MAGIC_ITEMS), weight=1)]
        if 3 <= talent_roll <= 7 or talent_roll == 12:
            if ctx.stats["intelligence"] < 18:
                return [StatFeature(stat="intelligence", value=2)]
            else:
                return [BonusFeature(bonus=Bonus.SPELL_CASTING, value=1)]
        if 8 <= talent_roll <= 9:
            return [
                SpellMasteryFeature(
                    spell=random.choice(
                        [x for x in ctx.spells if x not in ctx.spell_masteries]
                    )
                )
            ]
        return [
            SpellFeature(
                spell=random.choice([x for x in WIZARD_SPELLS if x not in ctx.spells])
            )
        ]


class KnightOfStYdris(CharacterClass):
    name = "Knight of St. Ydris"
    hit_dice = "1d6"
    weapon_preferences = [
        "bastard sword",
        "longsword",
        "spear",
        "dagger",
        "club",
    ]

    @staticmethod
    def choose_race() -> Type[Race]:
        return random.choice([Human, HalfOrc, Dwarf])

    @staticmethod
    def get_default_features(race: Type[Race], alignment: str) -> List[Feature]:
        return [
            LanguageFeature(language="diabolic"),
            BonusFeature(Bonus.DEMONIC_POSSESSION, 1),
        ]

    @staticmethod
    def get_features_for_roll(
        talent_roll: int, ctx: FeatureContext, race: Race
    ) -> List[Feature]:
        """
        Returns a feature for a character class

        :param: talent_roll: the roll of the talent
        :param: ctx: the context of the character
        :returns: a feature
        """
        if talent_roll in (2, 12):
            return [BonusFeature(Bonus.DEMONIC_POSSESSION, 1)]

        if 3 <= talent_roll <= 6:
            return [
                BonusFeature(bonus=Bonus.MELEE_ATTACK, value=1),
            ]
        if 7 <= talent_roll <= 9:
            if ctx.stats["strength"] < 18:
                return [StatFeature(stat="strength", value=2)]
            if ctx.stats["constitution"] < 18:
                return [StatFeature(stat="constitution", value=2)]
            else:
                return [StatFeature(stat="dexterity", value=2)]
        if ctx.stats["charisma"] < 18:
            return [StatFeature(stat="charisma", value=2)]
        else:
            return [BonusFeature(Bonus.SPELL_CASTING, 1)]


class Warlock(CharacterClass):
    name = "Warlock"
    hit_dice = "1d6"
    weapon_preferences = ["longsword", "mace", "dagger", "club"]

    @staticmethod
    def choose_race() -> Type[Race]:
        return random.choice([Human, HalfOrc, Dwarf, Elf, Goblin, Halfling])


class SlimeWarlock(Warlock):
    name = "Slime Warlock"

    @staticmethod
    def get_default_features(race: Type[Race], alignment: str) -> List[Feature]:
        return [MiscellaneousFeature(name="warlock of Mugdulblub")]

    @staticmethod
    def get_features_for_roll(
        talent_roll: int, ctx: FeatureContext, race: Race
    ) -> List[Feature]:
        """
        Returns a feature for a character class

        :param: talent_roll: the roll of the talent
        :param: ctx: the context of the character
        :returns: a feature
        """
        if talent_roll == 2:
            return [BonusFeature(Bonus.MUGDULBLUB_SLIME, 1)]
        if 3 <= talent_roll <= 7:
            return [
                BonusFeature(bonus=Bonus.MUGDULBLUB_HD, value=2),
            ]
        if (8 <= talent_roll <= 9) or talent_roll == 12:
            if ctx.stats["constitution"] < 18:
                return [StatFeature(stat="constitution", value=2)]
            else:
                return [StatFeature(stat="dexterity", value=2)]
        return [
            ImmunityFeature(
                damage_immunity=random.choice(
                    [
                        x
                        for x in ["acid", "cold", "poison"]
                        if x not in ctx.damage_immunities
                    ]
                )
            ),
        ]


class DemonWarlock(Warlock):
    name = "Demon Warlock"

    @staticmethod
    def get_default_features(race: Type[Race], alignment: str) -> List[Feature]:
        return [MiscellaneousFeature(name="warlock of Almazzat")]

    @staticmethod
    def requires_reroll(talent_rolls: Iterable[int]) -> bool:
        """
        Returns whether or not a character class requires a reroll
        :param: talent_rolls: rolls for talent
        :returns: whether or not the character class requires a reroll
        """
        if len(list(talent_rolls)) == 1:
            return False
        if all((x in (10, 11) for x in talent_rolls)):
            return True
        return False

    @staticmethod
    def get_features_for_roll(
        talent_roll: int, ctx: FeatureContext, race: Race
    ) -> List[Feature]:
        """
        Returns a feature for a character class

        :param: talent_roll: the roll of the talent
        :param: ctx: the context of the character
        :returns: a feature
        """
        if talent_roll == 2:
            return [BonusFeature(Bonus.ALMAZZAT_MELEE, 1)]
        if 3 <= talent_roll <= 7:
            return [BonusFeature(Bonus.MELEE_ATTACK, 1)]
        if (8 <= talent_roll <= 9) or talent_roll == 12:
            if ctx.stats["strength"] < 18:
                return [StatFeature(stat="strength", value=2)]
            else:
                return [BonusFeature(Bonus.MELEE_ATTACK, 1)]
        return [MiscellaneousFeature(name="advantage on initiative checks")]


class FateWarlock(Warlock):
    name = "Fate Warlock"

    @staticmethod
    def get_default_features(race: Type[Race], alignment: str) -> List[Feature]:
        return [MiscellaneousFeature(name="warlock of Kytheros")]

    @staticmethod
    def requires_reroll(talent_rolls: Iterable[int]) -> bool:
        """
        Returns whether or not a character class requires a reroll
        :param: talent_rolls: rolls for talent
        :returns: whether or not the character class requires a reroll
        """
        if len(list(talent_rolls)) == 1:
            return False
        if all((x in (10, 11) for x in talent_rolls)):
            return True
        return False

    @staticmethod
    def get_features_for_roll(
        talent_roll: int, ctx: FeatureContext, race: Race
    ) -> List[Feature]:
        """
        Returns a feature for a character class

        :param: talent_roll: the roll of the talent
        :param: ctx: the context of the character
        :returns: a feature
        """
        if talent_roll == 2:
            return [BonusFeature(Bonus.KYTHEROS_REROLL, 1)]
        if 3 <= talent_roll <= 7:
            [BonusFeature(Bonus.ARMOR, 1)]
        if (8 <= talent_roll <= 9) or talent_roll == 12:
            if ctx.stats["wisdom"] < 18:
                return [StatFeature(stat="wisdom", value=2)]
            if ctx.stats["dexterity"] < 18:
                return [StatFeature(stat="dexterity", value=2)]
            return [StatFeature(stat="strength", value=2)]
        return [MiscellaneousFeature(name="3/day, add WIS bonus to any roll")]


class VileWarlock(Warlock):
    name = "Vile Warlock"

    @staticmethod
    def get_default_features(race: Type[Race], alignment: str) -> List[Feature]:
        return [MiscellaneousFeature(name="warlock of Shune the Vile")]

    @staticmethod
    def get_features_for_roll(
        talent_roll: int, ctx: FeatureContext, race: Race
    ) -> List[Feature]:
        """
        Returns a feature for a character class

        :param: talent_roll: the roll of the talent
        :param: ctx: the context of the character
        :returns: a feature
        """
        if talent_roll == 2:
            return [BonusFeature(Bonus.SHUNE_MIND, 1)]
        if 3 <= talent_roll <= 7 or talent_roll == 12:
            return [
                SpellFeature(
                    spell=random.choice(
                        [x for x in WIZARD_SPELLS if x not in ctx.spells]
                    )
                )
            ]
        if 8 <= talent_roll <= 9:
            if ctx.stats["intelligence"] < 18:
                return [StatFeature(stat="intelligence", value=2)]
            return [StatFeature(stat="dexterity", value=2)]
        return [BonusFeature(Bonus.SHUNE_XP, 1)]


class FeyWarlock(Warlock):
    name = "Fey Warlock"

    @staticmethod
    def get_default_features(race: Type[Race], alignment: str) -> List[Feature]:
        return [MiscellaneousFeature(name="warlock of Titania")]

    @staticmethod
    def requires_reroll(talent_rolls: Iterable[int]) -> bool:
        """
        Returns whether or not a character class requires a reroll
        :param: talent_rolls: rolls for talent
        :returns: whether or not the character class requires a reroll
        """
        if len(list(talent_rolls)) == 1:
            return False
        if all((x in (10, 11) for x in talent_rolls)):
            return True
        return False

    @staticmethod
    def get_features_for_roll(
        talent_roll: int, ctx: FeatureContext, race: Race
    ) -> List[Feature]:
        """
        Returns a feature for a character class

        :param: talent_roll: the roll of the talent
        :param: ctx: the context of the character
        :returns: a feature
        """
        if talent_roll == 2:
            return [BonusFeature(Bonus.TITANIA_HYPNOTIZE, 1)]
        if 3 <= talent_roll <= 7:
            if "longbow" not in ctx.weapon_proficiencies:
                return [WeaponProficiencyFeature(weapon="longbow")]
            return [BonusFeature(Bonus.RANGED_ATTACK, 1)]
        if (8 <= talent_roll <= 9) or talent_roll == 12:
            if ctx.stats["dexterity"] < 18:
                return [StatFeature(stat="dexterity", value=2)]
            return [StatFeature(stat="charisma", value=2)]
        return [
            MiscellaneousFeature(name="hostile spells that target you are hard to cast")
        ]


class WillowWarlock(Warlock):
    name = "Willow Warlock"

    @staticmethod
    def get_default_features(race: Type[Race], alignment: str) -> List[Feature]:
        return [MiscellaneousFeature(name="warlock of The Willowman")]

    @staticmethod
    def get_features_for_roll(
        talent_roll: int, ctx: FeatureContext, race: Race
    ) -> List[Feature]:
        """
        Returns a feature for a character class

        :param: talent_roll: the roll of the talent
        :param: ctx: the context of the character
        :returns: a feature
        """
        if talent_roll == 2:
            return [BonusFeature(Bonus.WILLOWMAN_TELEPORT, 1)]
        if 3 <= talent_roll <= 7:
            return [BonusFeature(Bonus.MELEE_ATTACK, 1)]
        if (8 <= talent_roll <= 9) or talent_roll == 12:
            if ctx.stats["strength"] < 18:
                return [StatFeature(stat="strength", value=2)]
            return [StatFeature(stat="dexterity", value=2)]
        return [BonusFeature(Bonus.WILLOWMAN_MORALE, 1)]


class Witch(CharacterClass):
    name = "Witch"
    hit_dice = "1d4"
    weapon_preferences = ["dagger", "staff"]

    @staticmethod
    def choose_race() -> Type[Race]:
        return random.choice([Human, Elf, Goblin, Halfling])

    @staticmethod
    def get_default_features(race: Type[Race], alignment: str) -> List[Feature]:
        spells: Set[Spell] = set()
        while len(spells) < 3:
            spells.add(random.choice(WITCH_SPELLS))
        return (
            [SpellFeature(spell=x) for x in spells]  # type: ignore
            + [
                LanguageFeature(language=x)  # type: ignore
                for x in {"diabolic", "primoridal", "sylvan"}
            ]
            + [
                MiscellaneousFeature(  # type: ignore
                    name="familiar: you have a little buddy, it speaks common"
                    + "and you can cast spells through it"
                )
            ]
        )

    @staticmethod
    def get_features_for_roll(
        talent_roll: int, ctx: FeatureContext, _
    ) -> List[Feature]:
        """
        Returns a feature for a character class

        :param: talent_roll: the roll of the talent
        :param: ctx: the context of the character
        :returns: a feature
        """
        if talent_roll == 2:
            return [BonusFeature(bonus=Bonus.WITCH_TELEPORT, value=1)]
        if 3 <= talent_roll <= 7 or talent_roll == 12:
            if ctx.stats["charisma"] < 18:
                return [StatFeature(stat="charisma", value=2)]
            else:
                return [BonusFeature(bonus=Bonus.SPELL_CASTING, value=1)]
        if 8 <= talent_roll <= 9:
            return [
                SpellMasteryFeature(
                    spell=random.choice(
                        [x for x in ctx.spells if x not in ctx.spell_masteries]
                    )
                )
            ]
        return [
            SpellFeature(
                spell=random.choice([x for x in WITCH_SPELLS if x not in ctx.spells])
            )
        ]


@dataclass
class Character:
    """
    A shadowdark character.
    """

    race: Type[Race]
    character_class: Type[CharacterClass]
    stats: StatArray
    hit_points: int
    spells: Set[Spell]
    talents: List[Talent]
    languages: Set[Language]
    name: str


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
# {self.character.name}, {self.character.race.name} {self.character.character_class.name}

HP: {self.character.hit_points}

```
STR: {self._format_stat(self.character.stats['strength'])}
DEX: {self._format_stat(self.character.stats['dexterity'])}
CON: {self._format_stat(self.character.stats['constitution'])}
INT: {self._format_stat(self.character.stats['intelligence'])}
WIS: {self._format_stat(self.character.stats['wisdom'])}
CHA: {self._format_stat(self.character.stats['charisma'])}
```

{self._format_languages(self.character.languages)}

{self._format_talents(self.character.talents)}
{self._format_spells(self.character.spells)}
{self._format_gear(self.gear)}
        """


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


def make_talent_rolls(race: Type[Race]) -> List[int]:
    """
    Returns the results of a series of 2d6 rolls, suitable
    for use in determining talents.

    :param: race: necessary because humans get extra starting talents
    :returns: a list of integers, representing results of the rolls
    """
    return [roll("2d6") for _ in range((2 if race is Human else 1))]


def generate_character_sheet() -> CharacterSheet:
    """
    Create a character sheet. This follows the rules of Shadowdark's character
    creation process, and attempts to make a fair, viable, character.

    :returns: a CharacterSheet
    """
    # roll stats - if any under 14, re-roll
    while True:
        stats: StatArray = {
            "strength": roll("3d6"),
            "dexterity": roll("3d6"),
            "constitution": roll("3d6"),
            "intelligence": roll("3d6"),
            "wisdom": roll("3d6"),
            "charisma": roll("3d6"),
        }
        if max(list(stats.values())) >= 14:  # type: ignore
            break

    # choose class based on best stat
    best: Tuple[str, int] = max(
        (x for x in stats.items() if x[0] != "constitution"), key=lambda x: x[1]  # type: ignore
    )

    character_class: Optional[Type[CharacterClass]] = None
    if best[1] < 14:  # good at nothing, serve the underlords!
        if best[1] < 10:
            # true scrubs serve the slime god
            character_class = SlimeWarlock
        elif best[0] == "strength":
            character_class = DemonWarlock
        elif best[0] == "dexterity":
            character_class = FeyWarlock
        elif best[0] == "intelligence":
            character_class = VileWarlock
        elif best[0] == "wisdom":
            character_class = FateWarlock
        else:
            character_class = WillowWarlock
    elif best[0] == "dexterity":
        character_class = Thief
    elif best[0] == "wisdom":
        character_class = Cleric
    elif best[0] == "strength":
        if stats["charisma"] >= 14:
            character_class = KnightOfStYdris  # look good enough to be an edgelord?
        else:
            character_class = Fighter
    elif best[0] == "intelligence":
        character_class = Wizard
    elif best[0] == "charisma":
        character_class = Witch

    if not character_class:
        raise Exception("Could not determine character class")

    alignment = random.choice(["lawful", "neutral"])
    race = character_class.choose_race()

    while True:
        talent_rolls = make_talent_rolls(race)
        if not character_class.requires_reroll(talent_rolls):
            break

    ctx = FeatureContext(stats)

    for feature in race.get_default_features(character_class):
        ctx.apply_feature(feature)
    for feature in character_class.get_default_features(race, alignment):
        ctx.apply_feature(feature)
    for talent_roll in talent_rolls:
        for feature in character_class.get_features_for_roll(  # type: ignore
            talent_roll, ctx, race
        ):
            ctx.apply_feature(feature)

    # special case logic for wizard languages
    if character_class is Wizard:
        for language in set(
            random.choice(
                list(
                    itertools.combinations(
                        [x for x in COMMON_LANGUAGES if x not in ctx.languages], 2
                    )
                )
            )
        ).union(
            set(
                random.choice(
                    list(
                        itertools.combinations(
                            [x for x in RARE_LANGUAGES if x not in ctx.languages], 2
                        )
                    )
                )
            )
        ):
            ctx.apply_feature(LanguageFeature(language))

    for spell in ctx.spell_masteries:
        ctx.talents.append(f"advantage on casting {spell}")

    for damage_type in ctx.damage_immunities:
        ctx.talents.append(f"immune to {damage_type} damage")

    # add the bonuses as talents
    if ctx.bonuses[Bonus.ALMAZZAT_MELEE]:
        ctx.talents.append(
            f"{ctx.bonuses[Bonus.ALMAZZAT_MELEE]}/day, gain advantage on melee attacks for 3 rounds"
        )
    if ctx.bonuses[Bonus.ARMOR]:
        ctx.talents.append(f"+{ctx.bonuses[Bonus.ARMOR]} to AC")
    if ctx.bonuses[Bonus.BACKSTAB]:
        ctx.talents.append(
            f"+{ctx.bonuses[Bonus.BACKSTAB]} damage dice to backstab attacks"
        )
    if ctx.bonuses[Bonus.DEMONIC_POSSESSION]:
        ctx.talents.append(
            f"demonic possession: 3/day, gain a {ctx.bonuses[Bonus.DEMONIC_POSSESSION]} "
            + "half-level bonus to damage rolls for 3 rounds"
        )
    if ctx.bonuses[Bonus.KYTHEROS_REROLL]:
        ctx.talents.append(
            f"{ctx.bonuses[Bonus.KYTHEROS_REROLL]}/day, force the GM to reroll a single roll"
        )
    if ctx.bonuses[Bonus.MELEE_ATTACK]:
        ctx.talents.append(f"+{ctx.bonuses[Bonus.MELEE_ATTACK]} to melee attacks")
    if ctx.bonuses[Bonus.MUGDULBLUB_HD]:
        ctx.talents.append(
            f"Maximize {ctx.bonuses[Bonus.MUGDULBLUB_HD]} hit dice rolls (prior or future)"
        )
    if ctx.bonuses[Bonus.MUGDULBLUB_SLIME]:
        ctx.talents.append(
            f"{ctx.bonuses[Bonus.MUGDULBLUB_SLIME]}/day, turn into a "
            + "crawling puddle of slime for 3 rounds"
        )
    if ctx.bonuses[Bonus.PLATE_ARMOR]:
        ctx.talents.append(
            f"+{ctx.bonuses[Bonus.PLATE_ARMOR]} to AC while wearing plate armor"
        )
    if ctx.bonuses[Bonus.RANGED_ATTACK]:
        ctx.talents.append(f"+{ctx.bonuses[Bonus.RANGED_ATTACK]} to ranged attacks")
    if ctx.bonuses[Bonus.SHUNE_MIND]:
        ctx.talents.append(
            f"{ctx.bonuses[Bonus.SHUNE_MIND]}/day, read the mind "
            + "of a creature you touch for 3 rounds"
        )
    if ctx.bonuses[Bonus.TITANIA_HYPNOTIZE]:
        ctx.talents.append(
            f"{ctx.bonuses[Bonus.TITANIA_HYPNOTIZE]}/day, "
            + "hypnotize a 5 HD or less creature for 3 rounds"
        )

    if ctx.bonuses[Bonus.SHUNE_XP]:
        ctx.talents.append(
            f"+{ctx.bonuses[Bonus.SHUNE_XP]} XP whenever you learn a valuable or significant secret"
        )
    if ctx.bonuses[Bonus.SPELL_CASTING]:
        ctx.talents.append(
            f"+{ctx.bonuses[Bonus.SPELL_CASTING]} to spellcasting checks"
        )
    if ctx.bonuses[Bonus.WILLOWMAN_MORALE]:
        ctx.talents.append(
            f"{ctx.bonuses[Bonus.WILLOWMAN_MORALE]}/day, "
            + "force a close being to check morale, even if immune"
        )
    if ctx.bonuses[Bonus.WILLOWMAN_TELEPORT]:
        ctx.talents.append(
            f"{ctx.bonuses[Bonus.WILLOWMAN_TELEPORT]}/day, "
            + "teleport to a far location you see as your move"
        )
    if ctx.bonuses[Bonus.WITCH_TELEPORT]:
        ctx.talents.append(
            f"{ctx.bonuses[Bonus.WITCH_TELEPORT]}/day, teleport "
            + "to your familiar's location as a move"
        )

    assert len(set(ctx.talents)) == len(ctx.talents), "duplicate talents"

    gold = float(roll("2d6") * 5)
    gear_slots = max([10, ctx.stats["strength"]]) + (
        STAT_BONUS_TABLE[ctx.stats["constitution"]]
        if (
            character_class is Fighter
            and STAT_BONUS_TABLE[ctx.stats["constitution"]] > 0
        )
        else 0
    )
    gear = copy.deepcopy(ctx.gear)
    weight = ctx.gear_weight
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
        x for x in character_class.weapon_preferences if PRICE_TABLE[x] <= gold
    ]
    assert affordable_weapons, "no affordable weapons"
    if affordable_weapons and weight < gear_slots:
        best_weapon = affordable_weapons[0]
        if best_weapon == "bastard sword" and race is Dwarf:
            best_weapon = "greataxe"
        gear += [best_weapon]
        weight += 1
        gold -= PRICE_TABLE[best_weapon]

    # get a shield if plausible
    if (
        character_class in (Fighter, Cleric, KnightOfStYdris, Warlock)
        and gold >= 10
        and weight < gear_slots
    ):
        gear += ["shield"]
        weight += 1
        gold -= 10

    # get leather armor if plausible
    if (
        character_class in (Fighter, Cleric, Thief, KnightOfStYdris, Warlock, Witch)
        and gold >= 10
        and weight < gear_slots
    ):
        gear += ["leather armor"]
        weight += 1
        gold -= 10

    gear += [f"{gold} gold pieces"]

    ctx.talents.append(
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
        hit_points=roll(character_class.hit_dice, advantage=(race is Dwarf))
        + max(STAT_BONUS_TABLE[ctx.stats["constitution"]], 1),
        stats=stats,
        spells=ctx.spells,
        talents=ctx.talents,
        languages=ctx.languages,
        name=random.choice(race.names),
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


print("\n---\n".join(x.as_markdown() for x in generate_party(size=6)))
