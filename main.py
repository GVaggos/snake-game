import pygame
import random

pygame.init()

clock = pygame.time.Clock()

width = 600
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

cell_size = 20

# αρχικό snake
snake = [(300, 200)]
dx = 0
dy = 0

# food θέση
food_x = random.randrange(0, width, cell_size)
food_y = random.randrange(0, height, cell_size)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
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

    # αν δεν έχει πατηθεί κατεύθυνση ακόμα, δεν κουνιέται
    if dx != 0 or dy != 0:
        head_x, head_y = snake[0]
        new_head = (head_x + dx * cell_size, head_y + dy * cell_size)

        # game over στα όρια
        if new_head[0] < 0 or new_head[0] >= width or new_head[1] < 0 or new_head[1] >= height:
            running = False

        # game over αν χτυπήσει τον εαυτό του
        elif new_head in snake:
            running = False

        else:
            snake.insert(0, new_head)

            # αν φάει food, μεγαλώνει
            if new_head[0] == food_x and new_head[1] == food_y:
                food_x = random.randrange(0, width, cell_size)
                food_y = random.randrange(0, height, cell_size)
            else:
                snake.pop()

    # draw
    screen.fill((0, 0, 0))

    # food
    pygame.draw.rect(screen, (255, 0, 0), (food_x, food_y, cell_size, cell_size))

    # snake body
    for segment in snake:
        pygame.draw.rect(screen, (0, 255, 0), (segment[0], segment[1], cell_size, cell_size))

    pygame.display.update()

    clock.tick(5)

pygame.quit()