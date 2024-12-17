import sys
from collections import deque

rawGrid, movements = open(sys.argv[1]).read().split('\n\n')
movements = movements.replace('\n', '')
grid = rawGrid.split('\n')

G = dict()

WIDTH = len(grid[0])
HEIGHT = len(grid)

robotPosition = None

for r, l in enumerate(grid):
    for c, cell in enumerate(l):
        G[(r,c)] = cell
        if cell == '@':
            robotPosition = (r,c)
mv = {
    '>': (0, 1),
    '^': (-1, 0),
    '<': (0, -1),
    'v': (1, 0)
}

def addTuple(t1, t2):
    return (t1[0]+t2[0], t1[1]+t2[1]) 

def printGrid(G):
    for r in range(HEIGHT):
        for c in range(WIDTH):
            print(G[(r,c)], end='')
        print('')


for m in movements:
    move = mv[m]
    newTile = addTuple(robotPosition, move)
    
    
    # Move in the direction and collect all boxes we might also want to move
    # We can only move if we encounter a free spot before a wall
    toMove = [robotPosition]
    canMove = False
    cur = newTile
    while G[cur] != '#':
        if G[cur] == '.':
            canMove = True
            break
        elif G[cur] == 'O':
            toMove.append(cur)
        cur = addTuple(cur, move)
        
    if canMove:
        while len(toMove) > 0:
            t = toMove.pop()
            n = addTuple(t, move)
            G[n] = G[t]
            if G[n] == '@':
                robotPosition = n
            G[t] = '.'


total = 0
for t, cell in G.items():
    r, c = t
    if cell == 'O':
        total += r*100+c
        
print(total)


#### PART 2
WIDTH = WIDTH*2

def search(G, start, direction):
    
    Q = deque([start])
    seen = set()
    
    moveOrder = deque()
    
    while len(Q) > 0:
        tile = Q.popleft()
        
        if tile in seen:
            continue
        seen.add(tile)
        
        moveOrder.append(tile)
        
        neighbor = addTuple(tile, direction)
        if G[neighbor] == '.':
            continue
        elif G[neighbor] == '[':
            restOfBox = addTuple(neighbor, mv['>'])
            if not neighbor in seen:
                Q.append(neighbor)
            if not restOfBox in seen:
                Q.append(restOfBox)
        elif G[neighbor] == ']':
            restOfBox = addTuple(neighbor, mv['<'])
            if not neighbor in seen:
                Q.append(neighbor)
            if not restOfBox in seen:
                Q.append(restOfBox)
        # Whenever we encounter an unmovable block, nothing will move
        else:
            return deque()
    
    return moveOrder

grid2 = rawGrid.replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.').split('\n')

G = dict()

robotPosition = None

for r, l in enumerate(grid2):
    for c, cell in enumerate(l):
        G[(r,c)] = cell
        if cell == '@':
            robotPosition = (r,c)


for m in movements:
    
    # For horizontal moves, the algorithm stays the same, we can just scan until we find a "#" and then move everything one spot to the right/left 
    move = mv[m]
    if m == '<' or m == '>':
        newTile = addTuple(robotPosition, move)
        #print('Moving from horizontally', robotPosition, ' to ', newTile, '(move =', m, ' => ', move, ')')
        toMove = [robotPosition]
        movable = False
        cur = newTile
        while G[cur] != '#':
            if G[cur] == '.':
                movable = True
                break
            elif G[cur] == '[' or G[cur] == ']':
                toMove.append(cur)
            cur = addTuple(cur, move)
            
        if movable:
            while len(toMove) > 0:
                t = toMove.pop()
                n = addTuple(t, move)
                G[n] = G[t]
                if G[n] == '@':
                    robotPosition = n
                G[t] = '.'
    else:
        # For vertical moves, things get trickier. We start with a search width of 1;
        # If we encounter an empty space, we can move.
        # If we encounter [, we will also need to move the tile one to the right
        # If we encounter ], we will also need to move the tile one to the left
        # This results in a recursive structure, where we need to check for both tiles
        # if they can be moved
        toMove = search(G, robotPosition, move)
        while len(toMove) > 0:
            t = toMove.pop()
            n = addTuple(t, move)
            G[n] = G[t]
            if G[n] == '@':
                robotPosition = n
            G[t] = '.'
            
    #printGrid(G)

total = 0
for t, cell in G.items():
    r, c = t
    if cell == '[':
        total += r*100+c
        
print(total)
