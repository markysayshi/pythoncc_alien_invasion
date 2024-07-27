import pygame

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            print(event.type)
