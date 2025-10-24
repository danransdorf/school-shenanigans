maximum, second_maximum = (None, None)

while True:
  number = int(input())
  if number == -1:
    break
  if maximum is None or number > maximum:
    second_maximum = maximum
    maximum = number
  elif second_maximum is None or number > second_maximum:
    second_maximum = number

print(second_maximum)