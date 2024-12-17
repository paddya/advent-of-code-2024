import sys
import re
from collections import defaultdict

lines = open(sys.argv[1]).read().split('\n')
WIDTH = 101
HEIGHT = 103
if 'example' in sys.argv[1]:
    WIDTH = 11
    HEIGHT = 7
print(WIDTH, HEIGHT)

def printGrid(G):
    for r in range(HEIGHT):
        for c in range(WIDTH):
            num = len(G[(r,c)])
            print(num if num > 0 else '.', end='')
        print('')

pattern = re.compile(r'p=(\-?\d+),(\-?\d+) v=(\-?\d+),(\-?\d+)')
robots = dict()
G = defaultdict(list)

for id, l in enumerate(lines):
    px, py, vx, vy = map(int, pattern.findall(l)[0])
    robots[id] = (vy, vx)
    G[(py, px)].append(id)

def addTuple(t1, t2):
    return ((t1[0]+t2[0])%HEIGHT, (t1[1]+t2[1])%WIDTH)

def checkTree(i, G):
    for r in range(HEIGHT):
        for c in range(WIDTH):
            if len(G[(r,c)]) > 1:
                return False
    return True

def toFile(i, G):
    with open('./output/'+str(i)+'.txt', 'w') as f:
        for r in range(HEIGHT):
            for c in range(WIDTH):
                num = len(G[(r,c)])
                print('⬛' if num > 0 else '⬜', end='', file=f)
            print('', file=f)

def quadrant(pos):
    y, x = pos
    if x == (WIDTH//2) or y == (HEIGHT//2):
        return None
    if y < HEIGHT/2 and x < WIDTH/2:
        return 0
    elif y < HEIGHT/2 and x > WIDTH/2:
        return 1
    elif y > HEIGHT/2 and x < WIDTH/2:
        return 2
    elif y > HEIGHT/2 and x > WIDTH/2:
        return 3
    else:
        return None    
    

n = 0

for i in range(103 * 101):
    G2 = defaultdict(list)
    for pos, ids in G.items():
        for id in ids:
            newPos = addTuple(pos, robots[id])
            assert 0 <= newPos[0] < HEIGHT
            assert 0 <= newPos[1] < WIDTH
            G2[newPos].append(id)
    
    G = G2
    if checkTree(i, G):
        print(i+1)
    # Interesting = 82 + n * 101
    #if i == 82 + n * 101:
    #    toFile(i, G)
    #    n += 1
            
    if i == 99:
        counter = defaultdict(int)
        for pos, ids in G.items():
            q = quadrant(pos)
            if q != None:
                counter[q] += len(ids)
                total = 1
        print(counter)
        for c in counter.values():
            total *= c

        print(total)

#printGrid(G)
    



GNEW = dict()
for pos, ids in G.items():
    if len(ids) > 0:
        GNEW[pos] = len(ids)


