"""
Idea: Tabulace, rozdělení počtu dle jednotlivých končících výšek.
"""

import sys


def ceil_division(dividend: int, divisor: int) -> int:
  return -(dividend // -divisor)  # src: stackoverflow


length = int(input())
height = int(input())

if height in (0, 1, 2):
  print(height**length)
  sys.exit(0)


height_dp = ceil_division(height, 2)  # strany jsou symetrické, ukládejme jen první půlku (včetně prostředku)
middle_sum_third_element = height_dp - 1 - height % 2
"""
Slouží pro zjištění třetího prvku sumy, když počítáme prostřední prvek.
Výška lichá => započítáme znovu prostřední prvek (symetrický prvek na druhé straně)
Výška sudá  => započítáme prvek o jeden nižší (symetrický prvek na druhé straně středu)
"""

dp = [[1 for _ in range(height_dp)] for _ in range(length)]
"""Tabulace, dp[i][j]: kolik různých klíčů vyrobím o délce `i`, končících na výšce `j`."""  # ignorujme +1
for col in range(1, length):
  for row in range(height_dp):
    if row == 0:  # sčítáme pouze první dva prvky
      dp[col][row] = dp[col - 1][row] + dp[col - 1][row + 1]
      continue
    if row == height_dp - 1:  # sčítáme prostředek, tj. aktuální řádek, o jeden menší, a ještě třetí prvek (viz výše)
      dp[col][row] = dp[col - 1][row - 1] + dp[col - 1][row] + dp[col - 1][middle_sum_third_element]
      continue
    dp[col][row] = dp[col - 1][row - 1] + dp[col - 1][row] + dp[col - 1][row + 1]

result = 2 * sum(dp[length - 1])
if height % 2 == 1:  # odeberme dvakrát započtený prostřední prvek při liché výšce
  result -= dp[length - 1][height_dp - 1]

print(result)
