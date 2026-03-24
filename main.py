import pygame

pygame.init()

# clock για FPS
clock = pygame.time.Clock()

# παράθυρο
width = 600
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# grid
cell_size = 20

# αρχική θέση (πάντα πολλαπλάσιο του cell_size)
x = 300
y = 200

# κατεύθυνση (σε grid steps)
dx = 0
dy = 0

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

    # κίνηση σε grid
    x += dx * cell_size
    y += dy * cell_size

    # background
    screen.fill((0, 0, 0))

    # snake head (προς το παρόν μόνο ένα κουτάκι)
    pygame.draw.rect(screen, (0, 255, 0), (x, y, cell_size, cell_size))

    pygame.display.update()

    # FPS (snake-like speed)
    clock.tick(5)

pygame.quit()