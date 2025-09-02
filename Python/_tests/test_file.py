import tkinter as tk
import random

root = tk.Tk()
root.title("Rock-Paper-Scissors")
root.geometry("400x300")

choices = ['rock', 'paper', 'scissors']
player_score = 0
computer_score = 0

title_label = tk.Label(root, text="Rock-Paper-Scissors", font=("Arial", 16))
title_label.pack(pady=10, padx=(1,0))

root.mainloop()
