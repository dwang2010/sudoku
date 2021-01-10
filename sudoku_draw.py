import pygame as pg
from typing import Tuple
import sudoku_classes as sc
import sudoku_const as sconst

# class for rendering individual sudoku tiles
class Tile:
    # create a square, selectable tile for showing current cell number
    def __init__(self, i: int, j: int, x: int, y: int, side: int,
                 bg: pg.Surface, font: pg.font, cell: sc.Cell):
        # pos    : (i,j) mapping to board cell object
        # coords : (x,y) coordinates for top left corner
        # img    : tile image surface
        # rect   : coordinate rectangle
        self.pos = (i, j)
        self.coords = (x, y)
        self.img = pg.Surface((side, side))
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = x, y
        self.font = font
        self.bg = bg
        self.cell = cell
        self.update(False)

    # check if selected point coordinate hits tile, and tile cell not locked
    def chk_slctd(self, x: int, y: int) -> bool:
        lock = self.cell.get_lock()
        if lock: return False
        return self.rect.collidepoint(x,y)

    # update and render new tile image
    def update(self, slct: bool) -> None:
        val = self.cell.get_val()
        lock = self.cell.get_lock()

        # configure box / text color
        bclr = sconst.BEIGE if slct else sconst.WHITE
        if lock:
            tclr = sconst.RED
        else:
            tclr = sconst.GREY if val == 0 else sconst.BLACK

        # render text and get coords to center in tile
        txt = self.font.render(str(val), True, tclr)
        txt_rect, img_rect = txt.get_rect(), self.img.get_rect()
        txt_x = img_rect.width / 2 - txt_rect.width / 2
        txt_y = img_rect.height / 2 - txt_rect.height / 2

        # blit text render onto tile; blit tile onto background
        self.img.fill(bclr)
        self.img.blit(txt, (txt_x, txt_y))
        self.bg.blit(self.img, self.coords)

# collection of sudoku tiles for rendering
class Render:
    N = 9 # grid of NxN boxes

    def __init__(self, width: int, bg: pg.Surface, font: pg.font, board: sc.Board):
        # tiles: grid of selectable cells (rect + surface)
        # last: last selected tile
        self.tiles = [[None for _ in range(self.N)] for __ in range(self.N)]
        self.last = None

        lines = 10      # grid lines in between / on outside
        l_clr = (0,0,0) # line color
        l_width = 2     # line width
        x, y, step = 0, 0, width / self.N
        # draw grid lines
        for i in range(lines):
            x, y = i*step, i*step
            l_width = 4 if i in [3,6] else 2
            pg.draw.line(bg, l_clr, (0,y), (width,y), l_width) # horiz
            pg.draw.line(bg, l_clr, (x,0), (x,width), l_width) # vert

        b_brdr = step // 20   # box border thickness
        x, y = 0, 0
        # create grid of Tile, store in self.tiles
        for i in range(self.N):
            for j in range(self.N):
                x, y = j*step, i*step
                rx = x + b_brdr + l_width
                ry = y + b_brdr + l_width
                rside = step - (2 * b_brdr + l_width)
                cell = board.get_cell(i, j)
                self.tiles[i][j] = Tile(i, j, rx, ry, rside, bg, font, cell)

    # highlight tile if coords fall within a pre-defined rect region
    def chk_coords(self, bg: pg.Surface, x: int, y: int) -> Tuple[int,int]:
        for i in range(self.N):
            for j in range(self.N):
                if self.tiles[i][j].chk_slctd(x,y):
                    if self.last: self.last.update(False)
                    self.tiles[i][j].update(True)
                    self.last = self.tiles[i][j]
                    return (i, j)
        return (-1, -1)

    # re-render specified tile
    def update_tile(self, i: int, j: int) -> None:
        self.tiles[i][j].update(False)

    # re-render all tiles
    def update_all(self) -> None:
        for i in range(self.N):
            for j in range(self.N):
                self.update_tile(i, j)

# class for display box containing messages for the player
class Msgbox:
    def __init__(self, x: int, y: int, width: int, height: int,
                 bg: pg.Surface, font: pg.font):
        self.s = "Press 'h' for active hints or 'm' for manual board config"
        self.coords = (x, y)
        self.img = pg.Surface((width, height))
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = x, y
        self.bg = bg
        self.font = font
        self.update()

    # update message box text
    def set_txt(self, s: str) -> None:
        self.s = s
        self.update()

    # render text to image and blit onto background
    def update(self) -> None:
        txt = self.font.render(self.s, True, sconst.BLACK)
        txt_rect = txt.get_rect()
        txt_x = self.rect.width / 2 - txt_rect.width / 2
        txt_y = self.rect.height / 2 - txt_rect.height / 2
        self.img.fill(sconst.WHITE)
        self.img.blit(txt, (txt_x, txt_y))
        self.bg.blit(self.img, self.coords)
