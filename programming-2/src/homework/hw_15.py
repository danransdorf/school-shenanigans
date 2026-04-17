"""
Idea: Iterace po znakách, udržujeme počet aktuálně otevřených závorek.
  Je-li někdy počet otevřených závorek záporný => neplatné uzávorkování (byla uzavřena neexistující závorka)
  Není-li na konci 0 otevřených závorek => některé závorky zůstaly otevřené
"""

import sys
from pathlib import Path

expression = Path("zavorky.in").read_text(encoding="utf-8")
currently_open = 0
for idx in range(len(expression)):
  match expression[idx]:
    case "(":
      currently_open += 1
    case ")":
      if 0 >= currently_open:
        print("ne")
        sys.exit(0)
      currently_open -= 1
    case _:
      pass

if 0 == currently_open:
  print("ano")
else:
  print("ne")
