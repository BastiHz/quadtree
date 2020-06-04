
import random
import pygame

import quadtree


DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 768
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)
NUM_POINTS = 100

pygame.init()
display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 20)

tree = quadtree.PointQuadtree(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, 4)
for _ in range(NUM_POINTS):
    x = random.uniform(0, DISPLAY_WIDTH - 1)
    y = random.uniform(0, DISPLAY_HEIGHT - 1)
    tree.insert(quadtree.Point(x, y))

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            p = quadtree.Point(*event.pos)
            tree.insert(p)

    display.fill(BACKGROUND_COLOR)
    tree.draw(display)

    fps_text = font.render(f"{clock.get_fps():.0f}", False, (255, 255, 255))
    display.blit(fps_text, (0, 0))

    pygame.display.flip()
