sizes = list(map(int, input().split()))
max_size = sizes[-1]

for row in range(max_size):
  current_size = len(sizes) - 1
  index = 0
  while index < max_size:
    if (
      current_size - 1 >= 0
      and index >= max_size - sizes[current_size - 1]
      and sizes[current_size - 1] >= max_size - row
    ):
      current_size -= 1
    print("-" if (len(sizes) - current_size) % 2 == 1 else "+", end="")
    index += 1
  print(end="\n")
