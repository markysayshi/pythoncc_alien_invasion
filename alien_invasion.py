# alien invasion start, page 229
import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from random import randint

# for playing with inspect
import inspect

class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        ### full screen, don't like how this looks
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height

        ## window mode 1200 x 800
        self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        # trying to understand how bullets.update() calls bullet.update()
        #print(self.bullets)
        #print(self.bullets.update())

        # this print call is cool, it tells me what self refers to
        # https://ehmatthes.github.io/pcc_2e/reader_questions/ship_self/
        #print(f"\nself in AlienInvasion: {self}")
        #print(self, type(self))
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        ## tiy 253
        ## change to elif if re-enable right left
        #if event.key == pygame.K_UP:
        #    self.ship.moving_up = True
        #elif event.key == pygame.K_DOWN:
        #    self.ship.moving_down = True

        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to keyreleases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

        ## tiy 253
        ## change to elif if re-enable right left
        #if event.key == pygame.K_UP:
        #    self.ship.moving_up = False
        #elif event.key == pygame.K_DOWN:
        #    self.ship.moving_down = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
            ## tiy 253, comment only 1 line below to restore
            #if bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)
        # Shows bullets being deleted as they move off screen.
        # Keep uncommented to save memory, page 251.
        #print(len(self.bullets))
        #print(self.bullets)

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        #print(alien.rect.size)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height

        ##current_x, current_y = (0, 0)
        ##print(current_x)
        ##print(current_y)
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                #print(current_x)
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finished a row; reset x value, and increment y value.
            #print(current_y)
            current_x = alien_width
            current_y += 2 * alien_height

        ## tiy 263
        #alien_width, alien_height = alien.rect.size
        ##current_x, current_y = alien_width, alien_height
        #current_x, current_y = (randint(0, 50), 2)

        #while current_y < (self.settings.screen_height - alien_height):
        #    while current_x < (self.settings.screen_width - 2 * alien_width):
        #        self._create_alien(current_x, current_y)
        #        current_x += randint(50, 200)

        #    # Finished a row; reset x value, and increment y value.
        #    current_x = randint(0, 200)
        #    current_y += randint(0, 100)

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self)
        ## wtf does this do, if I comment it out, still works
        ## new_alien.x, it has the same values as new_alien.rect.x
        ## looks like something for the future possibly
        ## used print calls to debug
        #print(new_alien.x)
        new_alien.x = x_position
        #print(new_alien.x)
        #print(new_alien.rect.x)
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        #print(new_alien.rect.x)
        self.aliens.add(new_alien)
        # prints the number of aliens in the group as they are added
        #print(self.aliens)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()

#print(inspect.getsource(init))
#print(inspect.getsource(pygame.sprite.Group))
#print(inspect.getsource(pygame.sprite.Group.update))
#print(inspect.getsource(pygame.sprite.Sprite))

## as to what is happening on page 249
## the class Bullet is inheriting from Sprite
## Sprite has a builtin method called update(), that does nothing
## that you are expected to overwrite with your own update() method
## from the child class you create
## reread classes in book, mainly the parent/child inheritence part
    #print(ai.bullets)
    #print(ai.aliens)
