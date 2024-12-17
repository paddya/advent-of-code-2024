import sys
import re
from decimal import *

machines = open(sys.argv[1]).read().split('\n\n')


# Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400

# Solution: solve linear unequation system:
# x1*a + x2*b = tx
# y1*a + y2*b = ty
# a <= 100
# b <= 100
patternButton = re.compile(r'Button (A|B): X\+(\d+), Y\+(\d+)')
patternPrize = re.compile(r'Prize: X=(\d+), Y=(\d+)')


for p2 in [False, True]:
    
    total = 0
    for m in machines:
        
        a, b, prize = m.split('\n')
        _, x_a, y_a = patternButton.findall(a)[0]

        x_a = Decimal(x_a)
        y_a = Decimal(y_a)
        
        _, x_b, y_b = patternButton.findall(b)[0]
        x_b = Decimal(x_b)
        y_b = Decimal(y_b)
        
        t_x, t_y = patternPrize.findall(prize)[0]
        t_x = Decimal(t_x)
        t_y = Decimal(t_y)
        
        if p2:
            t_x += Decimal(10000000000000)
            t_y += Decimal(10000000000000)
        
        #print(x_a, y_a, x_b, y_b, t_x, t_y)
        
        solution_b = (t_y - ((y_a/x_a)*t_x))/(y_b - (y_a/x_a)*x_b)
        solution_a = (t_x-x_b*solution_b)/(x_a)

        if (abs(solution_b - round(solution_b)) < 10e-5):
            solution_b = round(solution_b)
            #print(solution_b)
            
            if (solution_a <= 100 and solution_b <= 100) or p2:
                #print(solution_a, solution_b)
                total += 3*solution_a + solution_b
        
        #solution_a = (t_x) / ((t_y / ))
        
    print(round(total))