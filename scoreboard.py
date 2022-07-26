import pygame
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    def __init__(self, ai_game):

        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.text_color = "white"
        self.font = pygame.font.Font("font/Pixeltype.ttf", 40)
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ship()

    def prep_score(self):
        # Prepares the score
        rounded_score = int(round(self.stats.score, -1))
        self.str_score = "{:,}".format(rounded_score)
        self.score_img = self.font.render(f"SCORE {self.str_score}", True, self.text_color)
        self.score_rect = self.score_img.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 10

    def prep_high_score(self):
        self.high_score = int(round(self.stats.high_score, -1))
        self.high_score_str = "{:,}".format(self.high_score)
        self.high_score_img = self.font.render(self.high_score_str, True, self.text_color)
        self.high_score_rect = self.high_score_img.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_ship(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
            
    def draw_scoreboard(self):
        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.high_score_img, self.high_score_rect)
        self.screen.blit(self.level_img, self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        self.level_str = str(self.stats.level)
        self.level_img = self.font.render(f"LEVEL {self.level_str}", True, self.text_color)
        self.level_rect = self.level_img.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 5




