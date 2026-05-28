import pygame, sys
from pygame.locals import * # import pygame modules
"""
The pygame.locals module contains some 280 constants used and defined by pygme.

We find the key modifiers (alt, ctrl, cmd, etc.)
KMOD_ALT, KMOD_CAPS, KMOD_CTRL, KMOD_LALT,
KMOD_LCTRL, KMOD_LMETA, KMOD_LSHIFT, KMOD_META,
KMOD_MODE, KMOD_NONE, KMOD_NUM, KMOD_RALT, KMOD_RCTRL,
KMOD_RMETA, KMOD_RSHIFT, KMOD_SHIFT,

the number keys:
K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9,

the special character keys:
K_AMPERSAND, K_ASTERISK, K_AT, K_BACKQUOTE,
K_BACKSLASH, K_BACKSPACE, K_BREAK,

the letter keys of the alphabet:
K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_l, K_m,
K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z,

Instead of writing pygame.KEYDOWN we can now just write KEYDOWN.
"""

clock = pygame.time.Clock()

pygame.init() # Initialize Pygame

pygame.display.set_caption('My Pygame Window') # set the window tittle

WINDOW_SIZE = (400,400)

"""                            
pygame.display.set_mode :  initialize the window
this function sets the screen size and returns a surface object which we assign to the variable screen.

"""
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) 

player_image = pygame.image.load('img/player.png')
GREEN= (0,255,0)
GRAY = (127,127,127)
RED = (255,0,0)
background= GRAY
"""
Event loop : 
"""
while True: #game loop 
    screen.blit(player_image,(50,50))
    for event in pygame.event.get(): # event loop
        # print(event) 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                background = RED
            elif event.key == pygame.K_g:
                background = GREEN  
        screen.fill(background)
        pygame.display.update()
        if event.type == pygame.QUIT:  # check for window quit
            # print('I don\'t want to close')
            pygame.quit() #stop pygame
            sys.exit() # stop script

    pygame.display.update()    # update display
    clock.tick(60)     # maintain 60 fps