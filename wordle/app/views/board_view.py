import tkinter as tk
from app.core.settings import *
from app.models.game_state import LetterState


class BoardView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.labels = []

        for r in range(MAX_ATTEMPTS):
            row_labels = []
            for c in range(WORD_LENGTH):
                lbl = tk.Label(
                    self,
                    text="",
                    width=4,
                    height=2,
                    font=("Helvetica", 24, "bold"),
                    highlightthickness=0,
                    bg=COLOR_EMPTY,
                    fg="black",
                    relief="solid",
                    borderwidth=2,
                )
                lbl.grid(row=r, column=c, padx=3, pady=3)
                row_labels.append(lbl)

            self.labels.append(row_labels)

    def refresh(self):
        attempts = self.controller.state.attempts
        for r, (guess, result) in enumerate(attempts):
            for c, ch in enumerate(guess):
                lbl = self.labels[r][c]
                lbl.config(text=ch.upper())

                if result[c] == LetterState.CORRECT:
                    lbl.config(bg=COLOR_CORRECT, fg="white")
                elif result[c] == LetterState.PRESENT:
                    lbl.config(bg=COLOR_PRESENT, fg="white")
                else:
                    lbl.config(bg=COLOR_ABSENT, fg="white")
