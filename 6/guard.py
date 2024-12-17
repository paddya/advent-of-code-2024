import sys
from collections import defaultdict
from copy import copy

G = [[c for c in l] for l in open(sys.argv[1]).read().split('\n')]

HEIGHT = len(G)
WIDTH = len(G[0])

guardPosition = None

GRID = defaultdict(lambda: None)

for r,line in enumerate(G):
    for c,cell in enumerate(line):
        GRID[(r,c)] = cell
        if cell == '^':
            guardPosition = (r,c)        
        
        

def rotateRight(direction):
    y,x = direction
    
    return (x,-y)

def addTuple(t1, t2):
    return (t1[0]+t2[0], t1[1]+t2[1])

def walk(GRID, guardPosition):
    guardDirection = (-1, 0)
    visited = set()

    while GRID[guardPosition] != None:
        visited.add(guardPosition)
        
        # Figure out next direction
        while True:
            newPos = addTuple(guardPosition, guardDirection)
            if GRID[newPos] != '#':
                guardPosition = newPos
                break
            else:
                guardDirection = rotateRight(guardDirection)

    return visited
    
visited = walk(GRID, guardPosition)
print(len(visited))


def detectLoopWithAddedObstacle(G, guardPosition, addedObstacle):
    G2 = copy(G)
    G2[addedObstacle] = '#'
    
    guardDirection = (-1, 0)
    visited = set()
    
    while G2[guardPosition] != None:
        if (guardPosition, guardDirection) in visited:
            return True
        visited.add((guardPosition, guardDirection))
        
        # Figure out next direction
        newPos = addTuple(guardPosition, guardDirection)
        if G2[newPos] != '#':
            guardPosition = newPos
        else:
            guardDirection = rotateRight(guardDirection)
    return False

p2 = 0
for y in range(HEIGHT):
    for x in range(WIDTH):
        if (y,x) in visited and (y,x) != guardPosition and GRID[(y,x)] != '#':
            foundLoop = detectLoopWithAddedObstacle(GRID, guardPosition, (y,x))
            if foundLoop:
                p2 += 1
print(p2)