#!/usr/bin/python3

import pygame as pg
import sudoku_classes as sc
import sudoku_draw as sd

def main():
    # init display
    pg.display.init()
    pg.font.init()
    width = 630
    height = 700
    caption = "Sudoku!"
    scrn = pg.display.set_mode((width, height))
    pg.display.set_caption(caption)

    # create background surface
    bg = pg.Surface(scrn.get_size()) # create new surface image object
    bg.fill((255, 255, 255))         # fill surface with solid color
    scrn.blit(bg, (0, 0))            # draw source surface onto this surface

    # init game objects
    clock = pg.time.Clock()
    font = pg.font.SysFont('notomono', 50)

    board = sc.Board()
    if board.load_board( [[0,0,3,7,0,0,0,0,4],
                          [0,9,0,0,2,8,0,7,0],
                          [0,0,1,6,0,0,9,0,2],
                          [0,0,2,3,7,0,0,6,0],
                          [3,0,8,9,0,2,5,0,7],
                          [0,7,0,0,8,4,2,0,0],
                          [2,0,7,0,0,6,4,0,0],
                          [0,8,0,2,5,0,0,9,0],
                          [5,0,0,0,0,1,7,0,0]] ):
        board._print_board()
    rndr = sd.Render(width, scrn, font, board)

    run, actv = True, False
    i, j = 0, 0
    hints = False
    while run:
        # handle input events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYDOWN and event.key <= 122:
                pg.key.set_repeat(0) # disable repeat
                key = chr(event.key)

                if key.isdigit():
                    if actv:
                        cell = board.update_cell(i, j, int(key))
                        rndr.update_tile(i, j)
                        #board._print_board()
                        if hints and not board.chk_board():
                            print ("Hint: repeat num found in region!")
                        actv = False
                elif key == "h":
                    hints = not hints
                    print ("Hints active:", hints)

            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                i, j = rndr.chk_coords(scrn, *event.pos)
                if (i >= 0 and j >= 0):
                    actv = True

        clock.tick(30)    # lock framerate to 30 fps
        pg.display.flip() # update display

    pg.quit()

if __name__ == '__main__':
    print("game start")
    main()
    print("game end")
