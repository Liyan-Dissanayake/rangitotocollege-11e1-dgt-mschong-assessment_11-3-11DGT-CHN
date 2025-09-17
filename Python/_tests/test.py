import tkinter as tk
from tkinter import messagebox
import math, random

CELL_SIZE = 30       # pixels per cell
FRAME_MS = 16        # ~60 FPS (16ms per frame)
SPEED_PX = 4         # pixels per frame (smoothness)

# Maze sizes by difficulty
diFFICULTY_SIZES = {
    "Easy": (9, 9),
    "Medium": (15, 15),
    "Hard": (21, 21)
}

class MazeGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Maze Game")
        self.resizable(False, False)

        # Top control bar
        ctrl = tk.Frame(self, pady=6)
        ctrl.pack(fill="x")

        tk.Label(ctrl, text="Select Difficulty:").pack(side="left", padx=(6,4))
        self.diff_var = tk.StringVar(value="Easy")
        tk.OptionMenu(ctrl, self.diff_var, *diFFICULTY_SIZES.keys()).pack(side="left")

        tk.Button(ctrl, text="Start", command=self.start_game).pack(side="left", padx=8)
        tk.Button(ctrl, text="Reset", command=self.reset_game).pack(side="left")

        # Status / instructions
        self.status = tk.Label(self, text="Use arrow keys to move. Reach the green exit.")
        self.status.pack(fill="x")

        # Canvas placeholder (created on start so size matches maze)
        self.canvas = tk.Canvas(self, bg="#eeeeee")
        self.canvas.pack()

        # State
        self.maze = None
        self.rows = self.cols = 0
        self.player_id = None
        self.exit_cell = None

        # Movement state
        self.grid_x = self.grid_y = 0   # integer cell coordinates
        self.px = self.py = 0.0         # pixel coordinates (center of player)
        self.target_px = self.target_py = None
        self.vx = self.vy = 0.0
        self.moving = False
        self.dir_input = None           # current key held: 'Left','Right','Up','Down'
        self.running = False

        # Bind key events to the whole app
        self.bind_all('<KeyPress>', self.on_key_press)
        self.bind_all('<KeyRelease>', self.on_key_release)

    # --- game setup / draw ---
    def start_game(self):
        diff = self.diff_var.get()
        self.rows, self.cols = diFFICULTY_SIZES[diff]
        self.maze = self.generate_maze(self.rows, self.cols)

        width = self.cols * CELL_SIZE
        height = self.rows * CELL_SIZE
        self.canvas.config(width=width, height=height)

        self.draw_maze()
        self.place_start_and_exit()

        self.running = True
        self.after(FRAME_MS, self.game_loop)
        self.status.config(text="Use arrow keys (hold to keep moving). Reach the green exit.")

    def reset_game(self):
        # Clear canvas and reset movement state
        self.canvas.delete('all')
        self.player_id = None
        self.moving = False
        self.dir_input = None
        self.running = False
        self.status.config(text="Use arrow keys to move. Select difficulty and press Start.")

    # Maze generator (recursive backtracker = perfect maze)
    def generate_maze(self, rows, cols):
        maze = [[1 for _ in range(cols)] for _ in range(rows)]

        def carve(r, c):
            dirs = [(0,1),(1,0),(-1,0),(0,-1)]
            random.shuffle(dirs)
            for dr, dc in dirs:
                nr, nc = r+dr*2, c+dc*2
                if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 1:
                    maze[r+dr][c+dc] = 0
                    maze[nr][nc] = 0
                    carve(nr, nc)

        # Start from (1,1)
        maze[1][1] = 0
        carve(1,1)
        return maze

    def draw_maze(self):
        self.canvas.delete('all')
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                if self.maze[r][c] == 1:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='black', width=0)
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='#ffffff', width=0)

    def place_start_and_exit(self):
        # start: top-left open cell, exit: bottom-right open cell
        self.grid_x, self.grid_y = 1, 1
        ex, ey = self.cols-2, self.rows-2

        # draw exit
        ex1 = ex * CELL_SIZE
        ey1 = ey * CELL_SIZE
        self.canvas.create_rectangle(ex1+6, ey1+6, ex1+CELL_SIZE-6, ey1+CELL_SIZE-6, fill='green', width=0, tags='exit')
        self.exit_cell = (ex, ey)

        # create player
        r = CELL_SIZE // 2 - 6
        px = self.grid_x * CELL_SIZE + CELL_SIZE//2
        py = self.grid_y * CELL_SIZE + CELL_SIZE//2
        self.px, self.py = float(px), float(py)
        self.player_id = self.canvas.create_oval(px-r, py-r, px+r, py+r, fill='red', width=0)

    # --- input handling ---
    def on_key_press(self, event):
        if not self.running:
            return
        key = event.keysym
        if key in ('Left','Right','Up','Down'):
            self.dir_input = key
            if not self.moving:
                self.try_start_move()

    def on_key_release(self, event):
        if event.keysym == self.dir_input:
            self.dir_input = None

    # --- movement ---
    def try_start_move(self):
        if self.moving or not self.dir_input:
            return
        dx = dy = 0
        if self.dir_input == 'Left': dx = -1
        elif self.dir_input == 'Right': dx = 1
        elif self.dir_input == 'Up': dy = -1
        elif self.dir_input == 'Down': dy = 1

        nx = self.grid_x + dx
        ny = self.grid_y + dy
        if self.can_move(nx, ny):
            self.target_px = nx * CELL_SIZE + CELL_SIZE//2
            self.target_py = ny * CELL_SIZE + CELL_SIZE//2
            dist = math.hypot(self.target_px - self.px, self.target_py - self.py)
            self.vx = (self.target_px - self.px) / dist * SPEED_PX
            self.vy = (self.target_py - self.py) / dist * SPEED_PX
            self.moving = True
            self.target_cell = (nx, ny)

    def can_move(self, x, y):
        if x < 0 or y < 0 or x >= self.cols or y >= self.rows:
            return False
        return self.maze[y][x] == 0

    # --- game loop ---
    def game_loop(self):
        if not self.running:
            return

        if self.moving:
            prev_px, prev_py = self.px, self.py
            self.px += self.vx
            self.py += self.vy

            reached_x = (self.vx >= 0 and self.px >= self.target_px) or (self.vx <= 0 and self.px <= self.target_px)
            reached_y = (self.vy >= 0 and self.py >= self.target_py) or (self.vy <= 0 and self.py <= self.target_py)

            if reached_x and reached_y:
                self.px, self.py = float(self.target_px), float(self.target_py)
                self.canvas.move(self.player_id, self.px - prev_px, self.py - prev_py)

                self.grid_x, self.grid_y = self.target_cell
                self.moving = False
                self.vx = self.vy = 0.0

                if (self.grid_x, self.grid_y) == self.exit_cell:
                    self.running = False
                    messagebox.showinfo("You Win!", "You reached the exit. Well done!")
                    self.status.config(text="You won! Press Reset to play again.")
                    return

                if self.dir_input:
                    self.try_start_move()
            else:
                self.canvas.move(self.player_id, self.px - prev_px, self.py - prev_py)
        else:
            if self.dir_input:
                self.try_start_move()

        self.after(FRAME_MS, self.game_loop)


if __name__ == '__main__':
    app = MazeGame()
    app.mainloop()