import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((640,320))

RED = (255,0,0)
BLUE = (0,0,255)
GRAY = (127,127,127)

start=(0,0)
dia = (0,0)
drawing = False
cir_list =[]

running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            start = event.pos
            dia = 0,0
            drawing = True  
        elif event.type == MOUSEBUTTONUP:
            end = event.pos
            dia = (
                end[0] - start[0],
                end[1] - start[1]
            )
            rect = pygame.Rect(start, dia)
            rect.normalize()
            cir_list.append(rect)
            drawing = False
        elif event.type == MOUSEMOTION and drawing:
            end = event.pos
            dia = end[0]-start[0],end[1]-start[1]

    screen.fill(GRAY)
    for cir in cir_list:
        pygame.draw.ellipse(screen,RED,cir,5)
    pygame.draw.ellipse(screen,BLUE,(start,dia),3)
    pygame.display.update()

pygame.quit()        

      
