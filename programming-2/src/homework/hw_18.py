def count_combinations(size: int, eaten_in_row: list[set[int]], unused_cols: set[int], current_row: int) -> int:
  if current_row >= size:
    return 1

  counter = 0
  for x in unused_cols.difference(eaten_in_row[current_row]):
    counter += count_combinations(
      size=size, eaten_in_row=eaten_in_row, unused_cols=unused_cols.difference((x,)), current_row=current_row + 1
    )

  return counter


size = int(input().strip())
eaten_in_row = [set() for _ in range(size)]
for row_idx in range(size):
  line = input().strip()
  for idx in range(size):
    if line[idx] == "X":
      eaten_in_row[row_idx].add(idx)


print(count_combinations(size=size, eaten_in_row=eaten_in_row, unused_cols=set(range(size)), current_row=0))
