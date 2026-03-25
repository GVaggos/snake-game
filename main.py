import pygame
import random
import os
import math
import sys

pygame.init()
pygame.mixer.init()

# ===== SETTINGS =====
width, height = 600, 400
cell = 20
cols, rows = width // cell, height // cell

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("🐍 Snake Game")

clock = pygame.time.Clock()

# ===== FONTS =====
font = pygame.font.SysFont("Arial", 20)
big_font = pygame.font.SysFont("Arial", 40)

# ===== COLORS =====
bg_color = (20, 20, 20)

# ===== FILES =====
BURGER_FILE = "burger.png"
EAT_FILE = "eat.flac"
DEATH_FILE = "death.ogg"
MUSIC_FILE = "music.mp3"

# ===== ASSETS =====
food_img = pygame.image.load(BURGER_FILE).convert_alpha()
food_img = pygame.transform.scale(food_img, (cell, cell))

eat_sound = pygame.mixer.Sound(EAT_FILE)
death_sound = pygame.mixer.Sound(DEATH_FILE)

pygame.mixer.music.load(MUSIC_FILE)

# ===== GAME STATES =====
MENU = "menu"
SETTINGS = "settings"
PLAYING = "playing"
GAME_OVER = "game_over"

state = MENU

# ===== SETTINGS VALUES =====
volume = 0.3
difficulty = 10  # FPS

pygame.mixer.music.set_volume(volume)

# ===== RESET =====
def reset_game():
    snake = [(cols//2, rows//2)]
    dx, dy = 0, 0
    food = (random.randint(0, cols-1), random.randint(0, rows-3))
    score = 0
    return snake, dx, dy, food, score

snake, dx, dy, food, score = reset_game()

death_played = False

# ===== MAIN LOOP =====
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            # ===== MENU =====
            if state == MENU:
                if event.key == pygame.K_1:
                    state = PLAYING
                    pygame.mixer.music.play(-1)
                if event.key == pygame.K_2:
                    state = SETTINGS

            # ===== SETTINGS =====
            elif state == SETTINGS:
                if event.key == pygame.K_LEFT:
                    volume = max(0, volume - 0.1)
                    pygame.mixer.music.set_volume(volume)
                elif event.key == pygame.K_RIGHT:
                    volume = min(1, volume + 0.1)
                    pygame.mixer.music.set_volume(volume)

                elif event.key == pygame.K_UP:
                    difficulty = min(20, difficulty + 2)
                elif event.key == pygame.K_DOWN:
                    difficulty = max(5, difficulty - 2)

                elif event.key == pygame.K_ESCAPE:
                    state = MENU

            # ===== PLAYING =====
            elif state == PLAYING:

                if event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -1
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, 1
                elif event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -1, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = 1, 0

            # ===== GAME OVER =====
            elif state == GAME_OVER:
                if event.key == pygame.K_r:
                    snake, dx, dy, food, score = reset_game()
                    death_sound.stop()
                    pygame.mixer.music.play(-1)
                    death_played = False
                    state = PLAYING

                if event.key == pygame.K_ESCAPE:
                    state = MENU

    # ===== UPDATE =====
    if state == PLAYING and (dx != 0 or dy != 0):

        head = (snake[0][0] + dx, snake[0][1] + dy)

        if head in snake or not (0 <= head[0] < cols and 0 <= head[1] < rows-2):
            state = GAME_OVER
        else:
            snake.insert(0, head)

            if head == food:
                score += 1
                eat_sound.play()
                food = (random.randint(0, cols-1), random.randint(0, rows-3))
            else:
                snake.pop()

    # ===== DEATH SOUND =====
    if state == GAME_OVER and not death_played:
        pygame.mixer.music.stop()
        death_sound.play()
        death_played = True

    # ===== DRAW =====
    screen.fill(bg_color)

    # ===== MENU SCREEN =====
    if state == MENU:
        title = big_font.render("SNAKE GAME", True, (0,255,100))
        start = font.render("1 - Start Game", True, (255,255,255))
        settings = font.render("2 - Settings", True, (255,255,255))

        screen.blit(title, (width//2 - 140, 100))
        screen.blit(start, (width//2 - 90, 200))
        screen.blit(settings, (width//2 - 90, 240))

    # ===== SETTINGS SCREEN =====
    elif state == SETTINGS:
        title = big_font.render("SETTINGS", True, (255,255,0))

        vol_text = font.render(f"Volume: {round(volume,1)} (← →)", True, (255,255,255))
        diff_text = font.render(f"Difficulty: {difficulty} (↑ ↓)", True, (255,255,255))
        back_text = font.render("ESC - Back", True, (200,200,200))

        screen.blit(title, (width//2 - 120, 100))
        screen.blit(vol_text, (width//2 - 120, 200))
        screen.blit(diff_text, (width//2 - 120, 240))
        screen.blit(back_text, (width//2 - 80, 300))

    # ===== GAME =====
    elif state == PLAYING or state == GAME_OVER:

        # grid
        for x in range(cols):
            for y in range(rows-2):
                rect = pygame.Rect(x*cell+2, y*cell+2, cell-4, cell-4)
                pygame.draw.rect(screen, (35,35,35), rect, border_radius=6)

        # snake
        for i, segment in enumerate(snake):
            radius = 8 if i == 0 else 6
            color = (0,255,120) if i == 0 else (0,200,80)
            rect = pygame.Rect(segment[0]*cell+2, segment[1]*cell+2, cell-4, cell-4)
            pygame.draw.rect(screen, color, rect, border_radius=radius)

        # food
        bounce = int(math.sin(pygame.time.get_ticks()*0.01)*3)
        screen.blit(food_img, (food[0]*cell, food[1]*cell + bounce))

        # UI
        pygame.draw.rect(screen, (30,30,30), (0,height-40,width,40))
        score_text = font.render(f"Score: {score}", True, (255,255,255))
        screen.blit(score_text, (10,height-30))

    # ===== GAME OVER SCREEN =====
    if state == GAME_OVER:
        over = big_font.render("GAME OVER", True, (255,0,0))
        restart = font.render("R - Restart | ESC - Menu", True, (255,255,255))

        screen.blit(over, (width//2 - 120, height//2 - 40))
        screen.blit(restart, (width//2 - 140, height//2 + 10))

    pygame.display.flip()
    clock.tick(difficulty)