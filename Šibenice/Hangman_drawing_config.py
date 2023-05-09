class HangmanConfig:
    """
        Poloha šibenice, délky čar a jejich pozice, šířka čar
            """
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.draw_positions = {
            "hangman_draw_lives9": (
                self.screen_width * 0.5, self.screen_height * 0.555, self.screen_width * 0.7,
                self.screen_height * 0.555),
            "hangman_draw_lives8": (
                self.screen_width * 0.6, self.screen_height * 0.55, self.screen_width * 0.6, self.screen_height * 0.18),
            "hangman_draw_lives7": (
                self.screen_width * 0.5, self.screen_height * 0.20, self.screen_width * 0.6, self.screen_height * 0.20),
            "hangman_draw_lives6": (
                self.screen_width * 0.52, self.screen_height * 0.20, self.screen_width * 0.52,
                self.screen_height * 0.26),
            "hangman_draw_lives5": (
                self.screen_width * 0.495, self.screen_height * 0.26, self.screen_width * 0.545,
                self.screen_height * 0.33),
            "hangman_draw_lives4": (
                self.screen_width * 0.52, self.screen_height * 0.33, self.screen_width * 0.52,
                self.screen_height * 0.48),
            "hangman_draw_lives3": (
                self.screen_width * 0.52, self.screen_height * 0.36, self.screen_width * 0.47,
                self.screen_height * 0.43),
            "hangman_draw_lives2": (
                self.screen_width * 0.52, self.screen_height * 0.36, self.screen_width * 0.57,
                self.screen_height * 0.43),
            "hangman_draw_lives1": (self.screen_width * 0.52, self.screen_height * 0.475, self.screen_width * 0.495,
                                    self.screen_height * 0.535),
            "hangman_draw_lives0": (
                self.screen_width * 0.52, self.screen_height * 0.475, self.screen_width * 0.545,
                self.screen_height * 0.535)
        }

    gibbet_base = 30
    gibbet = 20
    line_width = 5
