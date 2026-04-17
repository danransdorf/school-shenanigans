"""
Idea: Budeme evidovat aktuální přítomné vlny zákazníků pomocí double-ended queue (deque),
  protože deque poskytuje O(1) .append() a .popleft().
  Nové vlny budeme přidávat doprava, staré vlny budeme odebírat zleva.
"""

from collections import deque

duration = int(input())
customers_max = 0
customers_current = 0
waves_current: deque[int] = deque()  # aktuálně přítomné vlny zákazníků
while True:
  try:
    wave = int(input())
  except ValueError:
    break

  customers_current += wave
  waves_current.append(wave)

  if len(waves_current) > duration:
    customers_current -= waves_current.popleft()  # nejstarší vlna zákazníků odejde

  if customers_current > customers_max:
    customers_max = customers_current

print(customers_max)
