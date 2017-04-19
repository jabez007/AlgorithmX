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