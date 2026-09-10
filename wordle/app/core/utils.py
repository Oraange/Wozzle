import os
from collections import defaultdict
import sys


class WordleSolver:
    def __init__(self):
        self.words = self.load_words()

    def load_words(self):
        word_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'words.txt')
        with open(word_path, 'r') as file:
            words = [line.strip().upper() for line in file.readlines()]

        return words

    def wordle_solver(self):
        self.words = self.load_words()
        def filter_words(word):
            match = True
            checked = defaultdict(int)
            for i, res in enumerate(result):
                checked[guess[i]] += 1
                if res == "G":
                    if word[i] != guess[i]:
                        match = False
                        break

                elif res == "Y":
                    if word[i] == guess[i] or guess[i] not in word:
                        match = False
                        break

                elif res == "B":
                    if word[i] == guess[i] or checked[guess[i]] <= word.count(guess[i]):
                        match = False
                        break

            return match

        try:
            while True:
                guess = input("Guess: ").strip().upper()
                if guess == "EXIT":
                    print("Exiting the solver.")
                    break

                if guess == "R":
                    self.reset_words()
                    print("Word list has been reset.")
                    continue

                if len(guess) != 5:
                    print("Guess must be 5 characters long!")
                    continue

                if not guess.isalpha():
                    print("Guess must only contain alphabetic characters!")
                    continue

                result = input("Result: ").strip().upper()

                if len(result) != 5:
                    print("Result must be 5 characters long!")
                    continue

                if any(c not in "GYB" for c in result):
                    print("Result must only contain G, Y, or B characters!")
                    continue

                self.words = list(filter(filter_words, self.words))
                print(self.words)

        except KeyboardInterrupt:
            print("\nExiting the solver.")
    
    def reset_words(self):
        self.words = self.load_words()
