# https://www.addictinggames.com/puzzle/daily-sort
# Hard Level

# class _obj:
#     def __init__(self, x):
#         self.obj = x
#     def value(self):
#         return self.obj
#     def set(self, x):
#         self.obj = x

from enum import Enum
import time

class Color(Enum):
    Orange = 1
    Cyan = 2
    Blue = 3
    Yellow = 4
    Red = 5
    Purple = 6
    Magenta = 7
    Lime = 8
    Green = 9
    Grey = 10

# Last index is top of tube
# testtubes = [[Color.Lime, Color.Green, Color.Grey, Color.Magenta],
#              [Color.Yellow, Color.Green, Color.Orange, Color.Cyan],
#              [Color.Green, Color.Orange, Color.Lime, Color.Red],
#              [Color.Blue, Color.Cyan, Color.Yellow, Color.Lime],
#              [Color.Purple, Color.Green, Color.Magenta, Color.Grey],
#              [Color.Cyan, Color.Grey, Color.Purple, Color.Red],
#              [Color.Blue, Color.Yellow, Color.Magenta, Color.Red],
#              [Color.Cyan, Color.Grey, Color.Magenta, Color.Blue],
#              [Color.Orange, Color.Red, Color.Purple, Color.Blue],
#              [Color.Purple, Color.Yellow, Color.Lime, Color.Orange],
#              [],
#              []]

testtubes = [[Color.Grey, Color.Cyan, Color.Red, Color.Purple],
             [Color.Lime, Color.Magenta, Color.Yellow, Color.Cyan],
             [Color.Orange, Color.Lime, Color.Blue, Color.Cyan],
             [Color.Lime, Color.Cyan, Color.Yellow, Color.Red],
             [Color.Orange, Color.Magenta, Color.Green, Color.Red],
             [Color.Purple, Color.Grey, Color.Yellow, Color.Green],
             [Color.Green, Color.Blue, Color.Lime, Color.Grey],
             [Color.Yellow, Color.Magenta, Color.Blue, Color.Orange],
             [Color.Red, Color.Blue, Color.Purple, Color.Green],
             [Color.Magenta, Color.Purple, Color.Orange, Color.Grey],
             [],
             []]

def getcount():
    count = 0
    for tube in testtubes:
        count += len(tube)
    return count

def checklegal(start, end):
    if start == end:
        return False
    # if end is full, return false
    if len(testtubes[end]) == 4:
        return False
    # if start is empty, return false
    if len(testtubes[start]) == 0:
        return False
    # if end is empty, return true
    if len(testtubes[end]) == 0:
        return True
    # if peek(start) != peek(end) return false
    if peek(start) != peek(end):
        return False
    else:
        return True
    
def makemove (start, end):
    testtubes[end].append(testtubes[start].pop())

def peek(tube):
    return testtubes[tube][-1]

def checkstate():
    for tube in testtubes:
        if len(tube) > 0 and len(tube) < 4:
            return False
        
        if len(tube) == 4:
            firstcolor = tube[0]
            for i in range(1, 4):
                if tube[i] != firstcolor:
                    return False
    return True

currentpath = []
moves = []
hashset = set()
min = float('inf')
currentbest = None

def createmoves():
    newmoves = []
    for i in range(len(testtubes)):
        for j in range(len(testtubes)):
            if checklegal(i, j):
                newmoves.append([i, j])
    return newmoves

# WIP :)
def hashstate():
    global testtubes

    toreturn = ""
    for tube in testtubes:
        for color in tube:
            toreturn += str(color.value)+","
        toreturn += "_," * (4-len(tube))
    return toreturn

bitboard = [None,0,0,0,0,0,0,0,0,0,0]

# def test_set_board():
#     global bitboard
#     for i in range(1, 11):
#         bitboard[i] |= 0xff

def clear_board():
    global bitboard
    for i in range(1, 11):
        bitboard[i] &= 0b0

# operations:
def add_color(color, index):
    global bitboard
    bitboard[color.value] |= (0b1 << index)

# def bitwise_hash():
#     clear_board()
#     for i in range(0, 12):
#         for j in range(0, len(testtubes[i])):
#             add_color(testtubes[i][j], i*4 + j)
#     # print(bitboard[1:11])
#     toreturn = 0
#     for i in range(1, 11):
#         toreturn ^= bitboard[i]
#     return toreturn    

def bitwise_hash():
    clear_board()
    for i in range(0, 12):
        for j in range(0, len(testtubes[i])):
            add_color(testtubes[i][j], i*4 + j)
    # print(bitboard[1:11])
    toreturn = 1 << 256
    for i in range(1, 11):
        toreturn ^= bitboard[i]
    return toreturn    

max = 0

def dfs(depth):
    # if (depth == 50):
    #     return
    global max
    if depth > max:
        max = depth
        print(max)

    global testtubes
    global min
    global currentbest
    global currentpath
    global moves
    global hashset

    # print(currentpath)
    if checkstate():
        if len(currentpath) < min:
            min = len(currentpath)
            currentbest = currentpath
            print(min)
            print(currentbest)

        return True

    # hashset.add(hashstate())
    hashset.add(bitwise_hash())

    for i in range(len(testtubes)):
        tube = testtubes[i]
        if len(tube) == 4:
            tocontinue = True
            firstcolor = tube[0]
            for j in range(1, 4):
                if tube[j] != firstcolor:
                    tocontinue = False
            if tocontinue:
                continue
                
        for j in range(len(testtubes)):
            if len(tube) > 0 and len(testtubes[j]) == 0:
                samecolors = True
                firstcolor = tube[0]
                for k in range(1, len(tube)):
                    if tube[k] != firstcolor:
                        samecolors = False
                if samecolors:
                    continue

            islegal = checklegal(i, j)
            isNewState = None
            if islegal:
                makemove(i, j)
                # isNewState = hashstate() not in hashset
                isNewState = bitwise_hash() not in hashset
                makemove(j, i)

            if islegal and isNewState:
                makemove(i, j)
                currentpath.append([i, j])
                dfs(depth+1)
                makemove(j, i)
                currentpath.pop()
t0 = time.time()
dfs(0)
if currentbest is not None:
    print(f"min: {min}")
    print(currentbest)

print("done!")
print(time.time()-t0)