import pygame
from sys import exit

pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GUTTER BALL")  # Title
clock = pygame.time.Clock()  # for frame rate

# test_surface = pygame.Surface((100, 200))  # creating a surface
# test_surface.fill('Red')  # coloring

# loading image
test_surface = pygame.image.load('assets/balls.jpg')
red_ball = pygame.image.load('assets/red.png')

# creating text
test_font = pygame.font.Font(None, 50)  # find how to change font
text_surface = test_font.render("This is a text", False, 'Red')  # 2nd param -> smooth the text

"""
while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # X BUTTON
            pygame.quit()  # quit pygame
            exit()  # exit the window

    # draw all needed elements
    # screen.blit(test_surface, (0, 0))  # use .blit to put one surface on another. Placed in top left
    # screen.blit(test_surface, (200, 100))
    # screen.blit(text_surface, (400, 200))
    screen.blit(red_ball, (0, 0))
    pygame.display.update()  # updates the screen after drawing all needed elements
    clock.tick(60)  # the while true loop should not run more than 60 times/sec i.e. 60 frames/sec
"""