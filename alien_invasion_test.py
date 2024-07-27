###### taking apart alien invasion to better understand it
import sys
import pygame
import inspect

screen_width = 1200
screen_height = 800
bg_color = (230, 230, 230)
#bg_color = (117, 14, 98)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
###### FULLSCREEN, don't like this, but testing it out
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#screen_width = screen.get_rect().width
#screen_height = screen.get_rect().height
######
pygame.display.set_caption("testing")

#image = pygame.image.load('images/ship.bmp')
###### for try it yourself, page 246
image = pygame.image.load('images/rocketship.bmp')
#image = pygame.image.load('images/jackhead.bmp')

## this gets the rect of the image's surface
## and sets it to the variable rect
rect = image.get_rect()

######
## print calls to underwhat what is going on with rect positions
print(rect)

## this gets the rect of the screen's surface
## and sets it to the variable screen_rect
screen_rect = screen.get_rect()

## this sets the image rect position, midbottom
## to the screens rect position, midbottom
###### made this center for jackhead
rect.center = screen_rect.center
###### This is the original
#rect.midbottom = screen_rect.midbottom
######
## an example of putting the image in the screen's center
#rect.midbottom = screen_rect.center

######
## print calls to understand what is going on with rect positions
## https://www.pygame.org/docs/ref/rect.html
#print(image.get_rect())
print(rect)
#print(rect.midbottom)
#print(screen_rect.midbottom)

moving_right = False
moving_left = False
###### for try it yourself, page 246
moving_up = False
moving_down = False
## this works, if I wanted a function
#def move_ship():
#    if moving_right:
#        rect.x += 1

## ship speed settings
ship_speed = 4.5
## converting from int to float
x = float(rect.x)
###### for try it yourself, page 246
y = float(rect.y)

###### testing function, doesn't work, will mess with it later
#def check_keydown_events(event):
#    """Respond to key presses."""
#    if event.key == pygame.K_RIGHT:
#        moving_right = True
#    elif event.key == pygame.K_LEFT:
#        moving_left = True
#
#def check_keyup_events(event):
#    """Respond to key releases."""
#    if event.key == pygame.K_RIGHT:
#        moving_right = False
#    elif event.key == pygame.K_LEFT:
#        moving_left = False
######

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            ###### check what keys are pressed with print
            ## shows the name of the key pressed
            #print(pygame.key.name(event.key))
            ## shows only the key pressed unicode
            #print(event.key)
            ## shows everything about the event
            print(event)
            ######
            #check_keydown_events(event)
            if event.key == pygame.K_RIGHT:
                moving_right = True
            elif event.key == pygame.K_LEFT:
                moving_left = True
            ###### for try it yourself, page 246
            elif event.key == pygame.K_UP:
                moving_up = True
            elif event.key == pygame.K_DOWN:
                moving_down = True
            # exit game if q is pressed
            elif event.key == pygame.K_q:
                sys.exit()

        elif event.type == pygame.KEYUP:
            #check_keyup_events(event)
            if event.key == pygame.K_RIGHT:
                moving_right = False
            elif event.key == pygame.K_LEFT:
                moving_left = False
            ###### for try it yourself, page 246
            elif event.key == pygame.K_UP:
                moving_up = False
            elif event.key == pygame.K_DOWN:
                moving_down = False

    ## ship movement
    ## this works, if I wanted a function
    #move_ship()
    ## this works
    if moving_right and rect.right < screen_rect.right:
        x += ship_speed
    if moving_left and rect.left > 0:
        x -= ship_speed
    ###### for try it yourself, page 246
    if moving_up and rect.top > 0:
        y -= ship_speed
    if moving_down and rect.bottom < screen_rect.bottom:
        y += ship_speed

    ## ship speed settings
    rect.x = x
    rect.y = y

    screen.fill((bg_color))
    screen.blit(image, rect)
    pygame.display.flip()
    clock.tick(60)

#print(inspect.ismodule(clock.tick))
#print(inspect.ismethod(clock.tick))
#print(inspect.isfunction(clock.tick))
#print(inspect.isclass(clock.tick))
