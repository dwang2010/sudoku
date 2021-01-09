#!/usr/bin/python3

import pygame as pg
import sudoku_classes as sc
import sudoku_draw as sd

def main():
    # init display
    pg.display.init()
    width = 630
    height = 700
    caption = "Sudoku!"
    scrn = pg.display.set_mode((width, height))
    pg.display.set_caption(caption)

    # create background surface
    bg = pg.Surface(scrn.get_size()) # create new surface image object
    bg.fill((250, 250, 250))         # fill surface with solid color
    scrn.blit(bg, (0, 0))            # draw source surface onto this surface

    # init game objects
    clock = pg.time.Clock()
    board = sc.Board()
    if board.load( [[0,0,3,7,0,0,0,0,4],
                    [0,9,0,0,2,8,0,7,0],
                    [0,0,1,6,0,0,9,0,2],
                    [0,0,2,3,7,0,0,6,0],
                    [3,0,8,9,0,2,5,0,7],
                    [0,7,0,0,8,4,2,0,0],
                    [2,0,7,0,0,6,4,0,0],
                    [0,8,0,2,5,0,0,9,0],
                    [5,0,0,0,0,1,7,0,0]] ):
        board._print_board()
    print(board.chk_valid())
    grid = sd.Grid(width, scrn)

    run, actv = True, False
    while run:
        # handle input events
        x,y,k = 0, 0, None
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYDOWN:
                pg.key.set_repeat(0)      # disable repeat
                if 48 <= event.key <= 57: # limit to digits 0-9
                    k = chr(event.key)
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                x,y = event.pos
                grid.chk_coords(scrn, x, y)

        if k: print (k)
        clock.tick(30) # lock framerate to 20 fps
        pg.display.flip()

    pg.quit()

if __name__ == '__main__':
    print("game start")
    main()
    print("game end")
