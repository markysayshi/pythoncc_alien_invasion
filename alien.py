import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen

        # Load the alien image and set its rect attribute.
        #self.image = pygame.image.load('images/alien.bmp')
        # tiy 263
        self.image = pygame.image.load('images/star.bmp')
        self.rect = self.image.get_rect()
        # the rect starts at 0, 0
        #print(self.rect.x)
        #print(self.rect.y)

        # Start each new alien near the top left of the screen.
        # the rect start is changed to the width and height of the image
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

#rect_test = Alien()
#print(rect_test.rect)
#print(rect_test.rect.x)
#print(rect_test.rect.y)
