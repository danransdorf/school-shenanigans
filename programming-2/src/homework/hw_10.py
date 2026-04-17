"""
Řešení je O(M*logN), dalo by se udělat O(M) pro N <= 127 převodem zakódováním volných
míst do 128-bitového integeru (bitmasking). Tím by se dala měnit obsazenost místa v O(1)
a zároveň by se dalo konstantně hledat nejmenší volné místo. Je to ale implementační komplikace.
"""

import heapq
from collections import deque

parking_spaces, cars = map(int, input().strip().split(maxsplit=1))
parking_space_prices: list[int] = []
car_weights: list[int] = []
events: list[int] = []
for _ in range(parking_spaces):
  parking_space_prices.append(int(input()))
for _ in range(cars):
  car_weights.append(int(input()))
for _ in range(2 * cars):
  events.append(int(input()))


def get_price(space, car):
  return parking_space_prices[space - 1] * car_weights[car - 1]  # 1-indexing => 0-indexing


total_paid = 0
car_parking_space: dict[int, int | None] = dict.fromkeys(range(1, cars + 1))
car_queue: deque[int] = deque()
free_spaces = list(range(1, parking_spaces + 1))
for car in events:
  if car > 0:  # auto přijelo
    if 0 == len(free_spaces):  # není volné místo, auto jde do fronty
      car_queue.append(car)
      continue

    # auto získá nejnižší místo
    parking_space_min = heapq.heappop(free_spaces)
    car_parking_space[car] = parking_space_min
    total_paid += get_price(parking_space_min, car)
  elif car < 0:  # auto odjelo
    car = -car
    freed_space = car_parking_space[car]
    car_parking_space[car] = None
    if 0 == len(car_queue):  # nejsou žádná auta ve frontě, místo přidáme do volných
      heapq.heappush(free_spaces, freed_space)
      continue

    # Místo získá první auto ve frontě
    queued_car = car_queue.popleft()
    car_parking_space[queued_car] = freed_space
    total_paid += get_price(freed_space, queued_car)

print(total_paid)
