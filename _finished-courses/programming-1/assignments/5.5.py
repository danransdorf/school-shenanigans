size = int(input())
square_char = input()

while len(triangle_chars := input()) != 0:
  for padding in range(size):
    for triangle_char in triangle_chars:
      print(square_char * padding + triangle_char * (size - padding), end="")
    print(end="\n")
