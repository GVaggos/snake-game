import pygame
import random
import os

pygame.init()

# Window
width, height = 600, 400
cell_size = 30
ui_height = 40
game_height = height - ui_height

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("Arial", 22)
big_font = pygame.font.SysFont("Arial", 48)

# Load burger
food_img = pygame.image.load("burger.png").convert()
food_img = pygame.transform.scale(food_img, (cell_size, cell_size))

# Highscore
HIGHSCORE_FILE = "highscore.txt"

def load_highscore():
    if not os.path.exists(HIGHSCORE_FILE):
        return 0
    with open(HIGHSCORE_FILE, "r") as f:
        return int(f.read())

def save_highscore(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

highscore = load_highscore()

# Particles
particles = []

def create_particles(x, y):
    for _ in range(15):
        particles.append([
            x, y,
            random.uniform(-2, 2),
            random.uniform(-2, 2),
            random.randint(4, 7),
            255
        ])

# Food spawn
def spawn_food(snake):
    while True:
        x = random.randrange(0, width, cell_size)
        y = random.randrange(0, game_height, cell_size)
        if (x, y) not in snake:
            return x, y

# Reset
def reset_game():
    start_x = (width // 2 // cell_size) * cell_size
    start_y = (game_height // 2 // cell_size) * cell_size

    snake = [(start_x, start_y)]
    dx, dy = 0, 0
    food_x, food_y = spawn_food(snake)
    score = 0

    return snake, dx, dy, food_x, food_y, score


snake, dx, dy, food_x, food_y, score = reset_game()

game_over = False
paused = False
running = True

move_timer = 0
base_speed = 180
min_speed = 90

while running:
    dt = clock.tick(60)
    move_timer += dt

    move_delay = max(min_speed, base_speed - score * 4)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_p:
                paused = not paused

            if not game_over and not paused:
                if event.key == pygame.K_LEFT and dx != 1:
                    dx, dy = -1, 0
                if event.key == pygame.K_RIGHT and dx != -1:
                    dx, dy = 1, 0
                if event.key == pygame.K_UP and dy != 1:
                    dx, dy = 0, -1
                if event.key == pygame.K_DOWN and dy != -1:
                    dx, dy = 0, 1

            if game_over:
                if event.key == pygame.K_r:
                    snake, dx, dy, food_x, food_y, score = reset_game()
                    game_over = False
                    paused = False

    # Movement
    if not game_over and not paused and (dx != 0 or dy != 0):
        if move_timer >= move_delay:
            move_timer = 0

            head_x, head_y = snake[0]
            new_head = (head_x + dx * cell_size, head_y + dy * cell_size)

            # Wall collision
            if (
                new_head[0] < 0 or new_head[0] >= width or
                new_head[1] < 0 or new_head[1] >= game_height
            ):
                game_over = True

            # Self collision
            if new_head in snake:
                game_over = True

            snake.insert(0, new_head)

            # Food collision
            if new_head == (food_x, food_y):
                score += 1
                create_particles(food_x, food_y)
                food_x, food_y = spawn_food(snake)

                if score > highscore:
                    highscore = score
                    save_highscore(highscore)
            else:
                snake.pop()

    # Draw
    screen.fill((0, 0, 0))

    # Rounded grid
    padding = 3
    for x in range(0, width, cell_size):
        for y in range(0, game_height, cell_size):
            rect = pygame.Rect(
                x + padding,
                y + padding,
                cell_size - padding*2,
                cell_size - padding*2
            )
            pygame.draw.rect(screen, (30, 30, 30), rect, border_radius=6)

    # Snake (clean rounded square)
    for i, segment in enumerate(snake):
        color = (0, 255, 0) if i == 0 else (0, 200, 0)

        rect = pygame.Rect(
            segment[0] + padding,
            segment[1] + padding,
            cell_size - padding*2,
            cell_size - padding*2
        )

        pygame.draw.rect(screen, color, rect, border_radius=8)

    # Food
    screen.blit(food_img, (food_x, food_y))

    # Particles
    for particle in particles[:]:
        particle[0] += particle[2]
        particle[1] += particle[3]
        particle[4] -= 0.2
        particle[5] -= 5

        if particle[5] <= 0:
            particles.remove(particle)
            continue

        glow_surface = pygame.Surface((20, 20), pygame.SRCALPHA)

        pygame.draw.circle(
            glow_surface,
            (0, 255, 0, int(particle[5])),
            (10, 10),
            int(particle[4])
        )

        screen.blit(glow_surface, (particle[0], particle[1]))

    # UI
    pygame.draw.rect(screen, (30, 30, 30), (0, game_height, width, ui_height))
    pygame.draw.line(screen, (80, 80, 80), (0, game_height), (width, game_height), 2)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    highscore_text = font.render(f"Highscore: {highscore}", True, (200, 200, 200))

    screen.blit(score_text, (10, game_height + 8))
    screen.blit(highscore_text, (width // 2 - 80, game_height + 8))

    # Pause
    if paused:
        pause_text = big_font.render("PAUSED", True, (255, 255, 0))
        screen.blit(pause_text, (width//2 - 100, height//2 - 30))

    # Game Over
    if game_over:
        over_text = big_font.render("GAME OVER", True, (255, 0, 0))
        restart_text = font.render("Press R to Restart", True, (255, 255, 255))

        screen.blit(over_text, (width//2 - 140, height//2 - 50))
        screen.blit(restart_text, (width//2 - 110, height//2 + 10))

    pygame.display.update()

pygame.quit()