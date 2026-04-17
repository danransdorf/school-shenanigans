"""
Idea: Průchod všech kombinací pomocí rekurze, kdy v každém kroku vybereme typ mince A
  a odečtením od cílové sumy B úlohu redukujeme na podúlohu nalezení všech kombinací pro sumu B-A.
  Deduplikaci a pořadí vyřešme procházením typů mincí zleva doprava (nejvyšší po nejnižší), nevracejíc se doleva.

Technikálie: Použijme mutace listu .append(), .pop() místo sčítání listu "coin_stack + [coin_type]"
  Důvod: Sčítání je vytváření nového listu, časově složitější než mutace listu.
"""

input()  # nepotřebné
COIN_TYPES = list(map(int, input().strip().split()))  # předpoklad: seřazeno sestupně
TARGET = int(input())


def print_combinations(*, target: int, coin_stack: list[int], type_start_idx: int = 0) -> None:
  if 0 > target:
    return
  if 0 == target:
    print(*coin_stack)
    return

  for idx in range(type_start_idx, len(COIN_TYPES)):
    coin_type = COIN_TYPES[idx]
    coin_stack.append(coin_type)
    print_combinations(target=target - coin_type, coin_stack=coin_stack, type_start_idx=idx)
    coin_stack.pop()  # pro "resetování" stavu pro další iterace


print_combinations(target=TARGET, coin_stack=[])
