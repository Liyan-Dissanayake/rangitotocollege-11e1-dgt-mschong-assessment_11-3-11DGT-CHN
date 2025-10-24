"""A Tkinter game where the player guesses a number between 1 and 100."""

import tkinter as tk
import random

root = tk.Tk()
root.title("Number Guessing Game")
root.geometry("600x650")
root.resizable(True, True)
root.config(bg="#2e3440")

# Colors and fonts
COLOR_BG = "#2e3440"
COLOR_FG = "#eceff4"
COLOR_ACCENT = "#88c0d0"
COLOR_SUCCESS = "#a3be8c"
COLOR_ERROR = "#bf616a"
FONT_TITLE = ("Helvetica", 22, "bold")
FONT_TEXT = ("Helvetica", 16)
FONT_BUTTON = ("Helvetica", 12, "bold")

# Game variables
secret_number = random.randint(1, 100)
attempts = 0
game_over = False

def check_guess(event=None):
    """Validate and check player's guess, update history and feedback."""
    global attempts, game_over
    if game_over:
        return

    guess_str = guess_entry.get().strip()
    if not guess_str.isdigit():
        result_label.config(text="Enter a valid number!", fg=COLOR_ERROR)
        return

    guess = int(guess_str)
    if not 1 <= guess <= 100:
        result_label.config(text="Number must be 1–100!", fg=COLOR_ERROR)
        return

    attempts += 1
    if guess < secret_number:
        outcome = "Too low"
        result_label.config(text="Too low! Try again.", fg=COLOR_ACCENT)
        flash_result("#81a1c1")
    elif guess > secret_number:
        outcome = "Too high"
        result_label.config(text="Too high! Try again.", fg=COLOR_ACCENT)
        flash_result("#bf616a")
    else:
        outcome = "Correct"
        result_label.config(
            text=f"Correct! The number was {secret_number}. "
                 f"You guessed it in {attempts} tries.",
            fg=COLOR_SUCCESS
        )
        flash_result("#a3be8c", correct=True)
        end_game()

    history_box.insert(tk.END, f"{guess} → {outcome}")
    guess_entry.delete(0, tk.END)

def flash_result(color, correct=False):
    """Flash the result label color; simple fade for correct guess."""
    result_label.config(fg=color)
    if correct:
        def fade(step=0):
            shades = ["#a3be8c", "#b5d19c", "#c8e4ac", "#b5d19c", 
                      "#a3be8c"]
            if step < len(shades):
                result_label.config(fg=shades[step])
                result_label.after(100, lambda: fade(step + 1))
            else:
                result_label.config(fg=COLOR_FG)
        fade()
    else:
        result_label.after(400, lambda: result_label.config(fg=COLOR_FG))

def end_game():
    """Disable input and show the Play Again button."""
    global game_over
    game_over = True
    guess_entry.config(state=tk.DISABLED)
    check_btn.config(state=tk.DISABLED)
    play_again_btn.pack()

def reset_game():
    """Reset game for a new round."""
    global secret_number, attempts, game_over
    secret_number = random.randint(1, 100)
    attempts = 0
    game_over = False
    guess_entry.config(state=tk.NORMAL)
    check_btn.config(state=tk.NORMAL)
    result_label.config(text="Guess a number between 1 and 100", fg=COLOR_FG)
    play_again_btn.pack_forget()
    guess_entry.delete(0, tk.END)
    guess_entry.focus()
    history_box.delete(0, tk.END)

# UI setup
title_label = tk.Label(root, text="Number Guessing Game", font=FONT_TITLE,
                       bg=COLOR_BG, fg=COLOR_ACCENT)
title_label.pack(pady=30)

instruction_label = tk.Label(root, text="Guess a number between 1 and 100",
                             font=FONT_TEXT, bg=COLOR_BG, fg=COLOR_FG)
instruction_label.pack(pady=10)

guess_entry = tk.Entry(root, font=FONT_TEXT, justify="center", width=10,
                       bd=2, relief="groove")
guess_entry.pack(pady=10)
guess_entry.focus()
guess_entry.bind("<Return>", check_guess)

check_btn = tk.Button(root, text="Check Guess", font=FONT_BUTTON,
                      bg=COLOR_ACCENT, fg=COLOR_BG, relief="flat",
                      command=check_guess)
check_btn.pack(pady=5)

result_label = tk.Label(root, text="", font=FONT_TEXT, bg=COLOR_BG,
                        fg=COLOR_FG)
result_label.pack(pady=15)

# History box with improved visuals
history_frame = tk.Frame(root, bg=COLOR_BG, bd=2, relief="sunken")
history_frame.pack(pady=10)
history_scroll = tk.Scrollbar(history_frame, orient=tk.VERTICAL)
history_box = tk.Listbox(history_frame, width=40, height=10, font=("Helvetica",
                                                                   12),
                         bg="#3b4252", fg="#eceff4", 
                         selectbackground="#88c0d0",
                         yscrollcommand=history_scroll.set)
history_box.pack(side=tk.LEFT, fill=tk.BOTH)
history_scroll.config(command=history_box.yview)
history_scroll.pack(side=tk.RIGHT, fill=tk.Y)

play_again_btn = tk.Button(root, text="Play Again", font=FONT_BUTTON,
                           bg=COLOR_SUCCESS, fg=COLOR_BG, relief="flat",
                           command=reset_game)
play_again_btn.pack_forget()

root.mainloop()
