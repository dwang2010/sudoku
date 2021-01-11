from typing import List, Tuple

# single square on board that can hold value from 1-9
class Cell:
    def __init__(self, i: int, j: int, val: int=0, lock: bool=False):
        self.pos = (i, j)
        self.val = val
        self.lock = lock

    def set_val(self, val: int) -> None:
        self.val = val

    def set_lock(self, lock: bool) -> None:
        self.lock = lock

    def get_val(self) -> int:
        return self.val

    def get_lock(self) -> bool:
        return self.lock

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
    def validate(self) -> Tuple[bool, int]:
        res, s = 0, set()
        for cell in self.cells:
            if cell.val > 0:
                res += 1
                s.add(cell.val)
        return (res == len(s), len(s))

# holds all the cells / regions
class Board:
    N = 9 # grid of NxN cells

    def __init__(self):
        rows, cols, blks = self.N, self.N, self.N

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

    # check all board regions for sudoku 1-9 uniqueness
    def chk_board(self) -> Tuple[bool, bool]:
        r_nums = 0
        for r in self.r_reg:
            uniq, nums = r.validate()
            if not uniq: return (False, False)
            r_nums += nums

        c_nums = 0
        for c in self.c_reg:
            uniq, nums = c.validate()
            if not uniq: return (False, False)
            c_nums += nums

        b_nums = 0
        for b in self.b_reg:
            uniq, nums = b.validate()
            if not uniq: return (False, False)
            b_nums += nums

        return (True, r_nums + c_nums + b_nums == 243)

    # load in board configuration
    # TBD: make this load from file?
    def load_board(self, grid: List[List[int]]) -> bool:
        rows, cols = len(grid), len(grid[0])
        if rows != self.N and cols != self.N: return False

        for r in range(rows):
            for c in range(cols):
                lock = True if grid[r][c] else False
                self.g[r][c].set_val(grid[r][c])
                self.g[r][c].set_lock(lock)
        return True

    # clear all board cells to zero value
    def clear_board(self) -> None:
        zero_grid = [[0 for _ in range(self.N)] for __ in range(self.N)]
        self.load_board(zero_grid)

    # set all cells with non-zero value to locked
    def lock_board(self) -> None:
        for r in range(self.N):
            for c in range(self.N):
                if self.g[r][c].get_val():
                    self.g[r][c].set_lock(True)

    # return current board state
    def _print_board(self) -> None:
        self.test = [[None for _ in range(self.N)] for __ in range(self.N)]

        for r in range(self.N):
            for c in range(self.N):
                self.test[r][c] = self.g[r][c].val

        for r in range(self.N):
            print (self.test[r])

    # return board cell
    def get_cell(self, i: int, j: int) -> Cell:
        return self.g[i][j]

    # update board cell with new value
    def update_cell(self, i: int, j: int, val: int) -> Cell:
        self.g[i][j].set_val(val)
        return self.g[i][j]

    # find solution for starting board condition
    def solve_board(self) -> bool:
        # clear existing non-locked cells
        # recursive dfs: try all board combos at each unlocked position
        # helper function takes index (i, j) returns bool
        # inserts starting from 1 at specified position
        # if board valid and recursive step into next step valid, return true
        # else if either fails, increments current val up to 9

        for i in range(self.N):
            for j in range(self.N):
                if not self.g[i][j].get_lock():
                    self.g[i][j].set_val(0)

        if not self.chk_board()[0]: return False

        def hlpr(i: int, j: int) -> bool:
            if i == self.N: return True

            cell = self.g[i][j]
            lock = cell.get_lock()

            ni = i+1 if j == 8 else i
            nj = (j+1) % 9

            if lock: return hlpr(ni, nj)

            for k in range(1, self.N+1):
                cell.set_val(k)
                if self.chk_board()[0] and hlpr(ni, nj):
                    return True
                cell.set_val(0)
            return False

        return hlpr(0,0)
