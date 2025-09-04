import tkinter as tk
import random

root = tk.Tk()
root.title("Rock-Paper-Scissors")
root.geometry("400x300")

choices = ['rock', 'paper', 'scissors']
player_score = 0
computer_score = 0

def play(user_choice):
    user_choice = user_choice.lower()
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

    result_label.config(text=result)
    score_label.config(text=f"Player: {player_score} | Computer: {computer_score}")
def submit_name():
    global player_name
    player_name = name_entry.get()
    name_label.pack_forget()
    name_entry.pack_forget()
    submit_button.pack_forget()
    title_label.config(text=f"Welcome, {player_name}! Rock-Paper-Scissors")
    score_label.pack(pady=5)
    result_label.pack(pady=5)
    quit_btn.pack(pady=10)
    scissors_btn.grid(row=0, column=2, padx=5)
    paper_btn.grid(row=0, column=1, padx=5)
    rock_btn.grid(row=0, column=0, padx=5)
def quit_game():
    root.destroy()

title_label = tk.Label(root, text="Rock-Paper-Scissors", font=("Arial", 16))
title_label.pack(pady=20, padx=1)

name_label = tk.Label(root, text="Enter your name:", font=("Arial", 12))
name_label.pack(pady=5)
name_entry = tk.Entry(root, font=("Arial", 12))
name_entry.pack(pady=5)
submit_button = tk.Button(root, text="Submit", font=("Arial", 12), command=submit_name)
submit_button.pack(pady=5)

score_label = tk.Label(root, text="Player: 0 | Computer: 0", font=("Arial", 12))
result_label = tk.Label(root, text="", font=("Arial", 12))

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

rock_btn = tk.Button(button_frame, text="Rock", width=10, command=lambda: play("rock"))
paper_btn = tk.Button(button_frame, text="Paper", width=10, command=lambda: play("paper"))
scissors_btn = tk.Button(button_frame, text="Scissors", width=10, command=lambda: play("scissors"))
quit_btn = tk.Button(root, text="Quit", width=10, command=quit_game)


root.mainloop()
