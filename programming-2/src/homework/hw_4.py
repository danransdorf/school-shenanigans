"""
Řešení je časově O(n*k), možno zlepšit na O(n*log(k)) použitím Heap queue (heapq).
"""

import sys

sequence = []

while True:
  line = input().strip()
  if line == "-1":
    break
  sequence.append(int(line))

k = int(input())  # "k" ze zadání

if len(sequence) < k:
  print("Nedostatek prvků.")
  sys.exit(1)

# Průběžně udržujme největší a nejmenší k-tici
min_elements = sorted(sequence[:k])
max_elements = list(reversed(min_elements))

for idx_seq in range(k, len(sequence)):
  for idx_k in range(k):
    # Proveď `insert` při nalezení prvního většího čísla
    if sequence[idx_seq] < min_elements[idx_k]:
      min_elements.insert(idx_k, sequence[idx_seq])
      min_elements.pop()
      break

  for idx_k in range(k):
    # Proveď `insert` při nalezení prvního menšího čísla
    if sequence[idx_seq] > max_elements[idx_k]:
      max_elements.insert(idx_k, sequence[idx_seq])
      max_elements.pop()
      break

print(sum(min_elements), sum(max_elements))
