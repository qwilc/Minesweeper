import copy
import random
from datetime import datetime
from states import State
from game_modes import Mode

LOSE_MESSAGE = "Lose"
WIN_MESSAGE = "Win!"
OFFSETS = [-1, 0, 1]  # for performing operations on all squares surrounding a square


class Square:
    def __init__(self, is_mine=False, state=State.HIDDEN):
        self.mine_count = 0
        self.state = state
        self.is_mine = is_mine

    def set_mine_count(self, count):
        self.mine_count = count

    def increment(self):
        self.mine_count += 1

    def place_mine(self):
        self.is_mine = True

    def flag(self):
        self.state = State.FLAGGED

    def unflag(self):
        self.state = State.HIDDEN

    def dig(self):
        self.state = State.REVEALED

    def explode(self):
        self.state = State.EXPLODED

    def reveal(self):
        if self.state == State.REVEALED or self.state == State.EXPLODED:
            pass
        elif self.is_mine:
            self.state = State.MINE
        else:
            self.state = State.REVEALED

    def __str__(self):
        if self.state == State.REVEALED:
            return str(self.mine_count)
        return str(self.state)

    def __repr__(self):
        if self.is_mine:
            return self.state.__str__()
        else:
            return str(self.mine_count)


class Board:
    def __init__(self, width=20, height=20, num_mines=15):
        self.start_square = None
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.instantiate_board()

    def instantiate_board(self):
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(Square())
            self.board.append(row)

    def place_mines(self):
        positions = self.generate_mine_positions()
        for pos in positions:
            self.place_mine(pos[0], pos[1])

    def place_mine(self, row, col):
        self.board[row][col].place_mine()
        [self.is_valid_coord(row + i, col + j) and self.board[row + i][col + j].increment() for i in OFFSETS for j in
         OFFSETS]

    def generate_mine_positions(self):
        positions = []
        i = 0
        while i < self.num_mines:
            row = random.randrange(self.height)
            col = random.randrange(self.width)
            if not (row, col) in positions and self[row][col] is not self.start_square:
                positions.append((row, col))
                i += 1
        return positions

    def reveal_all(self):
        for row in self.board:
            for square in row:
                square.reveal()

    def is_valid_coord(self, row, col):
        return 0 <= row < self.height and 0 <= col < self.width

    def __getitem__(self, item):  # TODO: Is this acceptable or should I have a custom get function?
        return self.board.__getitem__(item)

    def __str__(self):
        string = ""
        for row in self.board:
            for sq in row:
                string += str(sq) + " "
            string += "\n"
        return string


class Game:
    def __init__(self, mode=Mode.EASY):
        width = mode["width"]
        height = mode["height"]
        num_mines = mode["mines"]

        self.board = Board(width, height, num_mines)
        self.num_mines_left = num_mines
        self.num_safe_left = width * height - num_mines
        self.is_started = False
        self.start_time = None
        self.starting_square = None
        self.is_action_dig = True  # True: dig, False: flag
        self.is_game_over = False
        self.changed_coords = []

    def peek(self):
        test_board = copy.deepcopy(self.board)
        test_board.reveal_all()
        print(test_board)

    def start(self, row, col):
        self.board.start_square = self.board[row][col]
        self.board.place_mines()
        self.start_time = datetime.now()
        self.is_started = True

    def get_elapsed_time(self):
        if self.start_time:
            elapsed_time = datetime.now() - self.start_time
            return str(elapsed_time)[:-7]
        else:
            return "0:00:00"

    def win_game(self):
        self.final_message = WIN_MESSAGE
        self.is_game_over = True
        self.board.reveal_all()

    def lose_game(self):
        self.final_message = LOSE_MESSAGE
        self.is_game_over = True
        self.board.reveal_all()

    def final_reveal(self):
        self.board.reveal_all()
        return str(self.board)

    # TODO pass a parameter instead of storing is_action_dig and break into separate functions
    def perform_action_on(self, row, col):
        square = self.board[row][col]
        change_made = True
        if (square.state != State.HIDDEN and self.is_action_dig) or (
                square.state == State.REVEALED and not self.is_action_dig):
            change_made = False
        elif self.is_action_dig:
            self.dig(row, col)
        else:
            self.mark(row, col)

        if change_made:
            self.changed_coords.append((row, col))

    def dig(self, row, col):
        square = self.board[row][col]
        if square.state != State.HIDDEN:
            change_made = False
        elif square.is_mine:
            square.explode()
            self.lose_game()
        else:
            square.dig()
            self.num_safe_left -= 1
            if self.num_safe_left == 0:
                self.win_game()
                return

            if square.mine_count == 0:
                for i in OFFSETS:
                    for j in OFFSETS:
                        if self.board.is_valid_coord(row + i, col + j):
                            self.perform_action_on(row + i, col + j)
                # [self.board.is_valid_coord(row + i, col + j) and self.perform_action_on(row + i, col + j) for i in OFFSETS for j in OFFSETS]

    def mark(self, row, col):
        square = self.board[row][col]
        if square.state == State.FLAGGED:
            square.unflag()
            self.num_mines_left += 1
        elif square.state == State.HIDDEN:
            square.flag()
            self.num_mines_left -= 1
        else:  # square.state == State.REVEALED
            change_made = False
