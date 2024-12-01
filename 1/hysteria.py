import sys
from collections import Counter

lines = open(sys.argv[1]).read().split('\n')

l1 = []
l2 = []

for l in lines:
    num1, num2 = l.split('   ')
    l1.append(int(num1))
    l2.append(int(num2))
    
l1 = sorted(l1)
l2 = sorted(l2)

p1 = 0
for n1,n2 in zip(l1, l2):
    p1 += abs(n1-n2)

occurences = Counter(l2)

p2 = 0
for n in l1:
    p2 += n*occurences[n]

    
print(p1)
print(p2)

