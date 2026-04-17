"""
Generické typy byly vyhozeny, kvůli Python verzi v recodexu.
"""

from dataclasses import dataclass
from typing import Any


@dataclass(kw_only=True)
class Node:
  value: Any
  next: "Node | None"  # noqa: UP037 # starý Python


class PriorityQueue:
  def __init__(self) -> None:
    self._start: Node | None = None

  def is_empty(self) -> bool:
    return self._start is None

  def push(self, item):
    self._start = Node(value=item, next=self._start)

  def pop(self):
    if self.is_empty():
      raise Exception("Tried popping from empty queue")

    max_node = self._start
    max_previous: Node | None = None

    previous = self._start
    current = self._start.next

    while current is not None:
      if current.value > max_node.value:
        max_node = current
        max_previous = previous

      previous = current
      current = current.next

    if max_previous is None:
      self._start = max_node.next
    else:
      max_previous.next = max_node.next

    return max_node.value


queue = PriorityQueue()

while True:
  phrase = input().strip()
  if phrase == "-end-":
    print("-end-")
    break

  if phrase == "->":
    print(queue.pop())
    continue

  queue.push(int(phrase))
