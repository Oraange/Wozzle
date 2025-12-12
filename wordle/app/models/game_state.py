from enum import Enum, auto
from app.core.settings import MAX_ATTEMPTS, WORD_LENGTH


class LetterState(Enum):
    ABSENT = auto()  # 둘 다 포함 안함
    ONE_WRONG_POS = auto()  # 하나만 포함, 자리 틀림
    ONE_CORRECT_POS = auto()  # 하나만 포함, 자리 맞음
    TWO_WRONG_POS = auto()  # 둘 다 포함, 둘 다 자리 틀림
    TWO_ONE_CORRECT = auto()  # 둘 다 포함, 하나만 자리 맞음
    TWO_CORRECT_POS = auto()  # 둘 다 포함, 둘 다 자리 맞음


class GameState:
    def __init__(self, answer1: str, answer2: str):
        self.answer1 = answer1.upper()  # First word to guess
        self.answer2 = answer2.upper()  # Second word to guess
        self.current_guess = []
        self.attempt_index = 0
        self.attempts = []  # List of attempts made
        self.game_over = False
        self.win = False
        self.correct_count = 0  # 맞춘 단어 개수

    def add_letter(self, letter: str):
        if len(self.current_guess) < WORD_LENGTH:
            self.current_guess.append(letter.upper())

    def remove_letter(self):
        if self.current_guess:
            self.current_guess.pop()

    def is_complete(self):
        return len(self.current_guess) == WORD_LENGTH

    def submit_guess(self, guess: str) -> list[LetterState] | None:
        if self.game_over:
            return None

        guess = guess.upper()
        result = self._evaluate_guess(guess)
        self.attempts.append((guess, result))
        self.attempt_index += 1

        # 이전 시도에서 맞춘 단어가 있는지 체크
        matched_in_previous = set()
        if len(self.attempts) > 1:
            for prev_guess, _ in self.attempts[:-1]:
                if prev_guess == self.answer1:
                    matched_in_previous.add(self.answer1)
                if prev_guess == self.answer2:
                    matched_in_previous.add(self.answer2)

        # 현재 추측이 맞는지 체크
        current_matched = 0
        if guess == self.answer1 and self.answer1 not in matched_in_previous:
            current_matched += 1
        if guess == self.answer2 and self.answer2 not in matched_in_previous:
            current_matched += 1

        self.correct_count = len(matched_in_previous) + current_matched

        if self.correct_count >= 2:
            self.win = True
            self.game_over = True
        elif len(self.attempts) >= MAX_ATTEMPTS:
            self.game_over = True

        self.current_guess = []

        return result

    def _evaluate_guess(self, guess: str) -> list[LetterState]:
        result = [LetterState.ABSENT] * WORD_LENGTH

        for i in range(WORD_LENGTH):
            char = guess[i]
            in_answer1 = char in self.answer1
            in_answer2 = char in self.answer2
            pos_correct1 = self.answer1[i] == char if i < len(self.answer1) else False
            pos_correct2 = self.answer2[i] == char if i < len(self.answer2) else False

            # 둘 다 포함 안함
            if not in_answer1 and not in_answer2:
                result[i] = LetterState.ABSENT

            # 하나만 포함
            elif (in_answer1 and not in_answer2) or (in_answer2 and not in_answer1):
                pos_correct = pos_correct1 or pos_correct2
                if pos_correct:
                    result[i] = LetterState.ONE_CORRECT_POS  # 연두색
                else:
                    result[i] = LetterState.ONE_WRONG_POS  # 노란색

            # 둘 다 포함
            elif in_answer1 and in_answer2:
                correct_count = (1 if pos_correct1 else 0) + (1 if pos_correct2 else 0)
                if correct_count == 2:
                    result[i] = LetterState.TWO_CORRECT_POS  # 파란색
                elif correct_count == 1:
                    result[i] = LetterState.TWO_ONE_CORRECT  # 하늘색
                else:
                    result[i] = LetterState.TWO_WRONG_POS  # 주황색

        return result
