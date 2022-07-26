from pygame.sprite import Sprite
import pygame


class Ship(Sprite):
    """A class to manage the ship"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.moving_right = False
        self.moving_left = False
        self.settings = ai_game.settings
        # Load the ship image and get its rectangle
        self.image = pygame.image.load("images/DurrrSpaceShip.png").convert_alpha()
        self.rect = self.image.get_rect()
        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        # Store the decimal value of horizontal position of the ship
        self.x = float(self.rect.x)


    def blitme(self):
        """Draw the ship at the current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Updating the ship by the movement flag"""
        # Update self.x instead of self.rect.x
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        elif self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # updating the self.rect.x
        self.rect.x = self.x

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        # reset both values of self.rect.x and self.x because self.x is on it's own
        self.x = float(self.rect.x)