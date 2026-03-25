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
font = pygame.font.SysFont("Arial", 22)
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
pygame.mixer.music.set_volume(0.3)

# ===== STATES =====
MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"

state = MENU

# ===== DIFFICULTY SYSTEM =====
def get_speed(score):
    if score < 5:
        return 8, "EASY"
    elif score < 10:
        return 12, "MEDIUM"
    elif score < 20:
        return 16, "HARD"
    else:
        return 22, "IMPOSSIBLE"

# ===== RESET =====
def reset_game():
    snake = [(cols//2, rows//2)]
    dx, dy = 0, 0
    food = (random.randint(0, cols-1), random.randint(0, rows-3))
    score = 0
    return snake, dx, dy, food, score

snake, dx, dy, food, score = reset_game()

death_played = False

# ===== BUTTON CLASS =====
class Button:
    def __init__(self, text, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        mouse = pygame.mouse.get_pos()
        color = (60,60,60)

        if self.rect.collidepoint(mouse):
            color = (100,100,100)

        pygame.draw.rect(screen, color, self.rect, border_radius=8)

        txt = font.render(self.text, True, (255,255,255))
        screen.blit(txt, (self.rect.x + 20, self.rect.y + 10))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

# ===== BUTTONS =====
start_btn = Button("Start Game", width//2 - 100, 180, 200, 40)
quit_btn = Button("Quit", width//2 - 100, 240, 200, 40)

# ===== MAIN LOOP =====
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # ===== MENU =====
        if state == MENU:
            if start_btn.clicked(event):
                snake, dx, dy, food, score = reset_game()
                pygame.mixer.music.play(-1)
                state = PLAYING

            if quit_btn.clicked(event):
                pygame.quit()
                sys.exit()

        # ===== PLAYING =====
        elif state == PLAYING:
            if event.type == pygame.KEYDOWN:
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
            if event.type == pygame.KEYDOWN:
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

    # ===== DEATH =====
    if state == GAME_OVER and not death_played:
        pygame.mixer.music.stop()
        death_sound.play()
        death_played = True

    # ===== DRAW =====
    screen.fill(bg_color)

    # ===== MENU =====
    if state == MENU:
        title = big_font.render("SNAKE GAME", True, (0,255,100))
        screen.blit(title, (width//2 - 140, 100))

        start_btn.draw()
        quit_btn.draw()

    # ===== GAME =====
    elif state == PLAYING or state == GAME_OVER:

        # difficulty
        speed, diff_text = get_speed(score)

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
        diff_label = font.render(diff_text, True, (255,200,0))

        screen.blit(score_text, (10,height-30))
        screen.blit(diff_label, (width//2 - 40, height-30))

    # ===== GAME OVER =====
    if state == GAME_OVER:
        over = big_font.render("GAME OVER", True, (255,0,0))
        restart = font.render("R - Restart | ESC - Menu", True, (255,255,255))

        screen.blit(over, (width//2 - 120, height//2 - 40))
        screen.blit(restart, (width//2 - 140, height//2 + 10))

    pygame.display.flip()

    if state == PLAYING:
        speed, _ = get_speed(score)
        clock.tick(speed)
    else:
        clock.tick(60)