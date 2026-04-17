import math

input_number = int(input())
amount = input_number
for number in range(1, input_number + 1):
  for digit_index in range(math.ceil(math.log(number, 10))):
    digit_and_everything_after = number % 10 ** (digit_index + 1)
    digit = digit_and_everything_after // 10 ** (digit_index)
    if digit == 0 or number % digit != 0:
      amount -= 1
      break

print(amount)
