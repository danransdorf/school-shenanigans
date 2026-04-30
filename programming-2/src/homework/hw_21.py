"""
Idea: Průchod grafem (možnostmi), v procesu udržujeme jen jaké dílky jsou nepoužité
  a jakým číslem končí náš aktuálně sestavený řetěz domin.

Technická rozhodnutí:
  1. Pro udržování volných polí se nabízí set nebo list,
    ty bohůžel nejdou cachovat (hashovat), je třeba zvolit frozenset.
    Ten je ale pomalý v operacích, vždy se musí naklonovat v O(n). Tedy udržujme
    stav použití v globálním listu (used) a obsazené dílky hashujme sami
    pomocí sčítání mocnin. Zvolme bázi identifikátorů (1, 2, 4, ...) nad tělesem Z_2.
    Např. použité dílky jsou 0,3,5 => used_id = 2^0 + 2^3 + 2^5 = 1+8+32 = 41
  2. Kvůli paměti je nutno jít ještě níže a použít bitmasking.
    Tedy index v adjacency reprezentujeme pomocí shiftované 1,
    zda je daný index použitý kontrolujeme used&bit (bitwise AND)
  3. Stav rekuze se nutně musí smačknout do jednoho intu,
    počet domin je omezený <=16 a hodnota tail <=38, čili můžeme bezpečně použít shift
    ocasu o 16 doleva.
  4. Vyhazuji functools.cache, hodnoty domin jsou <= 38, počet domin <= 16.
    Čili potřebujeme jen 38*2**16 stavů (~2.5M), čili to můžeme předalokovat,
    testy v recodexu selhávají na 10MB.
"""

import sys
from collections import defaultdict


#####
# Input
#####
def token_stream():  # bez typů, šetříme paměť, museli bychom importovat
  for line in sys.stdin:
    for value in line.split():
      yield int(value)


numbers = token_stream()
count = next(numbers)
dominos: list[tuple[int, int]] = [(next(numbers), next(numbers)) for _ in range(count)]
del numbers


#####
# Adjacency sestavení
#####
domino_adjacency: dict[int, list[tuple[int, int]]] = defaultdict(list)
"""dict[tail, list[tuple[index_bit, new_tail]]]"""
for idx, (left, right) in enumerate(dominos):
  idx_bit = 1 << idx
  domino_adjacency[left].append((idx_bit, right))
  if left != right:
    domino_adjacency[right].append((idx_bit, left))

# pro počátek vezměme pouze jednu orientaci, druhá bude objevena v jiných cestách.
domino_adjacency[-1] = [(1 << idx, piece[0]) for idx, piece in enumerate(dominos)]

del dominos


#####
# Hledání
#####

MAX_USED_BITS = 16
MAX_USED_MASK = (1 << MAX_USED_BITS) - 1
MAX_DOMINO_VALUE = 38
UNKNOWN = 255
FULL_MASK = (1 << count) - 1  # 000...011111111...

memo = bytearray([UNKNOWN]) * ((MAX_DOMINO_VALUE + 1) << MAX_USED_BITS)  # +1 pro vychozi hodnotu tail=-1
"""indexace: (tail+1)<<16 | used_id"""


def pack_state(used_id: int, tail: int, /) -> int:
  return ((tail + 1) << MAX_USED_BITS) | used_id


def find_largest(used_id: int, tail: int, /) -> int:
  packed = pack_state(used_id, tail)
  if (cached := memo[packed]) != UNKNOWN:
    return cached

  maximum = 0
  possible = count - used_id.bit_count()
  for bit_idx, new_tail in domino_adjacency[tail]:
    if used_id & bit_idx:
      continue

    candidate = 1 + find_largest(used_id | bit_idx, new_tail)
    if candidate > maximum:
      maximum = candidate

      if maximum == possible:
        memo[packed] = maximum
        return maximum

  if maximum == count:
    print(maximum)
    sys.exit(0)

  memo[packed] = maximum
  return maximum


print(find_largest(0, -1))
