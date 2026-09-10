import os
import sys
import tkinter as tk
from threading import Thread
from app.core.settings import WINDOW_TITLE, WINDOW_SIZE
from app.views.board_view import BoardView
from app.views.keyboard_view import KeyboardView


class MainView:
    def __init__(self, controller):
        self.controller = controller
        self.controller.set_view(self)

        # highscore.txt를 AppData/Roaming/wozzle에 저장
        self.app_data_dir = os.path.join(os.getenv("APPDATA"), "wozzle")
        os.makedirs(self.app_data_dir, exist_ok=True)
        self.SCORE_PATH = os.path.join(self.app_data_dir, "highscore.txt")

        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.attributes("-alpha", 0.2)
        self.root.geometry(WINDOW_SIZE)
        self.root.bind("<Key>", self._on_key_event)

        self.board = BoardView(self.root, controller)
        self.board.pack(pady=20)

        self.current_guess = ""

        self.keyboard = KeyboardView(self.root, controller)
        self.keyboard.pack(pady=10)

        self.win_count = 0
        self.win_count_label = tk.Label(
            self.root,
            text=f"Win Streak: {self.win_count}",
            font=("Helvetica", 12, "bold"),
            fg="#333333",
        )
        self.win_count_label.pack(anchor="w", padx=10, pady=(10, 5))

        # Load high score from file
        self.high_score = self._load_high_score()
        self.high_score_label = tk.Label(
            self.root,
            text=f"High Score: {self.high_score}",
            font=("Helvetica", 12, "bold"),
            fg="#333333",
        )
        self.high_score_label.pack(anchor="w", padx=10, pady=(0, 10))

    def _load_high_score(self):
        """highscore.txt 파일에서 최고 기록을 읽어옵니다."""
        try:
            with open(self.SCORE_PATH, "r") as f:
                content = f.read().strip()
                if content.isdigit():
                    return int(content)
        except FileNotFoundError:
            # 파일이 없으면 0으로 초기화
            pass
        return 0

    def _save_high_score(self):
        """현재 최고 기록을 highscore.txt 파일에 비동기로 저장합니다."""

        def save_task():
            try:
                with open(self.SCORE_PATH, "w") as f:
                    f.write(str(self.high_score))
            except Exception as e:
                print(f"Failed to save high score: {e}")

        thread = Thread(target=save_task, daemon=True)
        thread.start()

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

    def increment_win_count(self):
        """연속 승리 카운트를 1 증가시키고 UI를 업데이트합니다."""
        self.win_count += 1
        self.win_count_label.config(text=f"Win Streak: {self.win_count}")

        # High score 체크 및 업데이트
        if self.win_count > self.high_score:
            self.high_score = self.win_count
            self.high_score_label.config(text=f"High Score: {self.high_score}")
            self._save_high_score()

    def reset_win_count(self):
        """연속 승리 카운트를 0으로 초기화하고 UI를 업데이트합니다."""
        self.win_count = 0
        self.win_count_label.config(text=f"Win Streak: {self.win_count}")

    def show_message(self, message: str):
        popup = tk.Toplevel(self.root)
        popup.title("Result")

        def restart_game():
            popup.destroy()
            self.controller._start_new_game()
            self.reset_window()

        tk.Label(popup, text=message, font=("Helvetica", 16)).pack(pady=15)
        restart_btn = tk.Button(popup, text="Restart", command=restart_game)
        restart_btn.pack(padx=10, pady=10)

        # Enter 키를 누르면 Restart 버튼 클릭
        popup.bind("<Return>", lambda event: restart_game())

        # 팝업에 포커스를 주어 키 입력이 바로 작동하도록 함
        popup.focus_set()

    def reset_window(self):
        self.current_guess = ""

        for r in range(len(self.board.labels)):
            for c in range(len(self.board.labels[r])):
                self.board.labels[r][c].config(text="", bg="white", fg="black")

        for _, btn in self.keyboard.buttons.items():
            btn.config(bg="SystemButtonFace", fg="black")

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
