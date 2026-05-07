"""Idea: Vstup je jen permutace, hledáme všechny cykly té permutace."""

permutation = list(map(int, input().split()))

cycles: list[list[int]] = []
visited = [False for _ in permutation]


for start_idx in range(len(permutation)):
  if visited[start_idx]:
    continue

  cycle = []
  idx = start_idx
  while not visited[idx]:
    cycle.append(idx)
    visited[idx] = True
    idx = permutation[idx]

  cycles.append(cycle)

print("\n".join([" ".join(map(str, cycle)) for cycle in cycles]))
