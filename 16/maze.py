import sys
import heapq
from collections import defaultdict, deque

lines = open(sys.argv[1]).read().split('\n')

WIDTH = len(lines[0])
HEIGHT = len(lines)

G = dict()
start = None
end = None
for r, l in enumerate(lines):
    for c, cell in enumerate(l):
        G[(r,c)] = cell
        if cell == 'S':
            start = ((r,c), (0, 1))
        elif cell == 'E':
            end = (r,c)
    


def rotate(direction):
    my, mx = direction
    return (mx, -my)

def rotateReverse(direction):
    my, mx = direction
    return (-mx, my)

def rotations(pos, direction):
    rotations = []
    newDir = rotate(direction)
    rotations.append((1001, (addTuple(pos, newDir), newDir)))
    
    # Rotating three times = rotating one time in the other direction, so the cost is only 1000
    newDir = rotateReverse(direction)
    rotations.append((1001, (addTuple(pos, newDir), newDir)))
    return rotations

def addTuple(t1, t2):
    return (t1[0]+t2[0], t1[1]+t2[1])

def printVisited(G, tiles):
    for r in range(HEIGHT):
        for c in range(WIDTH):
            print(G[(r,c)] if (r,c) not in tiles else 'O', end='')
        print('')
    
def dijkstra(G, start, end):
    Q = [(0, start)]
    heapq.heapify(Q)
    DIST = defaultdict(lambda: 10**10)
    DIST[start] = 0
    best = 10**20
    PREV = defaultdict(set)
    bestEndStates = set()
    while len(Q) > 0:
        cost, currentState = heapq.heappop(Q)
        if cost > best:
            break
        if cost > DIST[currentState]:
            continue

        pos, direction = currentState
        
        if pos == end:
            if cost <= best:
                if cost < best:
                    bestEndStates = set([currentState]) 
                else:
                    bestEndStates.add(currentState)               
                best = cost
                
            continue


        # Find all possible neighbors:
        rots = rotations(pos, direction)
        for addedCost, state in rots:
            np, _ = state
            if G[np] != '#':
                if cost + addedCost <= DIST[state]:
                    if cost + addedCost < DIST[state]:
                        PREV[state] = set([currentState])
                    else:
                        PREV[state].add(currentState)

                    DIST[state] = cost + addedCost
                    heapq.heappush(Q, (cost+addedCost, state))
                    
        newPos = addTuple(pos, direction)
        newState = (newPos, direction)
        if G[newPos] == '.' or G[newPos] == 'E':
            if cost+1 <= DIST[newState]:
                if cost + 1 < DIST[newState]:
                    PREV[newState] = set([currentState])
                else:
                    PREV[newState].add(currentState)
                DIST[newState] = cost+1
                heapq.heappush(Q, (cost+1, newState))

    Q = deque(bestEndStates)
    seen = set()
    tiles = set()
    
    while len(Q) > 0:
        s = Q.popleft()
        tile, _ = s
        tiles.add(tile)
        prev = PREV[s]
        #print(s, prev)

        for s in prev:
            if s not in seen:
                seen.add(s)
                Q.append(s)

    return best, len(tiles)

print(dijkstra(G, start, end))


        
        