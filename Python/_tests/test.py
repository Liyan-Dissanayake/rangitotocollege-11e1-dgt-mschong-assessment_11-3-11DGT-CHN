import tkinter as tk
import random

# --- Game settings ---
SIZE = 4   # 4x4 grid
CELL_SIZE = 100
FONT = ("Arial", 24, "bold")

# --- Tkinter window ---
root = tk.Tk()
root.title("2048 (Tkinter)")

frame = tk.Frame(root, bg="lightgrey")
frame.pack()

# Canvas for grid
canvas = tk.Canvas(frame, width=SIZE*CELL_SIZE, height=SIZE*CELL_SIZE, bg="lightgrey")
canvas.grid(row=1, column=0, columnspan=2)

# --- Score display ---
score = 0
score_label = tk.Label(frame, text=f"Score: {score}", font=("Arial", 16, "bold"), bg="lightgrey")
score_label.grid(row=0, column=0, sticky="w", padx=10)

# Restart button
def restart():
    global grid, score
    score = 0
    score_label.config(text=f"Score: {score}")
    grid = [[0]*SIZE for _ in range(SIZE)]
    add_new_tile()
    add_new_tile()
    draw_grid()

restart_btn = tk.Button(frame, text="Restart", command=restart, font=("Arial", 12))
restart_btn.grid(row=0, column=1, sticky="e", padx=10)

# --- Game state ---
grid = [[0]*SIZE for _ in range(SIZE)]

# --- Colors ---
COLORS = {
    0: ("#cdc1b4", "black"),
    2: ("#eee4da", "black"),
    4: ("#ede0c8", "black"),
    8: ("#f2b179", "white"),
    16: ("#f59563", "white"),
    32: ("#f67c5f", "white"),
    64: ("#f65e3b", "white"),
    128: ("#edcf72", "black"),
    256: ("#edcc61", "black"),
    512: ("#edc850", "black"),
    1024: ("#edc53f", "black"),
    2048: ("#edc22e", "black")
}

# --- Helpers ---
def add_new_tile():
    empty = [(r, c) for r in range(SIZE) for c in range(SIZE) if grid[r][c] == 0]
    if empty:
        r, c = random.choice(empty)
        grid[r][c] = random.choice([2, 4])

def draw_grid():
    canvas.delete("all")
    for r in range(SIZE):
        for c in range(SIZE):
            value = grid[r][c]
            bg, fg = COLORS.get(value, ("#3c3a32", "white"))
            x1, y1 = c*CELL_SIZE, r*CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
            canvas.create_rectangle(x1, y1, x2, y2, fill=bg, outline="black")
            if value != 0:
                canvas.create_text((x1+x2)//2, (y1+y2)//2, text=str(value), font=FONT, fill=fg)

def compress(row):
    new_row = [num for num in row if num != 0]
    new_row += [0] * (SIZE - len(new_row))
    return new_row

def merge(row):
    global score
    for i in range(SIZE - 1):
        if row[i] != 0 and row[i] == row[i+1]:
            row[i] *= 2
            score += row[i]
            row[i+1] = 0
    score_label.config(text=f"Score: {score}")
    return row

def move_left():
    moved = False
    for r in range(SIZE):
        new_row = compress(grid[r])
        new_row = merge(new_row)
        new_row = compress(new_row)
        if grid[r] != new_row:
            moved = True
        grid[r] = new_row
    if moved:
        add_new_tile()
    draw_grid()
    check_state()

def move_right():
    for r in range(SIZE):
        grid[r].reverse()
    move_left()
    for r in range(SIZE):
        grid[r].reverse()

def move_up():
    global grid
    grid = list(map(list, zip(*grid)))
    move_left()
    grid = list(map(list, zip(*grid)))

def move_down():
    global grid
    grid = list(map(list, zip(*grid)))
    move_right()
    grid = list(map(list, zip(*grid)))

def check_state():
    # Win check
    for row in grid:
        if 2048 in row:
            canvas.create_text(SIZE*CELL_SIZE//2, SIZE*CELL_SIZE//2,
                               text="YOU WIN 🎉", font=("Arial", 32, "bold"), fill="green")
            return

    # Continue if possible
    for r in range(SIZE):
        for c in range(SIZE):
            if grid[r][c] == 0:
                return
            if c < SIZE-1 and grid[r][c] == grid[r][c+1]:
                return
            if r < SIZE-1 and grid[r][c] == grid[r+1][c]:
                return

    # No moves left → Game Over
    canvas.create_text(SIZE*CELL_SIZE//2, SIZE*CELL_SIZE//2,
                       text="GAME OVER 💀", font=("Arial", 32, "bold"), fill="red")

# --- Key bindings ---
def key_handler(event):
    if event.keysym == "Left":
        move_left()
    elif event.keysym == "Right":
        move_right()
    elif event.keysym == "Up":
        move_up()
    elif event.keysym == "Down":
        move_down()

root.bind("<Key>", key_handler)

# --- Start game ---
restart()

root.mainloop()
