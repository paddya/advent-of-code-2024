import sys
import re

lines = open(sys.argv[1]).read()

def parseLine(line, p2=False):
    # Iterate over all characters and check if we reach a mul instruction
    matches = re.findall(r'(mul\((\d+),(\d+)\)|(do\(\))|(don\'t\(\)))', line)
    enabled = True
    total = 0
    for m in matches:
        if p2 and False:
            print('DO' if enabled else 'DONT', m)

        all, x, y, do, dont = m
        assert (do == '' and dont == '') or do != dont
        if do == 'do()':
            enabled = True
        elif dont == 'don\'t()':
            enabled = False
        else:
            if not p2 or enabled:
                total += int(x)*int(y)
    

    return total

total1 = 0
total2 = 0

result1 = parseLine(lines, False)
total1 += result1

result2 = parseLine(lines, True)
total2 += result2
    
   
print(total1)
print(total2)