start = 100000000000
end = 1000000000000

for i in range(start,end):
    num = i
    v6 = 0
    v5 = 1
    v3 = num
    if i % 2 == 0:
        continue
    while v3 != 0:
        v6 += v3 % 10 * v5
        v3 //= 10
        v5 *= 10
        v4 = v6 + v3
        a = 0
        if v6 < v3:
            a = 1
        else:
            break
        if a and v4 * v4 == num:
            print(num, v6)
            break

print('Done!')