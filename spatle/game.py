from pathlib import Path
import random


def word_list(text_file: Path = None) -> list:
    if not text_file:
        text_file = Path(__file__).parent / Path('sources') / Path('default.txt')
    with open(text_file) as fh:
        return [w.strip() for w in fh.readlines()]


class Word(str):
    def compare(self, word: str) -> list:
        """
        Compare each letter of this instance to a guessed word and return a list of
        values for each letter:
            True    - the guessed letter is in the right position
            False   - the guessed letter is in the wrong position
            None    - the guessed letter is not in this word
        """
        if len(word) != len(self):
            raise Exception(f"guess '{word}' must be exactly {len(self)} letters long.")
        results = []
        for pos, guess in enumerate(word):
            letter = self[pos]
            if guess == letter:
                results.append(True)
            elif guess in self:
                results.append(False)
            else:
                results.append(None)
        return results

    @classmethod
    def random_from_list(cls, text_file: Path = None):
        return cls(random.choice(word_list(text_file=text_file)))


class Game:
    def __init__(self, solution: str = None, guess_limit: int = 5):
        self.solution = Word(solution) if solution else Word.random_from_list()
        self._guesses = 0
        self._guess_limit = guess_limit
        self._state = [""] * len(self.solution)
        self._known = dict((letter, None) for letter in "abcdefghijklmnopqrstuvwxyz")

    @property
    def state(self) -> list:
        return self._state

    @property
    def solved(self) -> bool:
        return "".join(self._state) == self.solution

    @property
    def guesses_remaining(self) -> int:
        return self._guess_limit - self._guesses

    def letter_state(self, letter: str) -> bool:
        return self._known[letter]

    def guess(self, guess: str) -> bool:
        if not self.guesses_remaining:
            return False
        self._guesses += 1
        guess = guess.lower().strip()
        for pos, result in enumerate(self.solution.compare(guess)):
            if result is True:
                self._state[pos] = self.solution[pos]
            self._known[guess[pos]] = False if result is None else True

        return self.solved

    def __repr__(self):
        lines = []

        status = []
        for letter in self.state:
            status.append(letter or '_')
        lines.append(' '.join(status))
        lines.append('')
        lines.append(f"Guesses Remaining: {self.guesses_remaining}")
        lines.append(f"Letters Known:     {', '.join([k for k, v in self._known.items() if v])}")
        return "\n".join(lines)
