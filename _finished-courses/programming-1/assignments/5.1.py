minimum, maximum = None, None
sum_accumulator = 0
amount = 0
while True:
  number = int(input())
  if number == -1:
    break
  minimum = number if minimum is None else min(minimum, number)
  maximum = number if maximum is None else max(maximum, number)
  sum_accumulator += number
  amount += 1

print(maximum - minimum + 1, sum_accumulator // amount, minimum, maximum, sum_accumulator, sep="\n")
