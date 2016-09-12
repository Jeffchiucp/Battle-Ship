from general import (VERTICAL_SHIP, HORIZONTAL_SHIP)
import logging


class Ship:

    @staticmethod
    def char_range(loc_char):
        """Generates string of characters from loc_char (start location) to past the edge of grid ('z')"""
        grids_right = []
        loc_char = loc_char.lower()

        if ord('a') <= ord(loc_char) <= ord('z'):
            for c in range(ord(loc_char), ord('z')+1):  # use unicode to generate range
                grids_right.append(chr(c))     # convert back to char

            return "".join(grids_right)         # return string of available grid
        else:
            # sad face you broke it
            logging.error('in char_range(loc_char): character grid not in range or wrong type')
            return None

    def ship_builder(self):
        """creates a list of positions to represent the location of the ship"""
        loc_char, loc_num = self.loc
        loc_char = loc_char.lower()

        if self.direction.lower() == 'horizontal':
            horizontal_grid = [loc_char]*self.length
            vertical_grid = list(range(loc_num, (loc_num + self.length)))
            zipper = zip(horizontal_grid, vertical_grid)
            self.ship_pos = list(zipper)

        else:
            horizontal_grid = self.char_range(loc_char)
            vertical_grid = [loc_num]*self.length
            zipper = zip(horizontal_grid, vertical_grid)
            self.ship_pos = list(zipper)

    def __init__(self, loc, direction, length, name):
        self.ship_pos = []
        self.ship_hp = []
        self.length = length
        self.loc = loc
        self.direction = direction
        self.name = name
        self.ship_builder()
        direction.lower()
        if direction == 'horizontal':
            self.ship_hp = [HORIZONTAL_SHIP]*length
        else:
            self.ship_hp = [VERTICAL_SHIP]*length
