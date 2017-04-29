from itertools import product, combinations
from AlgorithmX import *

"""
In an exact cover problem we have to find subsets which cover each element in a given set exactly once. For example,

Given set X: {1, 2, 3, 4}

Subsets: A: {1, 2}, B: {2, 3, 4}, C: {3, 4}

Exact cover: A and C

The corresponding Algorithm X matrix which can be used is like this:

X: {1, 2, 3, 4} (this is just column titles, not the matrix itself)

_______________

A: {1, 1, 0, 0}

B: {0, 1, 1, 1}

C: {0, 0, 1, 1}

 

A hashi puzzle can be converted to an exact cover problem similarly.

I will proceed with my explanation using a similar (not the same) method as that used in the code you saw in the code 
golf page.

For example, consider the following puzzle:

1 2

  1

Coordinates of top-left 1, top-right 2 and bottom-right 1 are (0, 0), (1, 0) and (1, 1) respectively. For each pair of 
adjacent numbers, we may build 0, 1 or 2 bridges. If we denote each possible bridge as L(eft)/R(ight)/U(p)/D(own) and 
its bridge number (either 1 or 2), the possible bridges are:

Top-left 1 - R1

Top-right 2 - L1, D1

Bottom-right 1 - U1

Given set X: {(0, 0, R1), (1, 0, L1), (1, 0, D1), (1, 1, U1)}

Subsets: Bridge A (0, 0)-(1, 0), bridge B (1, 0)-(1, 1)

Exact cover: A and B

Matrix (sorry for the alignment):

X: {(0, 0, R1), (1, 0, L1), (1, 0, D1), (1, 1, U1)}

___________________________________________________

A: (1, 1, 0, 0}

B: {0, 0, 1, 1}

 

A more complex puzzle for you to think about:

1.3
...
123

EX below means exclude such bridge.

Given set X: {(0, 0, R1), (0, 2, R1), (1, 2, EX), (1, 2, L1), (1, 2, R1), (1, 2, R2), (2, 0, D1), (2, 0, D2), 
(2, 0, L1), (2, 2, EX), (2, 2, L1), (2, 2, L2), (2, 2, U1), (2, 2, U2)}

Subsets of bridges:

A (0, 0)-(2, 0) one bridge

B (0, 2)-(1, 2) one bridge

C (1, 2)-(2, 2) one bridge

D (1, 2)-(2, 2) two bridges

E (2, 0)-(2, 2) one bridge

F (2, 0)-(2, 2) two bridges

G Exclude (1, 2, R2)

H Exclude (1, 2, L1)

I Exclude (2, 2, L2)

J Exclude (2, 2, U2)

Exact cover: A, B, C, F, G, I

That means the bridges as described in A, B, C and F are required to complete the puzzle.

Matrix (I will skip the column titles for this case - the 14 column titles are in the same order as the 14 elements in 
given set X above):

A: {1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0}

B: {0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}

C: {0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0}

D: {0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0}

E: {0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0}

F: {0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1}

G: {0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0}

H: {0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}

I: {0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0}

J: {0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1}
"""


def solve_hashi(puzzle):
    positions = list(product(range(len(puzzle)), range(len(puzzle[0]))))  # coordinates for the grid

    islands = {(i, j): int(puzzle[i][j])
               for i, j in positions if '.' != puzzle[i][j]}
    # print("islands:", islands)

    edges = {p: list()
             for p in positions}
    # get all the possible edges in the puzzle
    edge_list = list()
    for p in islands.keys():  # position of each island in the puzzle
        for i, j in ((0, 1), (1, 0)):  # move down and to the right
            q = p[0] + i, p[1] + j
            e = [p, 0]  # edge starts at p
            while q in positions:
                edges[q] += [e]  # add that to the edges through q
                if q in islands:
                    if not (islands[p] == 1 and islands[q] == 1):  # make sure this is a valid edge
                        e[1] = q  # edge ends at q
                        edges[p] += [e]  # add that to the edges from p
                        edge_list += [e]  # add that to the list of all edges
                    break
                q = q[0] + i, q[1] + j
    # print("edges list:", edge_list)

    # remove edges that don't terminate; e[1] = 0
    edges = {pos: [e for e in y if e[1] != 0]
             for pos, y in edges.items()}
    # print(edges)

    intersecting_edges = {pos: y
                          for pos, y in edges.items() if pos not in islands.keys() and len(y) > 1}
    # print("intersections:", intersecting_edges)

    island_edges = {pos: y
                    for pos, y in edges.items() if pos in islands.keys()}
    '''this dict will have each island position in the puzzle as a key, 
    with a list of the edges to/from that position as the values'''
    # print("bridges:", island_edges)

    exclusions = {pos: sum(min(islands[p], islands[q], 2) for p, q in island_edges[pos]) - islands[pos]
                  for pos in islands.keys()}
    # {island_pos: number of bridges that need to be excluded from total possible}
    print("needed exclusions: ", exclusions)

    # # # #

    X = set()  # [(island_pos, (edge, index))]
    for island in islands.keys():
        for edge in island_edges[island]:
            p, q = edge

            for b in range(1, min(islands[p], islands[q], 2)+1):
                X.add((island, (tuple(edge), b)))

            for p_ex in range(exclusions[p]):
                X.add((p, "ex%s" % p_ex))

            for q_ex in range(exclusions[q]):
                X.add((q, "ex%s" % q_ex))

    X = sorted(list(X))
    print("X:", X)
    print("Constructed X")

    Y = dict()  # {(edge, number_of): [X_element1, X_element2, ...]}
    for edge in edge_list:
        p, q = edge
        bridges = min(islands[p], islands[q], 2)
        for b in range(1, bridges+1):
            if b == 2 and islands[p] == 2 and islands[q] == 2:  # can't double connect two 2 islands
                continue
            bridge_key = (tuple(edge), b)
            bridge_value = set()
            for pos in edge:
                for c in range(1, b+1):
                    if pos in edge:
                        bridge_value.add((pos, (tuple(edge), c)))
                    else:
                        bridge_value.add((pos, c))
            Y[bridge_key] = list(bridge_value)

        for ex in range(min(exclusions[p], exclusions[q], 2), 0, -1):
            for exes in combinations(product(range(exclusions[p]), range(exclusions[q])), ex):
                if ex == 1:
                    p_ex, q_ex = exes[0]
                    exclude_key = ((tuple(edge), bridges), (p_ex, q_ex))
                    exclude_value = set()
                    exclude_value.add((p, "ex%s" % p_ex))
                    exclude_value.add((q, "ex%s" % q_ex))
                    for pos in edge:
                        if pos in edge:
                            exclude_value.add((pos, (tuple(edge), bridges)))
                        else:
                            exclude_value.add((pos, bridges))
                    Y[exclude_key] = list(exclude_value)
                else:
                    ex1, ex2 = exes
                    p_ex1, q_ex1 = ex1
                    p_ex2, q_ex2 = ex2
                    if p_ex1 == p_ex2 or q_ex1 == q_ex2:
                        continue
                    exclude_key = ((tuple(edge), 1, 2), ((p_ex1, q_ex1), (p_ex2, q_ex2)))
                    exclude_value = set()
                    exclude_value.add((p, "ex%s" % p_ex1))
                    exclude_value.add((q, "ex%s" % q_ex1))
                    exclude_value.add((p, "ex%s" % p_ex2))
                    exclude_value.add((q, "ex%s" % q_ex2))
                    for pos in edge:
                        if pos in edge:
                            exclude_value.add((pos, (tuple(edge), 1)))
                            exclude_value.add((pos, (tuple(edge), 2)))
                        else:
                            exclude_value.add((pos, 1))
                            exclude_value.add((pos, 2))
                    Y[exclude_key] = list(exclude_value)

    print("Y:", Y)
    print("Constructed Y")

    # # # #

    X, Y = exact_cover(X, Y)
    print("new X:", X)
    print("Reformatted X")

    print("Solving...")
    extracted_solutions = set()
    for solution in solve(X, Y, []):
        extracted_sol = list()
        for sol in solution:
            if type(sol[1]) is int:
                extracted_sol.append((sol[0], sol[1]))
        extracted_sol = tuple(sorted(extracted_sol))
        if extracted_sol not in extracted_solutions:
            yield extracted_sol
            extracted_solutions.add(extracted_sol)


def traverse(edge):
    p, q = edge
    for pos in product(range(min(p[0], q[0]), max(p[0], q[0]) + 1), range(min(p[1], q[1]), max(p[1], q[1]) + 1)):
        yield pos

# # # #


if __name__ == "__main__":
    import time

    def draw(puzzle, solved):
        grid = [list(ln) for ln in puzzle]

        north_south = ".|$"
        east_west = ".-="

        for edge in solved:
            p, q = edge[0]
            b = edge[1]

            for pos in product(range(min(p[0], q[0]), max(p[0], q[0]) + 1),
                               range(min(p[1], q[1]), max(p[1], q[1]) + 1)):
                r, c = pos
                if grid[r][c] == ".":
                    if p[0] == q[0]:
                        grid[r][c] = east_west[b]
                    elif p[1] == q[1]:
                        grid[r][c] = north_south[b]

        return "\n".join(["".join(ln) for ln in grid])

    x7_1 = ["2..3.1.",
            "....3.4",
            ".1.2...",
            "3.5.5.4",
            ".1.1...",
            "1.2.1..",
            ".2.3..2"]
    """
    (((2, 3), (4, 3)), 1, (((((3, 2), (3, 4)), 1, 2), ('ex0', 'ex0'), ('ex0', 'ex1')),)): [((2, 3), (((2, 3), (4, 3)), 1)), ((4, 3), (((2, 3), (4, 3)), 1)), ((3, 2), (((3, 2), (3, 4)), 2)), ((3, 4), (((3, 2), (3, 4)), 2)), ((3, 2), 'ex0'), ((3, 2), (((3, 2), (3, 4)), 1)), ((3, 4), 'ex1'), ((3, 4), 'ex0'), ((3, 4), (((3, 2), (3, 4)), 1))], 
    
    (((3, 2), (3, 4)), 1, (((((2, 3), (4, 3)), 1), ('ex0', 'ex0')), ((((2, 3), (4, 3)), 1), ('ex1', 'ex0')))): [((3, 2), (((3, 2), (3, 4)), 1)), ((3, 4), (((3, 2), (3, 4)), 1)), ((2, 3), 'ex1'), ((2, 3), 'ex0'), ((4, 3), (((2, 3), (4, 3)), 1)), ((2, 3), (((2, 3), (4, 3)), 1)), ((4, 3), 'ex0')], 
    (((3, 2), (3, 4)), 2, (((((2, 3), (4, 3)), 1), ('ex0', 'ex0')), ((((2, 3), (4, 3)), 1), ('ex1', 'ex0')))): [((3, 2), (((3, 2), (3, 4)), 1)), ((3, 4), (((3, 2), (3, 4)), 1)), ((3, 2), (((3, 2), (3, 4)), 2)), ((3, 4), (((3, 2), (3, 4)), 2)), ((2, 3), 'ex1'), ((2, 3), 'ex0'), ((4, 3), (((2, 3), (4, 3)), 1)), ((2, 3), (((2, 3), (4, 3)), 1)), ((4, 3), 'ex0')]
    """

    # this one fails because (3, 0) <-> (3, 3) intersects two possible edges
    x7_2 = ["2.3..1.",
            ".1.1..2",
            "..3.1..",
            "2..1..3",
            "..2.2..",
            "1......",
            ".2..3.2"]
    """
    ((((3, 0), (3, 3)), 1), ('ex1', 'ex0')): [((3, 0), 'ex1'), ((3, 3), 'ex0'), ((3, 0), (((3, 0), (3, 3)), 1)), ((3, 3), (((3, 0), (3, 3)), 1))],
    ((((3, 0), (3, 3)), 1), ('ex0', 'ex0')): [((3, 0), 'ex0'), ((3, 3), 'ex0'), ((3, 0), (((3, 0), (3, 3)), 1)), ((3, 3), (((3, 0), (3, 3)), 1))], 
    
    (((1, 1), (6, 1)), 1, (((((3, 0), (3, 3)), 1), ('ex0', 'ex0')),)): [((1, 1), (((1, 1), (6, 1)), 1)), ((6, 1), (((1, 1), (6, 1)), 1)), ((3, 3), 'ex0'), ((3, 0), 'ex0'), ((3, 3), (((3, 0), (3, 3)), 1)), ((3, 0), (((3, 0), (3, 3)), 1))],
    (((1, 1), (6, 1)), 1, (((((3, 0), (3, 3)), 1), ('ex1', 'ex0')),)): [((1, 1), (((1, 1), (6, 1)), 1)), ((6, 1), (((1, 1), (6, 1)), 1)), ((3, 3), 'ex0'), ((3, 3), (((3, 0), (3, 3)), 1)), ((3, 0), 'ex1'), ((3, 0), (((3, 0), (3, 3)), 1))],
    
    (((2, 2), (4, 2)), 1, (((((3, 0), (3, 3)), 1), ('ex1', 'ex0')),)): [((2, 2), (((2, 2), (4, 2)), 1)), ((4, 2), (((2, 2), (4, 2)), 1)), ((3, 3), 'ex0'), ((3, 3), (((3, 0), (3, 3)), 1)), ((3, 0), 'ex1'), ((3, 0), (((3, 0), (3, 3)), 1))], 
    ((((2, 2), (4, 2)), 1), ('ex0', 'ex0')): [((2, 2), 'ex0'), ((4, 2), 'ex0'), ((2, 2), (((2, 2), (4, 2)), 1)), ((4, 2), (((2, 2), (4, 2)), 1))],
    ((((2, 2), (4, 2)), 1), ('ex1', 'ex1')): [((2, 2), 'ex1'), ((4, 2), 'ex1'), ((2, 2), (((2, 2), (4, 2)), 1)), ((4, 2), (((2, 2), (4, 2)), 1))],
    (((2, 2), (4, 2)), 1, (((((3, 0), (3, 3)), 1), ('ex0', 'ex0')),)): [((2, 2), (((2, 2), (4, 2)), 1)), ((4, 2), (((2, 2), (4, 2)), 1)), ((3, 3), 'ex0'), ((3, 0), 'ex0'), ((3, 3), (((3, 0), (3, 3)), 1)), ((3, 0), (((3, 0), (3, 3)), 1))],
    """

    """
    ((1, 1), (6, 1)) and ((2, 2), (4, 2)) both intersect ((3, 0), (3, 3))
    That means both subsets try to exclude that edge which means we can't select both subsets
    I think I need to redo X and Y then...
    """

    twos = ["2.2.2",
            ".....",
            "4.2.2",
            ".....",
            "2.2.2"]

    start = time.time()
    for solve in solve_hashi(x7_1):
        print(solve)
        print(draw(x7_1, solve))
        print("in %s minutes" % ((time.time() - start) / 60))
    print("Finished in %s minutes" % ((time.time() - start) / 60))
