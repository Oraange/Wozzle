# 🧩 Hardle

A challenging word-guessing puzzle game where players must guess **TWO hidden words simultaneously** within limited attempts!

## About

Hardle is an advanced word-guessing puzzle game that takes the Wordle concept to the next level. Instead of guessing one word, players must identify two different hidden words at the same time. Each guess provides color-coded feedback based on how the letters appear in **both** words, creating a unique and challenging puzzle experience.

## How to Play

1. **Guess valid words**: Enter 5-letter English words
2. **Analyze complex feedback**: After each guess, you'll receive sophisticated color clues based on **both hidden words**:
    - ⬜ **Gray**: Letter is in **neither** word
    - 🟨 **Yellow**: Letter is in **one word only**, but wrong position
    - 🟩 **Yellow-Green**: Letter is in **one word only**, and in the **correct position**
    - 🟧 **Orange**: Letter is in **both words**, but wrong position in both
    - 🟦 **Sky Blue**: Letter is in **both words**, and correct position in **one word**
    - 💙 **Blue**: Letter is in **both words**, and correct position in **both words**
3. **Strategic thinking**: Use the multi-word feedback to deduce both hidden words
4. **Win condition**: Correctly guess **both words** within **10 attempts**
    - Each time you guess one of the two words correctly, your progress count increases
    - You win when you've correctly guessed both words (count = 2/2)

## Color Guide Summary

| Color | Meaning |
|-------|---------|
| Gray | Not in either word |
| Yellow | In 1 word, wrong position |
| Yellow-Green | In 1 word, correct position |
| Orange | In 2 words, both wrong positions |
| Sky Blue | In 2 words, 1 correct position |
| Blue | In 2 words, both correct positions |

## How to Run

```bash
# Clone the repository
$ git clone https://github.com/Oraange/Wozzle.git
$ cd puzzles/wordle
$ git fetch origin
$ git checkout hardle

# No dependencies required!
python3 main.py
```

## Game Features

- 🎯 **Dual-word challenge**: Guess 2 words simultaneously
- 🎨 **6-color feedback system**: Complex color coding for advanced strategy
- 🔢 **10 attempts**: More tries to solve the harder puzzle
- ⌨️ **Interactive keyboard**: Visual feedback on used letters
- 🏆 **Progress tracking**: See how many words you've guessed correctly

---

Good luck and enjoy the challenge of Hardle! 🎯💪