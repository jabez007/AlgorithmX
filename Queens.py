from itertools import product
from AlgorithmX import *


def solve_queens(grid):
    """
    A n-Queens solver using Algorithm X.
    https://en.wikipedia.org/wiki/Eight_queens_puzzle
    :param grid: 
    :return: 
    """
    rows, columns = len(grid), len(grid[0])
    N = rows  # the grid should be square

    '''X is our universe - as a list'''
    X = ([("r", r) for r in range(N)] +  # each row in the grid
         [("c", c) for c in range(N)] +  # each column in the grid
         [("rd", rd, SECONDARY) for rd in right_diagonal_set(N)] +  # each right diagonal in the grid
         [("ld", ld, SECONDARY) for ld in left_diagonal_set(N)])  # each left diagonal in the grid
    # There are probably more diagonals than there are Queens to cover them all, so those are secondary

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
        Y[(r, c, "Q")] = [("r", r), ("c", c)]
        # Every row and column has to be covered by a Queen

        rd_moves = right_diagonal((r, c), N)
        if rd_moves:
            Y[(r, c, "Q")].append(("rd", rd_moves[0], SECONDARY))

        ld_moves = left_diagonal((r, c), N)
        if ld_moves:
            Y[(r, c, "Q")].append(("ld", ld_moves[0], SECONDARY))

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
        if rd_moves:
            rd.add(rd_moves[0])
    return sorted(list(rd))


def left_diagonal_set(N):
    ld = set()
    for rc in product(range(N), range(N)):
        ld_moves = left_diagonal(rc, N)
        if ld_moves:
            ld.add(ld_moves[0])
    return sorted(list(ld))


if __name__ == "__main__":
    puzzle = [
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""]]

    count = 0
    for sol in solve_queens(puzzle):
        count += 1
        for line in sol:
            print(line)
        print()
    print("%s solutions found" % count)
