# Uses python3
import sys

def fibonacci_sum_naive(n):
    if n <= 1:
        return n

    previous = 0
    current  = 1
    sum      = 1
    index = 0
    part = 0
    for x in range(n):
        previous, current = current, previous + current
        sum = (sum + current%10)%10
        # print(x, sum)
        if previous % 10 == 0 and current % 10 == 1 and x != 0:
            index = n % (x + 1)
            part = n/(x+1)
            # print(x)
            sum = sum-1
            break
        if x == n - 2:
            return sum
    previous = 0
    current  = 1
    # print(index, part, sum)
    sum = int(sum * part)%10 + 1
    for x in range(index):
        previous, current = current, previous + current
        sum = (current%10 + sum)%10
    return sum

# if __name__ == '__main__':
    # input = sys.stdin.read()

m, n = map(int, input().split())
if m == n:
    print(abs(fibonacci_sum_naive(n) - fibonacci_sum_naive(m-1)))
else:
    print(abs(fibonacci_sum_naive(n) - fibonacci_sum_naive(m)))
