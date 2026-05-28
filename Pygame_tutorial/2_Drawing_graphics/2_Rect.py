"""
Draw a rectangle with the mouse

We can use three events to draw a rectangle on the screen.
We define the rectangle by its diagonal start and end point.
We also need a flag which indicates if the mouse button is down and if we are drawing

start = (0,0)
size = (0,0)
drawing = False

when mouse btn is pressed, we set start and end to the current mouse posiiton and indicate
with the flag  that the drawing mode has started

when mouse btn is released, we set the end point and indicate with the flag that drawing mode ended

when mouse is moving e have also to check if we are in drawing mode. if yes, we set the end position to the currect mouse position


"""

import pygame
from pygame.locals import *

RED = (255,0,0)
BLUE = (0,0,255)
GRAY = (127,127,127)



pygame.init()
screen = pygame.display.set_mode((640,320))

start = (0,0)
size = (0,0)
drawing = False
rect_list = []

running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            start = event.pos
            size = 0,0
            drawing = True
        elif event.type == MOUSEBUTTONUP:
            end = event.pos
            size = end[0]-start[0] , end[1]-start[1]
            rect = pygame.Rect(start,size)
            rect_list.append(rect)
            drawing=False
        elif event.type == MOUSEMOTION and drawing:
            end = event.pos
            size = end[0]-start[0] , end[1]-start[1]
    screen.fill(GRAY)
    for rect in rect_list :
        pygame.draw.rect(screen,RED,rect,3)
    pygame.draw.rect(screen,BLUE,(start,size),1)
    pygame.display.update()

pygame.quit()                           