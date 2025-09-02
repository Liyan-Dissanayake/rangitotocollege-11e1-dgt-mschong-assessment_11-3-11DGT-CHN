import tkinter as tk

def calculate():
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get())
        result = num1 + num2
        result_label.config(text=f"Result: {result}")
    except ValueError:
        result_label.config(text="Please enter valid numbers!")

# Create main window
root = tk.Tk()
root.title("Simple Calculator")

# Create widgets
label1 = tk.Label(root, text="First Number:")
label2 = tk.Label(root, text="Second Number:")
entry1 = tk.Entry(root)
entry2 = tk.Entry(root)
calculate_button = tk.Button(root, text="Add", command=calculate)
result_label = tk.Label(root, text="Result: ")

# Arrange widgets using grid
label1.grid(row=0, column=0, padx=10, pady=5)
entry1.grid(row=0, column=1, padx=10, pady=5)
label2.grid(row=1, column=0, padx=10, pady=5)
entry2.grid(row=1, column=1, padx=10, pady=5)
calculate_button.grid(row=2, column=0, columnspan=2, pady=10)
result_label.grid(row=3, column=0, columnspan=2, pady=5)

# Start the application
root.mainloop()