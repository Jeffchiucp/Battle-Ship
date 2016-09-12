from general import (VERTICAL_SHIP, HORIZONTAL_SHIP, EMPTY, MISS, HIT, SUNK, alpha_to_index)
from ship import Ship
import logging


class Player:

    def attack(self):
        """request a position from the player to fire at"""
        print("{}'s Turn to pick a target.".format(self.name))
        return self.parse_position()

    def parse_position(self, position=None):
        if position is None:
            position = input("Please enter a position e.g. B4: ")

        if len(position) == 2 and position.isalnum():
            # get the number and letter regardless of order or case a1 , 1A
            for ref in position:
                try:
                    number = int(ref)
                except ValueError:
                    alpha = ref.lower()
            limit = alpha_to_index(alpha) + 1
            if limit <= self.game_state.BOARD_SIZE:
                try:  # if they have entered double eg AA or 11 catch it
                    return alpha, number
                except UnboundLocalError:
                    self.game_state.redraw()
                    print('you need a number 9 or less and a letter')
                    return self.parse_position()
            else:
                self.game_state.redraw()
                print('letter out of range')
                return self.parse_position()

        else:
            self.game_state.redraw()
            print('you need a number 9 or less and a letter')
            return self.parse_position()

    def __init__(self, world, player_num):  # player_num ie "Player One"
        self.game_state = world
        self.player_num = player_num
        self.message = ""
        self.ship_info = [
            ("Aircraft Carrier", 5),
            ("Battleship", 4),
            ("Submarine", 3),
            ("Cruiser", 3),
            ("Patrol Boat", 2)
        ]
        self.fleet_pos = set()  # all positions of all ships
        self.missed = set()  # all missed shots fired
        self.fleet = []  # the fleet is a list of ship objects
        self.life = len(self.ship_info)

        name = input("Player {}, what is your name:".format(player_num))
        self.name = name.title()

    def ship_placement(self):
        self.game_state.message = "{}'s turn to place ships".format(self.name)
        self.game_state.redraw()
        while self.ship_info:  # until there is no ships to add. list = []
            s_name, length = self.ship_info.pop()

            while True:
                position = input("Please enter an initial cell for {} ({} spaces) e.g. a2: ".format(s_name, length))
                loc = self.parse_position(position)
                direction = input("The location of the {} ({} spaces): {} Is it Horizontal? (Y)/N: ".format(s_name,
                                                                                                            length,
                                                                                                            loc))
                if direction.lower() == 'n' or direction.lower() == 'no':
                    direction = 'vertical'
                else:
                    direction = 'horizontal'
                new_ship = Ship(loc, direction, length, s_name)
                if self.ship_verify(new_ship):
                    break
                else:
                    self.game_state.redraw()
                    print(self.message)

    def status_report(self, position):
        if position in self.missed:
            return False
        elif position in self.fleet_pos:
            for ship in self.fleet:
                try:
                    index = ship.ship_pos.index(position)
                except ValueError:
                    pass  # didn't hit this ship
                else:
                    if ship.ship_hp[index] == HIT or ship.ship_hp[index] == SUNK:
                        return False
                    else:
                        ship.ship_hp[index] = HIT  # update ship health
                        # check if all spaces hit
                        if len(set(ship.ship_hp)) == 1:
                            length = len(ship.ship_hp)
                            ship.ship_hp = [SUNK]*length  # change ship to reflect sunk
                            self.game_state.message = 'DIRECT HIT! {} Sunk!'.format(ship.name)
                            self.game_state.new_hit_message = 'GOING DOWN! Your {} got sunk! at {}.'.format(ship.name,
                                                                                                            position)
                            self.game_state.update_game()
                            self.life -= 1
                            return True
                        else:
                            self.game_state.message = 'DIRECT HIT!'
                            self.game_state.new_hit_message = 'Your {} got hit! at {}.'.format(ship.name, position)
                            self.game_state.update_game()
                            return True
        else:
            self.missed.add(position)
            self.game_state.message = 'YOU MISSED!'
            self.game_state.new_hit_message = 'ENEMY MISSED!'
            self.game_state.update_game()
            return True

    def ship_verify(self, new_ship):
        """
        checks that a new_ship (Type = Ship) doesn't overlap with any other
        existing ships passed to this method and is located within the BOARD_SIZE.
        If successful will return True, add the new_ship to fleet and its positions
        to fleet_pos else return False and update self.message with an explanation
        for the next redraw.
        """
        position_list = new_ship.ship_pos
        outer_most_letter = position_list[-1][0]
        outer_most_letter = outer_most_letter.lower()
        board_chars = "_abcdefghijklmnopqrstuvwxyz"

        # check if the last position char in the new_ship is inside the grid
        if ord(outer_most_letter) > ord(board_chars[self.game_state.BOARD_SIZE]):
            logging.debug('horizontal ship outside of grid')
            self.message = 'ship outside of grid'
            return False

        # check if the last position number in the new_ship is inside the grid
        if position_list[-1][1] >= self.game_state.BOARD_SIZE:
            logging.debug('vertical ship outside of grid')
            self.message = 'ship outside of grid'
            return False

        # check that the new ship doesn't intersect with any existing ships
        position_set = set(position_list)
        if self.fleet_pos & position_set:  # ship intersect warn player
            logging.debug('ships intersect')
            self.message = 'Ship crosses existing placement'
            return False
        else:  # ship placement is good add to set of existing ship locations
            logging.debug('ship verified')
            self.fleet_pos.update(position_set)
            self.fleet.append(new_ship)
            self.game_state.update_game()
            self.game_state.redraw()
            return True

    def populate_board(self, hide_ships=False):
        """
        takes all information from player to display the location of hits, misses and ships.
        when hide ships is True all ship markers '-' and '|' will be replaced with 'O'
        """

        board = [[EMPTY for cell in range(0, 10)] for row in range(0, 10)]  # make an empty board

        for alpha, num in self.missed:  # Populate board with all missed positions

            index = alpha_to_index(alpha)
            board[index][num] = MISS

        for ship in self.fleet:  # add location of all ships and if they have been hit or not
            count = 0
            for alpha, num in ship.ship_pos:
                indicator = ship.ship_hp[count]
                if hide_ships:  # Hide the non hit ships if hide_ships is True
                    if indicator == HORIZONTAL_SHIP or indicator == VERTICAL_SHIP:
                        indicator = EMPTY
                index = alpha_to_index(alpha)
                board[index][num] = indicator
                count += 1
        return board
