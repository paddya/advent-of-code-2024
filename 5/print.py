import sys
from collections import defaultdict
from functools import cmp_to_key

rules, updates = open(sys.argv[1]).read().split('\n\n')


rules = list(map(lambda line: tuple(map(int, line.split('|'))), rules.split('\n')))

updates = list(map(lambda line: list(map(int, line.split(','))), updates.split('\n')))

# Build tree from rules

# T stores a map of node ID to a list of descendants
T = defaultdict(set)

def addNode(T, ancestor, descendant):
    T[ancestor].add(descendant)
    

def isBefore(T, start, end):
    return end in T[start]

# For each page, check if isBefore is true for all following pages
def checkUpdate(T, update):
    for idx, page in enumerate(update):
        following = update[idx+1:]
        
        if len(following) == 0:
            continue
        
        if not all(map(lambda follower: isBefore(T, page, follower), following)):
            return False
    
    return True        
    
def middle(update):
    return update[len(update)//2]
    

for (ancestor, descendant) in rules:
    addNode(T, ancestor, descendant)


incorrect = []
total = 0
for u in updates:
    inOrder = checkUpdate(T, u)
    if inOrder:
        total += middle(u)
    else:
        incorrect.append(u)
        
print(total)


p2 = 0
for i in incorrect:
    result = sorted(i, key=cmp_to_key(lambda a,b: -1 if isBefore(T, a, b) else 1))
    p2 += middle(result)
    
print(p2)