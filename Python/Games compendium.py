import tkinter as tk
import random
import time

# Main application window
root = tk.Tk()
root.title("Games Compendium")
root.geometry("600x450")
root.resizable(False, False)

# Global variables
player_name = ""
current_game = None  # Tracks which game is currently active

# Colors and fonts
COLOR_BG1 = "#1e1e2e"  # Typing Game
COLOR_FG1 = "#cdd6f4"
COLOR_ACCENT1 = "#89b4fa"
COLOR_GOOD = "#a6e3a1"
COLOR_BAD = "#f38ba8"

COLOR_BG2 = "#282c34"  # Rock-Paper-Scissors
COLOR_FG2 = "#abb2bf"
COLOR_ACCENT2 = "#61afef"
COLOR_WIN = "#98c379"
COLOR_LOSE = "#e06c75"
COLOR_TIE = "#d19a66"

FONT_TITLE = ("Helvetica", 22, "bold")
FONT_TEXT = ("Helvetica", 16)
FONT_BUTTON = ("Helvetica", 12, "bold")

# Name Entry
def ask_name():
    """Ask the player for their name at the very start."""
    clear_screen()
    global name_entry, name_label, submit_button
    root.config(bg="#333")
    
    title = tk.Label(root, text="Welcome to Games Compendium!", font=FONT_TITLE, bg="#333", fg="#fff")
    title.pack(pady=40)
    
    name_label = tk.Label(root, text="Enter your name:", font=FONT_TEXT, bg="#333", fg="#fff")
    name_label.pack(pady=(0,5))
    
    name_entry = tk.Entry(root, font=FONT_TEXT, justify="center", bd=2, relief="groove")
    name_entry.pack(pady=5)
    name_entry.focus()
    
    submit_button = tk.Button(root, text="Submit", font=FONT_BUTTON, bg="#61afef", fg="#282c34", relief="flat", command=submit_name)
    submit_button.pack(pady=20)

def submit_name():
    """Save player name and show the main menu."""
    global player_name
    player_name = name_entry.get().strip()
    if not player_name:
        name_entry.config(highlightthickness=2, highlightbackground="red")
        return
    show_menu()

# Main Menu
def show_menu():
    """Display the main menu for selecting games."""
    clear_screen()
    menu_label = tk.Label(root, text=f"Hello {player_name}, choose a game:", font=FONT_TITLE, bg="#444", fg="#fff")
    menu_label.pack(pady=30)

    tk.Button(root, text="Typing Speed Test", font=FONT_BUTTON, width=25,
              bg=COLOR_ACCENT1, fg=COLOR_BG1, command=start_typing_game).pack(pady=10)

    tk.Button(root, text="Rock-Paper-Scissors", font=FONT_BUTTON, width=25,
              bg=COLOR_ACCENT2, fg=COLOR_BG2, command=start_rps_game).pack(pady=10)

    tk.Button(root, text="Third Game (Coming Soon)", font=FONT_BUTTON, width=25,
              bg="#bbbbbb", fg="#222", state=tk.DISABLED).pack(pady=10)

def clear_screen():
    """Remove all widgets from the screen."""
    for widget in root.winfo_children():
        widget.destroy()

# Typing Speed Test
words_master = [
    "python", "keyboard", "speed", "challenge", "program", "window",
    "function", "variable", "random", "player", "typing", "testing",
    "accuracy", "loop", "game", "button", "logic", "winner", "input", "output",
    "developer", "computer", "syntax", "compile", "editor", "project",
    "error", "coding", "performance", "practice", "learn", "typewriter",
    "mechanical", "language", "debug", "structure", "indent", "runtime",
    "hardware", "software", "command", "processor", "virtual", "memory",
    "storage", "algorithm", "condition", "argument", "statement", "module"
]

words_unused = words_master.copy()
current_word = ""
start_time = None
score = 0
total_attempts = 0
game_running = False
time_limit = 30
times = []
word_start_time = None

def start_typing_game():
    global current_game
    current_game = "typing"
    clear_screen()
    init_typing_game_ui()
    reset_typing_game()

def next_word():
    global current_word, words_unused
    if not words_unused:
        words_unused = words_master.copy()
        random.shuffle(words_unused)
    current_word = words_unused.pop()
    word_label.config(text=current_word)

def check_word(event=None):
    global score, total_attempts, times, word_start_time
    if not game_running:
        return

    typed = entry.get().strip().lower()
    entry.delete(0, tk.END)
    total_attempts += 1

    end_time = time.time()
    time_taken = end_time - word_start_time
    times.append(time_taken)
    average_time = sum(times) / len(times)
    wpm = (score / sum(times)) * 60 if sum(times) > 0 else 0
    word_start_time = time.time()

    if typed == current_word:
        score += 1
        result_label.config(
            text=f"Correct! ({time_taken:.2f}s) | Avg: {average_time:.2f}s | WPM: {wpm:.1f}",
            fg=COLOR_GOOD
        )
    else:
        result_label.config(
            text=f"Wrong! ({current_word}) | Avg: {average_time:.2f}s | WPM: {wpm:.1f}",
            fg=COLOR_BAD
        )
    next_word()

def update_timer():
    global game_running
    if not game_running:
        return
    elapsed = int(time.time() - start_time)
    remaining = time_limit - elapsed
    if remaining <= 0:
        game_running = False
        entry.config(state=tk.DISABLED)
        word_label.config(text="Time's up!")
        wpm = (score / time_limit) * 60
        accuracy = (score / total_attempts * 100) if total_attempts > 0 else 0
        result_label.config(
            text=f"WPM: {wpm:.1f} | Accuracy: {accuracy:.1f}%",
            fg=COLOR_ACCENT1
        )
        play_again_btn.pack(pady=10)
        return
    timer_label.config(text=f"Time left: {remaining}s")
    root.after(1000, update_timer)

def start_game():
    global score, total_attempts, game_running, start_time, word_start_time
    score = 0
    total_attempts = 0
    game_running = True
    start_time = time.time()
    word_start_time = time.time()
    result_label.config(text="")
    entry.config(state=tk.NORMAL)
    entry.delete(0, tk.END)
    next_word()
    update_timer()

def reset_typing_game():
    global times
    times = []
    play_again_btn.pack_forget()
    start_game()

def quit_to_menu():
    show_menu()

def init_typing_game_ui():
    global timer_label, word_label, entry, result_label, play_again_btn
    root.config(bg=COLOR_BG1)
    title_label = tk.Label(root, text="Typing Speed Test", font=FONT_TITLE, bg=COLOR_BG1, fg=COLOR_ACCENT1)
    title_label.pack(pady=20)

    timer_label = tk.Label(root, text=f"Time left: {time_limit}s", font=FONT_TEXT, bg=COLOR_BG1, fg=COLOR_FG1)
    timer_label.pack()

    word_label = tk.Label(root, text="Press 'Start' to begin", font=("Helvetica", 24, "bold"), bg=COLOR_BG1, fg=COLOR_ACCENT1)
    word_label.pack(pady=30)

    entry = tk.Entry(root, font=FONT_TEXT, justify="center", width=20, bd=2, relief="groove", state=tk.DISABLED)
    entry.pack(pady=10)
    entry.bind("<Return>", check_word)

    result_label = tk.Label(root, text="", font=FONT_TEXT, bg=COLOR_BG1, fg=COLOR_FG1)
    result_label.pack(pady=15)

    button_frame = tk.Frame(root, bg=COLOR_BG1)
    button_frame.pack(pady=10)

    start_btn = tk.Button(button_frame, text="Start", font=FONT_BUTTON, bg=COLOR_ACCENT1, fg=COLOR_BG1, relief="flat", width=12, command=start_game)
    start_btn.grid(row=0, column=0, padx=10)

    play_again_btn = tk.Button(button_frame, text="Play Again", font=FONT_BUTTON, bg=COLOR_GOOD, fg=COLOR_BG1, relief="flat", width=12, command=reset_typing_game)
    quit_btn = tk.Button(button_frame, text="Quit to Menu", font=FONT_BUTTON, bg=COLOR_BAD, fg=COLOR_BG1, relief="flat", width=12, command=quit_to_menu)
    quit_btn.grid(row=0, column=1, padx=10)

# Rock-Paper-Scissors
choices = ['rock', 'paper', 'scissors']
player_score = 0
computer_score = 0
game_over = False

def start_rps_game():
    global current_game
    current_game = "rps"
    clear_screen()
    init_rps_ui()
    reset_rps_game()

def play_rps(user_choice):
    global player_score, computer_score, game_over
    if game_over:
        return
    user_choice = user_choice.lower()
    computer_choice = random.choice(choices)
    if user_choice == computer_choice:
        result_label.config(text=f"It's a tie!", fg=COLOR_TIE)
    elif (user_choice == 'rock' and computer_choice == 'scissors') or \
         (user_choice == 'paper' and computer_choice == 'rock') or \
         (user_choice == 'scissors' and computer_choice == 'paper'):
        player_score += 1
        result_label.config(text=f"You win! {user_choice.capitalize()} beats {computer_choice.capitalize()}", fg=COLOR_WIN)
    else:
        computer_score += 1
        result_label.config(text=f"Computer wins! {computer_choice.capitalize()} beats {user_choice.capitalize()}", fg=COLOR_LOSE)
    score_label.config(text=f"{player_name}: {player_score} | Computer: {computer_score}")
    check_winner_rps()

def reset_rps_game():
    global player_score, computer_score, game_over
    player_score = 0
    computer_score = 0
    game_over = False
    score_label.config(text=f"{player_name}: 0 | Computer: 0", fg=COLOR_FG2)
    result_label.config(text="", fg=COLOR_FG2)
    play_again_btn.pack_forget()
    enable_buttons(True)

def check_winner_rps():
    global game_over
    if player_score >= 5:
        result_label.config(text=f"Congratulations! You won the game!", fg=COLOR_WIN)
        play_again_btn.pack(pady=10)
        game_over = True
        enable_buttons(False)
    elif computer_score >= 5:
        result_label.config(text=f"Computer won the game! Better luck next time.", fg=COLOR_LOSE)
        play_again_btn.pack(pady=10)
        game_over = True
        enable_buttons(False)

def enable_buttons(state: bool):
    state_val = tk.NORMAL if state else tk.DISABLED
    rock_btn.config(state=state_val)
    paper_btn.config(state=state_val)
    scissors_btn.config(state=state_val)

def quit_rps_to_menu():
    show_menu()

def init_rps_ui():
    global score_label, result_label, button_frame, rock_btn, paper_btn, scissors_btn, play_again_btn, quit_btn, welcome_label
    root.config(bg=COLOR_BG2)
    title_label = tk.Label(root, text="Rock-Paper-Scissors", font=FONT_TITLE, bg=COLOR_BG2, fg=COLOR_ACCENT2)
    title_label.pack(pady=20)

    welcome_label = tk.Label(root, text=f"Welcome, {player_name}!", font=FONT_TEXT, bg=COLOR_BG2, fg=COLOR_ACCENT2)
    welcome_label.pack(pady=(0, 10))

    score_label = tk.Label(root, text=f"{player_name}: 0 | Computer: 0", font=FONT_TEXT, bg=COLOR_BG2, fg=COLOR_FG2)
    score_label.pack(pady=(5, 15))
    result_label = tk.Label(root, text="", font=FONT_TEXT, bg=COLOR_BG2)
    result_label.pack(pady=(0,15))

    button_frame = tk.Frame(root, bg=COLOR_BG2)
    button_frame.pack(pady=10)
    rock_btn = tk.Button(button_frame, text="Rock", width=12, font=FONT_BUTTON, bg="#3b4048", fg=COLOR_FG2, relief="raised", command=lambda: play_rps("rock"))
    paper_btn = tk.Button(button_frame, text="Paper", width=12, font=FONT_BUTTON, bg="#3b4048", fg=COLOR_FG2, relief="raised", command=lambda: play_rps("paper"))
    scissors_btn = tk.Button(button_frame, text="Scissors", width=12, font=FONT_BUTTON, bg="#3b4048", fg=COLOR_FG2, relief="raised", command=lambda: play_rps("scissors"))
    rock_btn.grid(row=0, column=0, padx=10)
    paper_btn.grid(row=0, column=1, padx=10)
    scissors_btn.grid(row=0, column=2, padx=10)

    quit_btn = tk.Button(root, text="Quit to Menu", width=12, font=FONT_BUTTON, bg=COLOR_LOSE, fg=COLOR_BG2, relief="flat", command=quit_rps_to_menu)
    quit_btn.pack(pady=10)
    play_again_btn = tk.Button(root, text="Play Again", width=12, font=FONT_BUTTON, bg=COLOR_WIN, fg=COLOR_BG2, relief="flat", command=reset_rps_game)

# Start by asking the player's name 
ask_name()
root.mainloop()
