"""
Problem statement: https://adventofcode.com/2021/day/22
"""

import copy

lines = []
with open('input22.txt', 'r') as f:
    for line in f:
        line = line.strip()
        line = line.split(' ')
        line[1] = line[1].split(',')
        for i in range(3):
            line[1][i] = line[1][i].split('=')[1]
            line[1][i] = line[1][i].split('..')
            line[1][i] = tuple([int(x) for x in line[1][i]])
        line[1] = tuple(line[1])
        lines.append(line)

class Line:
    def __init__(self,endpoints):
        self.left_endpoint = endpoints[0]
        self.right_endpoint = endpoints[1]

    def __eq__(self, other):
        left_eq = self.left_endpoint == other.left_endpoint
        right_eq = self.right_endpoint == other.right_endpoint
        return left_eq and right_eq

    def length(self):
        return self.right_endpoint - self.left_endpoint + 1

    def flatten(self):
        return (self.left_endpoint, self.right_endpoint)

class Cube:
    def __init__(self,ranges = ((0,0),(0,0),(0,0))):
        self.xrange = Line(ranges[0])
        self.yrange = Line(ranges[1])
        self.zrange = Line(ranges[2])

    def __eq__(self, other):
        x_eq = self.xrange == other.xrange
        y_eq = self.yrange == other.yrange
        z_eq = self.zrange == other.zrange
        return x_eq and y_eq and z_eq

    def volume(self):
        x = self.xrange.length()
        y = self.yrange.length()
        z = self.zrange.length()
        return x*y*z

    def flatten(self):
        return self.xrange.flatten() + self.yrange.flatten() + self.zrange.flatten()

def unflatten(flat):
    return Cube((flat[:2], flat[2:4], flat[4:6]))

def intersect_lines(line1,line2):
    """
    Returns a line which is the intersection of two given lines.
    """
    if line1.left_endpoint <= line2.left_endpoint:
        left_endpoint = line2.left_endpoint
        right_endpoint = min(line1.right_endpoint, line2.right_endpoint)
        return (Line((left_endpoint,right_endpoint)) if left_endpoint<=right_endpoint
                else None)
    else:
        return intersect_lines(line2,line1)

def intersect(cube1,cube2):
    """
    Returns a cube which is the intersection of two given cubes.
    """
    xrange = intersect_lines(cube1.xrange, cube2.xrange)
    yrange = intersect_lines(cube1.yrange, cube2.yrange)
    zrange = intersect_lines(cube1.zrange, cube2.zrange)
    if all([xrange,yrange,zrange]):
        res = Cube()
        res.xrange = xrange
        res.yrange = yrange
        res.zrange = zrange
        return res
    else:
        return None

def incr_value(dict, key, inc):
    if key in dict:
        dict[key] += inc
    else:
        dict[key] = inc

processed_by_level = {1:{}}

num_instr = len(lines)

def process_cube(cube):
    """
    Adds all intersections involving given cube to
    dictionary of intersections. Returns the volume
    of the cube outside the previously processed cubes,
    calculated according to the principle of
    inclusion-exclusion.
    """
    global processed_by_level
    depth = max(processed_by_level.keys())

    volume = cube.volume()
    new_pbl = copy.deepcopy(processed_by_level)
    for level in range(1, depth+1):
        for item in processed_by_level[level]:
            mult = processed_by_level[level][item]
            cube2 = unflatten(item)
            intersection = intersect(cube,cube2)
            if intersection:
                diff = (intersection.volume() if level%2 == 0 else
                        -intersection.volume())
                volume += diff * mult
                if level < depth:
                    incr_value(new_pbl[level+1], intersection.flatten(), mult)
                else:
                    new_pbl[level+1] = {intersection.flatten(): mult}

    incr_value(new_pbl[1], cube.flatten(), 1)
    processed_by_level = new_pbl
    return volume

res = 0

for i in range(num_instr-1, -1, -1):
    print('Processing %d' %i)
    [state, ranges] = lines[i]
    cube = Cube(ranges)
    contribution = process_cube(cube)
    if state == 'on':
        res += contribution
        print('contribution: %d' %contribution)

print(res)
