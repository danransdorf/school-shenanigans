"""
Byla upřednostněna přehlednost, program se dá "drobně" optimalizovat,
např. při vytváření heapu se dá začít v cca půlce, ne až na konci
"""


def create_bubble(heap: list):
  def _get_greater_child(idx: int, *, limit: int) -> int | None:
    """Najde index většího dítěte (pokud je menší než limit)"""
    left_idx = 2 * idx + 1  # ze vzorce
    right_idx = left_idx + 1  # ze vzorce
    if right_idx < limit and heap[left_idx] < heap[right_idx]:
      return right_idx  # pravé dítě je platné a větší
    if left_idx < limit:
      return left_idx  # levé dítě je platné
    return None  # děti nejsou platné

  def bubble_down(idx: int, *, limit: int) -> None:
    """Prvek na indexu zabublá do heapu směrem dolů (po limit)"""
    while True:
      child = _get_greater_child(idx, limit=limit)
      if child is None or heap[idx] >= heap[child]:
        return
      heap[idx], heap[child] = heap[child], heap[idx]
      idx = child

  return bubble_down


heap = []
bubble_down = create_bubble(heap)

for _ in range(int(input())):
  heap.append(int(input()))

for idx in reversed(range(len(heap))):  # O(n) vytvoření maxheapu
  # invariant: všechny podstromy s kořenem na indexech > idx jsou platný maxheap
  bubble_down(idx, limit=len(heap))

print(*heap)

# n-1 krát odeberme maximum na konec (tím se seznam seřadí), vlevo udržujme max-heap
for swap_idx in reversed(range(1, len(heap))):
  # invariant: heap[:swap_idx] je maxheap, heap[swap_idx:] je už seřazený suffix
  heap[0], heap[swap_idx] = heap[swap_idx], heap[0]
  bubble_down(0, limit=swap_idx)
  print(*heap)
