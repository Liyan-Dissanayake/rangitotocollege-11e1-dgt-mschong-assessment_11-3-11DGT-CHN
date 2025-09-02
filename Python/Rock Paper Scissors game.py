import random
import tkinter as tk


# Ask the user for their name
name = input("Enter your name: ")
# Display a welcome message
print(f"\nWelcome to Rock-Paper-Scissors, {name}!")
# List of valid choices
choices = ['rock', 'paper', 'scissors']
# Initialize scores
player_score = 0
computer_score = 0

# Main game loop
while True:
    # Prompt user for their choice
    user_choice = input("Enter rock, paper, or scissors (or 'quit' to return to menu): ").lower()
    
    # Check if user wants to quit
    if user_choice == 'quit':
        # Display final scores and exit
        print(f"\nThanks for playing, {name}!")
        print(f"Final Score - {name}: {player_score} | Computer: {computer_score}")
        break

    # Validate user input
    if user_choice not in choices:
        print("Invalid choice. Please enter 'rock', 'paper', or 'scissors'.")
        continue

    # Computer randomly selects a choice
    computer_choice = random.choice(choices)
    print(f"Computer chose: {computer_choice}")

    # Compare choices and determine the winner
    if user_choice == computer_choice:
        print("It's a tie!")
    elif (user_choice == 'rock' and computer_choice == 'scissors') or \
            (user_choice == 'paper' and computer_choice == 'rock') or \
            (user_choice == 'scissors' and computer_choice == 'paper'):
        print(f"You win this round, {name}!")
        player_score += 1
    else:
        print("Computer wins this round!")
        computer_score += 1

    # Display current scores
    print(f"Current Score - {name}: {player_score} | Computer: {computer_score}")
    print("-" * 40)

# GUI version of the game using tkinter

root = tk.Tk()
root.title("Rock-Paper-Scissors")
root.geometry("400x300")
