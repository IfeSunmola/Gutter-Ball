import pygame
from sys import exit

pygame.init()

#Window Set-Up

screen = pygame.display.set_mode((400, 400)) 

pygame.display.set_caption("GutterBall")

window_icon = pygame.image.load("graphics/window_icon.png")
pygame.display.set_icon(window_icon)

pygame.key.set_repeat(1, 4)
clock = pygame.time.Clock()

# font to use for all the text
text_font = pygame.font.Font('fonts/digital-dream/DIGITALDREAM.ttf', 30)

#Variables

menu_surf = pygame.image.load("graphics/menu.png").convert()

background_surf = pygame.image.load("graphics/background.png").convert()

player_surf = pygame.image.load('graphics/player.png').convert_alpha()
player_rect = player_surf.get_rect(center=(50, 200))

level_surf = text_font.render("LEVEL 1", False, 'green')  # play with the 2nd param to see what it does

#Main_menu

def main():
    while True:
        for event in pygame.event.get():
            screen.blit(menu_surf,(0,0))
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    levels()
        pygame.display.update()
        clock.tick(60)

#Game Loop

def levels():
    game_active = True

    while game_active:

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

            # checking boundaries
            if player_rect.left <= 0:
                player_rect.left = 0
            if player_rect.right >= 400:
                player_rect.right = 400
            if player_rect.top <= 50:
                player_rect.top = 50
            if player_rect.bottom >= 350:
                player_rect.bottom = 350

        if game_active:
            screen.blit(background_surf, (0, 0))

            pygame.draw.rect(screen, "Black", pygame.Rect(0, 0, 400, 50))  # black space above the 'play ground'
            screen.blit(level_surf, (120, 0))  # Shows level number

            pygame.draw.rect(screen, "Black", pygame.Rect(0, 350, 400, 50))  # black space below the 'play ground'
            screen.blit(player_surf, player_rect)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

# this runs the game.

main()