"""
Idea:
  Pozorování (*): Pro kandidáta a_n musí platit max(a_1,...,a_(n-1)) < a_n
  Pozorování (**): Pro kandidáta a_n musí platit a_n < min(a_(n+1),...)
  Postup:
    * zvol prvek 0 jako kandidáta, procházej zleva členy posloupnosti, udržuj si průběžné maximum (=: rolling_max)
    * najdeš-li napravo od kandidáta nižší hodnotu, kandidáta diskvalifikuj (spor s (**))
      (opačně aktuální prvek také diskvalifikuj kvůli sporu s (*))
    * (nemáš kandidáta a aktuální prvek > rolling_max) => aktuální prvek je kandidát (splňuje (*))
    * (máš kandidáta) => rolling_max ← max(rolling_max, aktuální prvek)
"""

import sys
from decimal import Decimal

sequence = []

while True:
  line = input().strip()
  if line == "-1":
    break

  sequence.append(Decimal(line))  # čteme REALNÁ čísla (viz zadání)

if 0 == len(sequence):
  print("-1")
  sys.exit(0)

candidate_idx = 0
"""-1 značí, že nemáme kandidáta"""
candidate_value = sequence[0]
rolling_max = sequence[0]
for idx in range(1, len(sequence)):
  if sequence[idx] <= candidate_value:
    candidate_idx = -1
    continue

  if sequence[idx] > rolling_max:
    rolling_max = sequence[idx]
    if candidate_idx == -1:
      candidate_idx = idx
      candidate_value = sequence[idx]


print(candidate_idx)
