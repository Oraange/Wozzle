import tkinter as tk
from functools import partial


from app.core.settings import *
from app.controllers.game_controller import GameController
from app.models.game_state import LetterState


class KeyboardView(tk.Frame):
    """
    KeyboardView 클래스는 Wordle 스타일 퍼즐의 가상 키보드를 Tkinter Frame
    으로 렌더링하고, 게임 상태에 따라 각 키의 색상을 갱신하는 역할을 합니다.
    Explanation:
    - 키보드는 세 줄로 구성되며, 각 줄은 문자열로 표현됩니다.
    - 각 키는 초기화 시 기본 색상으로 생성됩니다.
    - 컨트롤러의 상태(controller.state.attempts)를 참조하여 시도(guess)와 결과(result)에
        따라 각 키의 배경/전경 색상을 업데이트합니다.
    Args:
    - master: Tkinter의 부모 위젯(주로 루트나 다른 프레임).
    - controller: 게임 상태와 로직에 접근할 수 있는 컨트롤러 객체. 반드시
        controller.state.attempts 를 제공해야 하며, attempts는 (guess, result) 튜플들의
        순서열이어야 합니다.
    Attributes:
    - buttons: 생성된 tk.Button 객체들의 딕셔너리. 키는 문자, 값은 해당 버튼 객체.
    - controller: 생성자에 전달된 컨트롤러 참조.
    Methods:
    - on_click(key: str):
            - 키가 클릭되었을 때 호출되는 콜백 함수.
            - controller.view.on_keyboard_input(key) 를 호출하여 입력을 처리함.
    - update_colors():
            - controller.state.attempts 를 순회하면서 각 시도에 대해 문자(guess)와 결과(result)를
                참조.
            - 결과(result)는 각 문자 위치별 LetterState 값을 포함한다고 가정하며,
                LetterState.CORRECT -> 초록색 배경 (전경색: 흰색)
                LetterState.PRESENT -> 주황색 배경 (전경색: 검정색)
                그 외 (absent) -> 회색 배경 (전경색: 흰색) 으로 버튼 배경을 설정함.
    """

    def __init__(self, master, controller: GameController):
        super().__init__(master)
        self.controller = controller
        self.buttons = {}
        self.frame = tk.Frame(master, bg=master["bg"])
        self.frame.pack(pady=20)

        self.keys = {}
        self._build_keyboard()

    def _build_keyboard(self):
        rows = [
            list("QWERTYUIOP"),
            list("ASDFGHJKL"),
            ["Enter"] + list("ZXCVBNM") + ["Backspace"],
        ]

        for r_index, row_keys in enumerate(rows):
            row_frame = tk.Frame(self.frame, bg=self.frame["bg"])
            row_frame.pack(pady=6)

            for key in row_keys:
                if key == "Enter":
                    width = 4
                elif key == "Backspace":
                    width = 8
                else:
                    width = 2

                btn = tk.Button(
                    row_frame,
                    text=key,
                    width=width,
                    height=1,
                    bg=KEY_BG,
                    fg=KEY_FG,
                    font=KEY_FONT,
                    relief="raised",
                    bd=2,
                    command=partial(self.on_click, key),
                )

                btn.pack(side="left", padx=4)
                self.buttons[key] = btn

    def on_click(self, key: str):
        if key == "Enter":
            self.controller.view.on_key_enter()
        elif key == "Backspace":
            self.controller.view.on_key_backspace()
        else:
            self.controller.view.on_key_letter(key)

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
