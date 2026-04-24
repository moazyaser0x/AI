import tkinter as tk
from tkinter import messagebox
from solver import NQueensSolver


class App:
    def __init__(self, root):
        self.root = root

        # ===== Top Frame =====
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10)

        tk.Label(top_frame, text="N-Queens Solver", font=("Arial", 16, "bold")).pack()

        tk.Label(top_frame, text="Enter N:").pack(side=tk.LEFT)

        self.entry = tk.Entry(top_frame, width=5)
        self.entry.pack(side=tk.LEFT, padx=5)

        tk.Button(top_frame, text="Solve", command=self.solve).pack(side=tk.LEFT)

        # ===== Canvas (Board) =====
        self.canvas = tk.Canvas(root, width=500, height=500)
        self.canvas.pack()

        # ===== Bottom Frame =====
        bottom_frame = tk.Frame(root)
        bottom_frame.pack(pady=10)

        self.prev_btn = tk.Button(bottom_frame, text="Previous", command=self.prev_solution)
        self.prev_btn.pack(side=tk.LEFT, padx=5)

        self.next_btn = tk.Button(bottom_frame, text="Next", command=self.next_solution)
        self.next_btn.pack(side=tk.LEFT, padx=5)

        self.label = tk.Label(bottom_frame, text="Solution: 0 / 0")
        self.label.pack(side=tk.LEFT, padx=10)

        # ===== Data =====
        self.solutions = []
        self.current_index = 0
        self.n = 0

        # ===== Animation CheckBox =====
        self.animate_var = tk.BooleanVar()
        tk.Checkbutton(root, text="Show Solving Process", variable=self.animate_var).pack()

    # =========================
    # Solve Button
    # =========================
    def solve(self):
        try:
            self.n = int(self.entry.get())
        except:
            messagebox.showerror("Error", "Enter a valid number")
            return

        solver = NQueensSolver(self.n)

        if self.animate_var.get():
            self.board_state = [-1] * self.n
            self.generator = solver.solve_with_steps()
            self.animate()
        else:
            solver.solve()
            self.solutions = solver.solutions

            if not self.solutions:
                messagebox.showinfo("Result", "No solution found")
                return

            self.current_index = 0
            self.update_board()
    
    # =========================
    # Animation
    # =========================
    def animate(self):
        try:
            step = next(self.generator)

            if step[0] == "place":
                _, row, col = step
                self.board_state[row] = col

            elif step[0] == "remove":
                _, row, col = step
                self.board_state[row] = -1

            elif step[0] == "solution":
                pass  # optional: store it

            self.draw_board(self.board_state)

            self.root.after(1000, self.animate)  # MEDIUM speed

        except StopIteration:
            return
    
    # =========================
    # Highlight Conflicts
    # =========================
    def is_attacked(self, board, row, col):
        for r in range(len(board)):
            c = board[r]
            if c == -1:
               continue

            if r == row or c == col or abs(r - row) == abs(c - col):
               return True

        return False

    # =========================
    # Draw Board
    # =========================
    def draw_board(self, board):
        self.canvas.delete("all")

        size = 500 // self.n

        for row in range(self.n):
            for col in range(self.n):
                x1 = col * size
                y1 = row * size
                x2 = x1 + size
                y2 = y1 + size

                base_color = "#F0D9B5" if (row + col) % 2 == 0 else "#B58863"

                if board[row] == -1 and self.is_attacked(board, row, col):
                    color = "#FF0000"  # light red
                else:
                    color = base_color

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        for row in range(self.n):
            col = board[row]
            if col != -1:
                x = col * size + size // 2
                y = row * size + size // 2

                self.canvas.create_text( x, y, text="♛", font=("Arial", size // 2), fill="black")

    # =========================
    # Update Board + Label
    # =========================
    def update_board(self):
        board = self.solutions[self.current_index]
        self.draw_board(board)

        self.label.config(
            text=f"Solution: {self.current_index + 1} / {len(self.solutions)}"
        )

    # =========================
    # Navigation
    # =========================
    def next_solution(self):
        if not self.solutions:
            return

        self.current_index = (self.current_index + 1) % len(self.solutions)
        self.update_board()

    def prev_solution(self):
        if not self.solutions:
            return

        self.current_index = (self.current_index - 1) % len(self.solutions)
        self.update_board()


# ===== Run App =====
root = tk.Tk()
app = App(root)
root.mainloop()