import bisect
from datetime import timedelta
CACHE_REFRESH_TIME = timedelta(hours=4)
TIME_FORMAT_STRING = "%y/%m/%d %H:%M:%S"
# When calculating the price of a recipe, we consider breakpoints for number of recipes that the market must support for us to consider them
# For example, 1000 means that there must be 1000 * (required input items) sell orders on the market, and 1000 * (output item) buy orders on the market
RECIPE_AMOUNTS_TO_CHECK = [1, 10, 1_000, 10_000, 100_000]

xp_table = {
    1: 0,
    2: 75,
    3: 151,
    4: 227,
    5: 303,
    6: 380,
    7: 531,
    8: 683,
    9: 836,
    10: 988,
    11: 1141,
    12: 1294,
    13: 1447,
    14: 1751,
    15: 2054,
    16: 2358,
    17: 2663,
    18: 2967,
    19: 3272,
    20: 3577,
    21: 4182,
    22: 4788,
    23: 5393,
    24: 5999,
    25: 6606,
    26: 7212,
    27: 7819,
    28: 9026,
    29: 10233,
    30: 11441,
    31: 12648,
    32: 13856,
    33: 15065,
    34: 16273,
    35: 18682,
    36: 21091,
    37: 23500,
    38: 25910,
    39: 28319,
    40: 30729,
    41: 33140,
    42: 37950,
    43: 42761,
    44: 47572,
    45: 52383,
    46: 57195,
    47: 62006,
    48: 66818,
    49: 76431,
    50: 86043,
    51: 95656,
    52: 105269,
    53: 114882,
    54: 124496,
    55: 134109,
    56: 153323,
    57: 172538,
    58: 191752,
    59: 210967,
    60: 230182,
    61: 249397,
    62: 268613,
    63: 307028,
    64: 345444,
    65: 383861,
    66: 422277,
    67: 460694,
    68: 499111,
    69: 537528,
    70: 614346,
    71: 691163,
    72: 767981,
    73: 844800,
    74: 921618,
    75: 998437,
    76: 1075256,
    77: 1228875,
    78: 1382495,
    79: 1536114,
    80: 1689734,
    81: 1843355,
    82: 1996975,
    83: 2150596,
    84: 2457817,
    85: 2765038,
    86: 3072260,
    87: 3379481,
    88: 3686703,
    89: 3993926,
    90: 4301148,
    91: 4915571,
    92: 5529994,
    93: 6144417,
    94: 6758841,
    95: 7373264,
    96: 7987688,
    97: 8602113,
    98: 9830937,
    99: 11059762,
    100: 12288587,
    101: 13517412,
    102: 14746238,
    103: 15975063,
    104: 17203889,
    105: 19661516,
    106: 22119142,
    107: 24576769,
    108: 27034396,
    109: 29492023,
    110: 31949651,
    111: 34407278,
    112: 39322506,
    113: 44237735,
    114: 49152963,
    115: 54068192,
    116: 58983421,
    117: 63898650,
    118: 68813880,
    119: 78644309,
    120: 88474739,
}

# Precompute sorted XP values
xp_values = list(xp_table.values())
levels = list(xp_table.keys())

def get_level(xp: int) -> int:
    """Return nearest level for given XP (caps at 120)."""
    if xp >= xp_values[-1]:
        return levels[-1]
    if xp <= xp_values[0]:
        return levels[0]
    idx = bisect.bisect_left(xp_values, xp)
    before = xp_values[idx - 1]
    after = xp_values[idx]
    # choose closer one
    if abs(xp - before) <= abs(after - xp):
        return levels[idx - 1]
    else:
        return levels[idx]