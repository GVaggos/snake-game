import pygame
import random

pygame.init()

clock = pygame.time.Clock()

width = 600
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

cell_size = 20

# fonts
font = pygame.font.SysFont(None, 35)
big_font = pygame.font.SysFont(None, 60)

# 🍔 load burger image
food_img = pygame.image.load("burger.png")
food_img = pygame.transform.scale(food_img, (cell_size, cell_size))

def reset_game():
    snake = [(300, 200)]
    dx = 0
    dy = 0
    food_x = random.randrange(0, width, cell_size)
    food_y = random.randrange(0, height, cell_size)
    score = 0
    return snake, dx, dy, food_x, food_y, score

snake, dx, dy, food_x, food_y, score = reset_game()

game_over = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_over:
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
            else:
                if event.key == pygame.K_r:
                    snake, dx, dy, food_x, food_y, score = reset_game()
                    game_over = False

    if not game_over and (dx != 0 or dy != 0):
        head_x, head_y = snake[0]
        new_head = (head_x + dx * cell_size, head_y + dy * cell_size)

        # wall collision
        if new_head[0] < 0 or new_head[0] >= width or new_head[1] < 0 or new_head[1] >= height:
            game_over = True

        # self collision
        elif new_head in snake:
            game_over = True

        else:
            snake.insert(0, new_head)

            # eat food
            if new_head[0] == food_x and new_head[1] == food_y:
                score += 1
                food_x = random.randrange(0, width, cell_size)
                food_y = random.randrange(0, height, cell_size)
            else:
                snake.pop()

    # draw
    screen.fill((20, 20, 20))

    if not game_over:
        # 🍔 burger
        screen.blit(food_img, (food_x, food_y))

        # 🐍 snake (rects)
        for segment in snake:
            pygame.draw.rect(screen, (0, 200, 0), (segment[0], segment[1], cell_size, cell_size))
            pygame.draw.rect(screen, (0, 255, 0), (segment[0]+2, segment[1]+2, cell_size-4, cell_size-4))

        # score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    else:
        game_over_text = big_font.render("GAME OVER", True, (255, 0, 0))
        restart_text = font.render("Press R to Restart", True, (255, 255, 255))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))

        screen.blit(game_over_text, (150, 120))
        screen.blit(score_text, (230, 200))
        screen.blit(restart_text, (180, 250))

    pygame.display.update()
    clock.tick(5)

pygame.quit()