import sys

registers, program = open(sys.argv[1]).read().split('\n\n')

registers = registers.split('\n')
A = int(registers[0].removeprefix('Register A: '))
B = int(registers[1].removeprefix('Register B: '))
C = int(registers[2].removeprefix('Register C: '))

PROGRAM = list(map(int, program.removeprefix('Program: ').split(',')))


def runProgram(PROGRAM, A, B, C):
    REGISTERS = {
        4: A,
        5: B,
        6: C,
    }
    def comboVal(val):
        if 0 <= val <= 3:
            return val
        elif 0 <= val <= 6:
            return REGISTERS[val]
        else:
            assert False


    ip = 0
    OUT = []

    while ip < len(PROGRAM):
        instruction = PROGRAM[ip]
        operand = PROGRAM[ip+1]
        
        # adv
        if instruction == 0:
            numerator = REGISTERS[4]
            denominator = 2**comboVal(operand)
            REGISTERS[4] = numerator//denominator
        elif instruction == 1:
            REGISTERS[5] = REGISTERS[5] ^ operand
        elif instruction == 2:
            REGISTERS[5] = comboVal(operand) % 8
        elif instruction == 3:
            if REGISTERS[4] != 0:
                ip = operand
                continue
        elif instruction == 4:
            REGISTERS[5] = REGISTERS[5] ^ REGISTERS[6]
        elif instruction == 5:
            OUT.append(comboVal(operand) % 8)
        elif instruction == 6:
            numerator = REGISTERS[4]
            denominator = 2**comboVal(operand)
            REGISTERS[5] = numerator//denominator
        elif instruction == 7:
            numerator = REGISTERS[4]
            denominator = 2**comboVal(operand)
            REGISTERS[6] = numerator//denominator
        ip += 2
    return OUT


    
print(','.join(map(str, runProgram(PROGRAM, A, B, C))))


# 2,4, # B = A % 8
# 1,2, # B = B ^ 0b010
# 7,5, # C = A // (2**B)
# 1,7, # B = B ^ 0b111
# 4,4, # B = B ^ C
# 0,3, # A = A//8
# 5,5, # print B
# 3,0  # if A != 0 => JUMP 0

def run(A, B, C):
    OUT = []
    while A != 0:
        B = A % 8 # Set B to the last three bits of A
        B = B ^ 2 # Invert the second bit
        # Cut of the last B bits of A and store the result in C
        # At this point, B is the last three bits of A with the second bit inverted
        C = A // (2**B) 
        # We now completely invert B again, so
        #   1st bit = inverted from A
        #   2nd bit = original from A
        #   3rd bit = inverted from A
        B = B ^ 7
        # This is basically A shifted right by B bits and only the last three bits
        # are relevant due to B%8 later
        # What happens here is:
        #   1st bit = inverted from A 
        #   2nd bit = original from A
        #   3rd bit = inverted from A
        B = B ^ C 
        A = A//8 # Cut off the last three bits of A
        OUT.append(B%8)
    return OUT


A = 1
    
# Idea: we only have 10 bit "effect radius" for each output bit, so we can kind of bruteforce
# 
tryingToMatch = 1
A = 1
B = 0
C = 0
while True:
    expected = PROGRAM[len(PROGRAM)-tryingToMatch:len(PROGRAM)]
    output = runProgram(PROGRAM, A, 0, 0)     
    
    if output == expected:
        
        if tryingToMatch == len(PROGRAM):
            print(A)
            break
        else:
            A *= 8        
            tryingToMatch += 1
            continue
    
    A += 1





#print(run(41644071, 0, 0))

    