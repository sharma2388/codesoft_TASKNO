import tkinter as tk
import random

class RPSGame:
    def __init__(self, master):
        self.master = master
        master.title("Rock Paper Scissors")
        master.geometry("600x500")
        master.config(bg="#1e1e1e")

        # --- Game State ---
        self.user_score = 0
        self.computer_score = 0
        self.ties = 0
        self.history_list = []

        self.emoji_map = {
            "Rock": "✊",
            "Paper": "✋",
            "Scissors": "✌️"
        }

        # --- UI ---
        self.create_widgets()
        self.master.bind("<Key>", self.key_press)

    # --- Game Logic ---
    def determine_winner(self, user_choice, computer_choice):
        if user_choice == computer_choice:
            return "tie"
        winning_map = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}
        if winning_map[user_choice] == computer_choice:
            return "win"
        return "lose"

    # --- UI Update ---
    def update_ui(self, result, user_choice, computer_choice):
        user_emoji = self.emoji_map[user_choice]
        computer_emoji = self.emoji_map[computer_choice]

        if result == "tie":
            text = f"Tie! {user_choice} {user_emoji} = {computer_choice} {computer_emoji}"
            self.ties += 1
        elif result == "win":
            text = f"You Win! {user_choice} {user_emoji} beats {computer_choice} {computer_emoji}"
            self.user_score += 1
        else:
            text = f"You Lose! {user_choice} {user_emoji} loses to {computer_choice} {computer_emoji}"
            self.computer_score += 1

        self.result_var.set(text)
        self.score_var.set(f"Your Score: {self.user_score} | Computer Score: {self.computer_score} | Ties: {self.ties}")
        self.user_battle_label.config(text=user_emoji)
        self.computer_battle_label.config(text=computer_emoji)

        # Efficient history update
        self.history_list.append(text)
        if len(self.history_list) > 10:
            self.history_list = self.history_list[-10:]
        self.history_listbox.delete(0, tk.END)
        for item in self.history_list:
            self.history_listbox.insert(tk.END, item)

    # --- Button / Key Handlers ---
    def play(self, user_choice):
        computer_choice = random.choice(list(self.emoji_map.keys()))
        result = self.determine_winner(user_choice, computer_choice)
        self.update_ui(result, user_choice, computer_choice)

    def reset_scores(self):
        self.user_score = 0
        self.computer_score = 0
        self.ties = 0
        self.history_list = []
        self.score_var.set(f"Your Score: {self.user_score} | Computer Score: {self.computer_score} | Ties: {self.ties}")
        self.result_var.set("")
        self.history_listbox.delete(0, tk.END)
        self.user_battle_label.config(text="")
        self.computer_battle_label.config(text="")

    def key_press(self, event):
        key_map = {"r": "Rock", "p": "Paper", "s": "Scissors"}
        if event.char.lower() in key_map:
            self.play(key_map[event.char.lower()])

    # --- UI Setup ---
    def create_widgets(self):
        tk.Label(self.master, text="Rock Paper Scissors", font=("Arial", 18, "bold"),
                 bg="#1e1e1e", fg="white").pack(pady=10)

        # Emoji battle display
        battle_frame = tk.Frame(self.master, bg="#1e1e1e")
        battle_frame.pack(pady=10)
        self.user_battle_label = tk.Label(battle_frame, text="", font=("Arial", 50), bg="#1e1e1e", fg="white")
        self.user_battle_label.grid(row=0, column=0, padx=50)
        self.computer_battle_label = tk.Label(battle_frame, text="", font=("Arial", 50), bg="#1e1e1e", fg="white")
        self.computer_battle_label.grid(row=0, column=1, padx=50)
        tk.Label(battle_frame, text="You", font=("Arial", 12), bg="#1e1e1e", fg="white").grid(row=1, column=0)
        tk.Label(battle_frame, text="Computer", font=("Arial", 12), bg="#1e1e1e", fg="white").grid(row=1, column=1)

        # Buttons
        button_frame = tk.Frame(self.master, bg="#1e1e1e")
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="✊ Rock", font=("Arial", 14, "bold"), width=12, bg="#555", fg="white",
                  command=lambda: self.play("Rock")).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="✋ Paper", font=("Arial", 14, "bold"), width=12, bg="#555", fg="white",
                  command=lambda: self.play("Paper")).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="✌️ Scissors", font=("Arial", 14, "bold"), width=12, bg="#555", fg="white",
                  command=lambda: self.play("Scissors")).grid(row=0, column=2, padx=5)

        # Result display
        self.result_var = tk.StringVar()
        tk.Label(self.master, textvariable=self.result_var, font=("Arial", 14), bg="#1e1e1e", fg="white",
                 wraplength=550).pack(pady=10)

        # Score display
        self.score_var = tk.StringVar()
        self.score_var.set(f"Your Score: {self.user_score} | Computer Score: {self.computer_score} | Ties: {self.ties}")
        tk.Label(self.master, textvariable=self.score_var, font=("Arial", 14, "bold"), bg="#1e1e1e", fg="white").pack(pady=5)

        # Reset button
        tk.Button(self.master, text="Reset Scores", font=("Arial", 12, "bold"), bg="#f44336", fg="white",
                  command=self.reset_scores).pack(pady=5)

        # History listbox
        history_frame = tk.Frame(self.master, bg="#1e1e1e")
        history_frame.pack(pady=10)
        tk.Label(history_frame, text="Last 10 Rounds:", bg="#1e1e1e", fg="white").pack()
        self.history_listbox = tk.Listbox(history_frame, width=70, height=6, bg="#2d2d2d", fg="white")
        self.history_listbox.pack()

# --- Run Game ---
root = tk.Tk()
game = RPSGame(root)
root.mainloop()
