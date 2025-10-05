import tkinter as tk
import random

# Create the main application window
root = tk.Tk()
root.title("Rock-Paper-Scissors")
root.geometry("450x380")
root.resizable(False, False)
root.config(bg="#282c34")

# Game state variables
choices = ['rock', 'paper', 'scissors']
player_score = 0
computer_score = 0
game_over = False

# Colors and fonts
FONT_TITLE = ("Helvetica", 20, "bold")
FONT_LABEL = ("Helvetica", 14)
FONT_BUTTON = ("Helvetica", 12, "bold")
COLOR_BG = "#282c34"
COLOR_FG = "#abb2bf"
COLOR_ACCENT = "#61afef"
COLOR_WIN = "#98c379"
COLOR_LOSE = "#e06c75"
COLOR_TIE = "#d19a66"

def play(user_choice):
    global player_score, computer_score, game_over
    
    if game_over:
        return
    
    user_choice = user_choice.lower()
    computer_choice = random.choice(choices)

    if user_choice == computer_choice:
        result = "It's a tie!"
        result_label.config(fg=COLOR_TIE)
    elif (user_choice == 'rock' and computer_choice == 'scissors') or \
         (user_choice == 'paper' and computer_choice == 'rock') or \
         (user_choice == 'scissors' and computer_choice == 'paper'):
        result = f"You win! {user_choice.capitalize()} beats {computer_choice.capitalize()}"
        player_score += 1
        result_label.config(fg=COLOR_WIN)
    else:
        result = f"Computer wins! {computer_choice.capitalize()} beats {user_choice.capitalize()}"
        computer_score += 1
        result_label.config(fg=COLOR_LOSE)

    result_label.config(text=result)
    score_label.config(text=f"Player: {player_score}  |  Computer: {computer_score}")
    check_winner()

def submit_name():
    global player_name
    player_name = name_entry.get().strip()

    if not player_name:
        name_entry.config(highlightbackground="red", highlightcolor="red")
        return
    else:
        name_entry.config(highlightbackground=COLOR_BG)

    name_label.pack_forget()
    name_entry.pack_forget()
    submit_button.pack_forget()

    title_label.config(text=f"Welcome, {player_name}! Rock-Paper-Scissors")
    score_label.pack(pady=(5, 15))
    result_label.pack(pady=(0, 15))
    button_frame.pack(pady=10)
    quit_btn.pack(pady=15)
    reset_game()  # Initialize scores and buttons

def quit_game():
    root.destroy()

def reset_game():
    global player_score, computer_score, game_over
    player_score = 0
    computer_score = 0
    game_over = False
    score_label.config(text="Player: 0  |  Computer: 0", fg=COLOR_FG)
    result_label.config(text="", fg=COLOR_FG)
    play_again_btn.pack_forget()
    enable_buttons(True)

def check_winner():
    global player_score, computer_score, game_over
    if player_score >= 5:
        result_label.config(text=f"Congratulations {player_name}, you won the game!", fg=COLOR_WIN)
        play_again_btn.pack(pady=10)
        game_over = True
        enable_buttons(False)
    elif computer_score >= 5:
        result_label.config(text="Computer won the game! Better luck next time.", fg=COLOR_LOSE)
        play_again_btn.pack(pady=10)
        game_over = True
        enable_buttons(False)

def enable_buttons(state: bool):
    rock_btn.config(state=tk.NORMAL if state else tk.DISABLED)
    paper_btn.config(state=tk.NORMAL if state else tk.DISABLED)
    scissors_btn.config(state=tk.NORMAL if state else tk.DISABLED)

# UI Elements
title_label = tk.Label(root, text="Rock-Paper-Scissors", font=FONT_TITLE, bg=COLOR_BG, fg=COLOR_ACCENT)
title_label.pack(pady=20)

name_label = tk.Label(root, text="Enter your name:", font=FONT_LABEL, bg=COLOR_BG, fg=COLOR_FG)
name_label.pack(pady=(5, 2))

name_entry = tk.Entry(root, font=FONT_LABEL, justify="center", bd=2, relief="groove")
name_entry.pack(pady=(0, 10))
name_entry.focus()

submit_button = tk.Button(root, text="Submit", font=FONT_BUTTON, bg=COLOR_ACCENT, fg=COLOR_BG, relief="flat", command=submit_name)
submit_button.pack(pady=5)

score_label = tk.Label(root, text="Player: 0  |  Computer: 0", font=FONT_LABEL, bg=COLOR_BG, fg=COLOR_FG)

result_label = tk.Label(root, text="", font=FONT_LABEL, bg=COLOR_BG)

button_frame = tk.Frame(root, bg=COLOR_BG)

rock_btn = tk.Button(button_frame, text="Rock", width=12, font=FONT_BUTTON, bg="#3b4048", fg=COLOR_FG, relief="raised", command=lambda: play("rock"))
paper_btn = tk.Button(button_frame, text="Paper", width=12, font=FONT_BUTTON, bg="#3b4048", fg=COLOR_FG, relief="raised", command=lambda: play("paper"))
scissors_btn = tk.Button(button_frame, text="Scissors", width=12, font=FONT_BUTTON, bg="#3b4048", fg=COLOR_FG, relief="raised", command=lambda: play("scissors"))

rock_btn.grid(row=0, column=0, padx=10)
paper_btn.grid(row=0, column=1, padx=10)
scissors_btn.grid(row=0, column=2, padx=10)

quit_btn = tk.Button(root, text="Quit", width=12, font=FONT_BUTTON, bg="#e06c75", fg=COLOR_BG, relief="flat", command=quit_game)

play_again_btn = tk.Button(root, text="Play Again", width=12, font=FONT_BUTTON, bg=COLOR_WIN, fg=COLOR_BG, relief="flat", command=reset_game)

root.mainloop()
