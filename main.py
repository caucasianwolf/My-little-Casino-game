import json
import os
import random
import sys
import tkinter as tk
from tkinter import messagebox, simpledialog

_BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
LEADERBOARD_FILE = os.path.join(_BASE_DIR, "leaderboard.json")


def points_for_round(r):
    if r <= 10:
        return 10
    if r <= 20:
        return 25
    if r <= 30:
        return 50
    return 100


def ensure_leaderboard_file():
    if not os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


def load_leaderboard():
    ensure_leaderboard_file()
    with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return []


def save_leaderboard(board):
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(board, f, ensure_ascii=False, indent=2)


class GameApp:
    def __init__(self, root):
        self.root = root
        root.title("Higher or Lower — Casino Guess")
        root.geometry("420x560")
        root.resizable(False, False)

        # Casino-themed colors
        self.bg = "#0b6b3a"
        self.panel = "#153b2b"
        self.accent = "#d4af37"

        root.configure(bg=self.bg)

        # Decorative chip-like labels for a casino feel (created before other widgets)
        for x, y, size, color in [
            (40, 80, 28, '#e63946'),
            (360, 100, 24, '#f4a261'),
            (80, 420, 22, '#2a9d8f'),
            (320, 360, 26, '#e9c46a'),
            (220, 200, 20, '#e76f51'),
        ]:
            lbl_chip = tk.Label(root, text='◎', font=("Helvetica", size, 'bold'), bg=self.bg, fg=color)
            lbl_chip.place(x=x, y=y, anchor='center')

        # 777 logo
        self.logo_label = tk.Label(root, text="777", font=("Helvetica", 28, "bold"), bg=self.bg, fg="#ffd700")
        self.logo_label.place(relx=0.5, rely=0.05, anchor='n')

        header = tk.Label(root, text="Higher or Lower", font=("Helvetica", 20, "bold"), bg=self.bg, fg=self.accent)
        header.pack(pady=(12, 6))

        sub = tk.Label(root, text="Guess whether the next card is higher or lower.", font=("Helvetica", 10), bg=self.bg, fg="#ffffff")
        sub.pack(pady=(0, 8))

        self.card_frame = tk.Frame(root, bg=self.panel, bd=4, relief=tk.RIDGE)
        self.card_frame.pack(pady=12, ipadx=10, ipady=10)

        self.number_label = tk.Label(self.card_frame, text="--", font=("Helvetica", 72, "bold"), bg=self.panel, fg=self.accent)
        self.number_label.pack(padx=18, pady=10)

        info_frame = tk.Frame(root, bg=self.bg)
        info_frame.pack(pady=6)

        self.score_label = tk.Label(info_frame, text="Score: 0", font=("Helvetica", 12), bg=self.bg, fg="#ffffff")
        self.score_label.grid(row=0, column=0, padx=8)

        self.round_label = tk.Label(info_frame, text="Round: 1", font=("Helvetica", 12), bg=self.bg, fg="#ffffff")
        self.round_label.grid(row=0, column=1, padx=8)

        self.next_pts_label = tk.Label(info_frame, text="Next: 10 pts", font=("Helvetica", 12), bg=self.bg, fg="#ffffff")
        self.next_pts_label.grid(row=0, column=2, padx=8)

        self.tries_label = tk.Label(info_frame, text="Tries: 4", font=("Helvetica", 12), bg=self.bg, fg="#ffffff")
        self.tries_label.grid(row=0, column=3, padx=8)

        btn_frame = tk.Frame(root, bg=self.bg)
        btn_frame.pack(pady=12)

        self.higher_btn = tk.Button(btn_frame, text="Higher", width=10, height=2, bg=self.accent, fg="#102010", command=lambda: self.guess('higher'))
        self.higher_btn.grid(row=0, column=0, padx=10)

        self.lower_btn = tk.Button(btn_frame, text="Lower", width=10, height=2, bg=self.accent, fg="#102010", command=lambda: self.guess('lower'))
        self.lower_btn.grid(row=0, column=1, padx=10)

        control_frame = tk.Frame(root, bg=self.bg)
        control_frame.pack(pady=8)

        new_btn = tk.Button(control_frame, text="New Game", command=self.new_game)
        new_btn.grid(row=0, column=0, padx=6)

        lb_btn = tk.Button(control_frame, text="Leaderboard", command=self.show_leaderboard)
        lb_btn.grid(row=0, column=1, padx=6)

        self.message = tk.Label(root, text="Good luck!", font=("Helvetica", 12), bg=self.bg, fg="#ffffff")
        self.message.pack(pady=6)

        # Prominent lose overlay (hidden until loss)
        self.lose_overlay = tk.Label(root, text="YOU LOSE", font=("Helvetica", 36, "bold"), bg="#3b0000", fg="#ffd1a3")
        self.lose_overlay.place_forget()

        # Game state
        self.reset_state()

    def reset_state(self):
        self.round = 1
        self.score = 0
        self.tries = 4
        # Use 1-13 like cards for a casino feel (1->Ace, 11->J, 12->Q, 13->K)
        self.current = random.randint(1, 13)
        self.update_ui()

    def new_game(self):
        if messagebox.askyesno("Start New Game", "Start a new game? Current progress will be lost."):
            self.reset_state()

    def update_ui(self):
        self.number_label.config(text=self.card_text(self.current))
        self.score_label.config(text=f"Score: {self.score}")
        self.round_label.config(text=f"Round: {self.round}")
        self.next_pts_label.config(text=f"Next: {points_for_round(self.round)} pts")
        # update tries display if present
        try:
            self.tries_label.config(text=f"Tries: {self.tries}")
        except Exception:
            pass

    def card_text(self, n):
        # always show numbers (1-13)
        return str(n)

    def guess(self, direction):
        next_num = random.randint(1, 13)
        correct = False
        if next_num == self.current:
            # tie counts as incorrect (adds tension)
            correct = False
        else:
            if direction == 'higher' and next_num > self.current:
                correct = True
            if direction == 'lower' and next_num < self.current:
                correct = True

        # Reveal next card
        reveal = self.card_text(next_num)
        if correct:
            gained = points_for_round(self.round)
            self.score += gained
            self.message.config(text=f"Correct! Next was {reveal}. +{gained} pts", fg="#bfffbf")
            self.round += 1
            self.current = next_num
            self.update_ui()
        else:
            # decrement tries and continue unless out of tries
            self.tries -= 1
            if self.tries > 0:
                self.message.config(text=f"Wrong — next was {reveal}. Tries left: {self.tries}", fg="#ffbfbf")
                # move to the revealed card and continue
                self.current = next_num
                self.update_ui()
            else:
                self.message.config(text=f"Wrong — next was {reveal}.", fg="#ffbfbf")
                # show big lose message then end
                self.show_lose_overlay()
                # small delay so player sees the overlay before prompt
                self.root.after(400, lambda: self.end_game(next_num))

    def end_game(self, last_num):
        name = simpledialog.askstring("Game Over", f"Your score: {self.score}\nEnter your name for the leaderboard:")
        # hide overlay after player interaction
        self.hide_lose_overlay()
        if name:
            board = load_leaderboard()
            board.append({"name": name, "score": self.score})
            board = sorted(board, key=lambda x: x['score'], reverse=True)[:50]
            save_leaderboard(board)
            messagebox.showinfo("Saved", "Score saved to leaderboard.")
        else:
            messagebox.showinfo("Notice", "Score not saved.")
        # Reset for a fresh start
        self.reset_state()

    def show_lose_overlay(self):
        # place overlay centered and above other widgets
        self.lose_overlay.place(relx=0.5, rely=0.28, anchor='center')
        self.lose_overlay.lift()

    def hide_lose_overlay(self):
        self.lose_overlay.place_forget()

    def show_leaderboard(self):
        board = load_leaderboard()
        if not board:
            messagebox.showinfo("Leaderboard", "No entries yet.")
            return
        text = "Top Players:\n\n"
        for i, e in enumerate(sorted(board, key=lambda x: x['score'], reverse=True)[:10], start=1):
            text += f"{i}. {e['name']} — {e['score']}\n"
        messagebox.showinfo("Leaderboard", text)


if __name__ == "__main__":
    ensure_leaderboard_file()
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()
