import sys
from collections import defaultdict
from itertools import combinations

lines = open(sys.argv[1]).read().split('\n')

HEIGHT = len(lines)
WIDTH = len(lines[0])

print(HEIGHT, WIDTH)

ANTENNAS = defaultdict(list)
ANTENNA_LOCATIONS = dict()

for r,line in enumerate(lines):
    for c,antenna in enumerate(line):
        if antenna == '.':
            continue
        
        ANTENNAS[antenna].append((r,c))
        ANTENNA_LOCATIONS[(r,c)] = antenna
        
def continuation(a1, a2):
    dy = a2[0]-a1[0]
    dx = a2[1]-a1[1]
    
    return (a2[0]+dy, a2[1]+dx)

ANTINODES = set()

for antenna in ANTENNAS.keys():
    antennas = ANTENNAS[antenna]
    for i in range(len(antennas)):
        for j in range(len(antennas)):
            if i == j:
                continue
            c = continuation(antennas[i], antennas[j])
        
            if (0 <= c[0] < HEIGHT) and (0 <= c[1] < WIDTH):
                ANTINODES.add(c)
        
ANTINODES_P2 = set()

def addTuple(t1, t2):
    return (t1[0]+t2[0], t1[1]+t2[1])

for antenna in ANTENNAS.keys():
    antennas = ANTENNAS[antenna]
    for i in range(len(antennas)):
        for j in range(len(antennas)):
            if i == j:
                continue
            a1 = antennas[i]
            a2 = antennas[j]
            
            dy = a2[0]-a1[0]
            dx = a2[1]-a1[1]
            
            cur = a1
            
            while True:
                cur = addTuple(cur, (dy,dx))
                print(antenna, a1, cur)
                if (0 <= cur[0] < HEIGHT) and (0 <= cur[1] < WIDTH):
                    ANTINODES_P2.add(cur)
                else:
                    break


def printGrid():
    for r in range(HEIGHT):
        for c in range(WIDTH):
            p = (r,c)
            if p in ANTENNA_LOCATIONS:
                print(ANTENNA_LOCATIONS[p], end='')
            elif p in ANTINODES:
                print('#', end='')
            else:
                print('.', end='')
        print('')
        
printGrid()    
print(len(ANTINODES))
print(len(ANTINODES_P2))

        
        


        
        
        