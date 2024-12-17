import sys
from collections import defaultdict

stones = list(map(int, open(sys.argv[1]).read().split()))

map = defaultdict(int)

for s in stones:
    map[s] += 1

def printTotal(map):    
    total = 0
    for c in map.values():
        total += c
    
    print(total)
    
    
for round in range(75):
    newMap = defaultdict(int)
    for stone, count in map.items():
        stoneStr = str(stone)
        if stone == 0:
            newMap[1] += count
        elif len(stoneStr) % 2 == 0:
            middle = len(stoneStr)//2
            left = int(stoneStr[:(middle)])
            right = int(stoneStr[middle:])
            newMap[left] += count
            newMap[right] += count
        else:
            newMap[stone*2024] += count
    map = newMap
    if round == 24:
        printTotal(map)


printTotal(map)