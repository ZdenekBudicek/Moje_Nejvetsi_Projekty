import tkinter as tk
from PIL import Image, ImageTk
from Hangman_drawing_config import HangmanConfig


class HangmanWindow:
    def __init__(self):
        self.bg_color_button = "#015958"
        self.fg_color_button = "#DBF227"
        self.window = tk.Tk()
        self.window.title("Hangman")
        self.window.iconbitmap("img/icon_bit.ico")
        self.window.resizable(False, False)
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.my_image = Image.open("img/images.png")
        self.window.geometry("%dx%d+%d+%d" % (self.screen_width, self.screen_height, 0, 0))
        self.window.state("zoomed")
        self.canvas_bg = tk.Canvas(self.window)
        self.canvas_bg.pack(fill="both", expand=True)
        self.make_canvas_background()
        self.hangman_config = HangmanConfig(self.screen_width, self.screen_height)

    def create_widgets(self, highest_score, score, hidden_word, guess_letter_on_enter):
        """
        Tvorba textu a entry, umožňuje zadat vstup klávesou enter.
            """
        self.highest_score_text = self.canvas_bg.create_text(self.screen_width * 0.08, self.screen_height * 0.12,
                                                             text=f"Rekord: {highest_score}",
                                                             font=("Arial", 20, "bold"))
        self.score_text = self.canvas_bg.create_text(self.screen_width * 0.08, self.screen_height * 0.19,
                                                     text=f"Vaše skóre: {score}",
                                                     font=("Arial", 20, "bold"))
        self.secret_word = self.canvas_bg.create_text(self.screen_width * 0.53, self.screen_height * 0.62,
                                                      text=" ".join(hidden_word), font=("Arial", 60, "bold"),
                                                      fill="white")

        self.letter_entry_window = tk.Entry(self.window, bg="#D6D58E", font=("Arial", 30, "bold"))
        self.letter_entry_window.config(justify="center")
        self.canvas_bg.create_window(self.screen_width * 0.46, self.screen_height * 0.77, anchor="nw",
                                     window=self.letter_entry_window,
                                     width=50, height=50)
        self.letter_entry_window.bind("<Return>", guess_letter_on_enter)

    def create_buttons(self, help_click, guess_letter_click, word, set_values, main):
        """
        Vytvoří tlačítka a přiřazuje k nim command (metodu)
            """
        self.new_word_button = tk.Button(self.window, text="Nové slovo", bg=self.bg_color_button,
                                         fg=self.fg_color_button, font=("Arial", 15), borderwidth=7,
                                         command=lambda: self.new_word_button_click(word, set_values, main))
        self.canvas_bg.create_window(self.screen_width * 0.85, self.screen_height * 0.62, anchor="nw",
                                     window=self.new_word_button,
                                     width=125, height=50)
        self.help_button = tk.Button(self.window, text="Nápověda", bg=self.bg_color_button, fg=self.fg_color_button,
                                     font=("Arial", 15), borderwidth=7,
                                     command=help_click)
        self.canvas_bg.create_window(self.screen_width * 0.85, self.screen_height * 0.77, anchor="nw",
                                     window=self.help_button,
                                     width=125, height=50)
        self.submit_button = tk.Button(self.window, text="Hádej", bg=self.bg_color_button,
                                       fg=self.fg_color_button, font=("Arial", 15), borderwidth=7,
                                       command=guess_letter_click)
        self.canvas_bg.create_window(self.screen_width * 0.54, self.screen_height * 0.77, anchor="nw",
                                     window=self.submit_button,
                                     width=125, height=50)

    def update_drawing(self, lives):
        """
        Kreslí šibenici podle počtu životů
            """
        for i in range(lives, 10):
            if i == 5:
                self.canvas_bg.create_oval(self.hangman_config.draw_positions[f'hangman_draw_lives{i}'],
                                           width=self.hangman_config.line_width)
            else:
                if i == 9:
                    self.canvas_bg.create_line(self.hangman_config.draw_positions[f'hangman_draw_lives{i}'],
                                               width=self.hangman_config.gibbet_base)
                elif 9 > i >= 7:
                    self.canvas_bg.create_line(self.hangman_config.draw_positions[f'hangman_draw_lives{i}'],
                                               width=self.hangman_config.gibbet)
                else:
                    self.canvas_bg.create_line(self.hangman_config.draw_positions[f'hangman_draw_lives{i}'],
                                               width=self.hangman_config.line_width)

    def update_secret_word_on_screen(self, hidden_word):
        """
        Aktualizuje hádané slovo na obrazovce

        :param hidden_word: Slovo z podtržítek, postuponě se do něj vkládají uhodnutá písmena
        """
        self.secret_word = self.canvas_bg.create_text(self.screen_width * 0.53,
                                                      self.screen_height * 0.62,
                                                      text=" ".join(hidden_word),
                                                      font=("Arial", 60, "bold"), fill="white")

    def new_word_button_click(self, word, set_values, main):
        """
        Po stisknutí tlačítka se ukáže jaké bylo hádané slovo a za 1,5s restartuje hru
            """
        self.score = 0
        self.secret_word_was = self.canvas_bg.create_text(self.screen_width * 0.53, self.screen_height * 0.08,
                                                          text=f"Hádané slovo bylo: {word}",
                                                          font=("Arial", 50, "bold"))
        self.new_word_button.config(state="disabled")
        self.submit_button.config(state="disabled")
        self.help_button.config(state="disabled")
        self.letter_entry_window.config(state="disabled")
        self.window.update()
        self.window.after(1500, self.canvas_bg.delete(self.secret_word_was))
        self.repeat_game(set_values, main)

    def end_or_play_again(self, set_values, main):
        """
        Zavolá text "Chcete hrát znovu?" a tlačítka Ano/Ne
            """
        self.play_again = self.canvas_bg.create_text(self.screen_width * 0.53, self.screen_height * 0.65,
                                                     text="Chcete hrát znovu?",
                                                     font=("Arial", 35, "bold"))
        self.yes_button = tk.Button(self.window, text="Ano", bg=self.bg_color_button, fg=self.fg_color_button,
                                    font=("Arial", 15), borderwidth=7,
                                    command=lambda: self.repeat_game(set_values, main))
        self.canvas_bg.create_window(self.screen_width * 0.46, self.screen_height * 0.73, anchor="nw",
                                     window=self.yes_button,
                                     width=100, height=50)
        self.no_button = tk.Button(self.window, text="Ne", bg=self.bg_color_button, fg=self.fg_color_button,
                                   font=("Arial", 15), borderwidth=7, command=self.window.destroy)
        self.canvas_bg.create_window(self.screen_width * 0.56, self.screen_height * 0.73, anchor="nw",
                                     window=self.no_button,
                                     width=100, height=50)

    def lives_left(self, lives):
        """
        Vypisuje počet životů na obrazovku
            """
        self.dead_count = self.canvas_bg.create_text(self.screen_width * 0.53, self.screen_height * 0.87,
                                                     text=f"Váš počet životů je {lives}",
                                                     font=("Arial", 25, "bold"))

    def error_note(self, error_message):
        """
        Vypisuje chyby při nevalidním vstupu nebo při špatném použití tlačítka Nápověda

        :param error_message: Chybová hláška podle situace
            """
        self.error_notification = self.canvas_bg.create_text(self.screen_width * 0.53,
                                                             self.screen_height * 0.725,
                                                             text=error_message,
                                                             font=("Arial", 20))

    def error_cleaner(self):
        """
        Maže chybové hlášky na obrazovce
        """
        try:
            self.canvas_bg.delete(self.error_notification)
        except AttributeError:
            pass

    def game_result(self, word, result):
        self.canvas_bg.create_text(self.screen_width * 0.53, self.screen_height * 0.08,
                                   text=f"{result}: {word}",
                                   font=("Arial", 50, "bold"))

    def end_game(self, set_values, main, secret_word):
        """
        Konec hry, vypne tlačítka a vstupní pole
            """
        self.new_word_button.config(state="disabled")
        self.submit_button.destroy()
        self.help_button.config(state="disabled")
        self.canvas_bg.delete(self.dead_count)
        self.canvas_bg.delete(secret_word)
        self.letter_entry_window.destroy()
        self.end_or_play_again(set_values, main)

    def repeat_game(self, set_values, main):
        """
        Restartuje nastavení hry a spouští hru znovu
            """
        set_values()
        self.new_canvas()
        main()

    def new_canvas(self):
        """
        Smaže starý canvas a následně vytvoří nový
            """
        self.canvas_bg.delete(tk.ALL)
        self.make_canvas_background()

    def make_canvas_background(self):
        """
        Tvoří pozadí canvasu a roztahuje ho
            """
        self.new_image = self.my_image.resize((int(self.screen_width), int(self.screen_height)), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(self.new_image)
        self.canvas_bg.create_image(0, 0, image=self.bg, anchor=tk.NW)
        self.canvas_bg.focus_set()
