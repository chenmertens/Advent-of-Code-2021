"""
Problem statement: https://adventofcode.com/2021/day/23
"""

import copy

lines = []
with open('input23.txt', 'r') as f:
    for line in f:
        line = line.strip()
        line = line.split('#')
        lines.append(line)

lines[2] = lines[2][3:7]
lines[3] = lines[3][1:5]
lines = lines[2:4]

translation = {'A':1,'B':2,'C':3,'D':4}

for line in lines:
    for i in range(len(line)):
        line[i] = translation[line[i]]

lines = [lines[0]] + [[4,3,2,1],[4,2,1,3]] + [lines[1]]

reverse_lines = lines[::-1]
transpose_lines = list(map(list, zip(*reverse_lines)))
print(transpose_lines)

#############
#0123456789A#
###A#D#A#B###
  #D#C#B#A#
  #D#B#A#C#
  #B#C#D#C#
  #########

 #############
 #0123456789A#
 ###A#D#A#B###
   #D#C#B#A#
   #D#B#A#C#
   #B#C#D#C#
   #########

#7 waiting spots.

def value(current):
    return 10**(current-1)

class Board:
    def __init__(self,wells,well_cleared,waiting_spots,score=0):
        self.wells = wells
        self.well_cleared = well_cleared
        self.waiting_spots = waiting_spots
        self.score = score

    def distance(self, well, waiting_spot):
        return 4 - len(self.wells[well]) + abs(waiting_spot-well)

    def legalroommove(self, waiting_spot):
        current = self.waiting_spots[waiting_spot]
        if not current:
            return False
        if not self.well_cleared[current*2]:
            return False
        lesser = min(waiting_spot, current*2)
        greater = max(waiting_spot, current*2)
        for i in range(lesser+1, greater):
            if i in self.waiting_spots and self.waiting_spots[i]:
                return False
        return True

    def legalwaitingmove(self,well, waiting_spot):
        if not self.wells[well]:
            return False
        if self.well_cleared[well]:
            return False
        lesser = min(well, waiting_spot)
        greater = max(well, waiting_spot)
        for i in range(lesser, greater+1):
            if i in self.waiting_spots and self.waiting_spots[i]:
                return False
        return True

    def move(self, well, waiting_spot):
        current = self.wells[well].pop()
        if not self.wells[well]:
            self.well_cleared[well] = True
        self.waiting_spots[waiting_spot] = current
        self.score += self.distance(well,waiting_spot)*value(current)

    def check_room_moves(self):
        modified = True
        while modified:
            modified = False
            for waiting_spot in self.waiting_spots:
                current = self.waiting_spots[waiting_spot]
                if not current:
                    continue
                if self.legalroommove(waiting_spot):
                    self.waiting_spots[waiting_spot] = None
                    well = current * 2
                    self.score += self.distance(well,waiting_spot)*value(current)
                    self.wells[well].append(current)
                    modified = True

    def check_gridlock(self):
        for ws1 in self.waiting_spots:
            for ws2 in self.waiting_spots:
                curr1 = self.waiting_spots[ws1]
                curr2 = self.waiting_spots[ws2]
                if ws1 >= ws2:
                    continue
                if not curr1 or not curr2:
                    continue
                if 2*curr2 < ws1 < ws2 < 2*curr1:
                    return True
        return False



wells = {}
for i in range(1,5):
    wells[2*i] = transpose_lines[i-1]
print(wells)
well_cleared = {2:False,4:False,6:False,8:False}
waiting_spots = {0:None,1:None,3:None,5:None,7:None,9:None,10:None}


active = False
queue = [Board(wells,well_cleared,waiting_spots)]

while queue:
    board = queue.pop(0)
    if board.check_gridlock():
        continue
    if active and board.score >= res:
        continue

    if board.wells == {2:[1,1,1,1], 4:[2,2,2,2], 6:[3,3,3,3], 8:[4,4,4,4]}:
        res = board.score
        active = True
        continue
    for well in board.wells:
        for waiting_spot in board.waiting_spots:
            if board.legalwaitingmove(well, waiting_spot):
                new_board = copy.deepcopy(board)
                new_board.move(well, waiting_spot)
                new_board.check_room_moves()
                print(new_board.wells,new_board.well_cleared,new_board.waiting_spots,new_board.score)
                queue.append(new_board)
print(res)
