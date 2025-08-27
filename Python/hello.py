import random

# Simple Rock-Paper-Scissors Game
computer_choice = random.choice(['rock', 'paper', 'scissors'])
user_choice = input("Enter rock, paper, or scissors: ").lower()
print(f"Computer chose: {computer_choice}")
if user_choice == computer_choice:
    print("It's a tie!")
elif (user_choice == 'rock' and computer_choice == 'scissors') or \
     (user_choice == 'paper' and computer_choice == 'rock') or \
     (user_choice == 'scissors' and computer_choice == 'paper'):
    print("You win!")
else:
    print("Computer wins!")