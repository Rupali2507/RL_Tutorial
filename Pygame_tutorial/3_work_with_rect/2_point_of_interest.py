"""
The Rect class defines 4 cornerpoints, 4 mid points and 1 centerpoint.
"""
import pygame
from pygame.locals import *
from pygame.rect import *

SIZE = 500,200
RED = (255,0,0)
GRAY = (127,127,127)
GREEN = (0,255,0)
BLACK =(0,0,0)

pygame.init()
screen = pygame.display.set_mode(SIZE)

rect = Rect(50,60,200,80)
pts = ('topleft', 'topright', 'bottomleft', 'bottomright',
        'midtop', 'midright', 'midbottom', 'midleft', 'center')
font = pygame.font.SysFont(None, 24)

rect = Rect(50, 60, 200, 80)

running = True

def draw_text(text, pos):

    img = font.render(text, True, BLACK)

    screen.blit(img, pos)

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    screen.fill(GRAY)
    pygame.draw.rect(screen,RED,rect,4)
    for pt in pts:
        pos = eval('rect.'+pt)
        draw_text(pt,pos)
        pygame.draw.circle(screen,GREEN,pos,3)
    pygame.display.flip()

pygame.quit()            

