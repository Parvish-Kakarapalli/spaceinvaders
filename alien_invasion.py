import sys
from time import sleep

import json
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import random
from laser import Laser

class AlienInvasion:
    """Overall class to manage game assets and bahaviour"""

    def __init__(self):
        """Initializing the game , and create the game resources."""
        # Each time a game starts a new set of settings would be there
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # Creating an instance of game stats
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.settings.screen_height = self.screen.get_rect().height
        self.settings.screen_width = self.screen.get_rect().width
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "NEW_GAME")
        pygame.display.set_caption("Alien Invasion")
        self.make_difficulty_button()
        self.make_quit_button()
        self.sb = Scoreboard(self)
        self.icon_img = pygame.image.load("images/DurrrSpaceShip.png")
        self.bgm = pygame.mixer.music.load("music.wav")
        pygame.mixer.music.play(-1)
        self.shoot_music = pygame.mixer.Sound("laserfire01.ogg")
        self.blast_music = pygame.mixer.Sound("blast_music.wav")
        self.alien_fire = pygame.mixer.Sound("alien_fire.mp3")
        pygame.display.set_icon(self.icon_img)
        self.backdroung_image = pygame.transform.scale(pygame.image.load("images/space.png"), (self.screen.get_rect().width, self.screen.get_rect().height)).convert()
        self.win = pygame.mixer.Sound("win.wav")
        # Set the background color
        self.alien_lasers = pygame.sprite.Group()
        self.ALIENSHOOT = pygame.USEREVENT + 1
        self.loose_music = pygame.mixer.Sound("loose.wav")
        self.pause_active = False
        self.clock = pygame.time.Clock()




    def make_quit_button(self):
        self.quit_button = Button(self, "QUIT")
        self.quit_button.rect.top = (self.hard_button.rect.top + 1.5 * self.hard_button.height)
        self.quit_button._update_msg_location()

    def make_difficulty_button(self):
        self.easy_button = Button(self, "EASY")
        self.medium_button = Button(self, "MEDIUM")
        self.hard_button = Button(self, "HARD")
        # Positioning these buttons
        self.easy_button.rect.top = (self.play_button.rect.top + 1.5 * self.play_button.rect.height)
        self.easy_button._update_msg_location()
        self.medium_button.rect.top = (self.easy_button.rect.top + 1.5 * self.easy_button.rect.height)
        self.medium_button._update_msg_location()
        self.hard_button.rect.top = (self.medium_button.rect.top + 1.5 * self.medium_button.rect.height)
        self.hard_button._update_msg_location()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for the keyboard and mouse events.
            self._check_events()
            if self.stats.game_active:
                self.ship_update()
                self.alien_lasers.update()
                self.update_bullets()
                self._update_aliens()
                self._check_alien_bullet_collision()

            # Redraw the screen during every pass through the loop
            self._update_screen()
            self.clock.tick(60)

    def ship_update(self):
        self.ship.update()
        if pygame.sprite.spritecollideany(self.ship, self.alien_lasers):
            self._ship_hit()

    def _update_aliens(self):
        self.aliens.update()
        self._check_fleet_edges()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.loose_music.play()
            self.stats.ships_left -= 1
            self.sb.prep_ship()
            """Emptying any exsisting aliens and bullets"""
            self.alien_lasers.empty()
            self.aliens.empty()
            self.bullets.empty()
            """Create a new fleet and center the ship"""
            self._create_fleet()
            self.ship.center_ship()
            # pause for a moment before respawning
            sleep(0.5)

        else:
            self.stats.game_active = False
            self.pause_active = False
            pygame.mouse.set_visible(True)

    def update_bullets(self):
        self.bullets.update()
        # Deleting the old bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # Check that if the bullets hit the alien
        # if so get rid of the alien and the bullet
        self._check_alien_bullet_collision()



    def _check_alien_bullet_collision(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for alien in collisions.values():
                self.blast_music.play()
                self.stats.score +=self.settings.alien_points * len(alien)
            self.sb.prep_score()
            self.sb.check_high_score()
        # Repopulating the fleet Once the entire fleet is shot this would work
        if not self.aliens:
            self.win.play()
            self.bullets.empty()
            self._create_fleet()
            self.alien_lasers.empty()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == self.ALIENSHOOT and self.stats.game_active:
                self.aliens_shoot()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self.check_difficulty(mouse_pos)
                self.check_quit(mouse_pos)

    def check_quit(self, mousepos):
        exit = self.quit_button.rect.collidepoint(mousepos)
        if exit:
            pygame.quit()
            sys.exit()
    def aliens_shoot(self):
        if self.aliens.sprites():
            self.alien_fire.play()
            random_alien = random.choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 6, self.screen.get_rect().height)
            self.alien_lasers.add(laser_sprite)


    def _start_game(self):
        self.settings.initialize_dynamic_settings()
        pygame.time.set_timer(self.ALIENSHOOT, self.settings.time_gap)
        self.alien_lasers.empty()
        self.stats.reset_stats()
        self.sb.prep_level()
        self.sb.prep_score()
        self.sb.prep_ship()
        self.stats.game_active = True
        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()

        self.ship.center_ship()
        pygame.mouse.set_visible(False)

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and (not self.stats.game_active):
            self._start_game()
            self.pause_active = True

    def check_difficulty(self, mouse_pos):
        easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        medium_button_clicked = self.medium_button.rect.collidepoint(mouse_pos)
        hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)

        if easy_button_clicked:
            self.settings.difficulty_level = "easy"
            self._start_game()
            self.pause_active = True
        elif medium_button_clicked:
            self.settings.difficulty_level = "medium"
            self._start_game()
            self.pause_active = True
        elif hard_button_clicked:
            self.settings.difficulty_level = "hard"
            self._start_game()
            self.pause_active = True

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - 2 * alien_width
        available_space_y = self.settings.screen_height - 3 * alien_height - self.ship.rect.height
        number_aliens_x = available_space_x // (2 * alien_width)
        number_rows = available_space_y // (2 * alien_height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alein_height = alien.rect.size
        alien.x = alien_width + 2 * alien_number * alien_width + random.randint(-30, 30)
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number + random.randint(-30, 30)
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """respond appropriatly if any alien gets to the edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    # method to check the aliens reach the bottom to make a ship hit

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the entire fleet direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.backdroung_image, (0, 0))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.alien_lasers.draw(self.screen)
        self.sb.draw_scoreboard()
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()
            self.quit_button.draw_button()
        pygame.display.flip()

    def _check_keydown_events(self, event):
        """Responds to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self.fire_bullets()
        elif event.key == pygame.K_p:
            self._start_game()
            self.pause_active = True
        elif event.key == pygame.K_e:
            self.settings.difficulty_level = "easy"
            self._start_game()
            self.pause_active = True
        elif event.key == pygame.K_h:
            self.settings.difficulty_level = "hard"
            self._start_game()
            self.pause_active = True
        elif event.key == pygame.K_m:
            self.settings.difficulty_level = "medium"
            self._start_game()
            self.pause_active = True
        elif event.key == pygame.K_ESCAPE and self.pause_active:
            if self.stats.game_active:
                self.stats.game_active = False
                pygame.mouse.set_visible(True)
            else:
                self.stats.game_active = True
                pygame.mouse.set_visible(False)
        elif event.key == pygame.K_q:
            with open("highscore.json", "r") as f:
                hscore = json.load(f)
            if hscore < self.stats.high_score:
                with open("highscore.json", mode ="w") as f:
                    json.dump(self.stats.high_score, f)
            sys.exit()

    def _check_keyup_events(self, event):
        """Responds to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def fire_bullets(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            self.shoot_music.play()
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


if __name__ == "__main__":
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()

