from typing import List


class Hangman:

    def __init__(self, word: str, max_tries: int):
        self.letters_guessed_dict = {x: False for x in word}

        self.max_tries = max_tries
        self.letters_missed = set()

    @property
    def tries_left(self) -> int:
        return self.max_tries - len(self.letters_missed)

    @property
    def is_lost(self) -> bool:
        return self.tries_left <= 0

    @property
    def is_win(self) -> bool:
        return not False in self.letters_guessed_dict.values()

    def get_word(self, masked=False, mask_char="*") -> str:
        letters = None
        if not masked:
            letters = self.letters_guessed_dict.keys()
        else:
            letters = [mask_char if not is_guessed else x for x,
                       is_guessed in self.letters_guessed_dict.items()]

        return "".join(letters)

    def get_letter_positions(self, str: str) -> List[int]:
        return [i for i, x in enumerate(self.letters_guessed_dict.keys()) if x == str]

    def guess(self, letter: str) -> bool:
        """
        Returns False if already tried this letter
        Returns True if guessed correct and False if not
        """
        if letter in self.letters_tried:
            return False

        hit = False
        for key in self.letters_guessed_dict.keys():
            if (key == letter):
                hit = True
                self.letters_guessed_dict[key] = True

        if not hit:
            self.letters_missed.add(letter)

        return hit

    def reset(self) -> None:
        self.letters_missed = set()
        self.letters_guessed_dict = {
            x: False for x in self.letters_guessed_dict.keys()}

    @property
    def letters_tried(self) -> set:
        return self.letters_missed.union(set([k for k, is_guessed in self.letters_guessed_dict.items() if is_guessed]))
