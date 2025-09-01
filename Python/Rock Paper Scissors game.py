import random

name = input("Enter your name: ")
print(f"\nWelcome to Rock-Paper-Scissors, {name}!")
choices = ['rock', 'paper', 'scissors']
player_score = 0
computer_score = 0

while True:
    user_choice = input("Enter rock, paper, or scissors (or 'quit' to return to menu): ").lower()
    
    if user_choice == 'quit':
        print(f"\nThanks for playing, {name}!")
        print(f"Final Score - {name}: {player_score} | Computer: {computer_score}")
        break

    if user_choice not in choices:
        print("Invalid choice. Please enter 'rock', 'paper', or 'scissors'.")
        continue

    computer_choice = random.choice(choices)
    print(f"Computer chose: {computer_choice}")

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

    print(f"Current Score - {name}: {player_score} | Computer: {computer_score}")
    print("-" * 40)


"""Here are the steps to make a flow chart for your Rock Paper Scissors program:

Start

Begin with a "Start" symbol.
Input Name

Show a step for the user to enter their name.
Display Welcome Message

Indicate the welcome message is shown.
Game Loop (Repeat Until Quit)

Use a loop symbol to show the game repeats.
User Input: Choice

User enters "rock", "paper", "scissors", or "quit".
Check for Quit

Decision: Is input "quit"?
If yes, go to "End Game" steps.
If no, continue.
Validate Input

Decision: Is input valid?
If not, show error and loop back for input.
Computer Chooses

Computer randomly selects "rock", "paper", or "scissors".
Compare Choices

Decision:
Tie?
Player wins?
Computer wins?
Update Scores

Add points to player or computer.
Display Round Results & Scores

Show who won the round and current scores.
Repeat Loop

Go back to user input.
End Game

Display final scores and exit."""