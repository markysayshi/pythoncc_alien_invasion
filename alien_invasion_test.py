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
pygame.display.set_caption("testing")

image = pygame.image.load('images/ship.bmp')
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
#rect.center = screen_rect.center
rect.midbottom = screen_rect.midbottom
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
## this works, if I wanted a function
#def move_ship():
#    if moving_right:
#        rect.x += 1

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
            if event.key == pygame.K_RIGHT:
                moving_right = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                moving_right = False

    ## this works, if I wanted a function
    #move_ship()
    ## this works
    if moving_right:
        rect.x += 1

    screen.fill((bg_color))
    screen.blit(image, rect)
    pygame.display.flip()
    clock.tick(60)

#print(inspect.ismodule(clock.tick))
#print(inspect.ismethod(clock.tick))
#print(inspect.isfunction(clock.tick))
#print(inspect.isclass(clock.tick))
