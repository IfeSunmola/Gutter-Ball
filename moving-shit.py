import pygame
from sys import exit

pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))

background = pygame.Surface((800, 400))
pygame.display.set_caption("GUTTER BALL")  # Title

clock = pygame.time.Clock()  # for frame rate
ball = pygame.image.load('assets/red.png').convert_alpha()
ball_x_pos = 0
ball_y_pos = 200

while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # X BUTTON
            pygame.quit()  # quit pygame
            exit()  # exit the window

    # draw all needed elements
    screen.blit(background, (0, 0))

    if ball_x_pos <= WIDTH - 150:
        ball_x_pos += 10
    else:
        ball_x_pos -= 10

    screen.blit(ball, (ball_x_pos, 0))

    pygame.display.update()  # updates the screen after drawing all needed elements
    clock.tick(60)  # the while true loop should not run more than 60 times/sec i.e. 60 frames/sec
