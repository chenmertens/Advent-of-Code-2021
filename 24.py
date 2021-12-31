lines = []
with open('input24.txt', 'r') as f:
    for line in f:
        line = line.strip()
        line = line.split(' ')
        if len(line) == 3:
            try:
                line[2] = int(line[2])
            except:
                pass
        lines.append(line)

#only w gets inp. w never gets overwritten by other operations.

ALU = {'add':(lambda a,b:a+b), 'mul':(lambda a,b:a*b),
       'div': (lambda a,b:a//b), 'mod': (lambda a,b:a%b), 'eql': (lambda a,b: int(a == b))}
index = {'w':0, 'x':1, 'y':2, 'z':3}

def check(memory, model_number, lines):
    head = 0
    for line in lines:
        idx1 = index[line[1]]

        if line[0] == 'inp':
            memory[idx1] = int(model_number[head])
            head += 1
        else:
            var1 = memory[idx1]
            var2 = memory[index[line[2]]] if line[2] in index else line[2]
            memory[idx1] = ALU[line[0]](var1,var2)
    return memory[3]

class Memoize:
    def __init__(self, fn):
        self.fn = fn
        self.memo = {}
    def __call__(self, *args):
        if args not in self.memo:
            self.memo[args] = self.fn(*args)
        return self.memo[args]

@Memoize
def fastcheck(model_number):
    length = len(model_number)
    if length == 0:
        return 0
    else:
        return check([0,0,0,fastcheck(model_number[:-1])],model_number[-1],lines[(length - 1)*18:length*18])

#
# def check(memory, model_number, lines):
#     head = 0
#     for line in lines:
#         idx1 = index[line[1]]
#
#         if line[0] == 'inp':
#             memory[idx1] = int(model_number[head])
#             head += 1
#         else:
#             var1 = memory[idx1]
#             var2 = memory[index[line[2]]] if line[2] in index else line[2]
#             memory[idx1] = ALU[line[0]](var1,var2)
#     return memory[3]
# for i in range(1,10):
#     print(i,check([0,0,0,0],str(i), lines[:18]))
#
# for num in range(-10000,10000):
#     for i in range(1,10):
#         for target in range(8,17):
#             if check([0,0,0,num],str(i), lines[-36:-18])==target:
#                 print(i,num,target)
#
# def find_pairs(target,block):
#     nums = set()
#     digits = set()
#     for num in range(-100,100):
#         for i in range(1,10):
#             if check([0,0,0,num],str(i), lines[len(lines)-18*(block+1):len(lines)-18*block])==target:
#                 nums.add(num)
#                 digits.add(i)
#     return [nums,digits]
#
# block = 0
# targets = {0}
# nums = set()
# digits = set()
# while block < 12:
#     print('block %d' %block)
#     for target in targets:
#         [a,b] = find_pairs(target,block)
#         nums = nums.union(a)
#         digits = digits.union(b)
#     targets = nums
#     block += 1
# print(targets)
# first_targets = [[i,check([0,0,0,23],str(i),lines[18:36])] for i in range(1,10)]
# print(first_targets)
# for pair in first_targets:
#     if pair[1] in targets:
#         print(pair[0],pair[1])
w = [0]*14
w[0] = 1
w[13] = 8
w[1] = 9
w[12] = 1
w[2] = 5
w[11] = 1
w[9] = 1
w[10] = 6
w[7] = 1
w[8] = 3
w[3] = 1
w[6] = 2
w[4] = 8
w[5] = 1
w_str = ''
for char in w:
    w_str += str(char)
print(w_str)
