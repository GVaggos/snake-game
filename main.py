import pygame
import random
import os

pygame.init()

clock = pygame.time.Clock()

cell_size = 30
width = (600 // cell_size) * cell_size
height = (400 // cell_size) * cell_size

hud_height = 50
screen = pygame.display.set_mode((width, height + hud_height))
pygame.display.set_caption("Snake Game")

food_size = 40

font = pygame.font.SysFont(None, 35)
big_font = pygame.font.SysFont(None, 70)

# 🍔 LOAD BURGER
try:
    food_img = pygame.image.load("burger.png").convert_alpha()
except:
    food_img = pygame.image.load("burger.jpg").convert()
    food_img.set_colorkey((255, 255, 255))

food_img = pygame.transform.scale(food_img, (food_size, food_size))


# 🏆 HIGH SCORE
def load_highscore():
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")
    with open("highscore.txt", "r") as f:
        return int(f.read())


def save_highscore(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))


highscore = load_highscore()


def spawn_food(snake):
    while True:
        x = random.randrange(0, width, cell_size)
        y = random.randrange(0, height, cell_size)
        if (x, y) not in snake:
            return x, y


def reset_game():
    start_x = (width // 2) // cell_size * cell_size
    start_y = (height // 2) // cell_size * cell_size

    snake = [(start_x, start_y)]
    dx = 0
    dy = 0

    food_x, food_y = spawn_food(snake)
    score = 0

    return snake, dx, dy, food_x, food_y, score


snake, dx, dy, food_x, food_y, score = reset_game()

game_over = False
paused = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused

            if not game_over and not paused:
                if event.key == pygame.K_LEFT and dx != 1:
                    dx = -1
                    dy = 0
                if event.key == pygame.K_RIGHT and dx != -1:
                    dx = 1
                    dy = 0
                if event.key == pygame.K_UP and dy != 1:
                    dx = 0
                    dy = -1
                if event.key == pygame.K_DOWN and dy != -1:
                    dx = 0
                    dy = 1
            elif game_over:
                if event.key == pygame.K_r:
                    snake, dx, dy, food_x, food_y, score = reset_game()
                    game_over = False
                    paused = False

    if not game_over and not paused and (dx != 0 or dy != 0):
        head_x, head_y = snake[0]
        new_head = (head_x + dx * cell_size, head_y + dy * cell_size)

        if (
            new_head[0] < 0 or
            new_head[0] >= width or
            new_head[1] < 0 or
            new_head[1] >= height
        ):
            game_over = True

        elif new_head in snake:
            game_over = True

        else:
            snake.insert(0, new_head)

            if new_head[0] == food_x and new_head[1] == food_y:
                score += 1
                food_x, food_y = spawn_food(snake)
            else:
                snake.pop()

    # 🎨 BACKGROUND
    screen.fill((15, 15, 15))

    # 🔲 GRID (μόνο gameplay)
    for x in range(0, width, cell_size):
        pygame.draw.line(screen, (30, 30, 30), (x, 0), (x, height))
    for y in range(0, height, cell_size):
        pygame.draw.line(screen, (30, 30, 30), (0, y), (width, y))

    if not game_over:
        screen.blit(food_img, (food_x - 5, food_y - 5))

        for segment in snake:
            pygame.draw.rect(screen, (0, 200, 0),
                             (segment[0], segment[1], cell_size, cell_size), border_radius=5)

            pygame.draw.rect(screen, (0, 255, 0),
                             (segment[0] + 4, segment[1] + 4,
                              cell_size - 8, cell_size - 8), border_radius=3)

        if paused:
            pause_text = big_font.render("PAUSED", True, (255, 255, 0))
            screen.blit(pause_text, (200, 150))

    else:
        # 🏆 update highscore
        if score > highscore:
            highscore = score
            save_highscore(highscore)

        game_over_text = big_font.render("GAME OVER", True, (255, 0, 0))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        high_text = font.render(f"Highscore: {highscore}", True, (200, 200, 200))
        restart_text = font.render("Press R to Restart", True, (255, 255, 255))

        screen.blit(game_over_text, (140, 80))
        screen.blit(score_text, (240, 160))
        screen.blit(high_text, (220, 200))
        screen.blit(restart_text, (180, 260))

    # 🔳 HUD (ΚΑΤΩ)
    pygame.draw.rect(screen, (25, 25, 25), (0, height, width, hud_height))

    # 🔥 SEPARATOR LINE
    pygame.draw.line(screen, (50, 50, 50), (0, height), (width, height), 2)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    high_text = font.render(f"Highscore: {highscore}", True, (180, 180, 180))

    screen.blit(score_text, (10, height + 10))
    screen.blit(high_text, (200, height + 10))

    pygame.display.update()
    clock.tick(7)

pygame.quit()