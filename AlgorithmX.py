"""
Algorithm X in 30-ish lines of Python
from
http://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html
"""

SECONDARY = "secondary"


def exact_cover(x, y):
    """
    converts a list/set of elements X into and dict where the keys are the set's elements and the values are the set of
    subsets from Y that contain the element 
    :param x: <list or set> all the elements that make up our universal set
    :param y: <dict> the subsets that our set elements are divided in to
    :return: <tuple(dict, dict)> X converted into a dict and Y unchanged
    """
    x = {j: set() for j in x}
    for i, row in y.items():
        for j in row:
            x[j].add(i)
    return x, y


def solve(x, y, solution=[]):
    if not x or \
            (all(isinstance(k, tuple) for k in x.keys()) and all(k[-1] == SECONDARY for k in x.keys())):
        yield list(solution)
    else:
        # find the element contained in the least number of subsets
        c = min(x, key=lambda c: len(x[c]) if not isinstance(c, tuple) or c[-1] != SECONDARY else len(y.keys()))
        for r in list(x[c]):  # for each subset that contains this element
            solution.append(r)  # add that subset to our potential solution
            cols = select(x, y, r)  # remove the columns for the other elements contained in this subset
            for s in solve(x, y, solution):
                yield s
            deselect(x, y, r, cols)
            solution.pop()


def select(x, y, r):
    cols = []
    for j in y[r]:  # for each element in this subset
        for i in x[j]:  # for each other subset that contains the element
            for k in y[i]:  # for each other element in that subset
                if k != j:
                    x[k].remove(i)  # remove this subset from the other element; remove the row from the matrix
        cols.append(x.pop(j))  # remove the column for the element; remove the column from the matrix
    return cols


def deselect(x, y, r, cols):
    for j in reversed(y[r]):
        x[j] = cols.pop()
        for i in x[j]:
            for k in y[i]:
                if k != j:
                    x[k].add(i)

if __name__ == "__main__":
    X = {1, 2, 3, 4, 5, 6, 7, (8, SECONDARY)}
    Y = {
        'A': [1, 4, 7, (8, SECONDARY)],
        'B': [1, 4],
        'C': [4, 5, 7],
        'D': [3, 5, 6],
        'E': [2, 3, 6, 7],
        'F': [2, 7]}

    X, Y = exact_cover(X, Y)

    for s in solve(X, Y):
        print(s)  # prints each possible solution
