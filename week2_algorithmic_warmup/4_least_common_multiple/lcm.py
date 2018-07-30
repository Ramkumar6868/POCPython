# Uses python3
import sys

def lcm_naive(a, b):
    if a > b:
        c, tmp = a, a
        d = b
    else:
        c, tmp = b, b
        d = a
    while c % d != 0:
        c = c + tmp
    # for l in range(c, a*b+1):
    #     if l%a == 0 and l%b==0:
    #         return l
    return c
    # return a*b

a, b = map(int, input().split())
print(lcm_naive(a, b))

