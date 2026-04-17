first_row = input()
width = len(first_row)
left = {i for i, char in enumerate(first_row) if char == "/"}
right = {i for i, char in enumerate(first_row) if char == "\\"}

while len(left) + len(right) > 0:
  for pos in range(width):
    if pos in left and pos in right:
      print("X", end="")
    elif pos in left:
      print("/", end="")
    elif pos in right:
      print("\\", end="")
    else:
      print("-", end="")

  print(end="\n")
  left = {x - 1 for x in left if x > 0}
  right = {x + 1 for x in right if x < width - 1}
