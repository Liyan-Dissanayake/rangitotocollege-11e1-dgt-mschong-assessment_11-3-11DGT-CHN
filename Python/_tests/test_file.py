import tkinter as tk
import random

# Initialize main window
root = tk.Tk()
root.title("Rock-Paper-Scissors")
root.geometry("400x300")

# Game variables
choices = ['rock', 'paper', 'scissors']
player_score = 0
computer_score = 0

# Functions
def play(user_choice):
    global player_score, computer_score
    
    computer_choice = random.choice(choices)
    result = ""

    if user_choice == computer_choice:
        result = "It's a tie!"
    elif (user_choice == 'rock' and computer_choice == 'scissors') or \
         (user_choice == 'paper' and computer_choice == 'rock') or \
         (user_choice == 'scissors' and computer_choice == 'paper'):
        result = f"You win! {user_choice} beats {computer_choice}"
        player_score += 1
    else:
        result = f"Computer wins! {computer_choice} beats {user_choice}"
        computer_score += 1
    
    # Update labels
    result_label.config(text=result)
    score_label.config(text=f"Player: {player_score} | Computer: {computer_score}")

def quit_game():
    root.destroy()

# Widgets
title_label = tk.Label(root, text="Rock-Paper-Scissors", font=("Arial", 16))
title_label.pack(pady=10)

score_label = tk.Label(root, text="Player: 0 | Computer: 0", font=("Arial", 12))
score_label.pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

rock_btn = tk.Button(button_frame, text="Rock", width=10, command=lambda: play("rock"))
rock_btn.grid(row=0, column=0, padx=5)

paper_btn = tk.Button(button_frame, text="Paper", width=10, command=lambda: play("paper"))
paper_btn.grid(row=0, column=1, padx=5)

scissors_btn = tk.Button(button_frame, text="Scissors", width=10, command=lambda: play("scissors"))
scissors_btn.grid(row=0, column=2, padx=5)

quit_btn = tk.Button(root, text="Quit", width=10, command=quit_game)
quit_btn.pack(pady=10)

# Run application
root.mainloop()
