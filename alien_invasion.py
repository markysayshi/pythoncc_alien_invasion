# alien invasion start, page 229
import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from button import Button, Button1, Button2
from rectangle import Rectangle
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

        # window mode 1200 x 800
        self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

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

        # tiy 283 disabled
        #self._create_fleet()

        # Start Alien Invasion in an inactive state.
        self.game_active = False

        # Make the Play button.
        self.play_button = Button(self, "Play")

        # tiy 186
        self.fast_button = Button1(self, "faster")
        self.reset_button = Button2(self, "reset")

        # tiy 283
        # Make the rectangle for target practice.
        self.target_practice = Rectangle(self)
        self.target = pygame.sprite.Group()
        self.target.add(self.target_practice)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self.target.update()
                self._update_bullets()
                # tiy 283 disabled
                #self._update_aliens()
                ## tiy 266
                #self._delete_rain()
                #self._continue_rain()

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_faster_slower(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        # tiy 283
        if button_clicked:
            # tiy 286 disabled
            #self.settings.initialize_dynamic_settings()
            self._start_game()

    # tiy 286
    def _check_faster_slower(self, mouse_pos):
        faster = self.fast_button.rect.collidepoint(mouse_pos)
        reset = self.reset_button.rect.collidepoint(mouse_pos)
        if faster:
            print("going faster")
            self.settings.increase_speed()
            print(self.settings.bullet_speed)
        if reset:
            print("resetting speed")
            self.settings.initialize_dynamic_settings()
            print(self.settings.bullet_speed)

    # tiy 283
    def _start_game(self):
        if not self.game_active:
            # Reset the game statistics.
            self.stats.reset_stats()
            self.game_active = True

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            #self.aliens.empty()
            # tiy 283
            self.target.empty()
            self.target.add(self.target_practice)
            for target in self.target.sprites():
                target.draw_button()
                target.center_target()

            # Create a new fleet and center the ship.
            # tiy 283 disabled
            #self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        #if event.key == pygame.K_RIGHT:
        #    self.ship.moving_right = True
        #elif event.key == pygame.K_LEFT:
        #    self.ship.moving_left = True

        # tiy 253, tiy 270
        # change to elif if re-enable right left
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True

        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        # tiy 283
        elif event.key == pygame.K_p:
            # tiy 286 disabled
            #self.settings.initialize_dynamic_settings()
            self._start_game()

    def _check_keyup_events(self, event):
        """Respond to keyreleases."""
        #if event.key == pygame.K_RIGHT:
        #    self.ship.moving_right = False
        #elif event.key == pygame.K_LEFT:
        #    self.ship.moving_left = False

        # tiy 253, tiy 270
        # change to elif if re-enable right left
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

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
            #if bullet.rect.bottom <= 0:
            # tiy 253,tiy 270 uncomment only 1 line below to restore
            if bullet.rect.left >= self.settings.screen_width:
                # tiy 283
                self.stats.bullets_left -= 1
                self.bullets.remove(bullet)
                print(self.stats.bullets_left)
                if self.stats.bullets_left == 0:
                    print("out of bullets!")
                    self._ship_hit()
        # Shows bullets being deleted as they move off screen.
        # Keep uncommented to save memory, page 251.
        #print(len(self.bullets))
        #print(self.bullets)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        # tiy 283
        # find out why target doesn't delete with True, True
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.target, True, True)
        if not self.target:
        #if len(self.target) == 0:
            print("TARGET DESTROYED!")
            self.bullets.empty()
            self.stats.reset_stats()
            print(f"bullets reset: {self.stats.bullets_left}")
            print("spawning new target")
            sleep(0.5)
            self.settings.increase_speed()
            print(self.settings.bullet_speed)
            self.target.add(self.target_practice)
            for target in self.target.sprites():
                target.center_target()
            # same as above, just different way of writing it
            # see help for pygame.sprite.Group.sprites
            #for sprite in self.target:
            #    sprite.center_target()
            #self._ship_hit()
        #print(collisions)

        ## tiy 283 disabled
        #collisions = pygame.sprite.groupcollide(
        #        self.bullets, self.aliens, True, True)
        ##print(collisions)

        #if not self.aliens:
        #    # Destroy existing bullets and create new fleet.
        #    self.bullets.empty()
        #    self._create_fleet()

    # tiy 283
    #def _update_target(self):
    #    self.target_practice.update()

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.aliens.update()
        # print number of aliens on screen
        #print(len(self.aliens))

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        #if self.stats.ships_left > 0:
        # tiy 283
        self.game_active = False
        pygame.mouse.set_visible(True)
        #if len(self.target) == 0:
        #    print("target is empty")
        #    # Decrement ships left.
        #    #self.stats.bullets_left -= 1
        #    #self.stats.ships_left -= 1

        #    # Get rid of any remaining bullets and aliens.
        #    self.bullets.empty()
        #    #self.aliens.empty()

        #    # Create a new fleet and center the ship.
        #    #self._create_fleet()
        #    self.ship.center_ship()
        #    #print(self.stats.ships_left)

        #    # Pause
        #    sleep(0.5)
        #else:
        #    self.game_active = False
        #    pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            # 275
            if alien.rect.left <= 0:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    # tiy 270
    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        #print(alien.rect.size)
        alien_width, alien_height = alien.rect.size
        #print(alien_width)
        #print(alien_height)

        current_x, current_y = 1080, alien_height

        #print(current_x)
        #print(current_y)
        while current_x > (2 * alien_width):
            while current_y < (self.settings.screen_height - 1 * alien_height):
                self._create_alien(current_x, current_y)
                current_y += 2 * alien_height
                #print(current_y)
                #print(current_x)

            current_y = alien_height
            current_x -= 2 * alien_width
            #print(current_y)
            #print(current_x)

    ## tiy 270
    #def _create_fleet(self):
    #    """Create the fleet of aliens."""
    #    # Create an alien and keep adding aliens until there's no room left.
    #    # Spacing between aliens is one alien width and one alien height.
    #    alien = Alien(self)
    #    #print(alien.rect.size)
    #    alien_width, alien_height = alien.rect.size
    #    #print(alien_width)
    #    #print(alien_height)

    #    current_x, current_y = 1080, alien_height

    #    #print(current_x)
    #    #print(current_y)
    #    while current_x > (2 * alien_width):
    #        while current_y < (self.settings.screen_height - 1 * alien_height):
    #            self._create_alien(current_x, current_y)
    #            current_y += 2 * alien_height
    #            #print(current_y)
    #            #print(current_x)

    #        current_y = alien_height
    #        current_x -= 2 * alien_width
    #        #print(current_y)
    #        #print(current_x)

    #def _create_fleet(self):
    #    """Create the fleet of aliens."""
    #    # Create an alien and keep adding aliens until there's no room left.
    #    # Spacing between aliens is one alien width and one alien height.
    #    alien = Alien(self)
    #    #print(alien.rect.size)
    #    alien_width, alien_height = alien.rect.size
    #    #print(alien_width)
    #    #print(alien_height)
    #    current_x, current_y = alien_width, alien_height

    #    ##current_x, current_y = (0, 0)
    #    ##print(current_x)
    #    ##print(current_y)
    #    while current_y < (self.settings.screen_height - 1 * alien_height):
    #        while current_x < (self.settings.screen_width - 2 * alien_width):
    #            #print(current_x)
    #            self._create_alien(current_x, current_y)
    #            current_x += 2 * alien_width

    #        # Finished a row; reset x value, and increment y value.
    #        #print(current_y)
    #        current_x = alien_width
    #        current_y += 2 * alien_height

    #    ## tiy 263
    #    #alien_width, alien_height = alien.rect.size
    #    ##current_x, current_y = alien_width, alien_height
    #    #current_x, current_y = (randint(0, 50), 2)

    #    #while current_y < (self.settings.screen_height - alien_height):
    #    #    while current_x < (self.settings.screen_width - 2 * alien_width):
    #    #        self._create_alien(current_x, current_y)
    #    #        current_x += randint(50, 200)

    #    #    # Finished a row; reset x value, and increment y value.
    #    #    current_x = randint(0, 200)
    #    #    current_y += randint(0, 100)

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self)
        ## wtf does this do, if I comment it out, still works
        ## new_alien.x, it has the same values as new_alien.rect.x
        ## looks like something for the future possibly
        ## used print calls to debug
        #print(new_alien.x)
        new_alien.x = x_position

        # tiy 266
        # this fixed an issue with raindrops being created, not sure how exactly
        # something to do with _create_fleet
        # going to leave it enabled for now
        new_alien.y = y_position

        #print(new_alien.x)
        #print(new_alien.rect.x)
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        #print(new_alien.rect.x)
        self.aliens.add(new_alien)
        # prints the number of aliens in the group as they are added
        #print(self.aliens)
        #print(len(self.aliens))
        #print(self.aliens.sprites)
        # this is interesting, search by 'Group' to see
        # that bullets and aliens are just being assigned to a 'Group'
        # look this up in help/dir
        #pygame.sprite.Group.sprites

    ## tiy 266
    ## this is a modified _update_bullets method
    ## it deletes raindrops when they hit bottom of the screen
    #def _delete_rain(self):
    #    """Update position of bullets and get rid of old bullets."""
    #    # Update bullet positions.
    #    self.aliens.update()

    #    # Get rid of bullets that have disappeared.
    #    for alien in self.aliens.copy():
    #        if alien.rect.top >= 800:
    #        ## tiy 253, comment only 1 line below to restore
    #        #if bullet.rect.left >= self.settings.screen_width:
    #            self.aliens.remove(alien)
    #    # Shows bullets being deleted as they move off screen.
    #    # Keep uncommented to save memory, page 251.
    #    print(len(self.aliens))
    #    #print(alien.rect.top)

    ## tiy 266
    #def _continue_rain(self):
    #    alien = Alien(self)
    #    #print(alien.rect.size)
    #    alien_width, alien_height = alien.rect.size
    #    #print(alien_width)
    #    #print(alien_height)
    #    current_x, current_y = alien_width, alien_height

    #    if (len(self.aliens)) <= 558:
    #    #if (len(self.aliens)) <= 0:
    #    #    self._create_fleet()

    #        while current_x < (self.settings.screen_width - 2 * alien_width):
    #            #print(current_x)
    #            self._create_alien(current_x, current_y)
    #            current_x += 2 * alien_width

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            #alien.rect.y += self.settings.fleet_drop_speed

            # tiy 270
            #print(alien.rect.x)
            alien.rect.x -= self.settings.fleet_drop_speed
            #print(alien.rect.x)

        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Draw the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()

        # tiy 286
        if not self.game_active:
            self.fast_button.draw_button()
            self.reset_button.draw_button()

        # tiy 283
        #self.target_practice.draw_button()
        #for target in self.target.copy():
        for target in self.target.sprites():
            target.draw_button()

        pygame.display.flip()

# I think this returns __main__ because it's being called
# from the main file, if it was called from another file, it might
# return the actual name of this file.
#print(__name__)

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
