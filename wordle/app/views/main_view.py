import tkinter as tk
from app.core.settings import WINDOW_TITLE, WINDOW_SIZE
from app.views.board_view import BoardView
from app.views.keyboard_view import KeyboardView


class MainView:
    def __init__(self, controller):
        self.controller = controller
        self.controller.set_view(self)

        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.bind("<Key>", self._on_key_event)

        # Content frame to hold board and instruction side by side
        content_frame = tk.Frame(self.root)
        content_frame.pack(pady=20, padx=10, fill="x")

        # Left side: Board
        left_frame = tk.Frame(content_frame)
        left_frame.pack(side="left", anchor="n")

        self.board = BoardView(left_frame, controller)
        self.board.pack()

        # Right side: Instruction box
        right_frame = tk.Frame(
            content_frame, bg="#f0f0f0", relief="ridge", borderwidth=2
        )
        right_frame.pack(side="left", padx=(15, 0), anchor="n", fill="both")

        instr_title = tk.Label(
            right_frame,
            text="🎯 How to Play Hardle",
            font=("Helvetica", 13, "bold"),
            bg="#f0f0f0",
            fg="#333333",
        )
        instr_title.pack(anchor="w", padx=10, pady=(10, 5))

        instr_text = tk.Label(
            right_frame,
            text=(
                "Guess TWO 5-letter words!\n\n"
                "Colors mean:\n"
                "⬜ Gray: not in either word\n"
                "🟨 Yellow: in 1 word, wrong pos\n"
                "🟩 Y-Green: in 1 word, correct pos\n"
                "🟧 Orange: in 2 words, wrong pos\n"
                "🔵 Sky Blue: in 2 words, 1 correct\n"
                "💙 Blue: in 2 words, both correct\n\n"
                "You have 10 attempts.\n"
                "Win by guessing both words!"
            ),
            justify="left",
            wraplength=220,
            bg="#f0f0f0",
            fg="#333333",
            font=("Helvetica", 9),
        )
        instr_text.pack(anchor="w", padx=10, pady=(0, 10))

        self.current_guess = ""

        # Keyboard below
        self.keyboard = KeyboardView(self.root, controller)
        self.keyboard.pack(pady=10)

    def run(self):
        self.controller._start_new_game()
        self.root.mainloop()

    def on_key_letter(self, ch: str):
        if not self.controller.state:
            return

        if len(ch) == 1 and ch.isalpha():
            self.controller.state.add_letter(ch.upper())
            self.update_current_row()

    def on_key_backspace(self):
        if not self.controller.state:
            return

        self.controller.state.remove_letter()
        self.update_current_row()

    def on_key_enter(self):
        if not self.controller.state:
            return

        if self.controller.state.is_complete():
            guess = "".join(self.controller.state.current_guess)
            self.controller.submit_guess(guess)
            self.update_current_row()

    def _on_key_event(self, event):
        key = event.keysym
        ch = event.char.upper()
        if key == "BackSpace":
            self.on_key_backspace()
        elif key == "Return":
            self.on_key_enter()
        elif ch and ch.isalpha() and len(ch) == 1:
            self.on_key_letter(ch)

        return

    def update_current_row(self):
        self.board.update_current_row()

    def update_board(self):
        self.board.refresh()

    def update_keyboard(self):
        self.keyboard.update_colors()

    def show_message(self, message: str):
        popup = tk.Toplevel(self.root)
        popup.title("Result")

        def restart_game():
            popup.destroy()
            self.controller._start_new_game()
            self.reset_window()

        tk.Label(popup, text=message, font=("Helvetica", 16)).pack(pady=15)
        tk.Button(popup, text="Restart", command=restart_game).pack(padx=10, pady=10)

    def reset_window(self):
        self.current_guess = ""

        from app.core.settings import COLOR_EMPTY, KEY_BG, KEY_FG

        for r in range(len(self.board.labels)):
            for c in range(len(self.board.labels[r])):
                self.board.labels[r][c].config(text="", bg=COLOR_EMPTY, fg="black")

        for _, btn in self.keyboard.buttons.items():
            btn.config(bg=KEY_BG, fg=KEY_FG)

    # deprecated
    def flash_invalid_word(self):
        overlay = tk.Frame(
            self.root,
            bg="#FFFFFF",
            width=self.root.winfo_width(),
            height=self.root.winfo_height(),
        )
        overlay.place(x=0, y=0)

        overlay.configure(bg="#F3A8A8")
        self.root.after(100, overlay.destroy)

    def show_not_in_list_message(self):
        if hasattr(self, "invalid_label") and self.invalid_label.winfo_exists():
            return

        self.invalid_label = tk.Label(
            self.root,
            text="Not in word list",
            font=("Helvetica", 12, "bold"),
            fg="#FF5555",
            bg=self.root["bg"],
        )
        self.invalid_label.place(relx=0.5, rely=0.1, anchor="center")

        self.fade_out_text(self.invalid_label, 100)

    def fade_out_text(self, label, alpha):
        if alpha <= 0:
            label.destroy()
            return

        r = int(255 - (255 - 230) * (1 - alpha / 100))
        g = int(85 - (85 - 230) * (1 - alpha / 100))
        b = int(85 - (85 - 230) * (1 - alpha / 100))

        label.config(fg=f"#{r:02x}{g:02x}{b:02x}")
        self.root.after(5, lambda: self.fade_out_text(label, alpha - 2))
