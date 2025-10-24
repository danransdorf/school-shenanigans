number = int(input())
while number != 1:
  print(number)
  if number % 2 == 0:
    number = int(number / 2)
  else:
    number = 3*number + 1

print(number)