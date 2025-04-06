import pygame
from pygame.sprite import Sprite

class Rectangle(Sprite):
    """A class to build buttons for the game."""

    def __init__(self, ai_game):
        """Initialize button attributes."""
        # this was needed to inherit from Sprite
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        # Set the dimensions and properties of the button.
        self.width, self.height = 25, 150
        self.button_color = (0, 0, 0)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midright = self.screen_rect.midright
        #print(self.rect.x)
        #print(self.rect.y)

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)
        #print(self.x)

        self.y = float(self.rect.y)
        #print(self.y)

    def center_target(self):
        """Center the ship on the screen."""
        #self.rect.midbottom = self.screen_rect.midbottom
        #self.x = float(self.rect.x)
        # 275
        self.rect.midright = self.screen_rect.midright
        self.y = float(self.rect.y)

    def draw_button(self):
    #def draw_button(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button_color, self.rect)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        ### unsure if this is needed, already called above
        #screen_rect = self.screen.get_rect()
        # to see screen size, 1200 x 800
        #print(screen_rect)
        #return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

        # tiy 270
        return (self.rect.bottom >= self.screen_rect.bottom) or (self.rect.top <= 0)

    def update(self):
        """Move the alien right or left."""
        #self.x += self.settings.alien_speed * self.settings.fleet_direction

        # tiy 270
        self.y += self.settings.alien_speed * self.settings.fleet_direction

        # not sure what this is for, maybe 266 testing
        #self.x += self.settings.alien_speed
        # this breaks 270 drop speed for some reason, not sure
        # i think x is just getting reupdated with same value over and over
        # that is why
        #self.rect.x = self.x

        # tiy 270
        self.rect.y = self.y

        ## tiy 266
        #self.y += self.settings.rain_speed
        #self.rect.y = self.y

        # tiy 283
        if self.check_edges():
            #print(self.check_edges)
            self.settings.fleet_direction *= -1
