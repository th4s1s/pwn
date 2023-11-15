arr = [0x1]

with open('./bruh.txt') as file:
    for line in file:
        l = int(line.rstrip().split()[-1], 16)
        if(l == 0x15c):
            print('bruh')
        arr.append(l)

print(hex(max(arr)))