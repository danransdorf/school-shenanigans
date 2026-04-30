from queue import Queue
from typing import cast

vol1, vol2, vol3, amount1, amount2, amount3 = map(int, input().strip().split())
volumes = (vol1, vol2, vol3)

type VolumeState = tuple[int, int, int]
"""(amount1, amount2, amount3)"""
type State = tuple[VolumeState, int]
"""(volume_state, depth)"""

result: dict[int, int] = {}
"""dict[amount, steps]"""

memo: set[VolumeState] = set()

queue: Queue[State] = Queue()
queue.put(((amount1, amount2, amount3), 0))
while not queue.empty():
  volume_state, depth = queue.get()
  memo.add(volume_state)

  result.setdefault(volume_state[0], depth)
  result.setdefault(volume_state[1], depth)
  result.setdefault(volume_state[2], depth)

  for bucket_from in range(3):
    for bucket_to in range(3):
      if bucket_from == bucket_to:
        continue

      amount_to_pour = min(volume_state[bucket_from], volumes[bucket_to] - volume_state[bucket_to])
      new_state_raw = list(volume_state)
      new_state_raw[bucket_to] += amount_to_pour
      new_state_raw[bucket_from] -= amount_to_pour

      if (new_state := cast(tuple[int, int, int], tuple(new_state_raw))) not in memo:
        queue.put((new_state, depth + 1))

for idx, key in enumerate(sorted(result.keys())):
  print(f"{key}:{result[key]}", end=" " if idx != len(result) - 1 else "")
