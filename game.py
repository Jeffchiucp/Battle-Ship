from player import Player
from general import EMPTY
import os
import sys


class Game:

    CREDIT = "Art from: http://www.chris.com/ascii"
    MAIN_DISPLAY = "ascii-battleship.txt"
    BOARD_SIZE = 10

    message = "No message!"
    hit_message = ''
    new_hit_message = ''

    active_board = [[EMPTY]*10]*10  # 10x10 board displaying current players ships
    target_board = [[EMPTY]*10]*10  # 10x10 board displaying current players hits and misses on opponent

    def __init__(self):
        print('Welcome to Battleship:')
        self.active_player = Player(self, 1)  # self is passing instance of Game to Player
        self.defending_player = Player(self, 2)
        self.active_player.ship_placement()
        input('Press Enter to end turn: ')
        self.end_turn()
        self.active_player.ship_placement()
        input('Press Enter to end turn: ')
        self.end_turn()

    def end_turn(self):
        """swaps the active player sets up to begin that players turn and displays a waiting screen"""
        self.active_player, self.defending_player = self.defending_player, self.active_player  # swap players
        hide_board = [[EMPTY]*10]*10
        self.active_board = hide_board
        self.target_board = hide_board
        self.message = self.new_hit_message
        self.clear_screen()
        self.draw_title('END OF TURN')
        self.draw_file('ascii-wait.txt')
        self.draw_message(self.CREDIT)
        input("To begin {}'s turn press Enter: ".format(self.active_player.name))

    def game_loop(self):
        """main game loop"""
        while True:
            self.update_game()  # update board to show active players ships
            self.redraw()
            self.get_target()
            self.redraw()
            if self.defending_player.life <= 0:
                self.draw_victory()
            input("Press Enter to end turn: ")
            self.end_turn()

    def update_game(self):
        """re-populates the player boards with the current game state"""
        self.active_board = self.active_player.populate_board()
        self.target_board = self.defending_player.populate_board(True)

    def get_target(self):
        """get some coordinates from the player"""
        while True:
            position = self.active_player.attack()
            new_target = self.defending_player.status_report(position)
            if new_target:
                self.redraw()
                break
            else:
                self.redraw()
                print("You have already tried {}{}. Try a different location.".format(position[0].upper(), position[1]))

    @staticmethod
    def clear_screen():

        print("\033c", end="")
        if os.name == 'nt':
            os.system('cls')
            print("\033c", end="")
        else:
            os.system("clear")
            print("\033c", end="")

    @staticmethod
    def draw_title(title):
        """prints message to screen centered with boarders sides and top"""
        print('#'*81)
        title = '#' + title.center(79, ' ') + '#'
        print(title)

    @staticmethod
    def draw_file(ascii_file):
        """prints a text file to screen"""
        with open(ascii_file, 'r', newline='\n') as draw_file:
            temp = [line.rstrip('\n') for line in draw_file]
            for strip in temp:
                strip.rstrip('\n')
                print(strip)

    @staticmethod
    def draw_message(message):
        """prints message to screen centered with boarders sides and bottom"""
        message = '#' + message.center(79, ' ') + '#'
        print(message)
        print('#'*81)

    def draw_board(self, victory=False):
        """
        Draws section of game screen containing board grids. Has a secondary display state for end of game when
        victory = true
        """

        side1 = ['#    A  ', '#    B  ', '#    C  ', '#    D  ', '#    E  ',
                 '#    F  ', '#    G  ', '#    H  ', '#    I  ', '#    J  ']

        side2 = ['|    A  ', '|    B  ', '|    C  ', '|    D  ', '|    E  ',
                 '|    F  ', '|    G  ', '|    H  ', '|    I  ', '|    J  ']
        end_bit1 = '    '
        end_bit2 = '    #'

        if victory:
            victor = "{}'s fleet".format(self.active_player.name)
            loser = "{}'s fleet".format(self.defending_player.name)
            print('#' + victor.center(39, ' ') + '|' + loser.center(39, ' ') + '#')
            print('#' + ' '*39 + '|' + ' '*39 + '#')
        else:
            turn = "{}'s Turn".format(self.active_player.name)
            turn = '#' + turn.center(79, ' ') + '#'
            print(turn)
            print('#' + ' '*79 + '#')
            print('#' + 'Your Fleet'.center(39, ' ') + '|' + 'Enemy Waters'.center(39, ' ') + '#')
            print('#' + ' '*39 + '|' + ' '*39 + '#')

        print('#       0  1  2  3  4  5  6  7  8  9    |       0  1  2  3  4  5  6  7  8  9    #')
        for index in range(0, 9):
            home = "  ".join(self.active_board[index])
            target = "  ".join(self.target_board[index])
            print(side1[index] + home + end_bit1 + side2[index] + target + end_bit2)

        print('#' + ' '*39 + '|' + ' '*39 + '#')
        print('#'*81)

    def draw_victory(self):
        """Declares the winner and ends the game"""
        self.clear_screen()
        self.draw_title("BATTLESHIP")
        self.draw_file("ascii-game-over.txt")
        self.hit_message = "GAME OVER"
        self.draw_message("{} IS VICTORIOUS".format(self.active_player.name))
        self.draw_board(True)
        self.draw_message(self.CREDIT)
        sys.exit()

    def redraw(self):
        """redraws the screen for current game state"""
        # note width is 81
        self.clear_screen()
        self.draw_title("BATTLESHIP")
        self.draw_file(self.MAIN_DISPLAY)
        self.draw_message(self.message)
        self.draw_board()
