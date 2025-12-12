from enum import Enum, auto
from app.core.settings import MAX_ATTEMPTS, WORD_LENGTH


class LetterState(Enum):
    CORRECT = auto()
    PRESENT = auto()
    ABSENT = auto()


class GameState:
    def __init__(self, answer: str):
        self.answer = answer.upper()  # The correct word to guess
        self.current_guess = []
        self.attempt_index = 0
        self.attempts = []  # List of attempts made
        self.game_over = False
        self.win = False

    def add_letter(self, letter: str):
        if len(self.current_guess) < WORD_LENGTH:
            self.current_guess.append(letter.upper())

    def remove_letter(self):
        if self.current_guess:
            self.current_guess.pop()

    def is_complete(self):
        return len(self.current_guess) == WORD_LENGTH

    def submit_guess(self, guess: str) -> list[str] | None:
        if self.game_over:
            return None

        guess = guess.upper()
        result = self._evaluate_guess(guess)
        self.attempts.append((guess, result))
        self.attempt_index += 1

        if guess == self.answer:
            self.win = True
            self.game_over = True
        elif len(self.attempts) >= MAX_ATTEMPTS:
            self.game_over = True

        self.current_guess = []

        return result

    def _evaluate_guess(self, guess: str) -> list[str]:
        result = [LetterState.ABSENT] * WORD_LENGTH
        answer_chars = list(self.answer)

        for i in range(WORD_LENGTH):
            if guess[i] == self.answer[i]:
                result[i] = LetterState.CORRECT
                answer_chars[i] = None  # Mark this char as used

        for i in range(WORD_LENGTH):
            if result[i] == LetterState.CORRECT:
                continue
            if guess[i] in answer_chars:
                result[i] = LetterState.PRESENT
                answer_chars[answer_chars.index(guess[i])] = None  # Mark as used

        return result
