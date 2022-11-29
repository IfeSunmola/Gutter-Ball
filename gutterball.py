import pygame
from sys import exit

from pygame import mixer

# Constants
PLAYER_SPEED = 1
WINDOW_HEIGHT = 400
WINDOW_LENGTH = 400
NUM_LEVELS = 6
MAX_DEATHS = 10  # maximum number of times the player can hit obstacles

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
MENU_SURF = pygame.image.load("graphics/menu.png").convert_alpha()
BACKGROUND_SURF = pygame.image.load("graphics/background.png").convert_alpha()
PLAYER_SURF = pygame.image.load('graphics/player.png').convert_alpha()
WINNER_SURF = pygame.image.load("graphics/winning.png").convert_alpha()
LOSER_SURF = pygame.image.load("graphics/losing.png").convert_alpha()

PIN_SURFS = {
    "1": pygame.image.load("graphics/pin1.png").convert_alpha(),
    "2": pygame.image.load("graphics/pin2.png").convert_alpha(),
    "3": pygame.image.load("graphics/pin3.png").convert_alpha(),
    "4": pygame.image.load("graphics/pin4.png").convert_alpha(),
    "5": pygame.image.load("graphics/pin5.png").convert_alpha(),
    "6": pygame.image.load("graphics/pin6.png").convert_alpha()
}


def add_obstacles(level_num):
    """
    Function to draw obstacles to the screen of the current level (level_num)

    -----
    :param level_num: the current level

    -----
    :return: A list containing the rects of the obstacles that were drawn. They will be used to check for collisions
    """
    obstacles_rects = []
    if level_num == 2:
        obstacles_rects.append(pygame.draw.rect(screen, "Black", pygame.Rect(175, 100, 50, 200)))
    elif level_num == 3:
        obstacles_rects.append(pygame.draw.rect(screen, "Black", pygame.Rect(100, 150, 50, 200)))
        obstacles_rects.append(pygame.draw.rect(screen, "Black", pygame.Rect(250, 50, 50, 200)))
    elif level_num == 4:
        obstacles_rects.append(pygame.draw.rect(screen, "Black", pygame.Rect(100, 100, 50, 200)))
        obstacles_rects.append(pygame.draw.rect(screen, "Black", pygame.Rect(250, 50, 50, 100)))
        obstacles_rects.append(pygame.draw.rect(screen, "Black", pygame.Rect(250, 250, 50, 150)))
    elif level_num == 5:
        obstacles_rects.append(pygame.draw.rect(screen, "Black", pygame.Rect(100, 50, 50, 150)))
        obstacles_rects.append(pygame.draw.rect(screen, "Black", pygame.Rect(100, 250, 50, 100)))
        obstacles_rects.append(pygame.draw.rect(screen, "Black", pygame.Rect(250, 100, 50, 300)))
        obstacles_rects.append(pygame.draw.rect(screen, "Black", pygame.Rect(0, 100, 100, 50)))
        obstacles_rects.append(pygame.draw.rect(screen, "Black", pygame.Rect(350, 100, 50, 50)))
    elif level_num == 6:
        obstacles_rects.append(pygame.draw.rect(screen, "Black", pygame.Rect(100, 50, 200, 300)))

    return obstacles_rects


def level_init(level_num, death_counter, player_rect):
    """
    This function handles everything related to putting items on the screen for a certain level.\n
    After drawing the player and the pin, obstacles are added with the **add_obstacles** function.\n

    -----
    :param level_num the current level the game is on
    :param death_counter: number of times the player hit an obstacle
    :param player_rect: the position of the player (bowling ball)

    -----
    :return:A tuple containing: the rect of the pin drawn, and a list containing the rects of all the obstacles in the current level
    """

    pygame.draw.rect(screen, "Black", pygame.Rect(0, 0, 400, 50))  # black space above the 'play ground'

    level_surf = TEXT_FONT.render(f"LEVEL {level_num}", False, 'green')  # For the level text
    screen.blit(level_surf, (120, 0))  # Show "LEVEL {level_num}"

    pygame.draw.rect(screen, "Black", pygame.Rect(0, 350, 400, 50))  # black space below the 'play ground'

    deaths_surf = TEXT_FONT.render(f"DEATHS:{death_counter}", False, 'red')  # For the deaths text
    screen.blit(deaths_surf, (0, 365))  # Show death count

    pin_surf = PIN_SURFS[f"{level_num}"]
    pin_rect = pin_surf.get_rect(bottomright=(400, 220))

    # Draw the player and pin
    screen.blit(PLAYER_SURF, player_rect)
    screen.blit(pin_surf, pin_rect)

    # draw the obstacles, and returns the rects ,so they can be used for detecting collisions
    obstacles_rects = add_obstacles(level_num)
    return pin_rect, obstacles_rects


def check_boundary(player_rect):
    """
    Function to simply make sure that the player_rect stays between the bounds of the window

    -----
    :param player_rect: the current position of the player
    """
    if player_rect.left <= 0:
        player_rect.left = 0
    if player_rect.right >= WINDOW_LENGTH:
        player_rect.right = WINDOW_LENGTH
    if player_rect.top <= WINDOW_HEIGHT - 350:  # TODO: Change to be relative to WINDOW_SIZE
        player_rect.top = 50
    if player_rect.bottom >= (WINDOW_HEIGHT - 50):
        player_rect.bottom = (WINDOW_HEIGHT - 50)


def draw_bottom_pins(level_num):
    """
    Function to draw the pins that shows at the bottom right of the window

    ----
    :param level_num: current level, used to determine which pins to draw
    """

    # the x position moves by 32px, starting from 350, so we can just keep subtracting
    pos_x, pos_y = 350, 350
    i = 2
    while i <= level_num:
        temp_surf = pygame.image.load(f'graphics/pin{i - 1}.png')
        screen.blit(temp_surf, (pos_x, pos_y))
        pos_x -= 32
        i += 1


def main():
    player_rect = PLAYER_SURF.get_rect(center=(50, 200))  # starting position of the player

    # State variables -> to keep track of what actions to perform in the game
    game_active = True
    start_game = False
    level_num = 1
    death_counter = 0
    detect_collisions = True  # We want to detect collisions by default. This would change if the user is holding down shift
    event = None  # The for loop (for event in pygame ...) will store all the events. Like this, we can check for events outside the loop

    while game_active:
        screen.blit(MENU_SURF, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # User hit the space button to start the game
                start_sound = mixer.Sound('audio/start.wav')  # Sound when the user starts their game
                start_sound.play()
                start_game = True

            # we only want to track the buttons and move the player when start_game is true
            if start_game and event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_w] or pressed[pygame.K_UP]:
                    player_rect.y += PLAYER_SPEED
                if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
                    player_rect.x += PLAYER_SPEED
                if pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
                    player_rect.y -= PLAYER_SPEED
                if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
                    player_rect.x -= PLAYER_SPEED
                if pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]:
                    detect_collisions = False
                else:
                    detect_collisions = True  # To make sure that collision detection should occur if the player is not holding down shift

        check_boundary(player_rect)

        if game_active and start_game:  # we only want to show the levels if start_game is true
            screen.blit(BACKGROUND_SURF, (0, 0))

            if level_num > NUM_LEVELS:  # No levels left, User has won
                screen.blit(WINNER_SURF, (-30, -30))
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # User pressed space to restart the game
                    level_num, death_counter = 1, 0  # reset the counters
                    player_rect = PLAYER_SURF.get_rect(center=(50, 200))  # and player

            else:  # still some levels left. Anything level related should be done in this `else`
                # Draw the player, obstacles, and the appropriate pin
                pin_rect, obstacles = level_init(level_num, death_counter, player_rect)

                if player_rect.colliderect(pin_rect):  # player has hit the pin, move to next level
                    player_rect = PLAYER_SURF.get_rect(center=(50, 200))  # reset the player's position
                    score_sound = mixer.Sound('audio/score.mp3')  # Sound when the user hits the pin
                    score_sound.play()
                    start_sound = mixer.Sound('audio/start.wav')  # Sound when the user moves to the next level
                    start_sound.play()
                    level_num += 1  # move to next level

                if detect_collisions:  # RECALL: detect_collisions is set to true if any of the 'shift' buttons are pressed while moving
                    for obstacle in obstacles:  # checking if the player collided with any of the obstacles
                        if player_rect.colliderect(obstacle):  # Collision, reset the player position
                            death_counter += 1
                            player_rect = PLAYER_SURF.get_rect(center=(50, 200))
                            screen.blit(PLAYER_SURF, player_rect)

                draw_bottom_pins(level_num)  # pins that show in the bottom right of the screen

                if death_counter >= MAX_DEATHS:
                    # Show the `you lose` screen and wait for user input
                    screen.blit(LOSER_SURF, (-30, -30))
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        level_num, death_counter = 1, 0
                        player_rect = PLAYER_SURF.get_rect(center=(50, 200))

        pygame.display.update()
        clock.tick(60)


# Background Sound
mixer.music.load('audio/background_2.mp3')  # Background music that will be continuous
mixer.music.play(-1)

if __name__ == '__main__':
    main()
