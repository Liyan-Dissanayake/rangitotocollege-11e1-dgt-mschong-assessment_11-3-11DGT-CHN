import tkinter as tk
import random
import time

# --- Setup window ---
root = tk.Tk()
root.title("Typing Speed Test")
root.geometry("550x400")
root.resizable(False, False)
root.config(bg="#1e1e2e")

# --- Word list (Version 1) ---
words_master = [
    "python", "keyboard", "speed", "challenge", "program", "window",
    "function", "variable", "random", "player", "typing", "testing",
    "accuracy", "loop", "game", "button", "logic", "winner", "input", "output",
    "developer", "computer", "syntax", "compile", "editor", "project",
    "error", "coding", "performance", "practice", "learn", "typewriter",
    "mechanical", "language", "debug", "structure", "indent", "runtime",
    "hardware", "software", "command", "processor", "virtual", "memory",
    "storage", "algorithm", "condition", "argument", "statement", "module"
]

words_unused = words_master.copy()  # Tracks unused words
current_word = ""
start_time = None
score = 0
total_attempts = 0
game_running = False
time_limit = 30  # seconds

# --- Colors and fonts ---
COLOR_BG = "#1e1e2e"
COLOR_FG = "#cdd6f4"
COLOR_ACCENT = "#89b4fa"
COLOR_GOOD = "#a6e3a1"
COLOR_BAD = "#f38ba8"
FONT_TITLE = ("Helvetica", 22, "bold")
FONT_TEXT = ("Helvetica", 16)
FONT_BUTTON = ("Helvetica", 12, "bold")

# --- Functions ---
def start_game():
    global score, total_attempts, game_running, start_time
    score = 0
    total_attempts = 0
    game_running = True
    start_time = time.time()

    result_label.config(text="")
    entry.config(state=tk.NORMAL)
    entry.delete(0, tk.END)
    next_word()
    update_timer()

def next_word():
    global current_word, words_unused
    if not words_unused:  # Reset list if all words have been used
        words_unused = words_master.copy()
        random.shuffle(words_unused)  # Shuffle list for better randomization
    current_word = words_unused.pop()  # Pop instead of choice to prevent repetition
    word_label.config(text=current_word)

def check_word(event=None):
    global score, total_attempts
    if not game_running:
        return

    typed = entry.get().strip().lower()
    entry.delete(0, tk.END)
    total_attempts += 1

    if typed == current_word:
        score += 1
        result_label.config(text="Correct!", fg=COLOR_GOOD)
    else:
        result_label.config(text=f"Wrong! ({current_word})", fg=COLOR_BAD)

    next_word()

def update_timer():
    global game_running
    if not game_running:
        return

    elapsed = int(time.time() - start_time)
    remaining = time_limit - elapsed

    if remaining <= 0:
        game_running = False
        entry.config(state=tk.DISABLED)
        word_label.config(text="Time's up!")
        wpm = (score / time_limit) * 60
        accuracy = (score / total_attempts * 100) if total_attempts > 0 else 0
        result_label.config(
            text=f"WPM: {wpm:.1f} | Accuracy: {accuracy:.1f}%",
            fg=COLOR_ACCENT
        )
        play_again_btn.pack(pady=10)
        return

    timer_label.config(text=f"Time left: {remaining}s")
    root.after(1000, update_timer)

def reset_game():
    play_again_btn.pack_forget()
    start_game()

def quit_game():
    root.destroy()

# --- UI Layout ---
title_label = tk.Label(root, text="Typing Speed Test", font=FONT_TITLE, bg=COLOR_BG, fg=COLOR_ACCENT)
title_label.pack(pady=20)

timer_label = tk.Label(root, text=f"Time left: {time_limit}s", font=FONT_TEXT, bg=COLOR_BG, fg=COLOR_FG)
timer_label.pack()

word_label = tk.Label(root, text="Press 'Start' to begin", font=("Helvetica", 24, "bold"), bg=COLOR_BG, fg=COLOR_ACCENT)
word_label.pack(pady=30)
        
entry = tk.Entry(root, font=FONT_TEXT, justify="center", width=20, bd=2, relief="groove", state=tk.DISABLED)
entry.pack(pady=10)
entry.bind("<Return>", check_word)

result_label = tk.Label(root, text="", font=FONT_TEXT, bg=COLOR_BG, fg=COLOR_FG)
result_label.pack(pady=15)

button_frame = tk.Frame(root, bg=COLOR_BG)
button_frame.pack(pady=10)

start_btn = tk.Button(button_frame, text="Start", font=FONT_BUTTON, bg=COLOR_ACCENT, fg=COLOR_BG, relief="flat", width=12, command=start_game)
start_btn.grid(row=0, column=0, padx=10)

play_again_btn = tk.Button(button_frame, text="Play Again", font=FONT_BUTTON, bg="#a6e3a1", fg=COLOR_BG, relief="flat", width=12, command=reset_game)
quit_btn = tk.Button(button_frame, text="Quit", font=FONT_BUTTON, bg=COLOR_BAD, fg=COLOR_BG, relief="flat", width=12, command=quit_game)
quit_btn.grid(row=0, column=1, padx=10)

# --- Run app ---
root.mainloop()
