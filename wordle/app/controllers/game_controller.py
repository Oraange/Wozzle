from app.models.game_state import GameState
from app.models.word_loader import WordLoader


class GameController:
    """
    Wozzle 게임의 컨트롤러 클래스입니다. 게임 상태를 관리하고, 사용자 입력을 처리하며,
    모델과 뷰 간의 상호작용을 조정합니다.
    Args:
    - words_path: 단어 목록이 저장된 파일의 경로입니다.
    Attributes:
    - loader: WordLoader 인스턴스로, 단어 목록을 로드하고 유효성을 검사합니다.
    - state: 현재 게임 상태를 나타내는 GameState 인스턴스입니다.
    - view: 게임의 뷰를 나타내는 객체로, 컨트롤러가 뷰를 업데이트할 수 있도록 참조를 유지합니다.
    Methods:
    - _start_new_game(): 새로운 게임을 시작하고, 무작위 단어를 선택하여 게임 상태를 초기화합니다.
    - set_view(view): 뷰 객체를 설정하여 컨트롤러가 뷰를 업데이트할 수 있도록 합니다.
    - submit_guess(guess: str): 사용자의 입력을 처리하고 게임 상태를 업데이트합니다.
    """

    def __init__(self, words_path: str):
        self.loader = WordLoader(words_path)
        self.state = None
        self.view = None

    def _start_new_game(self):
        answer = self.loader.get_random_word()
        self.state = GameState(answer)
        print("Debug - New game started. Answer is:", answer)

    def set_view(self, view):
        self.view = view

    def submit_guess(self, guess: str):
        if len(guess) != len(self.state.answer):
            return  # Incomplete word

        if not self.loader.is_valid_word(guess):
            self.view.show_not_in_list_message()
            return  # Invalid word

        result = self.state.submit_guess(guess)

        if self.view:
            self.view.update_board()
            self.view.update_keyboard()

            if self.state.game_over:
                if self.state.win:
                    old_high_score = self.view.high_score
                    self.view.increment_win_count()

                    # 새로운 기록 달성 메시지
                    if self.view.win_count > old_high_score:
                        message = (
                            f"🎉 Congratulations! You've won!\n"
                            f"🏆 NEW HIGH SCORE: {self.view.win_count}!"
                        )
                    else:
                        message = (
                            f"Congratulations! You've won!\n"
                            f"Win Streak: {self.view.win_count}"
                        )
                    self.view.show_message(message)
                else:
                    self.view.reset_win_count()
                    self.view.show_message(
                        f"Game Over! The word was {self.state.answer}"
                    )

        return result
