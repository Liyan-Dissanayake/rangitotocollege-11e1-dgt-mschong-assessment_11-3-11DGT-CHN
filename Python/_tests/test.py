import tkinter as tk
from tkinter import messagebox
from random import randint

class Pet:
    def __init__(self):
        self.hunger = 100
        self.happiness = 100
        self.energy = 100

    def feed(self):
        self.hunger = min(100, self.hunger + 20)
        self.energy = max(0, self.energy - 5)

    def play(self):
        self.happiness = min(100, self.happiness + 15)
        self.energy = max(0, self.energy - 10)
        self.hunger = max(0, self.hunger - 5)

    def sleep(self):
        self.energy = min(100, self.energy + 30)
        self.hunger = max(0, self.hunger - 10)

    def decay(self):
        self.hunger = max(0, self.hunger - 2)
        self.happiness = max(0, self.happiness - 2)
        self.energy = max(0, self.energy - 1)

    def is_alive(self):
        return self.hunger > 0 and self.happiness > 0 and self.energy > 0

class PetSimulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🐾 Virtual Pet Simulator")
        self.geometry("400x500")
        self.resizable(False, False)

        self.pet = Pet()

        self.create_widgets()
        self.update_stats()
        self.game_loop()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=200, height=200)
        self.canvas.pack(pady=10)

        self.face = self.canvas.create_oval(50, 50, 150, 150, fill="yellow")
        self.eye1 = self.canvas.create_oval(70, 80, 90, 100, fill="black")
        self.eye2 = self.canvas.create_oval(110, 80, 130, 100, fill="black")
        self.mouth = self.canvas.create_line(80, 130, 120, 130, width=2)

        self.status_label = tk.Label(self, text="Welcome to your pet!", font=("Arial", 14))
        self.status_label.pack(pady=10)

        self.stats_frame = tk.Frame(self)
        self.stats_frame.pack()

        self.hunger_label = tk.Label(self.stats_frame, text="Hunger: 100")
        self.hunger_label.grid(row=0, column=0, padx=10)

        self.happiness_label = tk.Label(self.stats_frame, text="Happiness: 100")
        self.happiness_label.grid(row=0, column=1, padx=10)

        self.energy_label = tk.Label(self.stats_frame, text="Energy: 100")
        self.energy_label.grid(row=0, column=2, padx=10)

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(pady=20)

        tk.Button(self.buttons_frame, text="🍖 Feed", command=self.feed_pet).grid(row=0, column=0, padx=10)
        tk.Button(self.buttons_frame, text="🎾 Play", command=self.play_pet).grid(row=0, column=1, padx=10)
        tk.Button(self.buttons_frame, text="💤 Sleep", command=self.sleep_pet).grid(row=0, column=2, padx=10)

    def feed_pet(self):
        self.pet.feed()
        self.update_stats()

    def play_pet(self):
        self.pet.play()
        self.update_stats()

    def sleep_pet(self):
        self.pet.sleep()
        self.update_stats()

    def update_stats(self):
        self.hunger_label.config(text=f"Hunger: {self.pet.hunger}")
        self.happiness_label.config(text=f"Happiness: {self.pet.happiness}")
        self.energy_label.config(text=f"Energy: {self.pet.energy}")
        self.update_face()

    def update_face(self):
        mood = self.get_pet_mood()
        if mood == "happy":
            self.canvas.itemconfig(self.face, fill="lightgreen")
            self.canvas.coords(self.mouth, 80, 130, 100, 140, 120, 130)  # smile
        elif mood == "okay":
            self.canvas.itemconfig(self.face, fill="yellow")
            self.canvas.coords(self.mouth, 80, 130, 120, 130)  # straight
        else:
            self.canvas.itemconfig(self.face, fill="tomato")
            self.canvas.coords(self.mouth, 80, 140, 100, 130, 120, 140)  # sad

        self.status_label.config(text=f"Pet is feeling {mood}!")

    def get_pet_mood(self):
        if self.pet.hunger > 70 and self.pet.happiness > 70 and self.pet.energy > 70:
            return "happy"
        elif self.pet.hunger > 30 and self.pet.happiness > 30 and self.pet.energy > 30:
            return "okay"
        else:
            return "sad"

    def game_loop(self):
        if self.pet.is_alive():
            self.pet.decay()
            self.update_stats()
            self.after(2000, self.game_loop)
        else:
            self.game_over()

    def game_over(self):
        self.status_label.config(text="😢 Your pet has passed away...")
        messagebox.showinfo("Game Over", "Your pet has passed away. Game Over.")
        self.destroy()

if __name__ == "__main__":
    app = PetSimulator()
    app.mainloop()
