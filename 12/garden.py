import sys
from collections import deque, defaultdict

lines = open(sys.argv[1]).read().split('\n')

G = dict()

for r,l in enumerate(lines):
    for c, type in enumerate(l):
        G[(r,c)] = type
    
seen = set()

PERIMETERS = dict()

areaID = 0
# maps tiles to area IDs
AREA_MAPPING = dict()
AREAS = defaultdict(list)

TILE_BORDERS = defaultdict(set)
AREA_BORDERS = defaultdict(set)
# Iterate the grid and find regions. Start a new scan for each unseen tile

mv = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
]

SIDES = {
    'TOP': (-1, 0),
    'RIGHT': (0, 1),
    'BOTTOM': (1, 0),
    'LEFT': (0, -1)
}

SIDES_REVERSE = {
    (-1, 0): 'TOP',
    (0, 1): 'RIGHT',
    (1, 0): 'BOTTOM',
    (0, -1): 'LEFT'
}

def addTuple(t1, t2):
    return (t1[0]+t2[0], t1[1]+t2[1])

WIDTH = len(lines[0])
HEIGHT = len(lines)

for r in range(HEIGHT):
    for c in range(WIDTH):
        tile = (r,c)
        if tile in seen:
            continue
        
        assert tile not in PERIMETERS
        assert tile not in AREA_MAPPING
        
        #print('Starting new region at', tile, 'with type', G[tile])

        # At this point, we always start a new area
        id = areaID
        # The next new area will have a new ID
        areaID += 1
        
        # Run a BFS and find all tiles of the area and assign them
        Q = deque([tile])
        
        while len(Q) > 0:
            t = Q.pop()
            if t in seen:
                continue
            seen.add(t)
            #print('Adding', t, 'to region', id)    

            AREA_MAPPING[t] = id
            AREAS[id].append(t)
            perimeter = 0
            for m in mv:
                isNonDiagonal = True if abs(m[0])+abs(m[1]) == 1 else False
                neighbor = addTuple(t, m)
                if neighbor not in G or G[neighbor] != G[t]:
                    TILE_BORDERS[t].add(SIDES_REVERSE[m])
                    AREA_BORDERS[id].add((t, SIDES_REVERSE[m]))
                    perimeter += 1
                elif G[neighbor] == G[t]:
                    Q.append(neighbor)
                    
            PERIMETERS[t] = perimeter
        
#print(AREAS)        
#print(PERIMETERS)


total = 0
for id, areaTiles in AREAS.items():
    perimeter = 0
    for t in areaTiles:
        perimeter += PERIMETERS[t]
    total += len(areaTiles)*perimeter
    #print('ID', id, ' - ', G[areaTiles[0]], ' area ', len(areaTiles), ' perimeter', perimeter, ' = ', len(areaTiles)*perimeter)
    
print(total)

# Figure out which sides there are for each area

SAME = (0, 0)
RIGHT = (0, 1)
LEFT = (0, -1)
TOP = (-1, 0)
BOTTOM = (1, 0)
TOP_LEFT = (-1, -1)
TOP_RIGHT = (-1, 1)
BOTTOM_LEFT = (1, -1)
BOTTOM_RIGHT = (1, 1)

# Possible neighbors for the fences
# TOP => (0, 1) TOP, (0, -1) TOP, (-1, 1) LEFT, (-1, -1) RIGHT, (0, 0) RIGHT, (0, 0) LEFT
# BOTTOM => (0, 1) BOTTOM, (0, -1) BOTTOM, (1, -1) RIGHT, (1, 1) LEFT, (0, 0) LEFT, (0, 0) RIGHT
# RIGHT => (-1, 1) BOTTOM, (0, 0) TOP, (0, 0) BOTTOM, (1, 1) TOP, (1, 0) RIGHT, (-1, 0) RIGHT
# LEFT => (0, 0) TOP, (0, 0) BOTTOM, (1, 0) LEFT, (-1, 0) LEFT, (-1, -1) BOTTOM, (1, -1) TOP
POSSIBLE_NEIGHBORS = {
    'TOP': [
        ((RIGHT, 'TOP'), None), 
        ((LEFT, 'TOP'), None), 
        ((SAME, 'RIGHT'), None), 
        ((SAME, 'LEFT'), None), 
        ((TOP_LEFT, 'RIGHT'), LEFT), 
        ((TOP_RIGHT, 'LEFT'), RIGHT),
    ],
    'BOTTOM': [
        ((RIGHT, 'BOTTOM'), None),
        ((LEFT, 'BOTTOM'), None),
        ((BOTTOM_RIGHT, 'LEFT'), RIGHT),
        ((BOTTOM_LEFT, 'RIGHT'), LEFT),
        ((SAME, 'LEFT'), None),
        ((SAME, 'RIGHT'), None)
    ],
    'LEFT': [
        ((SAME, 'TOP'), None),
        ((SAME, 'BOTTOM'), None),
        ((TOP_LEFT, 'BOTTOM'), TOP),
        ((BOTTOM_LEFT, 'TOP'), BOTTOM),
        ((TOP, 'LEFT'), None),
        ((BOTTOM, 'LEFT'), None)
    ],
    'RIGHT': [
        ((SAME, 'TOP'), None),
        ((SAME, 'BOTTOM'), None),
        ((TOP, 'RIGHT'), None),
        ((BOTTOM, 'RIGHT'), None),
        ((TOP_RIGHT, 'BOTTOM'), TOP),
        ((BOTTOM_RIGHT, 'TOP'), BOTTOM)
    ]
    
}

def walkBorder(G, areaTiles, border):
    seen = set()
    numSides = 0

    while len(seen) < len(border):
        # Choose any element from the set that is not seen yet
        remaining = border - seen
        if len(remaining) < 4:
            print('#### FAIL ####')            
            for t, s in remaining:
                print(t, s, G[t])
        assert len(remaining) >= 4
        start = next(iter(remaining))
        _, startSide = start
        curSide = None
        curNumSides = 0
        Q = deque([start])
        while len(Q) > 0:
            tile, side = Q.pop()
            print(tile, side)
            if side != curSide:
                #print('new side!', side)
                curNumSides += 1
                curSide = side
            seen.add((tile, side))
            
            for (movement, newSide), additionalCheck in POSSIBLE_NEIGHBORS[side]:
                new = addTuple(tile, movement)
                ac = addTuple(tile, additionalCheck) in areaTiles if additionalCheck != None else True
                #print('checking', new, newSide)
                newTuple = (new, newSide)
                if newTuple in border and newTuple not in seen and ac:
                    Q.append(newTuple)
                    break
                # else:
                #    print('    ', new, newSide, ' not a candidate', newTuple in border, newTuple not in seen, ac)
        
        print('Done!')
        if curSide == startSide:
            curNumSides -= 1
        numSides += curNumSides
    assert len(seen) == len(border)
    return numSides
        
        
def boundingBox(tiles):
    min_x = 1000000
    min_y = 1000000
    max_x = 0
    max_y = 0
    
    for x,y in tiles:
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        
    return (min_y, max_y), (min_x, max_x)
      

def printGrid(G, yBounds, xBounds):
    min_x, max_x = xBounds
    min_y, max_y = yBounds
    
    for r in range(min_y, max_y+1):
        for c in range(min_x, max_x+1):
            print(G[(r,c)], end='')
        print('')

# for id, b in AREA_BORDERS.items():
#     print(id, b)

p2 = 0
printID = 5
tiles = AREAS[printID]

yBounds, xBounds = boundingBox(tiles)
printGrid(G, yBounds, xBounds)
for id in range(id+1):
    tiles = AREAS[id]
    print('Walking ', id)
    numSides = walkBorder(G, tiles, AREA_BORDERS[id])
    toAdd = numSides * len(tiles)
    print(id, numSides, 'sides', len(tiles), 'area', ' - ', toAdd)
    p2 += toAdd
    print('------------------------------------------------\n')
    
print(p2)
    
    
    

    
    
    

