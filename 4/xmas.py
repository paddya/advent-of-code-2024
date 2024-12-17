import sys
from collections import defaultdict

lines = open(sys.argv[1]).read().split('\n')

WIDTH = len(lines[0])
HEIGHT = len(lines)
print(WIDTH, HEIGHT)

G = defaultdict(str)

for r, l in enumerate(lines):
    for c,cell in enumerate(l):
        G[(r,c)] = cell

mv = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
    (1, 1),
    (-1, -1),
    (1, -1),
    (-1, 1)
]

def addTuple(t1, t2):
    return ((t1[0]+t2[0]), (t1[1]+t2[1]))

E = set()

def search(G, startPos, direction):
    assert G[startPos] == 'X'
    pos = addTuple(startPos, direction)
    expected = ['M', 'A', 'S']
    encountered = set([startPos])
    for i in range(3):
        newCell = G[pos]
        if newCell != expected[i]:
            return False
        encountered.add(pos)
        pos = addTuple(pos, direction)
        
       
    for e in encountered:
        E.add(e)
    return True
    

def printGrid(G, E):
    for r in range(HEIGHT):
        for c in range(WIDTH):
            print(G[(r,c)] if (r,c) in E else '.', end='')
        print('')
    

# Iterate over all cells, check if it's an X and then search in all directions

count = 0
for r in range(HEIGHT):
    for c in range(WIDTH):
        cell = G[(r,c)]
        if cell == 'X':
            for m in mv:
                found = search(G, (r,c), m)
                if found:
                    count += 1
        
#printGrid(G, E)            
print(count)


XMAS = [
    [
        ['M', '.', 'M'],
        ['.', 'A', '.'],     
        ['S', '.', 'S'],
    ],
    [
        ['M', '.', 'S'],
        ['.', 'A', '.'],      
        ['M', '.', 'S'],
    ],
    [
        ['S', '.', 'S'],
        ['.', 'A', '.'],      
        ['M', '.', 'M'],
    ],
    [
        ['S', '.', 'M'],
        ['.', 'A', '.'],      
        ['S', '.', 'M'],   
    ]
]

def matchXmas(G, pos, xmas):
    (r,c) = pos
    for rr in range(3):
        for cc in range(3):
            if xmas[rr][cc] == '.':
                continue
            if G[(r+rr, c+cc)] != xmas[rr][cc]:
                return False
            
    return True

p2 = 0
for r in range(WIDTH):
    for c in range(HEIGHT):
        for xmas in XMAS:
            if matchXmas(G, (r,c), xmas):
                p2 += 1
                
print(p2)