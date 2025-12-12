import tkinter as tk
from app.core.settings import *
from app.models.game_state import LetterState


class BoardView(tk.Frame):
    """
    BoardView 클래스는 Wordle 스타일 퍼즐의 게임 보드를 Tkinter Frame으로 렌더링하고
    게임 상태에 따라 각 칸(라벨)의 텍스트와 색상을 갱신하는 역할을 합니다.

    Explanation:
    - 보드는 MAX_ATTEMPTS x WORD_LENGTH 크기의 라벨 그리드로 구성됩니다.
    - 각 라벨은 초기화 시 빈 문자열과 COLOR_EMPTY 배경색으로 생성됩니다.
    - 컨트롤러의 상태(controller.state.attempts)를 참조하여 시도(guess)와 결과(result)에
        따라 각 칸의 문자 표시와 배경/전경 색상을 업데이트합니다.

    Args:
    - master: Tkinter의 부모 위젯(주로 루트나 다른 프레임).
    - controller: 게임 상태와 로직에 접근할 수 있는 컨트롤러 객체. 반드시
        controller.state.attempts 를 제공해야 하며, attempts는 (guess, result) 튜플들의
        순서열이어야 합니다.

    Attributes:
    - labels: 생성된 tk.Label 객체들의 2차원 리스트. 인덱스는 [시도번호][문자열 인덱스].
    - controller: 생성자에 전달된 컨트롤러 참조.

    Methods:
    - refresh():
            - controller.state.attempts 를 순회하면서 각 시도에 대해 문자(guess)를 대문자로
                라벨에 표시합니다.
            - 결과(result)는 각 문자 위치별 LetterState 값을 포함한다고 가정하며,
                LetterState.CORRECT -> COLOR_CORRECT (전경색: 흰색)
                LetterState.PRESENT -> COLOR_PRESENT (전경색: 흰색)
                그 외 (absent) -> COLOR_ABSENT (전경색: 흰색) 으로 라벨 배경을 설정합니다.
    """

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
                    width=2,
                    height=1,
                    font=("Helvetica", 18, "bold"),
                    highlightthickness=0,
                    bg=COLOR_EMPTY,
                    fg="black",
                    relief="solid",
                    borderwidth=2,
                )
                lbl.grid(row=r, column=c, padx=3, pady=3)
                row_labels.append(lbl)

            self.labels.append(row_labels)

    def update_current_row(self):
        if not self.controller.state:
            return

        guess = self.controller.state.current_guess
        for i in range(WORD_LENGTH):
            if self.controller.state.attempt_index >= MAX_ATTEMPTS:
                break
            lbl = self.labels[self.controller.state.attempt_index][i]
            if i < len(guess):
                lbl.config(text=guess[i].upper())
            else:
                lbl.config(text="")

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
