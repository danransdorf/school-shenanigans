import sys
from queue import Queue

#######
# Input
#######

board = [[0 for _ in range(8)] for __ in range(8)]
"""0=prázdné, 1=zabrané"""

start: tuple[int, int] = (-1, -1)
"""tuple[row, col]"""
target: tuple[int, int] = (-1, -1)
"""tuple[row, col]"""

for row_idx in range(8):
  input_line = input().strip()
  if len(input_line) != 8:
    raise ValueError("Invalid input")

  for col_idx in range(8):
    match input_line[col_idx]:
      case "x":
        board[row_idx][col_idx] = 1
      case "v":
        start = (row_idx, col_idx)
      case "c":
        target = (row_idx, col_idx)
      case ".":
        pass
      case unknown_char:
        raise ValueError(f"Unknown character `{unknown_char}`")

if -1 in start:
  raise ValueError("Start not set.")
if -1 in target:
  raise ValueError("Target not set.")

#####
# BFS
#####

visited: set[tuple[int, int]] = set()
queue: Queue[tuple[int, tuple[int, int]]] = Queue()
"""Obsahuje tuple[hloubka, tuple[row,col]]"""

queue.put((0, start))
while not queue.empty():
  depth, (start_row, start_col) = queue.get()
  if (start_row, start_col) == target:
    print(depth)
    sys.exit(0)

  visited.add((start_row, start_col))

  # Nahoru
  for row in range(start_row - 1, -1, -1):
    if board[row][start_col] == 1:
      break
    if (row, start_col) not in visited:
      queue.put((depth + 1, (row, start_col)))

  # Dolu
  for row in range(start_row + 1, 8):
    if board[row][start_col] == 1:
      break
    if (row, start_col) not in visited:
      queue.put((depth + 1, (row, start_col)))

  # Doleva
  for col in range(start_col - 1, -1, -1):
    if board[start_row][col] == 1:
      break
    if (start_row, col) not in visited:
      queue.put((depth + 1, (start_row, col)))

  # Doprava
  for col in range(start_col + 1, 8):
    if board[start_row][col] == 1:
      break
    if (start_row, col) not in visited:
      queue.put((depth + 1, (start_row, col)))

print(-1)
