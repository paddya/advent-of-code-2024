import sys
from collections import defaultdict, deque
import heapq

input = open(sys.argv[1]).read().strip()

class Block:
    def __init__(self, offset, id, size, isEmpty, prev = None):
        self.id = id
        self.size = size
        self.isEmpty = isEmpty
        self.next = None
        self.prev = prev
        self.offset = offset
        
    def addFollower(self, block):
        self.next = block
        block.prev = self
        
    # TODO: Maybe make work with defragmentation?
    # Should not remove the empty block from the list because it cuts off other blocks
    # Fills 
    def fill(self, block):
        assert self.isEmpty
        assert self.id == None
        
        newEmptyBlock = None
        # Completely absorb the other block
        # Add a new empty block with the remaining size if necessary
        if self.size >= block.size:
            self.id = block.id
            self.isEmpty = False
            remaining = self.size-block.size
            self.size = block.size

            # If the block fits perfectly, we do not 
            # need to insert a new empty block behind this one
            if remaining > 0:
                #print('inserting new empty block with size', remaining)
                split = Block(self.offset + self.size, None, remaining, True, self)
                split.next = self.next
                self.next.prev = split
                self.next = split
                newEmptyBlock = split
            
            # The other block is completely freed now
            block.isEmpty = True
            block.id = None
        else:
            self.id = block.id
            freed = self.size
            block.size -= self.size
            
            split = Block(block.offset + block.size, None, freed, True, block)
            split.next = block.next
            block.next.prev = split
            block.next = split
            
            
            self.isEmpty = False
            newEmptyBlock = split
        return newEmptyBlock
        
    def __str__(self):
        if self.isEmpty:
            return '.' * self.size
        else:
            return str(self.id) * self.size
        
def printBlocks(head, o = None):
    if o != None:
        print(' ' * o, end='')
        print('v')
    while True:
        print(head, end='')
        
        if head.next == None:
            break
        else:
            head = head.next
    print('')
            





def parse(input):
    gaps = defaultdict(list)
    blocks = []
    prev = None
    isEmpty = False
    curID = 0
    offset = 0
    for b in input:
        size = int(b)
        
        block = Block(offset, curID if not isEmpty else None, size, isEmpty, prev)
        
        if prev != None:
            prev.addFollower(block)
        
        if not isEmpty:
            curID += 1
        prev = block
        
        blocks.append(block)
        
        if isEmpty:
            gaps[size].append((offset, block))
        
        offset += size    
        isEmpty = not isEmpty

    for g in gaps.values():
        heapq.heapify(g)
    
    return blocks[0], blocks[len(blocks)-1], gaps
    
head, tail, _ = parse(input)
originalHead = head

# Algorithm: walk from head to tail and keep two pointers:
# head = everything before it in the list should be defragmented already
# tail = always points to the last non-empty block

# Part 1
startHead = head
o = 0
while head != tail:
    if not head.isEmpty:
        o += head.size
        head = head.next
        continue
    
    #print('Filling block', head.id, 'with', tail.id, ' at offset', o)
    # If we encounter a free block, fill it from the back
    head.fill(tail)
    
    while tail.isEmpty:
        tail = tail.prev
    
    #printBlocks(startHead, o)
    

head = originalHead

def checksum(head):
    total = 0
    offset = 0
    while head != None:
        if head.isEmpty:
            offset += head.size
            head = head.next
            continue
        for pos in range(offset, offset+head.size):
            #print(pos, pos*head.id)
            total += pos*head.id
        
        offset += head.size
        head = head.next
    return total

print(checksum(head))
# Part 2

# Algorithm: start at the end of the list and scan from the head for each block to find something fitting

head, tail, gaps = parse(input)
#printBlocks(head)
startTail = tail
seen = set()

while tail != None:
    
    if tail.isEmpty or tail.id in seen:
        tail = tail.prev
        continue
        
    print('Trying to place ', tail.id, ' at offset ' , tail.offset, 'with size ', tail.size)
    seen.add(tail.id)
    
    # h = head
    # found = False
    # while h != tail:
    #     #print('looking at', h.id, h.size, h.isEmpty)
    #     if h.size >= tail.size and h.isEmpty:
    #         found = True
    #         break
        
    #     h = h.next
    
    
    
    # if not found:
    #     tail = tail.prev
    #     continue
    #print('trying to move', tail.id, tail.size)
    size = tail.size
    minIdx = 10e12
    target = None
    for s in range(size, 10):
        if len(gaps[s]) == 0:
            continue
        idx, _ = gaps[s][0]
        if idx < minIdx:
            minIdx = idx
            target = s
    if target != None:
        o, h = heapq.heappop(gaps[target])
        if o < tail.offset:   
            print('found gap at offset ', h.offset, h.size)
            new = h.fill(tail)
            if new != None:
                print('adding at ', new.offset, ' with size ', new.size)
                heapq.heappush(gaps[new.size], (new.offset, new))
        else:
            print('next gap would be at ', o)
    else:
        print('no gap of size ', size)
    
    tail = tail.prev
    
    #printBlocks(head)
    
print(checksum(head))