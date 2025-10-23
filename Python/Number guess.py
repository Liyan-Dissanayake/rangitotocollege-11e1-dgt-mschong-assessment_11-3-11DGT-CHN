"""A Tkinter game where the player guesses a number between 1 and 100."""

import tkinter as tk
import random

root = tk.Tk()
root.title("Number Guessing Game")
root.geometry("600x450")
root.resizable(False, False)
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
secret_number = random.randint(1, 100)  # Number the player has to guess
attempts = 0  # Counter for number of guesses made
game_over = False  # Flag to check if the game has ended


def check_guess(event=None):
    """Check the player's guess and update the UI accordingly."""
    global attempts, game_over
    if game_over:
        return  # Do nothing if the game has ended

    # Get the guess from the entry widget and validate it
    guess = guess_entry.get().strip()
    if not guess.isdigit():
        result_label.config(
            text="Please enter a valid number!",
            fg=COLOR_ERROR
        )
        return

    # Convert the guess to integer and increase attempt count
    guess = int(guess)
    attempts += 1

    # Compare the guess to the secret number
    if guess < secret_number:
        result_label.config(
            text="Too low! Try again.",
            fg=COLOR_ACCENT
        )
    elif guess > secret_number:
        result_label.config(
            text="Too high! Try again.",
            fg=COLOR_ACCENT
        )
    else:
        # Correct guess, show success message and end game
        result_label.config(
            text=(
                f"Correct! The number was {secret_number}. "
                f"You guessed it in {attempts} tries."
            ),
            fg=COLOR_SUCCESS
        )
        end_game()

    # Clear the entry field for the next guess
    guess_entry.delete(0, tk.END)

    if guess < secret_number:
        flash_result("#81a1c1")  # Too low
    elif guess > secret_number:
        flash_result("#bf616a")  # Too high
    else:
        flash_result("#a3be8c", correct=True)  # Correct guess




def flash_result(color, correct=False):
    """Provide dynamic visual feedback for the player's guess."""

    # Change color immediately
    result_label.config(fg=color)

    # If correct, add a simple fade-in/fade-out brightness effect
    if correct:
        def fade(step=0):
            # Use lighter green shades to simulate a fade
            shades = ["#a3be8c", "#b5d19c", "#c8e4ac", "#b5d19c", 
                      "#a3be8c"]
            if step < len(shades):
                result_label.config(fg=shades[step])
                result_label.after(100, lambda: fade(step + 1))
            else:
                result_label.config(fg=COLOR_FG)

        fade()
    else:
        # Regular flash for wrong guesses
        result_label.after(400, lambda: result_label.config(fg=COLOR_FG))

def end_game():
    """Disable input and show the 'Play Again' button."""
    global game_over
    game_over = True
    # Disable entry field and check button to prevent further input
    guess_entry.config(state=tk.DISABLED)
    check_btn.config(state=tk.DISABLED)
    # Show the play again button
    play_again_btn.pack(pady=10)


def reset_game():
    """Reset the game variables and UI for a new round."""
    global secret_number, attempts, game_over
    # Generate a new number and reset attempts and game_over flag
    secret_number = random.randint(1, 100)
    attempts = 0
    game_over = False
    # Enable input widgets
    guess_entry.config(state=tk.NORMAL)
    check_btn.config(state=tk.NORMAL)
    # Reset result label
    result_label.config(
        text="Guess a number between 1 and 100",
        fg=COLOR_FG
    )
    # Hide the play again button until needed
    play_again_btn.pack_forget()
    # Clear entry field and set focus
    guess_entry.delete(0, tk.END)
    guess_entry.focus()


# Title label at the top of the window
title_label = tk.Label(
    root,
    text="Number Guessing Game",
    font=FONT_TITLE,
    bg=COLOR_BG,
    fg=COLOR_ACCENT
)
title_label.pack(pady=30)

# Instruction label to guide the player
instruction_label = tk.Label(
    root,
    text="Guess a number between 1 and 100",
    font=FONT_TEXT,
    bg=COLOR_BG,
    fg=COLOR_FG
)
instruction_label.pack(pady=10)

# Entry widget where the player types their guess
guess_entry = tk.Entry(
    root,
    font=FONT_TEXT,
    justify="center",
    width=10,
    bd=2,
    relief="groove"
)
guess_entry.pack(pady=10)
guess_entry.focus()
# Bind Enter key to submit the guess
guess_entry.bind("<Return>", check_guess)

# Button to check the player's guess
check_btn = tk.Button(
    root,
    text="Check Guess",
    font=FONT_BUTTON,
    bg=COLOR_ACCENT,
    fg=COLOR_BG,
    relief="flat",
    command=check_guess
)
check_btn.pack(pady=5)

# Label to display messages about the player's guesses
result_label = tk.Label(
    root,
    text="",
    font=FONT_TEXT,
    bg=COLOR_BG,
    fg=COLOR_FG
)
result_label.pack(pady=15)

# Button to reset and play again, shown only after game ends
play_again_btn = tk.Button(
    root,
    text="Play Again",
    font=FONT_BUTTON,
    bg=COLOR_SUCCESS,
    fg=COLOR_BG,
    relief="flat",
    command=reset_game
)

# Start the application
root.mainloop()