numbers = input().split()

odd = numbers[1::2][::-1]

numbers[1::2] = odd
print(*numbers, sep=" ")
