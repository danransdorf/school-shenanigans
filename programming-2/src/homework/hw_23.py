"""
Idea:
  Sestavujeme-li bipartitní graf, nezáleží na tom, kde začneme.
  začněme graf někde stavět, když ho postavíme, tak to jde.

Předpokládaná definice BP grafu: Graf bez lichých cyklů.
  Poznámka: graf může být nesouvislý!
"""

import sys
from queue import Queue

n_cities = int(input())
n_roads = int(input())

adjacency: list[set[int]] = [set() for _ in range(n_cities)]
for _ in range(n_roads):
  left, right = map(int, input().split())
  left, right = left - 1, right - 1  # vstup je 1-based, náš system je 0-based
  adjacency[left].add(right)
  adjacency[right].add(left)

unvisited = set(range(n_cities))
parts: tuple[set[int], set[int]] = set(), set()
queue: Queue[tuple[int, int]] = Queue()
"""queue[ (city, part) ]"""

while unvisited:
  start_city = unvisited.pop()
  parts[0].add(start_city)  # začátek nových komponent dávejme do skupiny 0
  queue.put((start_city, 0))
  while not queue.empty():
    city, part = queue.get()
    other_part = 1 - part
    for linked_city in adjacency[city]:
      if linked_city in parts[part]:
        print("Nelze")  # našli jsme hranu v rámci jedné skupiny
        sys.exit(0)
      if linked_city in parts[other_part]:  # řešme pouze nové příbytky do skupiny, abychom se nezacyklili
        continue
      parts[other_part].add(linked_city)
      queue.put((linked_city, other_part))
      unvisited.discard(linked_city)


# invariant: prošli jsme všechna města

print(*sorted([x + 1 for x in parts[0]]))  # +1 na převod 0-based na 1-based výstup
print(*sorted([x + 1 for x in parts[1]]))
