"""
The program uses the Rect class to represent a rectangular region. 
An instance is created from the ball image

A Rect object has 4 attributes:
rect.left
rect.top
rect.right
rect.bottom
"""

# import the pygame module.
import pygame
from pygame.locals import *

# define a few variables such as screen size and two colors:
size = 640 , 320
width, height = size
GREEN = (0,255,0)
RED = (255,0,0)

# Then we initialize pygame and create the screen variable:
pygame.init()
screen = pygame.display.set_mode(size)
running = True

# The ball position is represented with a Rect object:
ball = pygame.image.load("img/ball.gif")
rect = ball.get_rect()
speed=[2,2]

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
           running = False
        rect = rect.move(speed)
        if rect.left < 0 or rect.right>width:
            speed[0]=-speed[0]
        if rect.top < 0 or rect.bottom > height:
            speed[1]=-speed[1]

        screen.fill(GREEN)
        pygame.draw.rect(screen,RED,rect,1)
        screen.blit(ball,rect)
        pygame.display.update()

pygame.quit()   



