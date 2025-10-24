import sys
import time
from contextlib import ContextDecorator


class bench(ContextDecorator):  # noqa: N801
  def __init__(self, name="block", *, logger=print, unit="ms", precision=3):
    self.name = name
    self.logger = logger
    self.unit = unit
    self.precision = precision
    self._start: float

  def __enter__(self):
    self._start = time.perf_counter()
    return self

  def __exit__(self, exc_type, exc, tb):
    elapsed_s = time.perf_counter() - self._start
    factor = {"ns": 1e9, "us": 1e6, "µs": 1e6, "ms": 1e3, "s": 1}.get(self.unit, 1e3)
    value = elapsed_s * factor
    self.logger(f"[bench] {self.name}: {value:.{self.precision}f} {self.unit}")
    # Don't swallow exceptions
    return False

number = int(input())

with bench("Rozklad"):
  prime_composition = []

  # Vytáhni všechny dvojky
  while number % 2 == 0:
    number //= 2
    prime_composition.append(2)

  # Zkoušej postupně dělit lichými čísly menšími než odmocnina n
  potential_divisor = 3
  while number >= potential_divisor**2:
    while number % potential_divisor == 0:
      number //= potential_divisor
      prime_composition.append(potential_divisor)
    potential_divisor += 2 # posuň se na další liché číslo

  # Cokoli, co zbyde, je prvočíslo (nedělitelné čísly < n^(1/2))
  if number != 1:
    prime_composition.append(number)
    

  print(" ".join(map(str, prime_composition)), file=sys.stdout)