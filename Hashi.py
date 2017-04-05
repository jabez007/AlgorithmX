import sys
from itertools import product


def solve_hashi(grid):
    print(grid)

    positions = list(product(range(len(grid)), range(len(grid[0]))))  # coordinates for the grid
    edges = {p: list() for p in positions}

    print(positions)

    islands = {(i, j): int(grid[i][j]) for i, j in positions if '.' != grid[i][j]}  #Q#
    island_items = islands.items()  #J#

    print(islands)

    edge_list = list()
    for p, c in island_items:  # position of each island, and the number of bridges to/from that island
        for i, j in ((0, 1),(1, 0)):  # move down and to the right
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
    print(edges)

    connections = [edges[p] for p in positions if p not in islands and len(edges[p]) > 1]
    print(connections)

    total = len(islands) + 4 * len(edge_list) + len(connections)
    print(total)

    m = list()
    bridges_made = dict()
    so_far = 0
    for pos, count in island_items:
        e = edges[pos]
        max_bridges = len(e) * 2  # max number of edges possible from this island
        for t in product(*((0, 1, 2) for x in e)):  # attempting all possible combinations of number of each edge
            if sum(t) != count:
                continue
            row = [0] * total
            row[so_far+max_bridges] = 1
            for i, x in enumerate(t):
                k = so_far + i*2
                row[k:k+2] = ((1, 1), (0, 1), (0, 0))[x]
            m += [row]
        bridges_made[pos] = so_far
        so_far += max_bridges + 1
    print(m)  # is m some sort of matrix
    print(bridges_made)

    z = len(m)
    

"""
z=L(m)
for e in F:
 p,q=e;r=[0]*T;c,d=l[p]+E[p].index(e)*2,l[q]+E[q].index(e)*2;t=r[:];r[c]=r[d]=1
 for i,u in Z(C):r[T-L(C)+i]=int(e in u)
 t[c+1]=t[d+1]=1;m+=[r,t]

def I(x,d):
 y=d[x]
 while y!=x:yield y;y=d[y]
def A(c):
 L[R[c]],R[L[c]]=L[c],R[c]
 for x in I(c,D):
  for y in I(x,R):U[D[y]],D[U[y]]=U[y],D[y]
def B(c):
 for x in I(c,U):
  for y in I(x,L):U[D[y]],D[U[y]]=y,y
 L[R[c]],R[L[c]]=c,c
def S():
 c=R[h]
 if c==h:yield[]
 A(c)
 for r in I(c,D):
  for x in I(r,R):A(C[x])
  for t in S():yield[r[0]]+t
  for x in I(r,L):B(C[x])
 B(c)
L,R,U,D,C={},{},{},{},{}
h=T
L[h]=R[h]=D[h]=U[h]=h
for c in W(T):
 R[L[h]],R[c],L[h],L[c]=c,h,c,L[h];U[c]=D[c]=c
for i,l in Z(m):
 s=0
 for c in I(h,R):
  if l[c]:
   r=i,c;D[U[c]],D[r],U[c],U[r],C[r]=r,c,r,U[c],c
   if s==0:L[r]=R[r]=s=r
   R[L[s]],R[r],L[s],L[r]=r,s,r,L[s]
for s in S():
 b=V(map(V,a))
 for e in s:
  if e<z:continue
  (i,j),(x,y)=F[(e-z)//2]
  if j==y:
   for r in W(i+1,x):b[r][j]='|H'[b[r][j]=='|']
  else:
   for r in W(j+1,y):b[i][r]='-='[b[i][r]=='-']
 print('\n'.join(''.join(l)for l in b).replace('.',' '))
"""

if __name__ == "__main__":
    grid = """
    2.2.5.2.
    .....1.3
    6.3.....
    .2..6.1.
    3.1..2.6
    .2......
    1.3.5..3
    .2.3..2."""

    solve_hashi(grid.split())
