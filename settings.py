class Settings:
    """A class to store the overall settings of the alien_invasion"""

    def __init__(self):
        """Initaializing the game settings"""
        # Screen settings
        self.screen_width = 750
        self.screen_height = 750
        self.bg_color = (230, 230, 230)
        # ship settings
        # self.ship_limit = 3
        # bullet settings

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = "white"
        # self.bullets_allowed = 3
        # Alien settings

        self.fleet_drop_speed = 10
        # 1 means to the right and -1 means to the left
        self.fleet_direction = 1
        # How quickly the game speeds up
        self.speedup_scale = 1.125
        self.difficulty_level = "medium"
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        if self.difficulty_level == "medium":
            self.time_gap = 750
            self.alien_points = 50
            self.ship_speed = 20
            self.bullet_speed = 15
            self.fleet_drop_speed = 10.5
            self.alien_speed = 7.5
            self.ship_limit = 3
            self.bullets_allowed = 3
        elif self.difficulty_level == "easy":
            self.time_gap = 1750
            self.alien_points = 20
            self.fleet_drop_speed = 10.5
            self.ship_speed = 15
            self.bullet_speed = 10
            self.alien_speed = 5
            self.ship_limit = 5
            self.bullets_allowed = 3
        else:
            self.time_gap = 250
            self.alien_points = 75
            self.ship_speed = 25
            self.fleet_drop_speed = 10
            self.bullet_speed = 12.5
            self.alien_speed = 10
            self.ship_limit = 2
            self.bullets_allowed = 3

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points *= self.speedup_scale

    def set_difficulty(self, difficulty):
        self.difficulty_level = difficulty