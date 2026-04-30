"""
Idea: Průchod všemi stavy. Aktuální stav je množina volných dílků a číslo, kterým končí naše aktuální řada domin.

Algoritmické optimalizace:
  1. Před průchodem sestavit "seznam sousedů" (adjacency list), pak nebude třeba iterovat přes všechny volné dílky.
  2. Zbavit se symetrie, neprocházet identické řady akorát v otočeném pořadí
"""

import sys
from functools import lru_cache

#####
# Input
#####
input_raw = " ".join(sys.stdin.readlines())
numbers = iter(map(int, input_raw.strip().split()))
count = next(numbers)
dominos: list[tuple[int, int]] = [(next(numbers), next(numbers)) for _ in range(count)]


#####
# Hledání
#####
@lru_cache
def find_longest(free: frozenset[int], tail: int | None) -> int:
  maximum = 0
  for idx in list(free):
    left, right = dominos[idx]
    if tail is None:
      # řada domin ještě nezačala, zkusme obě orientace domina
      maximum = max(
        maximum,
        1 + find_longest(free=free - {idx}, tail=left),
        1 + find_longest(free=free - {idx}, tail=right),
      )
    elif tail == left:
      # konec řady se shoduje s hodnotou vlevo, položme domino a řada bude končit hodnotou vpravo
      maximum = max(
        maximum,
        1 + find_longest(free=free - {idx}, tail=right),
      )
    elif tail == right:
      # konec řady se shoduje s hodnotou vpravo, položme domino a řada bude končit hodnotou vlevo
      maximum = max(
        maximum,
        1 + find_longest(free=free - {idx}, tail=left),
      )
    else:
      pass  # domino nepasuje

  return maximum


print(find_longest(tail=None, free=frozenset(range(count))))
