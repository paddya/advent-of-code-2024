import sys
from collections import deque
lines = open(sys.argv[1]).read().split('\n')

G = dict()

trailheads = set()

for r,line in enumerate(lines):
    for c, level in enumerate(line):
        level = int(level)
        G[(r,c)] = int(level)
        if level == 0:
            trailheads.add((r,c))
            
mv = [
    (-1, 0),
    (1, 0),
    (0, 1),
    (0, -1)
]

def addTuple(t1, t2):
    return (t1[0]+t2[0], t1[1]+t2[1])
            
def score(G, t):
    visited = set()
    Q = deque([t])
    score = 0
    
    while len(Q) > 0:
        n = Q.pop()
        visited.add(n)
        
        if G[n] == 9:
            score += 1
        
        for m in mv:
            neighbor = addTuple(n, m)
            if not neighbor in visited and neighbor in G and G[neighbor] - 1 == G[n]:
                Q.append(neighbor)
        
    return score

def scoreAll(G, t):
    Q = deque([t])
    score = 0
    
    while len(Q) > 0:
        n = Q.pop()
        
        if G[n] == 9:
            score += 1
        
        for m in mv:
            neighbor = addTuple(n, m)
            if neighbor in G and G[neighbor] - 1 == G[n]:
                Q.append(neighbor)
        
    return score
    

total = 0
for t in trailheads:
    total += score(G, t)
    
print(total)

total = 0
for t in trailheads:
    total += scoreAll(G, t)
print(total)