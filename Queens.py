from itertools import product
from AlgorithmX import *


def solve_queens(grid, Q=4):
    """
    An efficient Latin Squares solver using Algorithm X.
    :param grid: 
    :param Q: number of Queens on the board 
    :return: 
    """
    rows, columns = len(grid), len(grid[0])
    N = rows  # the grid should be square

    '''X is our universe - as a list'''
    X = ([("r", r) for r in range(N)] +  # each row in the grid
         [("c", c) for c in range(N)] +  # each column in the grid
         [("rd", rd) for rd in right_diagonal_set(N)] +  # each right diagonal in the grid
         [("ld", ld) for ld in left_diagonal_set(N)])  # each left diagonal in the grid

    Y = dict()
    '''
    Y separates our universe into subsets
        where (row, column) covers
            - row
            - column
            - right_diagonal
            - left_diagonal
    '''
    for r, c in product(range(N), range(N)):
        rd_moves = right_diagonal((r, c), N)
        ld_moves = left_diagonal((r, c), N)

        if rd_moves and ld_moves:
            rd = ("rd", rd_moves[0])
            ld = ("ld", ld_moves[0])

            if rd in X and ld in X:
                Y[(r, c, "Q")] = [("r", r), ("c", c),
                                  ("rd", rd_moves[0]),
                                  ("ld", ld_moves[0])]

    X, Y = exact_cover(X, Y)

    '''Select the known elements of the puzzle grid'''
    for i, row in enumerate(grid):
        for j, p in enumerate(row):
            if p != "":
                select(X, Y, (i, j, p))

    for solution in solve(X, Y, []):
        for r, c in product(range(N), range(N)):
            grid[r][c] = ""
            for p in ("Q", "B", "R", "K"):
                if (r, c, p) in solution:
                    grid[r][c] = p
        yield grid


def queen_moves(rc, N):
    return row_move(rc, N) + column_move(rc, N) + diagonal_move(rc, N)


def row_move(rc, N):
    moves = list()
    for i, j in [(1, 0), (-1, 0)]:
        r = rc[0] + i
        c = rc[1] + j
        while (0 <= r < N) and (0 <= c < N):
            moves.append((r, c))
            r += i
            c += j
    return moves


def column_move(rc, N):
    moves = list()
    for i, j in [(0, 1), (0, -1)]:
        r = rc[0] + i
        c = rc[1] + j
        while (0 <= r < N) and (0 <= c < N):
            moves.append((r, c))
            r += i
            c += j
    return moves


def diagonal_move(rc, N):
    return right_diagonal(rc, N) + left_diagonal(rc, N)


def right_diagonal(rc, N):
    moves = list()
    for i, j in [(1, 1), (-1, -1)]:
        r = rc[0] + i
        c = rc[1] + j
        while (0 <= r < N) and (0 <= c < N):
            moves.append((r, c))
            r += i
            c += j
    if moves:
        moves.append(rc)
    return sorted(moves)


def left_diagonal(rc, N):
    moves = list()
    for i, j in [(1, -1), (-1, 1)]:
        r = rc[0] + i
        c = rc[1] + j
        while (0 <= r < N) and (0 <= c < N):
            moves.append((r, c))
            r += i
            c += j
    if moves:
        moves.append(rc)
    return sorted(moves)


def right_diagonal_set(N):
    rd = set()
    for rc in product(range(N), range(N)):
        rd_moves = right_diagonal(rc, N)
        if rd_moves and left_diagonal(rd_moves[0], N):  # we have a right and left diagonal
            rd.add(rd_moves[0])
    return list(rd)


def left_diagonal_set(N):
    ld = set()
    for rc in product(range(N), range(N)):
        ld_moves = left_diagonal(rc, N)
        if ld_moves and right_diagonal(ld_moves[0], N):  # we have a left and right diagonal
            ld.add(ld_moves[0])
    return list(ld)


if __name__ == "__main__":
    puzzle = [
        ["", "", "", ""],
        ["", "",  "", ""],
        ["", "",  "", ""],
        ["", "",  "", ""]]

    for sol in solve_queens(puzzle):
        for line in sol:
            print(line)
        print()
    """
    ["", "Q", "", ""]
    ["", "", "", "Q"]
    ["Q", "", "", ""]
    ["", "", "Q", ""]
    """
