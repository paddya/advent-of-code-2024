import sys
from operator import add, mul
from math import ceil, log

lines = open(sys.argv[1]).read().split('\n')

equations = []

for l in lines:
    result, operands = l.split(': ')
    
    operands = list(map(int, operands.split()))
    
    equations.append((int(result), operands))
    

def concat(a, b):
    return a*pow(10, ceil(log(b+1, 10)))+b

OPS = [add, mul, concat]
       

def isSolvable(target, memory, remaining, rangeLimit):
    if memory > target:
        return False
    
    if len(remaining) == 0:
        return target == memory
        
    for idx in range(rangeLimit):
        newMem = OPS[idx](memory, remaining[0])
        solvable = isSolvable(target, newMem, remaining[1:], rangeLimit)
        if solvable:
            return True
        
    return False    

#print(equations)
OPS_READABLE = ['+', '*', '||']
total = 0


p2List = []

for result, operands in equations:
    if isSolvable(result, operands[0], operands[1:], 2):
        total += result
    else:
        p2List.append((result, operands))
        
            
print(total)

OPS_READABLE = {
    mul: '*',
    add: '+',
    concat: '||'
}

p2 = 0
for result, operands in p2List:
    if isSolvable(result, operands[0], operands[1:], 3):
        p2 += result
        
        
print(total+p2)