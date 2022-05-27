import math
import tkinter as tk
from turtle import color
from typing import Callable, List

from PIL import Image, ImageTk
from pyparsing import Word

from src.core import Hangman


class WordFrame(tk.Frame):
    def __init__(self, parent, word_len: int):
        super(WordFrame, self).__init__(parent)

        self.string_vars: List[tk.StringVar] = []
        self.labels: List[tk.Label] = []

        for i in range(word_len):
            var = tk.StringVar()
            var.set("_")
            label = tk.Label(self, textvariable=var, font=("Arial", 24))
            label.grid(row=1, column=i, padx=5)
            self.labels.append(label)
            self.string_vars.append(var)

    def set_letter(self, index, letter):
        self.string_vars[index].set(letter)

    def set_font_color(self, color: str):
        for label in self.labels:
            label.configure(fg=color)


class PicFrame(tk.Frame):

    def __init__(self, parent):
        super(PicFrame, self).__init__(parent)

        self.img_idx = 7
        self.label_img = tk.Label(self)
        self.__place_image(self.img_idx, self.label_img)

        self.label_img.grid(column=0, row=0, columnspan=8)

    def next(self):
        self.img_idx -= 1
        self.__place_image(self.img_idx, self.label_img)

    def __place_image(self, img_id: int, label: tk.Label):
        img_source = Image.open(
            './src/gui/images/sprites/hangman_' + str(self.img_idx) + '.png')
        img_source = img_source.resize((200, 240))
        img_tk = ImageTk.PhotoImage(img_source)
        label.configure(image=img_tk)
        self.image = img_tk


class ScreenKeyboardFrame(tk.Frame):

    buttons = {}

    def __init__(self, parent, on_click: Callable[[str], None]):
        super(ScreenKeyboardFrame, self).__init__(parent)

        for i, letter in enumerate("abcdefghijklmnopqrstuvwxyz".upper()):
            def on_button_click(_letter=letter):
                on_click(_letter, self)

            letter_button = tk.Button(
                self, text=letter, font=("Arial", 24), width=4, command=on_button_click)

            self.buttons[letter] = letter_button
            row = 2 + math.floor(i / 8)
            column = i % 8

            letter_button.grid(row=row, column=column)

    def destroy_letter(self, letter: str):
        button = self.buttons[letter]
        button.destroy()
        self.buttons[letter] = None

    def disable(self):
      for button in self.buttons.values():
          if button != None:
              button['state'] = 'disabled'


class HangmanGui:

    hangman: Hangman = None
    pic_frame: PicFrame = None
    word_frame: WordFrame = None
    keyboard_frame: ScreenKeyboardFrame = None

    def __on_letter_click(self, letter: str, frame: ScreenKeyboardFrame):
        if self.hangman.guess(letter):
            idxs = self.hangman.get_letter_positions(letter)
            [self.word_frame.set_letter(i, letter) for i in idxs]
        else:
            self.pic_frame.next()

        frame.destroy_letter(letter)

        if (self.hangman.is_win):
            self.word_frame.set_font_color("#5a5")
            self.keyboard_frame.disable()
        if (self.hangman.is_lost):
            self.word_frame.set_font_color("#a55")
            for i, (k, is_guessed) in enumerate(self.hangman.letters_guessed_dict.items()):
                if not is_guessed:
                    self.word_frame.set_letter(i, k)
            self.keyboard_frame.disable()


    def __init__(self, word):
        self.root = tk.Tk()
        self.root.title("Hangman Game")
        self.root.resizable(0, 0)
        self.root.geometry("800x600")

        self.hangman = Hangman(word=word.upper(), max_tries=6)
        print(self.hangman.get_word())

        main_frame = tk.Frame(self.root)

        # Hangman Image
        self.pic_frame = PicFrame(main_frame)
        self.pic_frame.pack()

        # Word container
        self.word_frame = WordFrame(
            main_frame, word_len=len(self.hangman.get_word()))
        self.word_frame.pack()

        # Sceen keyboard
        self.keyboard_frame = ScreenKeyboardFrame(
            main_frame, on_click=self.__on_letter_click)
        self.keyboard_frame.pack()

        main_frame.place(relx=0.5, rely=0.5, anchor="center")

    def mainloop(self):
        self.root.mainloop()
