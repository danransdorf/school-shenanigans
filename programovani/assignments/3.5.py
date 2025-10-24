number_set = set()
repeating = set()
while True:
  number = int(input())
  if number == -1:
    break
  
  if number in number_set:
    repeating.add(number)
  else:
    number_set.add(number)

print("\n".join(map(str, repeating)))