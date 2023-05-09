import pickle
import random
from Hangman_window import HangmanWindow
from words_alphabet import alphabet_one_string, words_one_string


class HangmanGame:
    """
    Nastavení hodnot proměnných
        """
    def __init__(self):
        self.hidden_word = None
        self.word = None
        self.secret_word = None
        self.highest_score = None
        self.score = 0
        self.help_button_clicks = 0
        self.lives = 10
        self.alphabet = []
        self.letter = ""
        self.result = ""
        self.unused_letters = ""
        self.guessed_letters = []
        self.game_window = HangmanWindow()
        self.window = self.game_window.window
        self.canvas_bg = self.game_window.canvas_bg

    def complete_alphabet(self):
        """
        Rozdělí abecedu na písmena a zároveň abecedu při opakovaném spuštění doplní
            """
        self.alphabet = alphabet_one_string.split(", ")

    def generate_random_word(self):
        """
        Generování náhodného slova a tvoření podtržítek
            """
        self.word = random.choice(words_one_string.split(" | "))
        self.hidden_word = ["_" if letter in set(self.word) else letter for letter in self.word]

    def guess_letter_on_enter(self, event):
        """
        Spouští funkci po stisknutí klávesy enter v entry
        :param event: Umožňuje vložit input klávesou
            """
        self.guess_letter()

    def guess_letter(self):
        """
        Tvoří podmínky hry
            """
        self.canvas_bg.delete(self.game_window.dead_count)
        self.game_window.error_cleaner()
        self.letter = self.game_window.letter_entry_window.get().lower()
        self.game_window.letter_entry_window.delete(0, "end")
        if len(self.letter) == 1:
            if self.letter in self.alphabet:
                self.valid_input()
            else:
                error_message = "Tento znak jste už požil/a.\n   Nebo není v abecedě!"
                self.game_window.error_note(error_message)
        else:
            error_message = "Zadejte jeden znak!"
            self.game_window.error_note(error_message)
        self.game_window.lives_left(self.lives)

    def valid_input(self):
        """
        Maže písmeno z abecedy, kontroluje zda se písmeno nachází ve slově,
        pokud ne odečte život a volá metodu update_drawing.
        Pokud ve slově není žádné podtržítko volá metodu victory a pokud jsou životy 0 tak defeat
            """
        self.alphabet.remove(self.letter)
        if self.letter in set(self.word):
            self.correct_letter()
        else:
            self.lives -= 1
            self.game_window.update_drawing(self.lives)
            if self.lives == 0:
                self.defeat()
        if "_" not in self.hidden_word:
            self.victory()

    def correct_letter(self):
        """
        Projde písmena hádaného slova a přiřadí k ním index, pokud se písmeno shoduje,
        zařadí ho do slova z podrtžítek dle indexu a aktualizuje slovo na obrazovce
            """
        for index, symbol in enumerate(self.word):
            if symbol == self.letter:
                self.hidden_word[index] = self.letter
                self.guessed_letters.append(self.letter)
            self.canvas_bg.delete(self.secret_word)
            self.game_window.update_secret_word_on_screen(self.hidden_word)
            self.secret_word = self.game_window.secret_word

    def victory(self):
        """
        Připočítá skóre, kontroluje zda byl překonán rekord. Vypíše text Vyhráli jste.
            """
        self.score += 1
        if self.score > self.highest_score:
            self.highest_score = self.score
            with open("highest_score.pickle", "wb") as handle:
                pickle.dump(self.highest_score, handle)
        self.result = "Vyhráli jste, hádané slovo bylo"
        self.game_window.game_result(self.word, self.result)
        self.game_window.end_game(self.set_values, self.main, self.secret_word)

    def defeat(self):
        """
        Restartuje skóre na 0, Napíše text Prohrál jste a volá metodu end_game
            """
        self.score = 0
        self.result = "Prohrál jste, hádané slovo bylo"
        self.game_window.game_result(self.word, self.result)
        self.game_window.end_game(self.set_values, self.main, self.secret_word)

    def best_score_checker(self):
        """
        Otevírá uloženou hodnotu z předchozích her a nastaví ji jako nejlepší skóre,
        pokud uživatel hraje poprvé nastaví se na 0
            """
        try:
            with open("highest_score.pickle", "rb") as backup:
                self.highest_score = pickle.load(backup)
        except (FileNotFoundError, EOFError):
            pass

    def help(self):
        """
        Po stisknutí tlačítka generuje náhodné písmeno z hádaného slova (tvoří nápovědu),
        nápověda funguje pouze pokud zůstalo k uhádnutí více jak 3 písmena a lze použít pouze 2x na slovo
            """
        self.game_window.error_cleaner()
        if self.help_button_clicks < 2 and self.hidden_word.count("_") > 3:
            self.unused_letters = set(self.word) - set(self.guessed_letters)
            self.help_button_clicks += 1
            random_letter = random.choice(list(self.unused_letters))
            self.guessed_letters.append(random_letter)
            for i, letter in enumerate(self.word):
                if letter == random_letter:
                    self.hidden_word[i] = random_letter

            self.alphabet.remove(random_letter)
            self.canvas_bg.itemconfig(self.secret_word, text=" ".join(self.hidden_word))
        else:
            self.game_window.help_button.config(state="disabled")
            error_message = "Nápověda již není možná"
            self.game_window.error_note(error_message)

    def set_values(self):
        """
        Stanový základní hodnoty
            """
        self.help_button_clicks = 0
        self.lives = 10
        self.unused_letters = ""
        self.guessed_letters = []

    def main(self):
        """
        Hlavní cyklus, spouští celý program
            """
        self.best_score_checker()
        self.complete_alphabet()
        self.generate_random_word()
        self.game_window.create_widgets(self.highest_score, self.score, self.hidden_word, self.guess_letter_on_enter)
        self.game_window.letter_entry_window.focus()
        self.secret_word = self.game_window.secret_word
        self.game_window.lives_left(self.lives)
        self.game_window.create_buttons(self.help, self.guess_letter, self.word, self.set_values, self.main)
        self.window.mainloop()


game = HangmanGame()
game.main()
