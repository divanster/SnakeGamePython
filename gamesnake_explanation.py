import sys
import pygame
import random

pygame.init()

# Define colors and other constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

window_width = 800
window_height = 600

game_window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Snake Game")
snake_block_size = 20
snake_speed = 0
selected_speed = 0

font_style = pygame.font.SysFont(None, 50)
speed_font = pygame.font.SysFont(None, 35)

# Load initial screen music
initial_screen_music_path = "media/initial_screen.wav"
initial_screen_music = pygame.mixer.Sound(initial_screen_music_path)

# Load apple eating sound effect
apple_eat_sound_path = "media/apple.wav"
apple_eat_sound = pygame.mixer.Sound(apple_eat_sound_path)

# Load game-over music
game_over_music_path = "media/fart.wav"
game_over_music = pygame.mixer.Sound(game_over_music_path)

# Load in-game music
game_music_path = "media/game_music.wav"

# Set the initial screen music volume
initial_screen_music.set_volume(0.5)

# Set the in-game music volume
pygame.mixer.music.set_volume(0.5)

def show_menu():
    game_window.fill(BLACK)
    message("Snake Game", WHITE, -100)
    message("Select Speed:", WHITE, -30)
    message("1 - Slow", WHITE, 30)
    message("2 - Medium", WHITE, 70)
    message("3 - Fast", WHITE, 110)
    message("4 - Very Fast", WHITE, 150)
    message("5 - Insane", WHITE, 190)
    pygame.display.update()

def message(msg, color, y_offset=0):
    mesg = font_style.render(msg, True, color)
    text_rect = mesg.get_rect(center=(window_width / 2, window_height / 2 + y_offset))
    game_window.blit(mesg, text_rect)

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(game_window, GREEN, [x[0], x[1], snake_block, snake_block])

def game_loop():
    global snake_speed
    global selected_speed
    global initial_screen_music

    # Play the initial screen music
    initial_screen_music.play(-1)  # -1 plays the music in an infinite loop

    show_menu()

    speed_selected = False

    while not speed_selected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    snake_speed = 10
                    selected_speed = 1
                    speed_selected = True
                elif event.key == pygame.K_2:
                    snake_speed = 15
                    selected_speed = 2
                    speed_selected = True
                elif event.key == pygame.K_3:
                    snake_speed = 20
                    selected_speed = 3
                    speed_selected = True
                elif event.key == pygame.K_4:
                    snake_speed = 25
                    selected_speed = 4
                    speed_selected = True
                elif event.key == pygame.K_5:
                    snake_speed = 30
                    selected_speed = 5
                    speed_selected = True

        pygame.display.update()

    # Stop the initial screen music
    initial_screen_music.stop()

    # Play the in-game music
    pygame.mixer.music.load(game_music_path)
    pygame.mixer.music.play(-1)  # -1 plays the music in an infinite loop

    x1 = window_width / 2
    y1 = window_height / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    food_x = round(random.randrange(0, window_width - snake_block_size) / snake_block_size) * snake_block_size
    food_y = round(random.randrange(0, window_height - snake_block_size) / snake_block_size) * snake_block_size

    clock = pygame.time.Clock()

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if y1_change == 0:
                        x1_change = 0
                        y1_change = -snake_block_size
                elif event.key == pygame.K_DOWN:
                    if y1_change == 0:
                        x1_change = 0
                        y1_change = snake_block_size
                elif event.key == pygame.K_LEFT:
                    if x1_change == 0:
                        x1_change = -snake_block_size
                        y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    if x1_change == 0:
                        x1_change = snake_block_size
                        y1_change = 0
                elif event.key == pygame.K_m:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()  # Pause the music
                    else:
                        pygame.mixer.music.unpause()  # Unpause the music

        if x1 >= window_width or x1 < 0 or y1 >= window_height or y1 < 0:
            game_over = True

        x1 += x1_change
        y1 += y1_change
        game_window.fill(BLACK)
        pygame.draw.rect(game_window, WHITE, [food_x, food_y, snake_block_size, snake_block_size])
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_over = True

        our_snake(snake_block_size, snake_list)
        pygame.display.update()

        if x1 == food_x and y1 == food_y:
            food_x = round(random.randrange(0, window_width - snake_block_size) / snake_block_size) * snake_block_size
            food_y = round(random.randrange(0, window_height - snake_block_size) / snake_block_size) * snake_block_size
            length_of_snake += 1
            # Play the apple eating sound
            apple_eat_sound.play()

        clock.tick(snake_speed)

    game_window.fill(BLACK)
    message("Game Over!", WHITE)
    message("Score: " + str(length_of_snake - 1), WHITE, 30)
    message("Press C to Play Again or Q to Quit", WHITE, 90)
    pygame.display.update()

    # Play the game-over music
    game_over_music.play()

    waiting_for_input = True

    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_c:
                    game_loop()

        pygame.event.pump()  # Pump the event queue to avoid the KeyboardInterrupt
        pygame.time.delay(10)  # Introduce a small delay to reduce CPU usage

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()


