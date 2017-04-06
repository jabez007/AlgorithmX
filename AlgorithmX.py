
def exact_cover(x, y):
    x = {j: set() for j in x}
    for i, row in y.items():
        for j in row:
            x[j].add(i)
    return x, y


def solve(x, y, solution=[]):
    if not x:
        yield list(solution)
    else:
        c = min(x, key=lambda c: len(x[c]))
        for r in list(x[c]):
            solution.append(r)
            cols = select(x, y, r)
            for s in solve(x, y, solution):
                yield s
            deselect(x, y, r, cols)
            solution.pop()


def select(x, y, r):
    cols = []
    for j in y[r]:
        for i in x[j]:
            for k in y[i]:
                if k != j:
                    x[k].remove(i)
        cols.append(x.pop(j))
    return cols


def deselect(x, y, r, cols):
    for j in reversed(y[r]):
        x[j] = cols.pop()
        for i in x[j]:
            for k in y[i]:
                if k != j:
                    x[k].add(i)

if __name__ == "__main__":
    X = {1, 2, 3, 4, 5, 6, 7}
    Y = {
        'A': [1, 4, 7],
        'B': [1, 4],
        'C': [4, 5, 7],
        'D': [3, 5, 6],
        'E': [2, 3, 6, 7],
        'F': [2, 7]}

    X, Y = exact_cover(X, Y)

    for s in solve(X, Y):
        print(s)  # prints each possible solution
