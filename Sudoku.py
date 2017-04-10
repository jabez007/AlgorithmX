#!/usr/bin/env python3

# Author: Ali Assaf <ali.assaf.mail@gmail.com>
# Copyright: (C) 2010 Ali Assaf
# License: GNU General Public License <http://www.gnu.org/licenses/>

from itertools import product
from AlgorithmX import *


def solve_sudoku(grid):
    """
    An efficient Sudoku solver using Algorithm X.
    :param grid: 
    :return: 
    """
    rows, columns = int(len(grid) ** (1/2)), int(len(grid[0]) ** (1/2))
    N = rows * columns

    '''X is our universe - as a list'''
    X = ([("rc", rc) for rc in product(range(N), range(N))] +  # row, column; coordinates for the grid
         [("rn", rn) for rn in product(range(N), range(1, N + 1))] +  # 1 - 9 for each row (row_index, number)
         [("cn", cn) for cn in product(range(N), range(1, N + 1))] +  # 1 - 9 for each column (column_index, number)
         [("bn", bn) for bn in product(range(N), range(1, N + 1))])  # 1 - 9 for each "box" (box_index, number)

    Y = dict()
    '''
    Y separates our universe into subsets
        where (row, column, number) covers
            - (row, column)
            - (row_index, number)
            - (column_index, number)
            - (box_index, number)
    '''
    for r, c, n in product(range(N), range(N), range(1, N + 1)):
        b = (r // rows) * rows + (c // columns)  # Box index
        Y[(r, c, n)] = [
            ("rc", (r, c)),
            ("rn", (r, n)),
            ("cn", (c, n)),
            ("bn", (b, n))]

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
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]]

    for sol in solve_sudoku(puzzle):
        for line in sol:
            print(line)
        print()
    """
    [5, 3, 4, 6, 7, 8, 9, 1, 2]
    [6, 7, 2, 1, 9, 5, 3, 4, 8]
    [1, 9, 8, 3, 4, 2, 5, 6, 7]
    [8, 5, 9, 7, 6, 1, 4, 2, 3]
    [4, 2, 6, 8, 5, 3, 7, 9, 1]
    [7, 1, 3, 9, 2, 4, 8, 5, 6]
    [9, 6, 1, 5, 3, 7, 2, 8, 4]
    [2, 8, 7, 4, 1, 9, 6, 3, 5]
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
    """
