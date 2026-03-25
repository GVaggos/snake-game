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
HIGHSCORE_FILE = "highscore.txt"

# ===== ASSETS =====
food_img = pygame.image.load(BURGER_FILE).convert_alpha()
food_img = pygame.transform.scale(food_img, (cell, cell))

eat_sound = pygame.mixer.Sound(EAT_FILE)
death_sound = pygame.mixer.Sound(DEATH_FILE)

pygame.mixer.music.load(MUSIC_FILE)
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

# ===== HIGHSCORE =====
def load_highscore():
    if not os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "w") as f:
            f.write("0")
        return 0
    with open(HIGHSCORE_FILE, "r") as f:
        return int(f.read().strip() or 0)

def save_highscore(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

highscore = load_highscore()

# ===== PARTICLES =====
particles = []

def spawn_particles(x, y):
    for _ in range(10):
        particles.append([
            x, y,
            random.randint(-3, 3),
            random.randint(-3, 3),
            random.randint(3, 6)
        ])

def update_particles():
    for p in particles[:]:
        p[0] += p[2]
        p[1] += p[3]
        p[4] -= 1
        if p[4] <= 0:
            particles.remove(p)

def draw_particles():
    for p in particles:
        pygame.draw.circle(screen, (255, 200, 50), (int(p[0]), int(p[1])), 3)

# ===== RESET =====
def reset_game():
    snake = [(cols // 2, rows // 2)]
    dx, dy = 0, 0
    food = (random.randint(0, cols - 1), random.randint(0, rows - 3))
    score = 0
    return snake, dx, dy, food, score

snake, dx, dy, food, score = reset_game()

game_over = False
paused = False
death_played = False

# ===== MAIN LOOP =====
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if not game_over:
                if event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -1
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, 1
                elif event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -1, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = 1, 0

            if event.key == pygame.K_p:
                paused = not paused

            if event.key == pygame.K_r:
                snake, dx, dy, food, score = reset_game()
                game_over = False
                paused = False
                death_played = False

                death_sound.stop()
                pygame.mixer.music.play(-1)

    # ===== UPDATE =====
    if not game_over and not paused and (dx != 0 or dy != 0):
        head = (snake[0][0] + dx, snake[0][1] + dy)

        if head in snake or not (0 <= head[0] < cols and 0 <= head[1] < rows - 2):
            game_over = True
        else:
            snake.insert(0, head)

            if head == food:
                score += 1
                eat_sound.play()
                spawn_particles(head[0]*cell + cell//2, head[1]*cell + cell//2)
                food = (random.randint(0, cols - 1), random.randint(0, rows - 3))

                if score > highscore:
                    highscore = score
                    save_highscore(highscore)
            else:
                snake.pop()

    # ===== DEATH =====
    if game_over:
        if not death_played:
            pygame.mixer.music.stop()
            death_sound.play()
            death_played = True

    update_particles()

    # ===== DRAW =====
    screen.fill(bg_color)

    # grid
    for x in range(cols):
        for y in range(rows - 2):
            rect = pygame.Rect(x*cell+2, y*cell+2, cell-4, cell-4)
            pygame.draw.rect(screen, (35, 35, 35), rect, border_radius=6)

    # snake (ROUND SQUARE)
    for i, segment in enumerate(snake):
        if i == 0:
            color = (0, 255, 120)
            radius = 8
        else:
            color = (0, 200, 80)
            radius = 6

        rect = pygame.Rect(segment[0]*cell+2, segment[1]*cell+2, cell-4, cell-4)
        pygame.draw.rect(screen, color, rect, border_radius=radius)

    # food
    bounce = int(math.sin(pygame.time.get_ticks() * 0.01) * 3)
    screen.blit(food_img, (food[0]*cell, food[1]*cell + bounce))

    draw_particles()

    # UI
    pygame.draw.rect(screen, (30, 30, 30), (0, height-40, width, 40))
    pygame.draw.line(screen, (80, 80, 80), (0, height-40), (width, height-40), 2)

    score_text = font.render(f"Score: {score}", True, (255,255,255))
    high_text = font.render(f"Highscore: {highscore}", True, (200,200,200))

    screen.blit(score_text, (10, height-32))
    screen.blit(high_text, (width//2 - 70, height-32))

    if paused and not game_over:
        pause_text = big_font.render("PAUSED", True, (255,255,0))
        screen.blit(pause_text, (width//2 - 80, height//2 - 20))

    if game_over:
        over_text = big_font.render("GAME OVER", True, (255,0,0))
        restart_text = font.render("Press R to Restart", True, (255,255,255))

        screen.blit(over_text, (width//2 - 120, height//2 - 40))
        screen.blit(restart_text, (width//2 - 85, height//2 + 10))

    pygame.display.flip()
    clock.tick(10)