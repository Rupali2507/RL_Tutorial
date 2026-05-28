"""
The pygame.draw module allows to draw simple shapes to a surface.
It could be a screen surface or any surface object such as an image or drawing
- rectangle
- polygon
- circle
- ellipse

Common parameters:
draw_function(surface, color, shape_data, width)

The functions have in common that they:
- Take a surface object as first argument
- Take a color as second argument
- Take a Width parameter as a last argument
- Return a Rect object which bounds the changed area

If width = 0 (default) -> filled shape
If width > 0 -> outline only
ex : rect(Surface,color,Rect,width) returns Rect
"""

import pygame
from pygame.locals import *

size = 640 , 320
width, height = size

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

GRAY = (127,127,127)

background = GRAY

pygame.init()

screen = pygame.display.set_mode(size)
running = True



while running:
    for event in pygame.event.get():
        if event.type == QUIT:
          running = False

    screen.fill(background)
    # Draw solid and outlined rectangle
    pygame.draw.rect(screen, RED, (50, 20, 120, 100))
    # Draw solid and outlined ellipse
    pygame.draw.ellipse(screen, GREEN, (100, 60, 120, 100))

    pygame.draw.rect(screen, RED, (350, 20, 120, 100), 1)
    pygame.draw.ellipse(screen, GREEN, (400, 60, 120, 100), 4)
    pygame.display.update()

pygame.quit()        

        



