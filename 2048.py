import random
import os

class Game2048:
    def __init__(self):
        self.grid = [[0] * 4 for _ in range(4)]
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        empty_tiles = [(r, c) for r in range(4) for c in range(4) if self.grid[r][c] == 0]
        if empty_tiles:
            r, c = random.choice(empty_tiles)
            self.grid[r][c] = 2 if random.random() < 0.9 else 4

    def move_left(self):
        moved = False
        for r in range(4):
            original = self.grid[r]
            merged, new_row = self.merge(self.grid[r])
            if new_row != original:
                moved = True
            self.grid[r] = new_row
        return moved

    def move_right(self):
        self.reverse_grid()
        moved = self.move_left()
        self.reverse_grid()
        return moved

    def move_up(self):
        self.transpose_grid()
        moved = self.move_left()
        self.transpose_grid()
        return moved

    def move_down(self):
        self.transpose_grid()
        moved = self.move_right()
        self.transpose_grid()
        return moved

    def merge(self, row):
        non_zero = [num for num in row if num != 0]
        merged = []
        skip = False
        for i in range(len(non_zero)):
            if skip:
                skip = False
                continue
            if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
                merged.append(non_zero[i] * 2)
                skip = True
            else:
                merged.append(non_zero[i])
        merged += [0] * (4 - len(merged))
        return merged != row, merged

    def reverse_grid(self):
        for r in range(4):
            self.grid[r] = self.grid[r][::-1]

    def transpose_grid(self):
        self.grid = [list(row) for row in zip(*self.grid)]

    def check_game_over(self):
        if any(0 in row for row in self.grid):
            return False
        for r in range(4):
            for c in range(4):
                if c + 1 < 4 and self.grid[r][c] == self.grid[r][c + 1]:
                    return False
                if r + 1 < 4 and self.grid[r][c] == self.grid[r + 1][c]:
                    return False
        return True

    def display_grid(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for row in self.grid:
            print(f"| {' | '.join(str(num).center(4) if num != 0 else ' '.center(4) for num in row)} |")
        print("\nUse W (up), A (left), S (down), D (right) to move, or Q to quit.")

    def play(self):
        while True:
            self.display_grid()
            if self.check_game_over():
                print("Game Over! No more moves.")
                break
            move = input("Move: ").strip().lower()
            if move == 'q':
                print("Game Exited!")
                break
            elif move == 'a':
                moved = self.move_left()
            elif move == 'd':
                moved = self.move_right()
            elif move == 'w':
                moved = self.move_up()
            elif move == 's':
                moved = self.move_down()
            else:
                print("Invalid input, please use W/A/S/D or Q to quit.")
                continue

            if moved:
                self.add_random_tile()

if __name__ == "__main__":
    game = Game2048()
    game.play()
