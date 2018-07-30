# # Uses python3
# from sys import stdin

# def fibonacci_sum_squares_naive(n):
#     if n <= 1:
#         return n

#     previous = 0
#     current  = 1
#     sum      = 1

#     for _ in range(n - 1):
#         previous, current = current, previous + current
#         sum += current * current

#     return sum % 10

# if __name__ == '__main__':
#     n = int(stdin.read())
#     print(fibonacci_sum_squares_naive(n))

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
        sum = (sum + ((current%10)*(current%10))%10)%10
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
    print(index, part, sum)
    sum = int(sum * part)%10 + 1
    for x in range(index):
        previous, current = current, previous + current
        sum = (((current%10)*(current%10))%10 + sum)%10
    return sum

# if __name__ == '__main__':
    # input = sys.stdin.read()

n = int(input())
print(fibonacci_sum_naive(n))
