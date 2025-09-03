import tkinter as tk
import random

root = tk.Tk()
root.title("Rock-Paper-Scissors")
root.geometry("400x300")

choices = ['rock', 'paper', 'scissors']
player_score = 0
computer_score = 0

title_label = tk.Label(root, text="Rock-Paper-Scissors", font=("Arial", 16))
title_label.pack(pady=20, padx=1)

def play(user_choice):
    user_choice = user_choice.lower()
    global player_score, computer_score



name_label = tk.Label(root, text="Enter your name:", font=("Arial", 12))
name_label.pack(pady=5)
name_entry = tk.Entry(root, font=("Arial", 12))
name_entry.pack(pady=5)

root.mainloop()
