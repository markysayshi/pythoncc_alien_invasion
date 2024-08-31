import pygame

class Ship:
    """A class to manage the ship."""

    def __init__(self, ai_game):
        # this print call is cool, it tells me what self, ai_game refers to
        # https://ehmatthes.github.io/pcc_2e/reader_questions/ship_self/
        #print(f"\nself in Ship: {self}")
        #print(f"ai_game in Ship: {ai_game}")

        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom
        ## tiy 253
        #self.rect.midleft = self.screen_rect.midleft 

        # Store a float for the ship's exact horizontal position.
        self.x = float(self.rect.x)
        ## tiy 253
        #self.y = float(self.rect.y)

        # Movement flags; start with a ship that's not moving.
        self.moving_right = False
        self.moving_left = False
        ## tiy 253
        #self.moving_up = False
        #self.moving_down = False

    def update(self):
        """Update the ship's position based on the movement flags."""
        # Update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        ## tiy 253
        #if self.moving_up and self.rect.top > 0:
        #    self.y -= self.settings.ship_speed
        #if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
        #    self.y += self.settings.ship_speed

        # Update rect object from self.x
        self.rect.x = self.x
        ## tiy 253
        #self.rect.y = self.y

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
