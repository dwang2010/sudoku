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
    font_nums = pg.font.SysFont('notomono', 50)
    font_msg = pg.font.SysFont('notomono', 16)

    board = sc.Board()
    board.load_board( [[0,0,3,7,0,0,0,0,4],
                       [0,9,0,0,2,8,0,7,0],
                       [0,0,1,6,0,0,9,0,2],
                       [0,0,2,3,7,0,0,6,0],
                       [3,0,8,9,0,2,5,0,7],
                       [0,7,0,0,8,4,2,0,0],
                       [2,0,7,0,0,6,4,0,0],
                       [0,8,0,2,5,0,0,9,0],
                       [5,0,0,0,0,1,7,0,0]] )

#    board.load_board ( [[8, 2, 3, 7, 1, 9, 6, 5, 4],
#                        [4, 9, 6, 5, 2, 8, 1, 7, 3],
#                        [7, 5, 1, 6, 4, 3, 9, 8, 2],
#                        [9, 4, 2, 3, 7, 5, 8, 6, 1],
#                        [3, 1, 8, 9, 6, 2, 5, 4, 7],
#                        [6, 7, 5, 1, 8, 4, 2, 3, 9],
#                        [2, 3, 7, 8, 9, 6, 4, 1, 5],
#                        [1, 8, 4, 2, 5, 7, 3, 9, 6],
#                        [5, 6, 9, 4, 3, 1, 7, 2, 0]] )

    rndr = sd.Render(width, scrn, font_nums, board)
    msg = sd.Msgbox(0, 640, width, 50, scrn, font_msg)

    run = True
    i, j = 0, 0
    actv, hints, man_mode = False, False, False
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
                        actv = False
                        if not man_mode:
                            valid, done = board.chk_board()
                            if done:
                                msg.set_txt("Congratulations!")
                            elif hints:
                                if not valid:
                                    msg.set_txt("Hint: repeat num found in region!")
                                else:
                                    msg.set_txt("")

                        board._print_board()
                        print ("board updated")
                elif key == "h":
                    if not man_mode:
                        hints = not hints
                        if hints: msg.set_txt("Hints are now active!")
                        else: msg.set_txt("Hints have been turned off!")
                elif key == "m":
                    if not man_mode:
                        board.clear_board()
                        rndr.update_all()
                        msg.set_txt("Manual mode active! Press 'm' again to finish")
                        man_mode = True
                    else:
                        if not board.chk_board()[0]:
                            msg.set_txt("Board doesn't look valid!")
                        else:
                            board.lock_board()
                            msg.set_txt("Looks valid, good luck!")
                            rndr.update_all()
                            man_mode = False

            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                i1, j1 = rndr.chk_coords(scrn, *event.pos)
                if (i1 >= 0 and j1 >= 0):
                    i, j = i1, j1
                    actv = True

        clock.tick(30)    # lock framerate to 30 fps
        pg.display.flip() # update display

    pg.quit()

if __name__ == '__main__':
    print("game start")
    main()
    print("game end")
