import pygame
from board import *

pygame.init()
window = pygame.display.set_mode((ROWS*SQUARE_SIZE, COLS*SQUARE_SIZE))
board = Board();
board.draw_squares(window)
board.draw_pawns(window)
pygame.display.flip()
finished = False
while not finished:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            finished = True # Flag that we are done so we exit this loop
        if event.type == pygame.KEYDOWN:
            entry = str(event.key)
        if event.type == pygame.MOUSEBUTTONDOWN:
        	mouse_x, mouse_y = pygame.mouse.get_pos()
        	board.evaluate_click(pygame.mouse.get_pos())

    # --- Drawing code should go here
    # --- Go ahead and update the screen with what we've drawn.
    board.draw_pawns(window)
    pygame.display.flip()
pygame.quit()
