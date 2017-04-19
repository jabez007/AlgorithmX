from itertools import product

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

    islands = {(i, j): int(puzzle[i][j]) for i, j in positions if '.' != puzzle[i][j]}
    print(islands)

    edges = {p: list() for p in positions}
    # get all the possible edges in the puzzle
    edge_list = list()
    for p, b in islands.items():  # position of each island, and the number of bridges to/from that island
        for i, j in ((0, 1), (1, 0)):  # move down and to the right
            q = p[0] + i, p[1] + j
            e = [p, 0]  # edge starts at p
            while q in positions:
                edges[q] += [e]  # add that to the edges through q
                if q in islands:
                    e[1] = q  # edge ends at q
                    edges[p] += [e]  # add that to the edges from p
                    edge_list += [e]  # add that to the list of all edges
                    break
                q = q[0] + i, q[1] + j
    print(edge_list)

    # remove edges that don't terminate; e[1] = 0
    edges = {pos: [e for e in y if e[1] != 0] for pos, y in edges.items()}
    '''this dict will have each position in the puzzle as a key, 
    with a list of the edges through that position as the values'''
    print(edges)

    return

# # # #


if __name__ == "__main__":
    puzzle = ["2..3.1.",
              "....3.4",
              ".1.2...",
              "3.5.5.4",
              ".1.1...",
              "1.2.1..",
              ".2.3..2"]
    solve_hashi(puzzle)
