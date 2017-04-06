from itertools import product
from AlgorithmX import *


def solve_square(grid):
    """
    An efficient Latin Squares solver using Algorithm X.
    :param grid: 
    :return: 
    """
    rows, columns = len(grid), len(grid[0])
    N = rows

    '''X is our universe - as a list'''
    X = ([("rc", rc) for rc in product(range(N), range(N))] +  # row, column; coordinated for the grid
         [("rn", rn) for rn in product(range(N), range(1, N + 1))] +  # 1 - 9 for each row (row_index, number)
         [("cn", cn) for cn in product(range(N), range(1, N + 1))])  # 1 - 9 for each column (column_index, number)

    Y = dict()
    '''
    Y separates our universe into subsets
        where (row, column, number) covers
            - (row, column)
            - (row_index, number)
            - (column_index, number)
    '''
    for r, c, n in product(range(N), range(N), range(1, N + 1)):
        Y[(r, c, n)] = [
            ("rc", (r, c)),
            ("rn", (r, n)),
            ("cn", (c, n))]

    X, Y = exact_cover(X, Y)

    '''Select the known elements of the puzzle grid'''
    for i, row in enumerate(grid):
        for j, n in enumerate(row):
            if n:
                select(X, Y, (i, j, n))

    for solution in solve(X, Y, []):
        for (r, c, n) in solution:
            grid[r][c] = n
        yield grid


if __name__ == "__main__":
    puzzle = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]]

    for sol in solve_square(puzzle):
        for line in sol:
            print(line)
        print()
    """
    [1, 2, 3, 4]
    [2, 1, 4, 3]
    [3, 4, 1, 2]
    [4, 3, 2, 1]
    """