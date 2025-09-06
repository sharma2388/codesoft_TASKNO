import tkinter as tk
from tkinter import messagebox

# Create main window
root = tk.Tk()
root.title("To-Do List (Dark Mode)")
root.geometry("700x550")
root.config(bg="#1e1e1e")  # dark background

tasks = []  # store (task, deadline, priority, done_status)

# Functions
def refresh_listbox():
    """Update the listbox with serial numbers, deadlines, priorities, and done marks."""
    listbox.delete(0, tk.END)
    for i, (task, deadline, priority, done) in enumerate(tasks, start=1):
        status = "✔ Done" if done else f"Deadline: {deadline}, Priority: {priority}"
        listbox.insert(tk.END, f"{i}. {task}  ({status})")

def add_task(event=None):
    task = entry_task.get().strip()
    deadline = entry_deadline.get().strip()
    priority = priority_var.get()

    if task != "" and deadline != "" and priority != "Priorities":
        tasks.append((task, deadline, priority, False))  # False = not done
        refresh_listbox()
        entry_task.delete(0, tk.END)
        entry_deadline.delete(0, tk.END)
        priority_var.set("Priorities")  # reset to default
        entry_task.focus()  # back to task box
    else:
        messagebox.showwarning("Warning", "Please enter a task, deadline, and priority.")

def delete_task():
    try:
        selected = listbox.curselection()[0]
        tasks.pop(selected)
        refresh_listbox()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to delete.")

def clear_tasks():
    tasks.clear()
    refresh_listbox()

def mark_done():
    try:
        selected = listbox.curselection()[0]
        task, deadline, priority, _ = tasks[selected]
        tasks[selected] = (task, deadline, priority, True)  # mark as done
        refresh_listbox()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to mark as done.")

# --- Widgets ---
frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(pady=10)

listbox = tk.Listbox(
    frame, width=85, height=12,
    bg="#2d2d2d", fg="#ffffff",
    selectbackground="#444444",
    font=("Arial", 11)
)
listbox.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar = tk.Scrollbar(frame, bg="#1e1e1e")
scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Entry fields
entry_task = tk.Entry(root, width=40, font=("Arial", 12), bg="#2d2d2d", fg="white", insertbackground="white")
entry_task.pack(pady=5)
entry_task.insert(0, "Enter task here")

entry_deadline = tk.Entry(root, width=40, font=("Arial", 12), bg="#2d2d2d", fg="white", insertbackground="white")
entry_deadline.pack(pady=5)
entry_deadline.insert(0, "Enter deadline (e.g., 18:30 or Tomorrow 10 AM)")

# Priority dropdown (default = "Priorities")
priority_var = tk.StringVar(value="Priorities")
priority_menu = tk.OptionMenu(root, priority_var, "High", "Medium", "Low")
priority_menu.config(width=15, font=("Arial", 10, "bold"), bg="#444444", fg="white")
priority_menu.pack(pady=5)

# --- Key Bindings ---
def move_to_deadline(event):
    entry_deadline.focus()  # jump to deadline box

entry_task.bind("<Return>", move_to_deadline)     # Enter in task → go to deadline
entry_deadline.bind("<Return>", add_task)         # Enter in deadline → save task

# Buttons (Dark Mode Colors)
add_button = tk.Button(
    root, text="Add Task", width=15,
    bg="#4CAF50", fg="white",
    font=("Arial", 10, "bold"), command=add_task
)
add_button.pack(pady=5)

done_button = tk.Button(
    root, text="✔ Mark as Done", width=15,
    bg="#2196F3", fg="white",
    font=("Arial", 10, "bold"), command=mark_done
)
done_button.pack(pady=5)

delete_button = tk.Button(
    root, text="Delete Task", width=15,
    bg="#f44336", fg="white",
    font=("Arial", 10, "bold"), command=delete_task
)
delete_button.pack(pady=5)

clear_button = tk.Button(
    root, text="Clear All", width=15,
    bg="#555555", fg="white",
    font=("Arial", 10, "bold"), command=clear_tasks
)
clear_button.pack(pady=5)

# Run app
root.mainloop()
