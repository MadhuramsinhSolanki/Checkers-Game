import pygame
import random
from constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE, SANDALWOOD

# from .piece import Piece

pawn = {"b": "Black", "r": "Red"}


class Board:
    def __init__(self):
        self.game_board = [['b', '-', 'b', '-', 'b', '-', 'b', '-'],
                           ['-', 'b', '-', 'b', '-', 'b', '-', 'b'],
                           ['b', '-', 'b', '-', 'b', '-', 'b', '-'],
                           ['-', '-', '-', '-', '-', '-', '-', '-'],
                           ['-', '-', '-', '-', '-', '-', '-', '-'],
                           ['-', 'r', '-', 'r', '-', 'r', '-', 'r'],
                           ['r', '-', 'r', '-', 'r', '-', 'r', '-'],
                           ['-', 'r', '-', 'r', '-', 'r', '-', 'r']]
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.status = 'playing'
        self.turn = random.randrange(2)
        self.players = ['b', 'r']
        self.selected_token = None
        self.jumping = False
        pygame.display.set_caption("%s's turn" % pawn[self.players[self.turn % 2]])

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, SANDALWOOD, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pawns(self, win):
        for row in range(ROWS):
            for col in range(COLS):
                if (self.game_board[row][col] == "r"):  # If there's a red pawn on this square
                    x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                    y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                    pygame.draw.circle(win, RED, (x, y), SQUARE_SIZE // 2 - 15)
                elif (self.game_board[row][col] == "b"):  # If there's a black pawn on this square
                    x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                    y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                    pygame.draw.circle(win, BLACK, (x, y), SQUARE_SIZE // 2 - 15)
                else:
                    if ((row + col) % 2 == 0):
                        colour = SANDALWOOD
                    else:
                        colour = BLACK
                    pygame.draw.rect(win, colour, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate_click(self, mouse_pos):
        if self.status == 'playing':
            row, column = get_clicked_row(mouse_pos), get_clicked_column(mouse_pos)
            if (self.selected_token):
                move = self.is_valid_move(self.players[self.turn % 2], self.selected_token, row, column)
                print(move)
                if move[0]:
                    self.play(self.players[self.turn % 2], self.selected_token, row, column, move[1])
                elif row == self.selected_token[0] and column == self.selected_token[1]:
                    self.selected_token = None
                    if self.jumping:
                        self.jumping = False
                        self.next_turn()
                else:
                    print('invalid move')
            else:
                if (self.game_board[row][column].lower() == self.players[self.turn % 2]):
                    self.selected_token = [row, column]
        elif self.status == 'game over':
            self.__init__()

    def is_valid_move(self, player, token_location, to_row, to_col):
        from_row = token_location[0]
        from_col = token_location[1]
        token_char = self.game_board[from_row][from_col]
        if self.game_board[to_row][to_col] != '-':
            return False, None
        if (((token_char.isupper() and abs(from_row - to_row) == 1) or (player == 'b' and to_row - from_row == 1) or
             (player == 'r' and from_row - to_row == 1)) and abs(from_col - to_col) == 1) and not self.jumping:
            return True, None
        if (((token_char.isupper() and abs(from_row - to_row) == 2) or (player == 'b' and to_row - from_row == 2) or
             (player == 'r' and from_row - to_row == 2)) and abs(from_col - to_col) == 2):
            jump_row = (to_row - from_row) // 2 + from_row
            jump_col = (to_col - from_col) // 2 + from_col
            if self.game_board[jump_row][jump_col].lower() not in [player, '-']:
                return True, [jump_row, jump_col]
        return False, None

    def play(self, player, token_location, to_row, to_col, jump):
        """
        Move selected token to a particular square, then check to see if the game is over.
        """
        from_row = token_location[0]
        from_col = token_location[1]
        token_char = self.game_board[from_row][from_col]
        self.game_board[to_row][to_col] = token_char
        self.game_board[from_row][from_col] = '-'
        if (player == 'b' and to_row == 7) or (player == 'r' and to_row == 0):
            self.game_board[to_row][to_col] = token_char.upper()
        if jump:
            self.game_board[jump[0]][jump[1]] = '-'
            self.selected_token = [to_row, to_col]
            self.jumping = True
        else:
            self.selected_token = None
            self.next_turn()
        winner = self.check_winner()
        if winner is None:
            pygame.display.set_caption("%s's turn" % pawn[self.players[self.turn % 2]])
        elif winner == 'draw':
            pygame.display.set_caption("It's a stalemate! Click to start again")
            self.status = 'game over'
        else:
            pygame.display.set_caption("%s wins! Click to start again" % winner)
            self.status = 'game over'

    def next_turn(self):
        self.turn += 1
        pygame.display.set_caption("%s's turn" % pawn[self.players[self.turn % 2]])

    def check_winner(self):
        """
        check to see if someone won, or if it is a draw.
        """
        b = sum([row.count('b') + row.count('b') for row in self.game_board])
        if b == 0:
            return 'o'
        r = sum([row.count('r') + row.count('r') for row in self.game_board])
        if r == 0:
            return 'b'
        if b == 1 and r == 1:
            return 'draw'
        return None


def get_clicked_column(mouse_pos):
    x = mouse_pos[0]
    for i in range(1, 8):
        if x < (i * SQUARE_SIZE):
            return i - 1
    return 7


def get_clicked_row(mouse_pos):
    y = mouse_pos[1]
    for i in range(1, 8):
        if y < (i * SQUARE_SIZE):
            return i - 1
    return 7




