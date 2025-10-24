array = []
while True:
  number = int(input())
  if number == -1:
    break
  array.append(number)

print(" ".join(map(str, array[::-1])))