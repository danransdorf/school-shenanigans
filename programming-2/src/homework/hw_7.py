import re
import sys
from collections.abc import Iterable

input_row = input()
dimensions_unparsed = re.sub(r"\s+", " ", input_row).strip().split(" ")
if 2 != len(dimensions_unparsed):
  sys.exit(2)  # recodex debug
row_amount, _ = map(int, dimensions_unparsed)
rows: list[str] = []
for _ in range(row_amount):
  rows.append(input().strip())  # Input bývá vytvořený na Windows

rows_to_print: Iterable[int] = map(int, input().strip().split())
for row in rows_to_print:
  if row == 0:
    sys.exit(3)  # recodex debug
  print(rows[row - 1])  # `row` is 1-based
