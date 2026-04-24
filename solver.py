class NQueensSolver:
    def __init__(self, n):
        self.n = n
        self.board = [-1] * n   # board[row] = column
        self.solutions = []     # store all solutions

    def is_safe(self, row, col):
        for i in range(row):
            # same column OR same diagonal
            if self.board[i] == col or abs(self.board[i] - col) == abs(i - row):
                return False
        return True

    def solve(self, row=0):
        # if all queens are placed
        if row == self.n:
            # IMPORTANT: save a COPY of the board
            self.solutions.append(self.board.copy())
            return

        for col in range(self.n):
            if self.is_safe(row, col):
                self.board[row] = col

                # move to next row
                self.solve(row + 1)

                # backtrack
                self.board[row] = -1
    
    def solve_with_steps(self, row=0):
        if row == self.n:
            yield ("solution", self.board.copy())
            return
    
        for col in range(self.n):
            if self.is_safe(row, col):
                self.board[row] = col
                yield ("place", row, col)

                yield from self.solve_with_steps(row + 1)

                yield ("remove", row, col)
                self.board[row] = -1