
VERTICAL_SHIP = '|'
HORIZONTAL_SHIP = '-'
EMPTY = 'O'
MISS = '*'
HIT = 'X'
SUNK = '#'


def alpha_to_index(alpha):
    """changes letters into numbers where a,b,c = 0,1,2 for indexing"""
    alpha = alpha.lower()
    index = ord(alpha) - 97
    return index
