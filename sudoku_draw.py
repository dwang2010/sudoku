import pygame as pg

# sudoku board rendering class
class Grid:
    N = 9 # grid of NxN boxes

    def __init__(self, width: int, surf: pg.Surface):
        # rects: grid of selectable rectangles
        # last: last selected rectangle
        self.rects = [[None for _ in range(self.N)] for __ in range(self.N)]
        self.last = None

        lines = 10      # grid lines in between / on outside
        l_clr = (0,0,0) # line color
        l_width = 2     # line width
        x, y, step = 0, 0, width / self.N
        # draw grid lines
        for i in range(lines):
            x, y = i*step, i*step
            pg.draw.line(surf, l_clr, (0,y), (width,y), l_width) # horiz
            pg.draw.line(surf, l_clr, (x,0), (x,width), l_width) # vert

        b_clr = (255,255,255) # box color
        b_brdr = step // 20   # box border thickness
        x, y = 0, 0
        # draw cell rectangles, store in self.rects
        for i in range(self.N):
            for j in range(self.N):
                x, y = i*step, j*step
                r = pg.Rect(x+b_brdr+l_width, y+b_brdr+l_width,
                            step-(2*b_brdr+l_width), step-(2*b_brdr+l_width))
                pg.draw.rect(surf, b_clr, r)
                self.rects[i][j] = r

    # check if coords fall within a pre-defined rectangle
    # if so, select the box (highlight) and deselect last
    def chk_coords(self, surf: pg.Surface, x: int, y: int) -> None:
        for i in range(self.N):
            for j in range(self.N):
                if self.rects[i][j].collidepoint(x,y):
                    if self.last:
                        self.dslct_box(surf, self.last)
                    self.slct_box(surf, self.rects[i][j])
                    self.last = self.rects[i][j]
                    return

    # highlight grid cell when selected
    def slct_box(self, surf: pg.Surface, r: pg.Rect) -> None:
        slct_clr = (240,225,190)
        pg.draw.rect(surf, slct_clr, r)

    def dslct_box(self, surf: pg.Surface, r: pg.Rect) -> None:
        dslct_clr = (255,255,255)
        pg.draw.rect(surf, dslct_clr, r)
