import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os

# --- File for persistent storage ---
CONTACTS_FILE = "contacts.json"

# --- Load / Save contacts ---
def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as f:
            return json.load(f)
    return []

def save_contacts():
    with open(CONTACTS_FILE, "w") as f:
        json.dump(contacts, f, indent=4)

# --- Global contacts list ---
contacts = load_contacts()

# --- Functions ---
def update_treeview(filter_text=""):
    contact_tree.delete(*contact_tree.get_children())
    for idx, contact in enumerate(contacts):
        name, phone, email, address = contact["name"], contact["phone"], contact["email"], contact.get("address", "")
        if (filter_text.lower() in name.lower() or
            filter_text.lower() in phone.lower() or
            filter_text.lower() in email.lower() or
            filter_text.lower() in address.lower()):
            contact_tree.insert("", "end", iid=idx, values=(name, phone, email, address))

def clear_entries():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

def add_or_update_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()
    address = address_entry.get().strip()

    if not name or not phone:
        messagebox.showerror("Error", "Name and Phone are required!")
        return

    selected = contact_tree.selection()
    contact_data = {"name": name, "phone": phone, "email": email, "address": address}

    if selected:
        idx = int(selected[0])
        contacts[idx] = contact_data
        contact_tree.selection_remove(selected[0])
    else:
        contacts.append(contact_data)

    save_contacts()
    update_treeview(search_entry.get())
    clear_entries()
    name_entry.focus_set()

def delete_contact():
    selected = contact_tree.selection()
    if selected:
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this contact?"):
            idx = int(selected[0])
            contacts.pop(idx)
            save_contacts()
            update_treeview(search_entry.get())
    else:
        messagebox.showwarning("Warning", "Select a contact to delete.")

def on_tree_select(event):
    selected = contact_tree.selection()
    if selected:
        idx = int(selected[0])
        contact = contacts[idx]
        name_entry.delete(0, tk.END)
        name_entry.insert(0, contact["name"])
        phone_entry.delete(0, tk.END)
        phone_entry.insert(0, contact["phone"])
        email_entry.delete(0, tk.END)
        email_entry.insert(0, contact["email"])
        address_entry.delete(0, tk.END)
        address_entry.insert(0, contact.get("address", ""))

def live_search(event):
    query = search_entry.get().strip()
    update_treeview(query)

# --- Main Window ---
root = tk.Tk()
root.title("Professional Contact Book")
root.geometry("850x600")

# --- Background (Gradient effect with Canvas) ---
canvas = tk.Canvas(root, width=850, height=600, highlightthickness=0)
canvas.pack(fill="both", expand=True)

for i in range(0, 600):
    color = f"#{20+i//10:02x}{20+i//15:02x}{30+i//20:02x}"
    canvas.create_line(0, i, 850, i, fill=color)

# --- Main Frame on top of background ---
main_frame = tk.Frame(root, bg="#1e1e1e")
main_frame.place(relx=0.5, rely=0.5, anchor="center")

# --- Labels and Entries ---
tk.Label(main_frame, text="Name:", bg="#1e1e1e", fg="white", font=("Arial", 12)).pack(pady=(10,0))
name_entry = tk.Entry(main_frame, font=("Arial", 12), width=50, bg="#2d2d2d", fg="white", insertbackground="white")
name_entry.pack(pady=5)

tk.Label(main_frame, text="Phone:", bg="#1e1e1e", fg="white", font=("Arial", 12)).pack(pady=(10,0))
phone_entry = tk.Entry(main_frame, font=("Arial", 12), width=50, bg="#2d2d2d", fg="white", insertbackground="white")
phone_entry.pack(pady=5)

tk.Label(main_frame, text="Email:", bg="#1e1e1e", fg="white", font=("Arial", 12)).pack(pady=(10,0))
email_entry = tk.Entry(main_frame, font=("Arial", 12), width=50, bg="#2d2d2d", fg="white", insertbackground="white")
email_entry.pack(pady=5)

tk.Label(main_frame, text="Address:", bg="#1e1e1e", fg="white", font=("Arial", 12)).pack(pady=(10,0))
address_entry = tk.Entry(main_frame, font=("Arial", 12), width=50, bg="#2d2d2d", fg="white", insertbackground="white")
address_entry.pack(pady=5)

# --- Buttons ---
button_frame = tk.Frame(main_frame, bg="#1e1e1e")
button_frame.pack(pady=10)
tk.Button(button_frame, text="Add / Update Contact", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
          command=add_or_update_contact, width=18).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Delete Contact", font=("Arial", 12, "bold"), bg="#f44336", fg="white",
          command=delete_contact, width=15).grid(row=0, column=1, padx=5)

# --- Search ---
tk.Label(main_frame, text="Search:", bg="#1e1e1e", fg="white", font=("Arial", 12)).pack(pady=(10,0))
search_entry = tk.Entry(main_frame, font=("Arial", 12), width=50, bg="#2d2d2d", fg="white", insertbackground="white")
search_entry.pack(pady=5)
search_entry.bind("<KeyRelease>", live_search)

# --- Treeview ---
columns = ("Name", "Phone", "Email", "Address")
contact_tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=10)
for col in columns:
    contact_tree.heading(col, text=col)
    contact_tree.column(col, width=180)
contact_tree.pack(pady=10)
contact_tree.bind("<<TreeviewSelect>>", on_tree_select)

# --- Key Bindings ---
name_entry.bind("<Return>", lambda e: phone_entry.focus_set())
phone_entry.bind("<Return>", lambda e: email_entry.focus_set())
email_entry.bind("<Return>", lambda e: address_entry.focus_set())
address_entry.bind("<Return>", lambda e: add_or_update_contact())

# --- Initial Load ---
update_treeview()
name_entry.focus_set()

root.mainloop()
