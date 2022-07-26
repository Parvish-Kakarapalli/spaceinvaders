import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.image = pygame.image.load('images/ufo.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.y = float(self.rect.y)

    def update(self):
        self.x += self.settings.fleet_direction * self.settings.alien_speed
        self.rect.x = self.x

    def check_edges(self):
        """Returns True if the alien is at the edge"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        return False
    def fall(self):
        self.y += 10
        self.rect.y = self.y
