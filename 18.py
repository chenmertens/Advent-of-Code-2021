import functools

lines = []
with open('input18.txt', 'r') as f:
    for line in f:
        lines.append(line.strip())

processed = []
for line in lines:
    processed_line = []
    paren_diff = 0
    for i in range(len(line)):
        if line[i] == '[':
            paren_diff += 1
        elif line[i] ==  ']':
            paren_diff -= 1
        elif line[i] == ',':
            pass
        else:
            processed_line.append([int(line[i]),paren_diff])
    processed.append(processed_line)

def add(proc_sn1, proc_sn2):
    sum_sn = [[entry[0],entry[1]+1] for entry in proc_sn1 + proc_sn2]
    updated = True
    while updated:
        updated = False
        for i in range(len(sum_sn)):
            depth = sum_sn[i][1]
            if depth >= 5 and depth==sum_sn[i+1][1]:
                if i > 0:
                    sum_sn[i-1][0] += sum_sn[i][0]
                if i < len(sum_sn)-2:
                    sum_sn[i+2][0] += sum_sn[i+1][0]
                del sum_sn[i:i+2]
                sum_sn.insert(i,[0,depth-1])
                updated = True
                break
        if not updated:
            for i in range(len(sum_sn)):
                if sum_sn[i][0] > 9:
                    [val, depth] = sum_sn[i]
                    half_rounded_down = val//2
                    half_rounded_up = val - val//2
                    del sum_sn[i]
                    sum_sn.insert(i,[half_rounded_up, depth+1])
                    sum_sn.insert(i,[half_rounded_down, depth+1])
                    updated = True
                    break
    return sum_sn

def magnitude(sum):
    while len(sum) > 1:
        for i in range(len(sum)):
            if i < len(sum) - 1 and sum[i][1] == sum[i+1][1]:
                depth = sum[i][1]
                val = sum[i][0] * 3 + sum[i+1][0] * 2
                del sum[i:i+2]
                sum.insert(i,[val,depth-1])
                break
    return sum[0][0]

#print(magnitude(functools.reduce(add, processed)))
res = 0
for i in range(len(processed)-1):
    for j in range(i+1, len(processed)):
        res = max(res, magnitude(add(processed[i], processed[j])))
        res = max(res, magnitude(add(processed[j], processed[i])))
print(res)
