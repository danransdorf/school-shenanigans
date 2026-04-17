"""
Idea: Nahlédněme, že úlohu můžeme počítat Fibonacciho posloupností.
  Označme počet možností P(n), mrvek M, petržel P. Rozeberme první záhon:
    - zasadíme-li mrkev, další záhony můžeme zasadit libovolně P(n-1) způsoby
    - zasadíme-li petržel, do dalšího záhonu musíme dát mrkve, pak zbytek zasadit P(n-2) způsoby

  Tedy definujme P(0) := 1, P(1) := 2.
  Pak            P(n) := P(n-1) + P(n-2)     , pro n>2
"""

import sys

FIBO_DEFAULT_MEMO = {0: 1, 1: 2}


def fibo(x: int, *, memo: dict[int, int] = FIBO_DEFAULT_MEMO) -> int:
  if x < 0:
    raise RuntimeError("Panic: Negative fibonacci.")
  if (result := memo.get(x)) is not None:
    return result
  memo[x] = fibo(x - 1, memo=memo) + fibo(x - 2, memo=memo)
  print(sys.getsizeof(list(memo.values())))
  return memo[x]


count = int(input())
print(fibo(count))
