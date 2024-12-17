import sys
from itertools import pairwise

lines = open(sys.argv[1]).read().split('\n')

reports = [[int(k) for k in l.split()] for l in lines]


def isIncreasing(report):
    for p1,p2 in pairwise(report):
        if p2 <= p1:
            return False
    return True

def isDecreasing(report):
    for p1,p2 in pairwise(report):
        if p2 >= p1:
            return False
    return True

def validDifferences(report):
    for p1,p2 in pairwise(report):
        if abs(p1-p2) > 3:
            return False
    return True

def isSafe(report):
    return (isDecreasing(report) or isIncreasing(report)) and validDifferences(report)

total = 0
total_p2 = 0
for r in reports:
    if isSafe(r):
        total += 1
        total_p2 += 1
        print(r, ' is safe')
    else:
        for (remove, _) in enumerate(r):
            to_check = [v for (i, v) in enumerate(r) if i != remove]
            #print(remove, to_check, isSafe(to_check))
            if isSafe(to_check):
                total_p2 += 1
                break
    #print('=============')
print(total)
print(total_p2)