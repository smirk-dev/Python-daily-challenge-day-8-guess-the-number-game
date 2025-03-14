import pygame
import random
import sys
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Guess the Number Game")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARK_YELLOW = (200, 200, 0)
font_large = pygame.font.Font(None, 72)
font_medium = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 36)
success_sound = pygame.mixer.Sound("success.wav")
fail_sound = pygame.mixer.Sound("fail.wav")
click_sound = pygame.mixer.Sound("click.wav")
target_number = 0
attempts_left = 0
difficulty = None
input_number = ""
feedback_message = ""
game_active = False
def draw_text(text, font, color, x, y, center=True):
    """Draw text on the screen, optionally centered."""
    render = font.render(text, True, color)
    text_rect = render.get_rect(center=(x, y)) if center else (x, y)
    screen.blit(render, text_rect)
def draw_button(x, y, width, height, text, color, text_color, action=None):
    """Draw a clickable button with hover effects."""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    hovered = x < mouse[0] < x + width and y < mouse[1] < y + height
    pygame.draw.rect(screen, DARK_YELLOW if hovered else color, (x, y, width, height), border_radius=10)
    draw_text(text, font_medium, text_color, x + width // 2, y + height // 2)
    if hovered and click[0] == 1 and action:
        click_sound.play()
        action()
def start_game(level):
    """Initialize game based on difficulty."""
    global target_number, attempts_left, difficulty, game_active, feedback_message, input_number
    difficulty = level
    input_number = ""
    feedback_message = ""
    if level == "Easy":
        target_number = random.randint(1, 10)
        attempts_left = 5
    elif level == "Medium":
        target_number = random.randint(1, 50)
        attempts_left = 7
    elif level == "Hard":
        target_number = random.randint(1, 100)
        attempts_left = 10
    game_active = True
def check_guess():
    """Check the user's guess."""
    global attempts_left, feedback_message, game_active
    try:
        guess = int(input_number)
    except ValueError:
        feedback_message = "Invalid input. Enter a number!"
        return
    if guess < target_number:
        feedback_message = "Too low! Try again."
    elif guess > target_number:
        feedback_message = "Too high! Try again."
    else:
        feedback_message = "You guessed it! 🎉"
        success_sound.play()
        game_active = False
        return
    attempts_left -= 1
    if attempts_left == 0:
        feedback_message = f"Game Over! The number was {target_number}."
        fail_sound.play()
        game_active = False
def reset_game():
    """Reset the game to the main menu."""
    global game_active
    game_active = False
running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if game_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                input_number = input_number[:-1]
            elif event.key == pygame.K_RETURN:
                check_guess()
            elif event.unicode.isdigit():
                input_number += event.unicode
    if not game_active:
        draw_text("Guess the Number", font_large, BLACK, WIDTH // 2, HEIGHT // 8)
        draw_button(WIDTH // 3, HEIGHT // 3, 200, 60, "Easy", GREEN, BLACK, lambda: start_game("Easy"))
        draw_button(WIDTH // 3, HEIGHT // 2, 200, 60, "Medium", BLUE, WHITE, lambda: start_game("Medium"))
        draw_button(WIDTH // 3, HEIGHT // 1.5, 200, 60, "Hard", RED, WHITE, lambda: start_game("Hard"))
    else:
        draw_text(f"Difficulty: {difficulty}", font_medium, BLACK, 100, 40, center=False)
        draw_text(f"Attempts Left: {attempts_left}", font_medium, BLACK, 100, 100, center=False)
        draw_text("Your Guess:", font_medium, BLACK, 100, 160, center=False)
        draw_text(input_number, font_medium, BLACK, 300, 160, center=False)
        draw_text(feedback_message, font_medium, RED, WIDTH // 2, HEIGHT // 2.5)
        draw_button(WIDTH // 2 - 200, HEIGHT - 100, 200, 60, "Main Menu", RED, WHITE, reset_game)
    pygame.display.flip()