numbers = []
while True:
  number = int(input())
  if number == -1:
    break
  if last is None or number >= last:
    print(number)
    last = number
