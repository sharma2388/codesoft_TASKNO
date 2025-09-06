import tkinter as tk
import math

# --- Functions ---
def press(key):
    global expression
    expression += str(key)
    equation.set(expression)

def equalpress(event=None):
    global expression
    try:
        expr = expression
        # Convert sin, cos, tan input from degrees to radians
        expr = expr.replace("sin(", "math.sin(math.radians(")
        expr = expr.replace("cos(", "math.cos(math.radians(")
        expr = expr.replace("tan(", "math.tan(math.radians(")
        result = str(eval(expr, {"math": math}))  # Use math module in eval
        equation.set(result)
        history.append(f"{expression} = {result}")
        expression = result
    except:
        equation.set(" error ")

def clear_all(event=None):
    global expression
    expression = ""
    equation.set("")

def backspace(event=None):
    global expression
    expression = expression[:-1]
    equation.set(expression)

def sqrt():
    try:
        global expression
        result = str(math.sqrt(float(expression)))
        equation.set(result)
        expression = result
    except:
        equation.set(" error ")

def square():
    try:
        global expression
        result = str(float(expression) ** 2)
        equation.set(result)
        expression = result
    except:
        equation.set(" error ")

def log():
    try:
        global expression
        result = str(math.log10(float(expression)))
        equation.set(result)
        expression = result
    except:
        equation.set(" error ")

def ln():
    try:
        global expression
        result = str(math.log(float(expression)))
        equation.set(result)
        expression = result
    except:
        equation.set(" error ")

# --- History Functions ---
history = []

def toggle_history():
    if history_frame.winfo_ismapped():
        history_frame.grid_remove()
    else:
        history_listbox.delete(0, tk.END)
        for item in history:
            history_listbox.insert(tk.END, item)
        history_frame.grid(row=0, column=5, rowspan=8, padx=10, pady=10, sticky="ns")

def use_history(event):
    global expression
    selected = history_listbox.curselection()
    if selected:
        expression = history_listbox.get(selected[0]).split('=')[0].strip()
        equation.set(expression)

# --- Main Window ---
root = tk.Tk()
root.title("Scientific Calculator (Degrees)")
root.geometry("600x600")
root.config(bg="#1e1e1e")

expression = ""
equation = tk.StringVar()

# --- Display ---
display = tk.Entry(root, textvariable=equation, font=("Arial", 20),
                   bg="#2d2d2d", fg="white", bd=10, relief="ridge", justify="right")
display.grid(row=0, column=0, columnspan=5, ipadx=8, ipady=15, pady=15)

# --- Number & Operator Buttons ---
buttons = [
    ("7",1,0), ("8",1,1), ("9",1,2), ("/",1,3), ("√",1,4),
    ("4",2,0), ("5",2,1), ("6",2,2), ("*",2,3), ("x²",2,4),
    ("1",3,0), ("2",3,1), ("3",3,2), ("-",3,3), ("^",3,4),
    ("0",4,0), (".",4,1), ("=",4,2), ("+",4,3), ("%",4,4),
    ("(",5,0), (")",5,1)
]

for (text, row, col) in buttons:
    if text == "=":
        b = tk.Button(root, text=text, font=("Arial", 16, "bold"), bg="#4CAF50", fg="white",
                      command=equalpress, height=2, width=5)
    elif text == "√":
        b = tk.Button(root, text=text, font=("Arial", 16, "bold"), bg="#444", fg="white",
                      command=sqrt, height=2, width=5)
    elif text == "x²":
        b = tk.Button(root, text=text, font=("Arial", 16, "bold"), bg="#444", fg="white",
                      command=square, height=2, width=5)
    elif text == "^":
        b = tk.Button(root, text=text, font=("Arial", 16, "bold"), bg="#444", fg="white",
                      command=lambda: press("**"), height=2, width=5)
    elif text == "%":
        b = tk.Button(root, text=text, font=("Arial", 16, "bold"), bg="#444", fg="white",
                      command=lambda: press("/100"), height=2, width=5)
    else:
        b = tk.Button(root, text=text, font=("Arial", 16, "bold"), bg="#333", fg="white",
                      command=lambda t=text: press(t), height=2, width=5)
    b.grid(row=row, column=col, padx=5, pady=5)

# --- Extra scientific functions ---
extras = [
    ("sin",6,0, lambda: press("sin(")),
    ("cos",6,1, lambda: press("cos(")),
    ("tan",6,2, lambda: press("tan(")),
    ("log",6,3, log),
    ("ln",6,4, ln),
    ("π",7,0, lambda: press(str(math.pi))),
    ("e",7,1, lambda: press(str(math.e))),
    ("C",7,2, clear_all),
    ("⌫",7,3, backspace),
    ("History",7,4, toggle_history)
]

for (text, row, col, cmd) in extras:
    b = tk.Button(root, text=text, font=("Arial", 14, "bold"), bg="#555", fg="white",
                  command=cmd, height=2, width=6)
    b.grid(row=row, column=col, padx=5, pady=5)

# --- History Frame (Hidden by Default) ---
history_frame = tk.Frame(root, bg="#1e1e1e")
history_label = tk.Label(history_frame, text="History", bg="#1e1e1e", fg="white", font=("Arial", 14, "bold"))
history_label.pack(pady=5)

history_listbox = tk.Listbox(history_frame, width=25, height=25, bg="#2d2d2d", fg="white", selectbackground="#444")
history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
history_listbox.bind("<Double-1>", use_history)

scrollbar = tk.Scrollbar(history_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
history_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=history_listbox.yview)

# --- Keyboard Bindings ---
def key_press(event):
    key = event.char.lower()
    if key.isdigit() or key in "+-*/.%()":
        press(key)
    elif event.keysym == "KP_Divide":  # Numpad divide
        press("/")
    elif event.keysym == "Return":
        equalpress()
    elif event.keysym == "BackSpace":
        backspace()
    elif event.keysym == "Escape":
        clear_all()
    # --- Keyboard shortcuts for functions ---
    elif key == "s":
        press("sin(")
    elif key == "c":
        press("cos(")
    elif key == "t":
        press("tan(")
    elif key == "r":
        press(str(math.pi))

root.bind("<Key>", key_press)

root.mainloop()
