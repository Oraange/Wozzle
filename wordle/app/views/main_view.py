import tkinter as tk
from app.core.settings import WINDOW_TITLE, WINDOW_SIZE
from app.views.board_view import BoardView
from app.views.keyboard_view import KeyboardView


class MainView:
    def __init__(self, controller):
        self.controller = controller
        controller.set_view(self)

        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.bind("<Key>", self.on_key_press)

        self.board = BoardView(self.root, controller)
        self.board.pack(pady=20)

        self.current_guess = ""

        self.input_label = tk.Label(self.root, text="", font=("Helvetica", 22))
        self.input_label.pack(pady=10)

        self.keyboard = KeyboardView(self.root, controller)
        self.keyboard.pack()

    def run(self):
        self.controller._start_new_game()
        self.root.mainloop()

    def on_keyboard_input(self, key: str):
        if len(self.current_guess) < 5:
            self.current_guess += key.lower()
            self.input_label.config(text=self.current_guess.upper())

        if len(self.current_guess) == 5:
            self.controller.submit_guess(self.current_guess)
            self.current_guess = ""
            self.input_label.config(text="")

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
        self.input_label.config(text="")

        for r in range(len(self.board.labels)):
            for c in range(len(self.board.labels[r])):
                self.board.labels[r][c].config(text="", bg="white", fg="black")

        for ch, btn in self.keyboard.buttons.items():
            btn.config(bg="SystemButtonFace", fg="black")

    def on_key_press(self, event):
        key = event.char.upper()

        if key.isalpha() and len(key) == 1:
            self.on_keyboard_input(key)
            return

        if event.keysym == "BackSpace":
            self.current_guess = self.current_guess[:-1]
            self.input_label.config(text=self.current_guess.upper())
            return

        if event.keysym == "Return":
            if len(self.current_guess) == 5:
                self.controller.submit_guess(self.current_guess)
                self.current_guess = ""
                self.input_label.config(text="")

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
