import random

def rock_paper_scissors(name):
    print(f"\nWelcome to Rock-Paper-Scissors, {name}!")
    choices = ['rock', 'paper', 'scissors']
    player_score = 0
    computer_score = 0
    rounds_played = 0

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

        rounds_played += 1
        print(f"Current Score - {name}: {player_score} | Computer: {computer_score}")
        print("-" * 40)


player_name = input("Enter your name: ")
rock_paper_scissors(player_name)
