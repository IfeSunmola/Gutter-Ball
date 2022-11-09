import pygame
pygame.init() 

screen = pygame.display.set_mode((1500,600)) # size shows entire game window
pygame.display.set_caption("Gutter Ball")

windowicon = pygame.image.load("windowicon.png")
pygame.display.set_icon(windowicon)

playericon = pygame.image.load('playericon.png')
x = 50
y = 275
def player():
    screen.blit(playericon,(x,y)) #draws image


playing = True
while playing:

    screen.fill((216, 216, 224)) #background fill, we will change to image.

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False #to account for window closing


    player()

    pygame.display.update()
