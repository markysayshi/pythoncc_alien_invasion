import pygame
from pygame.sprite import Sprite

# Alien class is inheriting from Sprite class
class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
    # for rect_test
    #def __init__(self):
        """Initialize the alien and set its starting position."""
        super().__init__()
        # comment both of these out, when using rect_test
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        #print(ai_game)

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/alien.bmp')
        ## tiy 266
        #self.image = pygame.image.load('images/raindrop.bmp')
        ## tiy 263
        #self.image = pygame.image.load('images/star.bmp')
        self.rect = self.image.get_rect()
        # the rect starts at 0, 0
        #print(self.rect.x)
        #print(self.rect.y)
        # 19
        #print(self.rect.right)
        # 0
        #print(self.rect.left)

        # Start each new alien near the top left of the screen.
        # the rect start is changed to the width and height of the image
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)
        #print(self.x)

        # tiy 266, 270
        self.y = float(self.rect.y)
        #print(self.y)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        # to see screen size, 1200 x 800
        #print(screen_rect)
        #return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

        # tiy 270
        return (self.rect.bottom >= screen_rect.bottom) or (self.rect.top <= 0)

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

#rect_test = Alien()
#print(rect_test.rect)
#print(rect_test.rect.x)
#print(rect_test.rect.y)
#print(rect_test.x)
