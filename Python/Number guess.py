import tkinter as tk
import random

# Setup window
root = tk.Tk()
root.title("Number Guessing Game")
root.geometry("600x450")
root.resizable(False, False)
root.config(bg="#2e3440")

# Colors and Fonts
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

# Functions
def check_guess(event=None):
    """Check the user's guess against the secret number."""
    global attempts, game_over
    if game_over:
        return

    guess = guess_entry.get().strip()
    if not guess.isdigit():
        result_label.config(text="Please enter a valid number!", fg=COLOR_ERROR)
        return

    guess = int(guess)
    attempts += 1

    if guess < secret_number:
        result_label.config(text="Too low! Try again.", fg=COLOR_ACCENT)
    elif guess > secret_number:
        result_label.config(text="Too high! Try again.", fg=COLOR_ACCENT)
    else:
        result_label.config(
            text=f"Correct! The number was {secret_number}. You guessed it in {attempts} tries.",
            fg=COLOR_SUCCESS
        )
        end_game()

    guess_entry.delete(0, tk.END)

def end_game():
    """End the current round."""
    global game_over
    game_over = True
    guess_entry.config(state=tk.DISABLED)
    check_btn.config(state=tk.DISABLED)
    play_again_btn.pack(pady=10)

def reset_game():
    """Reset all game variables and UI."""
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

# UI Setup
title_label = tk.Label(root, text="Number Guessing Game", font=FONT_TITLE, bg=COLOR_BG, fg=COLOR_ACCENT)
title_label.pack(pady=30)

instruction_label = tk.Label(root, text="Guess a number between 1 and 100", font=FONT_TEXT, bg=COLOR_BG, fg=COLOR_FG)
instruction_label.pack(pady=10)

guess_entry = tk.Entry(root, font=FONT_TEXT, justify="center", width=10, bd=2, relief="groove")
guess_entry.pack(pady=10)
guess_entry.focus()

guess_entry.bind("<Return>", check_guess)

check_btn = tk.Button(root, text="Check Guess", font=FONT_BUTTON, bg=COLOR_ACCENT, fg=COLOR_BG, relief="flat", command=check_guess)
check_btn.pack(pady=5)

result_label = tk.Label(root, text="", font=FONT_TEXT, bg=COLOR_BG, fg=COLOR_FG)
result_label.pack(pady=15)

play_again_btn = tk.Button(root, text="Play Again", font=FONT_BUTTON, bg=COLOR_SUCCESS, fg=COLOR_BG, relief="flat", command=reset_game)

# Start the app
root.mainloop()


# START
#   ↓
# Generate random number between 1 and 100 → secret_number
# Set attempts = 0
# Set game_over = False
#   ↓
# WHILE game_over == False:
#     ↓
#     Get user input → guess
#     ↓
#     Is guess a number?
#       ├── No → Display "Please enter a valid number!" and go back to input
#       └── Yes → Convert guess to integer
#                  attempts = attempts + 1
#                  ↓
#                  Compare guess to secret_number:
#                    ├── guess < secret_number → Display "Too low! Try again."
#                    ├── guess > secret_number → Display "Too high! Try again."
#                    └── guess == secret_number:
#                           Display "Correct! Guessed in X tries."
#                           game_over = True
#                           ↓
#                           Ask "Play again?"
#                               ├── Yes → Reset secret_number, attempts = 0, game_over = False
#                               └── No  → END
