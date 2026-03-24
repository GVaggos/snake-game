import pygame
import random

pygame.init()

clock = pygame.time.Clock()

width = 600
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

cell_size = 20

# snake θέση
x = 300
y = 200

dx = 0
dy = 0

# food θέση (grid aligned)
food_x = random.randrange(0, width, cell_size)
food_y = random.randrange(0, height, cell_size)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
                dy = 0
            if event.key == pygame.K_RIGHT:
                dx = 1
                dy = 0
            if event.key == pygame.K_UP:
                dx = 0
                dy = -1
            if event.key == pygame.K_DOWN:
                dx = 0
                dy = 1

    # κίνηση
    x += dx * cell_size
    y += dy * cell_size

    # collision με food
    if x == food_x and y == food_y:
        food_x = random.randrange(0, width, cell_size)
        food_y = random.randrange(0, height, cell_size)

    # draw
    screen.fill((0, 0, 0))

    # snake
    pygame.draw.rect(screen, (0, 255, 0), (x, y, cell_size, cell_size))

    # food
    pygame.draw.rect(screen, (255, 0, 0), (food_x, food_y, cell_size, cell_size))

    pygame.display.update()

    clock.tick(5)

pygame.quit()