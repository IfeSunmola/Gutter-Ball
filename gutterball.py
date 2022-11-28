import pygame
from sys import exit

from pygame import mixer

# Constants
PLAYER_SPEED = 1
WINDOW_HEIGHT = 400
WINDOW_LENGTH = 400
NUM_LEVELS = 6

# Game initialization
pygame.init()
screen = pygame.display.set_mode((WINDOW_LENGTH, WINDOW_HEIGHT))

pygame.display.set_caption("GutterBall")

WINDOW_ICON = pygame.image.load("graphics/window_icon.png")
pygame.display.set_icon(WINDOW_ICON)

pygame.key.set_repeat(1, 4)
clock = pygame.time.Clock()

# More constants, these depend on pygame being initialized first, so they can't be with the constants above
TEXT_FONT = pygame.font.Font('fonts/digital-dream/DIGITALDREAM.ttf', 30)  # font to use for all the text
MENU_SURF = pygame.image.load("graphics/menu.png").convert()
BACKGROUND_SURF = pygame.image.load("graphics/background.png").convert()
PLAYER_SURF = pygame.image.load('graphics/player.png').convert_alpha()


def level_init(level_num, player_rect):
    pygame.draw.rect(screen, "Black", pygame.Rect(0, 0, 400, 50))  # black space above the 'play ground'

    level_surf = TEXT_FONT.render(f"LEVEL {level_num}", False, 'green')  # For the level text
    screen.blit(level_surf, (120, 0))  # Show "LEVEL {level_num}"

    pygame.draw.rect(screen, "Black", pygame.Rect(0, 350, 400, 50))  # black space below the 'play ground'

    pin_image = f"graphics/pin{level_num}.png"
    pin_surf = pygame.image.load(pin_image).convert_alpha()
    pin_rect = pin_surf.get_rect(bottomright=(400, 220))

    screen.blit(PLAYER_SURF, player_rect)
    screen.blit(pin_surf, pin_rect)

    return pin_rect


def check_boundary(player_rect):
    if player_rect.left <= 0:
        player_rect.left = 0
    if player_rect.right >= WINDOW_LENGTH:
        player_rect.right = WINDOW_LENGTH
    if player_rect.top <= WINDOW_HEIGHT - 350:  # TODO: Change to be relative to WINDOW_SIZE
        player_rect.top = 50
    if player_rect.bottom >= (WINDOW_HEIGHT - 50):
        player_rect.bottom = (WINDOW_HEIGHT - 50)


def draw_bottom_pins(level_num):
    # the x position moves by 32px, starting from 350, so we can just keep subtracting
    pos_x, pos_y = 350, 350
    i = 2
    while i <= level_num:
        temp_surf = pygame.image.load(f'graphics/pin{i - 1}.png')
        screen.blit(temp_surf, (pos_x, pos_y))
        pos_x -= 32
        i += 1


def new_level(level_num):
    rects = []
    if level_num == 2:
        rects.append(pygame.draw.rect(screen, "Black", pygame.Rect(175, 100, 50, 200)))
    if level_num == 3:
        rects.append(pygame.draw.rect(screen, "Black", pygame.Rect(100, 150, 50, 250)))
        rects.append(pygame.draw.rect(screen, "Black", pygame.Rect(250, 50, 50, 200)))
    if level_num == 4:
        rects.append(pygame.draw.rect(screen, "Black", pygame.Rect(100, 100, 50, 200)))
        rects.append(pygame.draw.rect(screen, "Black", pygame.Rect(250, 50, 50, 100)))
        rects.append(pygame.draw.rect(screen, "Black", pygame.Rect(250, 250, 50, 150)))
    if level_num == 5:
        rects.append(pygame.draw.rect(screen, "Black", pygame.Rect(100, 50, 50, 150)))
        rects.append(pygame.draw.rect(screen, "Black", pygame.Rect(100, 300, 50, 100)))
        rects.append(pygame.draw.rect(screen, "Black", pygame.Rect(250, 100, 50, 300)))
        rects.append(pygame.draw.rect(screen, "Black", pygame.Rect(0, 100, 100, 50)))
        rects.append(pygame.draw.rect(screen, "Black", pygame.Rect(350, 100, 50, 50)))
    if level_num == 6:
        rects.append(pygame.draw.rect(screen, "Black", pygame.Rect(100, 50, 200, 300)))
    return rects


def main():
    player_rect = PLAYER_SURF.get_rect(center=(50, 200))

    # State variables -> to keep track of what actions to perform in the game
    game_active = True
    start_game = False
    level_num = 1

    while game_active:
        screen.blit(MENU_SURF, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_sound = mixer.Sound('start.wav')  # Sound when the user starts their game
                start_sound.play()
                start_game = True

            # we only want to track the buttons and move the player when start_game is true
            if start_game and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    player_rect.y += PLAYER_SPEED
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    player_rect.x += PLAYER_SPEED
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    player_rect.y -= PLAYER_SPEED
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    player_rect.x -= PLAYER_SPEED

        check_boundary(player_rect)

        if game_active and start_game:  # we only want to show the levels if start_game is true
            screen.blit(BACKGROUND_SURF, (0, 0))

            if level_num > NUM_LEVELS:  # No levels left, exit
                print("Game Finished")  # Do what happens when the game finishes
                game_active = False

            else:  # still some levels left. Anything level related should be done in this `else`
                pin_rect = level_init(level_num, player_rect)  # show the screen for level_num
                obstacles_rect = new_level(level_num)

                # checking if the player collided with any of the obstacles
                # ISRA: Show failure screen when collision occurs
                for rect in obstacles_rect:
                    if player_rect.colliderect(rect):
                        print("FAILURE")

                if player_rect.colliderect(pin_rect):  # player has hit the pin
                    player_rect = PLAYER_SURF.get_rect(center=(50, 200))  # reset the player's position
                    print("Strike!")  # Just so I can see something in the console, delete later
                    score_sound = mixer.Sound('score.mp3')  # Sound when the user hits the pin
                    score_sound.play()
                    start_sound = mixer.Sound('start.wav')  # Sound when the user moves to the next level
                    start_sound.play()
                    level_num += 1  # move to next level

                draw_bottom_pins(level_num)

        pygame.display.update()
        clock.tick(60)


# Background Sound
mixer.music.load('background_2.mp3')  # Background music that will be continuous
mixer.music.play(-1)

if __name__ == '__main__':
    main()
