"""
Draw a pologyon line with the mouse

To draw a polygon line we need to add the points to a list of points. 
First we define an empty point list and a drawing flag:

At the MOUSEBUTTONDOWN event we add the current point to the list and 
set the drawing flag to True

At the MOUSEBUTTONUP event we deactivate the drawing flag

At the MOUSEMOTION event we move the last point in the polygon list if the drawing flag is set

If there are more than 2 points in the point list we draw a polygon line. Each pygame.draw function returns a Rect of the bounding rectangle.
We display this bounding rectangle in green

Pressing the ESCAPE key will remove the last point in the list
"""



import pygame
from pygame.locals import *

RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (150, 150, 150)

pygame.init()
screen = pygame.display.set_mode((640,320))

drawing = False
points = []
running = True

while running:
    for event in pygame.event.get():
        if event.type==QUIT:
            running = False
        elif event == KEYDOWN:
            if event.key == K_ESCAPE:
                if len(points)>0:
                    points.pop()
                   
        elif event.type== MOUSEBUTTONDOWN:
            points.append(event.pos)
            drawing = True    

        elif event.type == MOUSEBUTTONUP:  
            drawing = False

        elif event.type == MOUSEMOTION and drawing:
            points[-1] = event.pos

    screen.fill(GRAY)
    if len(points)>1:
        rect = pygame.draw.lines(screen,RED,True,points,3)
        pygame.draw.rect(screen,GREEN,rect,1)
    pygame.display.update()

pygame.quit()                    
              
