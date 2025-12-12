import os
import random


class WordLoader:
    def __init__(self, word_file_path: str):
        if not os.path.exists(word_file_path):
            raise FileNotFoundError(f"Word file not found: {word_file_path}")

        self.words = self._load_words(word_file_path)

        if not self.words:
            raise ValueError("Word list is empty")

        self.words = list(
            set(filter(lambda w: w.isalpha() and len(w) == 5, self.words))
        )

    def _load_words(self, path: str) -> list[str]:
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip().upper() for line in f if line.strip()]

    def get_random_word(self) -> str:
        return random.choice(self.words)

    def get_random_words(self, count: int = 2) -> list[str]:
        """중복 없이 랜덤으로 여러 단어를 선택합니다."""
        if count > len(self.words):
            raise ValueError(
                f"Not enough words. Requested: {count}, Available: {len(self.words)}"
            )
        return random.sample(self.words, count)

    def is_valid_word(self, word: str) -> bool:
        return word.upper() in self.words
