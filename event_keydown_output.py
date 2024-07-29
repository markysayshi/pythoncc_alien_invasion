import sys
import pygame

# pygame setup
pygame.init()
screen =  pygame.display.set_mode((200, 200))
bg_color = (92, 5, 107)
pygame.display.set_caption("event.key output")
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            print(event)
            print(event.key)
            print(pygame.key.name(event.key))

    screen.fill(bg_color)
    pygame.display.flip()
    clock.tick(60)
