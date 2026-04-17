number = input().strip()
amount_to_print = int(input())

for _ in range(amount_to_print):
  new_number = ""
  calculator = 0
  last_char = None
  for char in number:
    if last_char == char:
      calculator += 1
    else:
      if last_char is not None:
        new_number += str(calculator) + last_char
      last_char = char
      calculator = 1

  new_number += str(calculator) + last_char
  number = new_number
  print(new_number)
