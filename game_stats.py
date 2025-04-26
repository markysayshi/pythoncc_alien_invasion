from pathlib import Path

class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # tiy 299, 14-5
        path = Path('high_score.txt')
        if path.exists():
            self.high_score = int(path.read_text())
        else:
            self.high_score = 0
        # High score should never be reset.
        #self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
