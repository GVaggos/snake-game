import pygame

pygame.init()

width = 600
height = 400

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# θέση
x = 300
y = 200

# ταχύτητα
speed = 5

# κατεύθυνση
dx = 0
dy = 0

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -speed
                dy = 0
            if event.key == pygame.K_RIGHT:
                dx = speed
                dy = 0
            if event.key == pygame.K_UP:
                dy = -speed
                dx = 0
            if event.key == pygame.K_DOWN:
                dy = speed
                dx = 0

    x += dx
    y += dy

    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (0, 255, 0), (x, y, 20, 20))

    pygame.display.update()

pygame.quit()