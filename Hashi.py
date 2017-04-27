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
    # print(islands)

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
    # print(edge_list)

    # remove edges that don't terminate; e[1] = 0
    edges = {pos: [e for e in y if e[1] != 0]
             for pos, y in edges.items()}
    # print(edges)

    intersecting_edges = {pos: y
                          for pos, y in edges.items() if pos not in islands.keys() and len(y) > 1}
    # print(intersecting_edges)

    island_edges = {pos: y
                    for pos, y in edges.items() if pos in islands.keys()}
    '''this dict will have each island position in the puzzle as a key, 
    with a list of the edges to/from that position as the values'''
    # print(island_edges)

    exclusions = {pos: sum(min(islands[p], islands[q], 2) for p, q in island_edges[pos]) - islands[pos]
                  for pos in islands.keys()}
    # {island_pos: number of bridges that need to be excluded from total possible}
    # print(exclusions)

    X = list()  # [(island_pos, (edge, index))]
    for pos in islands.keys():
        for e in island_edges[pos]:
            p, q = e
            for b in range(1, min(islands[p], islands[q], 2)+1):
                element = (pos, (tuple(e), b))
                X.append(element)
        for ex in range(exclusions[pos]):
            element = (pos, "ex%s" % ex)
            X.append(element)
    # print("X:", X)
    print("Constructed X")

    def generate_exclusions(for_edge, all=False):
        pos1, pos2 = for_edge
        exes = list(product(range(exclusions[pos1]), range(exclusions[pos2])))
        if not all:
            for p_ex, q_ex in exes:
                for bridges in range(1, min(islands[pos1], islands[pos2], 2) + 1):
                    k = ((tuple(for_edge), bridges), ("ex%s" % p_ex, "ex%s" % q_ex))
                    v = [(pos1, "ex%s" % p_ex), (pos2, "ex%s" % q_ex),
                         (pos1, (tuple(for_edge), bridges)), (pos2, (tuple(for_edge), bridges))]
                    yield k, v
        else:
            comb_size = min(islands[pos1], islands[pos2], 2)
            for comb in combinations(exes, comb_size):
                if comb_size == 1:
                    p_ex, q_ex = comb[0]
                    k = ((tuple(for_edge), 1), ("ex%s" % p_ex, "ex%s" % q_ex))
                    v = [(pos1, "ex%s" % p_ex), (pos2, "ex%s" % q_ex),
                         (pos1, (tuple(for_edge), 1)), (pos2, (tuple(for_edge), 1))]
                    yield k, v
                else:
                    ex1, ex2 = comb
                    p_ex1, q_ex1 = ex1
                    p_ex2, q_ex2 = ex2
                    k = ((tuple(for_edge), 1, 2),
                         ("ex%s" % p_ex1, "ex%s" % q_ex1), ("ex%s" % p_ex2, "ex%s" % q_ex2))
                    v = set()
                    v.add((pos1, "ex%s" % p_ex1))
                    v.add((pos2, "ex%s" % q_ex1))
                    v.add((pos1, (tuple(for_edge), 1)))
                    v.add((pos2, (tuple(for_edge), 1)))
                    v.add((pos1, "ex%s" % p_ex2))
                    v.add((pos2, "ex%s" % q_ex2))
                    v.add((pos1, (tuple(for_edge), 2)))
                    v.add((pos2, (tuple(for_edge), 2)))
                    yield k, list(v)

    Y = dict()  # {(edge, number_of): [X_element1, X_element2, ...]}
    for edge in edge_list:
        intersects = False
        p, q = edge
        for b in range(1, min(islands[p], islands[q], 2)+1):
            start_key = (tuple(edge), b)
            start_value = list()
            for c in range(1, b+1):
                start_value.append((p, (tuple(edge), c)))
                start_value.append((q, (tuple(edge), c)))
            # need to exclude intersecting edges
            # trace the path from p to q checking each position in the intersection dict
            for pos in product(range(min(p[0], q[0]), max(p[0], q[0])+1), range(min(p[1], q[1]), max(p[1], q[1])+1)):
                # if an intersecting position is found, exclude all possible versions of the other edges
                if pos in intersecting_edges:
                    intersects = True
                    for inter_edge in intersecting_edges[pos]:
                        if inter_edge != edge:
                            for key, value in generate_exclusions(inter_edge, all=True):
                                Y[tuple(edge), b, key] = start_value + value
            if not intersects:
                Y[start_key] = start_value
    for edge in edge_list:
        for key, value in generate_exclusions(edge):
            Y[key] = value
    # print("Y:", Y)
    print("Constructed Y")

    X, Y = exact_cover(X, Y)
    # print("new X:", X)
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

# # # #


if __name__ == "__main__":
    grid = ["2..3.1.",
            "....3.4",
            ".1.2...",
            "3.5.5.4",
            ".1.1...",
            "1.2.1..",
            ".2.3..2"]
    hard = ["2.2...3.3",
            ".2..3..3.",
            "3....1..3",
            ".3.2...2.",
            "4.3.2...3",
            ".3.2.3.3.",
            "3.....2.4",
            ".3..3..1.",
            "3.2...4.5",
            ".2...5.2.",
            "3.3.2.3.2",
            ".2...3...",
            "3..3..6.2"]
    for solve in solve_hashi(hard):
        print(solve)
