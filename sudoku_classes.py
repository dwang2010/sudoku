from typing import List

# single square on board that can hold value from 1-9
class Cell:
    def __init__(self, i: int, j: int, val: int=0, fix: bool=False):
        self.val = val
        self.pos = (i,j)
        self.fix = fix

    # check if input value legal, if so set
    def set_val(self, val: int, fix: bool=False) -> bool:
        if val > 0:
            self.val = val
            self.fix = fix
            return True
        return False

    # clear cell value back to 0
    def clear_val(self) -> None:
        if not self.fix:
            self.val = 0

# group of nine cells on the board
# no need to separate per row / column / block
# load in appropriate cells in board init
class Region:
    def __init__(self):
        self.cells = []

    # add board cell to region during init
    def add_cell(self, c: Cell) -> None:
        self.cells.append(c)

    # check that region only holds unique values
    def validate(self) -> bool:
        res, s = 0, set()
        for cell in self.cells:
            if cell.val > 0:
                res += 1
                s.add(cell.val)
        return res == len(s)

# holds all the cells / regions
class Board:
    def __init__(self):
        rows, cols, blks = 9, 9, 9

        # init grid of cells
        self.g = [[Cell(r,c) for c in range(cols)] for r in range(rows)]

        # init row / col / blk regions
        self.r_reg = [Region() for _ in range(rows)]
        self.c_reg = [Region() for _ in range(cols)]
        self.b_reg = [Region() for _ in range(blks)]

        # populate regions with grid cells
        for r in range(rows):
            for c in range(cols):
                self.r_reg[r].add_cell(self.g[r][c]) # row
                self.c_reg[c].add_cell(self.g[r][c]) # col

                blk_ind = 3*(r//3) + c//3
                self.b_reg[blk_ind].add_cell(self.g[r][c]) # blk

    # check that all regions have legal number assignment
    def chk_valid(self) -> bool:
        if not all(r.validate() for r in self.r_reg): return False
        if not all(c.validate() for c in self.c_reg): return False
        if not all(b.validate() for b in self.b_reg): return False
        return True

    # load in board configuration, 0 denoting unfilled
    # otherwise, if value present, also configure cell as "fixed"
    # TBD: make this load from file
    def load(self, grid: List[List[int]]) -> bool:
        rows, cols = len(grid), len(grid[0])
        if rows != 9 and cols != 9: return False

        for r in range(rows):
            for c in range(cols):
                fix = True if grid[r][c] else False
                self.g[r][c].set_val( grid[r][c], fix )
        return True

    # debug: return current board
    def _print_board(self) -> None:
        rows, cols = 9, 9
        self.test = [[None for _ in range(rows)] for __ in range(cols)]

        for r in range(rows):
            for c in range(cols):
                self.test[r][c] = self.g[r][c].val

        for r in range(rows):
            print (self.test[r])
