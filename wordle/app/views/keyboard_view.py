import tkinter as tk

from app.models.game_state import LetterState


class KeyboardView(tk.Frame):
    KEYS = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.buttons = {}

        for r, row in enumerate(self.KEYS):
            for c, ch in enumerate(row):
                btn = tk.Button(
                    self,
                    text=ch,
                    width=4,
                    command=lambda k=ch: self.on_click(k),
                )
                btn.grid(row=r, column=c, padx=2, pady=2)
                self.buttons[ch] = btn

    def on_click(self, key: str):
        self.controller.view.on_keyboard_input(key)

    def update_colors(self):
        attempts = self.controller.state.attempts
        used = {}

        priority = {
            LetterState.CORRECT: 3,
            LetterState.PRESENT: 2,
            LetterState.ABSENT: 1,
        }

        for guess, result in attempts:
            for i, ch in enumerate(guess.upper()):
                state = result[i]
                if ch not in used or priority[state] > priority[used[ch]]:
                    used[ch] = state

        for ch, state in used.items():
            btn = self.buttons.get(ch)
            if not btn:
                continue
            if state == LetterState.CORRECT:
                btn.config(bg="green", fg="white")
            elif state == LetterState.PRESENT:
                btn.config(bg="orange", fg="black")
            else:
                btn.config(bg="gray", fg="white")
