#!/usr/bin/python3

import random

from src.gui import HangmanGui
from src.io import loadWords


class Application:

    def __init__(self):
        words = loadWords('./resources/words.txt')
        word = random.choice(words)
        self.ui = HangmanGui(word)

    def start(self) -> None:
        self.ui.mainloop()


def main():
    Application().start()


if __name__ == '__main__':
    main()
