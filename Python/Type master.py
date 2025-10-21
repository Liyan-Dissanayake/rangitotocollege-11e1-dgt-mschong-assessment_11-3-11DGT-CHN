"""
Player types words as fast and accurately as possible within a time limit.

Displays WPM, accuracy, and allows restarting the game or quitting.
"""

import tkinter as tk
import random
import time

# Create the main application window
root = tk.Tk()
root.title("Typing Speed Test")
root.geometry("550x400")
root.resizable(False, False)
root.config(bg="#1e1e2e")

# List of words to type in the game
words_master = [
    "python", "keyboard", "speed", "challenge", "program", "window",
    "function", "variable", "random", "player", "typing", "testing",
    "accuracy", "loop", "game", "button", "logic", "winner", "input",
    "output", "developer", "computer", "syntax", "compile", "editor",
    "project", "error", "coding", "performance", "practice", "learn",
    "typewriter", "mechanical", "language", "debug", "structure",
    "indent", "runtime", "hardware", "software", "command", "processor",
    "virtual", "memory", "storage", "algorithm", "condition", "argument",
    "statement", "module"
]

# Variables to track game state
words_unused = words_master.copy()  # Words not yet typed
current_word = ""                   # Current word to type
start_time = None                    # Game start time
score = 0                            # Number of correct words
total_attempts = 0                   # Total words attempted
game_running = False                 # Game active flag
time_limit = 30                      # Duration of the game in seconds
times = []                           # Track time taken for each word
word_start_time = None               # Time when current word displayed

# Colors and fonts for UI elements
COLOR_BG = "#1e1e2e"
COLOR_FG = "#cdd6f4"
COLOR_ACCENT = "#89b4fa"
COLOR_GOOD = "#a6e3a1"
COLOR_BAD = "#f38ba8"

FONT_TITLE = ("Helvetica", 22, "bold")
FONT_TEXT = ("Helvetica", 16)
FONT_BUTTON = ("Helvetica", 12, "bold")


def start_game():
    """Reset game variables and start the typing session."""
    global score, total_attempts, game_running, start_time, word_start_time
    score = 0
    total_attempts = 0
    game_running = True
    start_time = time.time()
    word_start_time = time.time()

    result_label.config(text="")      # Clear previous results
    entry.config(state=tk.NORMAL)     # Enable input box
    entry.delete(0, tk.END)
    next_word()                       # Show the first word
    update_timer()                     # Start countdown timer


def next_word():
    """Pick the next word from the list and display it."""
    global current_word, words_unused
    if not words_unused:              # Refill list if all words used
        words_unused = words_master.copy()
        random.shuffle(words_unused)
    current_word = words_unused.pop()
    word_label.config(text=current_word)


def check_word(event=None):
    """Check player's typed word, update score, and display feedback."""
    global score, total_attempts, times, word_start_time
    if not game_running:
        return

    typed = entry.get().strip().lower()
    entry.delete(0, tk.END)
    total_attempts += 1

    end_time = time.time()
    time_taken = end_time - word_start_time
    times.append(time_taken)
    average_time = sum(times) / len(times)
    wpm = (score / sum(times)) * 60 if sum(times) > 0 else 0
    word_start_time = time.time()  # Reset start time for next word

    # Update score and feedback depending on correctness
    if typed == current_word:
        score += 1
        result_label.config(
            text=(f"Correct! ({time_taken:.2f}s) | Avg: {average_time:.2f}s | "
                  f"WPM: {wpm:.1f}"),
            fg=COLOR_GOOD
        )
    else:
        result_label.config(
            text=(f"Wrong! ({current_word}) | Avg: {average_time:.2f}s | "
                  f"WPM: {wpm:.1f}"),
            fg=COLOR_BAD
        )

    next_word()  # Move to the next word


def update_timer():
    """Update countdown timer and handle end-of-game logic."""
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
    root.after(1000, update_timer)  # Schedule next timer update


def reset_game():
    """Reset game state and start a new round."""
    global times
    times = []
    play_again_btn.pack_forget()
    start_game()


def quit_game():
    """Close the application window."""
    root.destroy()


# Create UI elements
title_label = tk.Label(root, text="Typing Speed Test", font=FONT_TITLE,
                       bg=COLOR_BG, fg=COLOR_ACCENT)
title_label.pack(pady=20)

timer_label = tk.Label(root, text=f"Time left: {time_limit}s", font=FONT_TEXT,
                       bg=COLOR_BG, fg=COLOR_FG)
timer_label.pack()

word_label = tk.Label(root, text="Press 'Start' to begin",
                      font=("Helvetica", 24, "bold"), bg=COLOR_BG,
                      fg=COLOR_ACCENT)
word_label.pack(pady=30)

# Entry box for typing
entry = tk.Entry(root, font=FONT_TEXT, justify="center", width=20,
                 bd=2, relief="groove", state=tk.DISABLED)
entry.pack(pady=10)
entry.bind("<Return>", check_word)  # Pressing Enter checks the word

# Label to show correctness and stats
result_label = tk.Label(root, text="", font=FONT_TEXT, bg=COLOR_BG,
                        fg=COLOR_FG)
result_label.pack(pady=15)

# Frame for control buttons
button_frame = tk.Frame(root, bg=COLOR_BG)
button_frame.pack(pady=10)

# Buttons to start, play again, or quit
start_btn = tk.Button(button_frame, text="Start", font=FONT_BUTTON,
                      bg=COLOR_ACCENT, fg=COLOR_BG, relief="flat",
                      width=12, command=start_game)
start_btn.grid(row=0, column=0, padx=10)

play_again_btn = tk.Button(button_frame, text="Play Again", font=FONT_BUTTON,
                           bg=COLOR_GOOD, fg=COLOR_BG, relief="flat",
                           width=12, command=reset_game)

quit_btn = tk.Button(button_frame, text="Quit", font=FONT_BUTTON,
                     bg=COLOR_BAD, fg=COLOR_BG, relief="flat", width=12,
                     command=quit_game)
quit_btn.grid(row=0, column=1, padx=10)

# Start the Tkinter main loop
root.mainloop()
