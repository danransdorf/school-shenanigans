square_size = int(input())
dimensions = int(input())

for row in range(dimensions):
  for sub_row in range(square_size):
    if row % 2 == 0:
      print(("." * square_size + "*" * square_size) * (dimensions // 2) + "." * square_size * (dimensions % 2))
    else:
      print(("*" * square_size + "." * square_size) * (dimensions // 2) + "*" * square_size * (dimensions % 2))
