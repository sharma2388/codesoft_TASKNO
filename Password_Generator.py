import tkinter as tk
from tkinter import messagebox
import random

# --- Word and syllable list ---
words = ["Sun", "Moon", "Star", "Sky", "River", "Tree", "Leaf", "Cloud", "Fire", "Rain"]
numbers = [str(i) for i in range(10)]

# --- Functions ---
def generate_password(event=None):
    try:
        length = int(length_entry.get())
        if length <= 0:
            raise ValueError
    except:
        messagebox.showerror("Error", "Enter a valid positive number for length")
        return

    password = ""
    while len(password) < length:
        part = random.choice(words + numbers)
        password += part
    password_var.set(password[:length])


def copy_password(event=None):
    password = password_var.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

# --- Main Window ---
root = tk.Tk()
root.title("Memorable Password Generator")
root.geometry("500x300")

# --- Canvas for Background ---
canvas = tk.Canvas(root, width=500, height=300)
canvas.pack(fill="both", expand=True)

# Create a gradient background using rectangles
for i in range(0, 300):
    color = "#%02x%02x%02x" % (30 + i//4, 30 + i//4, 50 + i//3)  # gradient effect
    canvas.create_line(0, i, 500, i, fill=color)

# --- Labels and Entries ---
tk.Label(canvas, text="Enter Password Length:", bg="#1e1e1e", fg="white", font=("Arial", 12)).place(x=120, y=30)
length_entry = tk.Entry(canvas, font=("Arial", 12), justify="center")
length_entry.place(x=170, y=60, width=160)
length_entry.insert(0, "e.g., 12")  # placeholder

tk.Label(canvas, text="Generated Password:", bg="#1e1e1e", fg="white", font=("Arial", 12)).place(x=140, y=100)
password_var = tk.StringVar()
password_entry = tk.Entry(canvas, textvariable=password_var, font=("Arial", 12), justify="center")
password_entry.place(x=110, y=130, width=280)

# --- Buttons ---
generate_btn = tk.Button(canvas, text="Generate Password", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                         command=generate_password)
generate_btn.place(x=150, y=170, width=200)

copy_btn = tk.Button(canvas, text="Copy to Clipboard", font=("Arial", 12, "bold"), bg="#555", fg="white",
                     command=copy_password)
copy_btn.place(x=150, y=210, width=200)

# --- Bind Keys ---
root.bind('<Return>', generate_password)  # Enter key
root.bind('<Control-c>', copy_password)  # Ctrl+C

root.mainloop()
