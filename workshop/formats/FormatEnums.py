from enum import Enum


class PersonalFields(Enum):
    HP = 0
    ATK = 1
    DEF = 2
    SPE = 3
    SPATK = 4
    SPDEF = 5
    TYPE_1 = 6
    TYPE_2 = 7
    CATCH_RATE = 8
    BASE_EXP = 9
    EVS = 10
    ITEM_UNCOMMON = 11
    ITEM_RARE = 12
    GENDER_RATIO = 13
    HATCH_MULTIPLIER = 14
    BASE_HAPPINESS = 15
    EXP_RATE = 16
    EGG_GROUP_1 = 17
    EGG_GROUP_2 = 18
    ABILITY_1 = 19
    ABILITY_2 = 20
    RUN_CHANCE = 21
    COLOR = 22
    TMS = 23


class LevelUpLearnsetFields(Enum):
    MOVE_ID = 0
    LEVEL = 1


class EvolutionsFields(Enum):
    pass
