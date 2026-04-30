"""
Idea: Průchod všemi stavy. Aktuální stav je množina volných dílků a číslo, kterým končí naše aktuální řada domin.

Algoritmické optimalizace:
  1. Memoizace navštívených stavů
  2. Před průchodem sestavit "seznam sousedů" (adjacency list), pak nebude třeba iterovat přes všechny volné dílky.
  3. Zbavit se symetrie, neprocházet identické řady akorát v otočeném pořadí
"""

import sys

#####
# Input
#####
input_raw = " ".join(sys.stdin.readlines())
numbers = iter(map(int, input_raw.strip().split()))
count = next(numbers)
dominos: list[tuple[int, int]] = [(next(numbers), next(numbers)) for _ in range(count)]


#####
# BFS
#####
def find_longest(free: frozenset[int], tail: int | None) -> int:
  maximum = 0
  for idx in list(free):
    left, right = dominos[idx]
    if tail is None:
      maximum = max(
        maximum,
        1 + find_longest(free=free - {idx}, tail=left),
        1 + find_longest(free=free - {idx}, tail=right),
      )
    elif tail == left:
      maximum = max(
        maximum,
        1 + find_longest(free=free - {idx}, tail=right),
      )
    elif tail == right:
      maximum = max(
        maximum,
        1 + find_longest(free=free - {idx}, tail=left),
      )
    else:
      pass  # domino nepasuje

  return maximum


print(find_longest(tail=None, free=frozenset(range(count))))
