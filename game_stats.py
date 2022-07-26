import json

class GameStats:
    """Track statistics for the alien_invasion_game"""
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        # Start  Alien Invasion in an active stage
        self.game_active = False
        with open("highscore.json", "r") as f:
            hscore = json.load(f)
        self.high_score = hscore


    def reset_stats(self):
        self.diificulty_set = False
        """Intializing the stats for a new game"""
        self.level = 1
        self.score = 0
        self.ships_left = self.settings.ship_limit
