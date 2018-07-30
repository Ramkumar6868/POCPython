# Uses python3
import sys

def get_fibonacci_huge_naive(n, m):
    if n <= 1:
        return n

    previous = 0
    current  = 1
    index = 0
    for x in range(n):
        previous, current = current, previous + current
        # print(x, current)
        if previous % m == 0 and current % m == 1 and x != 0:
            index = n % (x + 1)
            break
        if x + 1 == n:
            return current % m
    previous = 0
    current  = 1
    for x in range(index - 1):
        previous, current = current, previous + current
    return current % m

# if __name__ == '__main__':
    # input = sys.stdin.read();
n, m = map(int, input().split())
print(get_fibonacci_huge_naive(n, m))
