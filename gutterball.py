import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((400,400))
pygame.display.set_caption("GutterBall")
# windowicon = pygame.image.load("windowicon.png")
# pygame.display.set_icon(windowicon)
pygame.key.set_repeat(1,4)
clock = pygame.time.Clock()

game_active = True

background_surf = pygame.image.load("graphics/background.png").convert()

player_surf = pygame.image.load('graphics/playericon.png').convert_alpha()
player_rect = player_surf.get_rect(center = (50,200))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                player_rect.y -= 1
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                player_rect.x -= 1
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                player_rect.y += 1
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                player_rect.x += 1
        if player_rect.left <= 0:
            player_rect.left = 0
        if player_rect.right >= 400:
            player_rect.right = 400
        if player_rect.top <= 50:
            player_rect.top = 50
        if player_rect.bottom >= 350:
            player_rect.bottom = 350


    if game_active:
        screen.blit(background_surf,(0,0))
        pygame.draw.rect(screen, "Black",pygame.Rect(0,0,400,50))
        pygame.draw.rect(screen, "Black",pygame.Rect(0,350,400,50))

        screen.blit(player_surf,player_rect)

    pygame.display.update()
    clock.tick(60)