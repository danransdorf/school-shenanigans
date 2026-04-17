"""
Idea: Iterace po znakách, jakmile narazíme na otevírací závorku, přidáme ji do stacku.
  Jakmile narazíme na zavírací závorku, ze stacku odebereme poslední a ověříme, že jsou typově shodné.

Design decisions:
  - Čtení více-znakových závorek: Iterujme po znakách, první zkontrolujme zda není závorka ve dvojici znaků,
    pak teprve samotný znak.
    - Alternativa: Možno implementovat pomocí udržování "bufferu" předchozího znaku,
      což bude o kousek levnější, ale vytvoří to obrovský state machine,
      kde se musíme rozhodovat, kdy které závorky přidáme do stacku. (viz odevzdání č. 1)
  - Stack: Zachovávejme stack s očekávanými zavíracími závorkami, místo s načtenými otvíracími.
    Můžeme pak elegantně srovnávat pop() s aktuální načtenou zavírací závorkou

(	)
[	]
/*	*/
<!	!>
($	$)
<<	>>
"""

from pathlib import Path

CLOSING_FOR = {"(": ")", "[": "]", "/*": "*/", "<!": "!>", "($": "$)", "<<": ">>"}
"""dict[otvírací, příslušná zavírací]"""

OPENING = set(CLOSING_FOR.keys())
CLOSING = set(CLOSING_FOR.values())


def check_expression(expression: str) -> bool:
  expected_closing_stack: list[str] = []
  """Stack s očekávanými zavíracími závorkami, např. při `<!` zapíšeme `!>`"""
  idx = 0

  while idx < len(expression):
    if idx + 1 < len(expression):
      char_pair = expression[idx : idx + 2]
      if char_pair in OPENING:
        expected_closing_stack.append(CLOSING_FOR[char_pair])
        idx += 2
        continue
      if char_pair in CLOSING:
        if 0 == len(expected_closing_stack):  # nejsou otevřené žádné závorky
          return False
        if expected_closing_stack.pop() != char_pair:  # zavíráme nekompatibilní závorku
          return False
        idx += 2
        continue

    char = expression[idx]
    if char in OPENING:
      expected_closing_stack.append(CLOSING_FOR[char])
      idx += 1
      continue
    if char in CLOSING:
      if 0 == len(expected_closing_stack):  # nejsou otevřené žádné závorky
        return False
      if expected_closing_stack.pop() != char:  # zavíráme nekompatibilní závorku
        return False
      idx += 1
      continue

    idx += 1

  return 0 == len(expected_closing_stack)


with Path("zavorky.in").open(encoding="utf-8") as reader:
  while expression := reader.readline():
    if check_expression(expression):
      print("true")
    else:
      print("false")
