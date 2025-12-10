from app.models.game_state import GameState
from app.models.word_loader import WordLoader


class GameController:
    def __init__(self, words_path: str):
        self.loader = WordLoader(words_path)
        self.state = None
        self.view = None

    def _start_new_game(self):
        answer = self.loader.get_random_word()
        self.state = GameState(answer)

    def set_view(self, view):
        self.view = view

    def submit_guess(self, guess: str):
        if len(guess) != len(self.state.answer):
            return  # Incomplete word

        if not self.loader.is_valid_word(guess):
            self.view.flash_invalid_word()
            self.view.current_guess = ""
            self.view.input_label.config(text="")
            return  # Invalid word

        result = self.state.submit_guess(guess)

        if self.view:
            self.view.update_board()
            self.view.update_keyboard()

            if self.state.game_over:
                if self.state.win:
                    self.view.show_message("Congratulations! You've won!")
                else:
                    self.view.show_message(
                        f"Game Over! The word was {self.state.answer}"
                    )

        return result
