import itertools
x = set(itertools.permutations([0,0,0,0,1,1]))
ind = ord('a')
for y in x:
    print (f'p{chr(ind)} = (0+2)*{y[0]}(0+2)*{y[1]}(0+2)*{y[2]}(0+2)*{y[3]}(0+2)*{y[4]}(0+2)*{y[5]}(0+2)*')
    ind += 1
