import pygame
import random
import time

pygame.init()
pygame.font.init()
pygame.mixer.init()

# DIMENSIONES DE LA VENTANA
WIDTH = 600
HEIGHT = 650

# colores en RGB
WHITE = (255, 255, 255)
BLACK = (36, 36, 36)
RED = (194, 59, 33)
GREEN = (0, 107, 61)
BLUE = (0, 0, 131)
YELLOW = (253, 204, 12)

# Font
MAIN_FONT = pygame.font.SysFont('Arial', 40)
LEVEL_FONT = pygame.font.SysFont('arialbold', 35)
LEVEL_COMPLETE_FONT = pygame.font.SysFont('Tahoma', 32)
GAME_OVER_FONT = pygame.font.SysFont('Tahoma', 27)
COLOR_FONT = pygame.font.SysFont('Tahoma', 32)

# Sonido
LEVEL_PASSED_SOUND = pygame.mixer.Sound('Assets/level_passed.mp3')
LEVEL_FAILED_SOUND = pygame.mixer.Sound('Assets/level_failed.mp3')
SOUND_1 = pygame.mixer.Sound('Assets/sound_1.mp3')
SOUND_2 = pygame.mixer.Sound('Assets/sound_2.mp3')
SOUND_3 = pygame.mixer.Sound('Assets/sound_3.mp3')
SOUND_4 = pygame.mixer.Sound('Assets/sound_4.mp3')

# innicializamos pygame
pygame.display.set_caption("Color Sequence Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

CORRECT_COLOR = (0, 0, 0)

def main():
    sequence_length = level = 1
    game_sequence = generate_color_sequence(sequence_length)
    player_sequence = []

    color_rectangles = { # color : rectangle
        RED: pygame.Rect(0, 100, 225, 225), # x, y, rectangle_length, rectangle_width
        GREEN: pygame.Rect(0, 325, 225, 225),
        BLUE: pygame.Rect(225, 100, 225, 225),
        YELLOW: pygame.Rect(225, 325, 225, 225)
    }

    display_sequence(game_sequence)
    running = True
    while running:

        for event in pygame.event.get():

            # el usuario presiono el boton de salir. 
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # usuario presiona algún boton del mouse
            if event.type == pygame.MOUSEBUTTONDOWN: 
                x, y = pygame.mouse.get_pos()

                for color, rect in color_rectangles.items():
                    if rect.collidepoint(x, y): 
                        generate_sound(color)
                        player_sequence.append(color)
                        break

                if compare_pressed_button(game_sequence, player_sequence):
                    if player_sequence == game_sequence:
                        sequence_length += 1
                        level += 1
                        draw_level_completed("Nivel completado, eres la verga! :)")
                        game_sequence = generate_color_sequence(sequence_length)
                        player_sequence = []
                        time.sleep(2)
                        display_sequence(game_sequence)
                else:
                    draw_game_over(f"Valiste verga, pendejo :( ")
                    running = False
                    break
        
        if running != False:
            draw_window(color_rectangles, str(level))
            clock.tick(60) 


# Makes random RGB color sequence
def generate_color_sequence(length):
    return [random.choice([RED, GREEN, BLUE, YELLOW]) for _ in range(length)]

# Returns the string equivalent of the RGB color 
def get_color_string(color):
    color_dictionary = {RED: "ROJO", YELLOW: "AMARILLO", GREEN: "VERDE", BLUE: "AZUL"}
    return color_dictionary.get(color, None)

def generate_sound(color):
    sound_dict = {RED: SOUND_1, BLUE: SOUND_2, YELLOW: SOUND_3, GREEN : SOUND_4}
    sound = sound_dict.get(color, None)
    sound.play()
    return sound

# Displays the sequence of colors the player must click
def display_sequence(sequence):
    for color in sequence:
        generate_sound(color) 
        screen.fill(color) 
        pygame.display.update()
        time.sleep(1)

# Outputs the main game interface
def draw_window(color_rectangles, level):
    screen.fill(WHITE)

    # Color Sequence Game Text
    color_game_text = MAIN_FONT.render("MEMORY MATRIX PUTOS", True, BLACK)
    screen.blit(color_game_text, (WIDTH / 2 - color_game_text.get_width() / 2, 0))

    # Level Text
    level_final_text = "Nivel " + level
    render_level_text = LEVEL_FONT.render(level_final_text, True, BLACK)
    screen.blit(render_level_text, (WIDTH / 2 - render_level_text.get_width() / 2, 60))

    # Outputs the four rectangle colors 
    for color, rect in color_rectangles.items():
        pygame.draw.rect(screen, color, rect)

    pygame.display.update()

# Draws Game Over Window
def draw_game_over(text):
    LEVEL_FAILED_SOUND.play()
    screen.fill(WHITE)

    draw_text = GAME_OVER_FONT.render(text, True, BLACK)  
    color_text = COLOR_FONT.render(get_color_string(CORRECT_COLOR), True, CORRECT_COLOR)

    total_width = draw_text.get_width() + color_text.get_width()
    start_x = WIDTH / 2 - total_width / 2

    screen.blit(draw_text, (start_x, HEIGHT / 2 - draw_text.get_height() / 2))
    screen.blit(color_text, (start_x + draw_text.get_width(), HEIGHT / 2 - color_text.get_height() / 2))

    pygame.display.update()
    pygame.time.delay(2000)
    
# Draws Level Completed Window
def draw_level_completed(text):
    LEVEL_PASSED_SOUND.play()
    screen.fill(WHITE)

    draw_text = LEVEL_COMPLETE_FONT.render(text, True, BLACK)

    text_x = (WIDTH - draw_text.get_width()) // 2
    text_y = (HEIGHT - draw_text.get_height()) // 2

    screen.blit(draw_text, (text_x, text_y))
    
    pygame.display.update()
    pygame.time.delay(800)

# compara la secuencia elegida por el jugadr por la seccuencia correcta.
def compare_pressed_button(game_sequence, player_sequence):
    global CORRECT_COLOR

    length_player_sequence = len(player_sequence)
    for i in range(length_player_sequence):
        if player_sequence[i] != game_sequence[i]:
            CORRECT_COLOR = game_sequence[i]
            return False
    return True

if __name__ == "__main__":
    main()
