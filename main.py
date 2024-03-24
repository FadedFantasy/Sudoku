import numpy as np
import random


class Board:
    def __init__(self, game_board):
        self.game_board = np.array(game_board)

    def get_square(self, row, col):
        if row <= 2:
            if col <= 2:
                # square 1
                square = self.game_board[0:3, 0:3]
            elif col <= 5:
                # square 2
                square = self.game_board[0:3, 3:6]
            else:
                # square 3
                square = self.game_board[0:3, 6:9]
        elif row <= 5:
            if col <= 2:
                square = self.game_board[3:6, 0:3]
            elif col <= 5:
                square = self.game_board[3:6, 3:6]
            else:
                square = self.game_board[3:6, 6:9]
        else:
            if col <= 2:
                square = self.game_board[6:9, 0:3]
            elif col <= 5:
                square = self.game_board[6:9, 3:6]
            else:
                square = self.game_board[6:9, 6:9]
        return square

    def find_empty(self):
        for row in range(self.game_board.shape[0]):
            for col in range(self.game_board.shape[1]):
                if self.game_board[row][col] == 0:
                    return row, col
        return None

    def get_possible_vals(self, row, col):
        # exclude row values
        exclude_val = set(self.game_board[row, :])
        # add col values
        exclude_val = set(exclude_val.union(set(self.game_board[:, col])))
        # add values of the square
        square = self.get_square(row, col)
        exclude_val = set(exclude_val.union(set(square.flatten())))

        possible_vals = list(set([i for i in range(0, 10)]) - exclude_val)
        random.shuffle(possible_vals)
        if possible_vals:
            success = True
        else:
            success = False

        return possible_vals, success

        # game_board[row][col] = random.choice(list(set([i for i in range(0, 10)]) - exclude_val))

    def solve(self):
        empty_cell = self.find_empty()
        if empty_cell:
            row, col = empty_cell
        else:
            return True, self.game_board

        possible_vals, success = self.get_possible_vals(row, col)
        if success:
            for possible_val in possible_vals:
                self.game_board[row][col] = possible_val

                if self.solve():
                    return True

                self.game_board[row][col] = 0

        return False

    def print_board(self):
        for row in range(len(self.game_board)):
            if row % 3 == 0 and row != 0:
                print("- - - - - - - - - - - - - ")
            for col in range(len(self.game_board[0])):
                if col % 3 == 0 and col != 0:
                    print(" | ", end="")
                if col == 8:
                    print(self.game_board[row][col])
                else:
                    print(str(self.game_board[row][col]) + " ", end="")


def main():
    mode = "gen"  # solve or gen
    gen_difficulty = 2
    game_board_solve = [[9, 0, 0, 0, 0, 6, 0, 0, 0],
                        [1, 0, 0, 0, 0, 0, 0, 3, 0],
                        [0, 0, 2, 9, 7, 0, 8, 0, 0],
                        [2, 0, 0, 6, 4, 0, 0, 0, 1],
                        [0, 0, 0, 0, 0, 5, 4, 0, 0],
                        [0, 0, 6, 0, 0, 8, 0, 0, 0],
                        [0, 7, 0, 0, 0, 0, 0, 0, 8],
                        [0, 0, 0, 0, 5, 0, 0, 0, 0],
                        [0, 0, 9, 4, 2, 0, 7, 0, 0]
                        ]
    game_board_gen = [[0 for x in range(9)] for y in range(9)]

    if mode == "solve":
        board = Board(game_board_solve)
        board.print_board()
        board.solve()
        print("___________________")
        board.print_board()

    elif mode == "gen":
        board = Board(game_board_gen)
        board.solve()
        random_indices = np.random.choice(81, replace=False, size=20*gen_difficulty)
        board.game_board.flat[random_indices] = 0
        board.print_board()


if __name__ == "__main__":
    main()
