class Vektor:
  # Začátek tvého kódu

  ### This HW had a template, my code starts here ###

  def __init__(self, coord1: int, coord2: int) -> None:
    self._coord1: int = coord1
    self._coord2: int = coord2

  # Immutable props
  @property
  def coord1(self) -> int:
    return self._coord1

  @property
  def coord2(self) -> int:
    return self._coord2

  # Mutators
  def vynasob(self, coef: int) -> None:
    self._coord1, self._coord2 = coef * self.coord1, coef * self.coord2

  # Methods
  def norma(self) -> float:
    return (self.coord1**2 + self.coord2**2) ** (1 / 2)

  def je_linearne_zavisly(self, other: "Vektor") -> bool:
    if not isinstance(other, Vektor):
      raise ValueError(f"Cannot determine linear independence with non-vector ({type(self).__name__})")

    return self.coord1 * other.coord2 == self.coord2 * other.coord1

  # Magic method override
  def __str__(self) -> str:
    return f"({self.coord1},{self.coord2})"

  def __mul__(self, other: "Vektor") -> int:
    if not isinstance(other, Vektor):
      raise ValueError(f"Cannot multiply vector with non-vector ({type(self).__name__})")

    return self.coord1 * other.coord1 + self.coord2 * other.coord2

  ### This HW had a template, my code ends here ###

  # Konec tvého kódu


ux, uy = tuple([int(t) for t in input().split()])
u = Vektor(ux, uy)

vx, vy = tuple([int(t) for t in input().split()])
v = Vektor(vx, vy)

while True:
  command = input()
  if command == "p":
    print(u)
    print(v)
  elif command == "v":
    print(f"{u.norma():.2f}")
    print(f"{v.norma():.2f}")
  elif command == "z":
    print(u.je_linearne_zavisly(v))
  elif command == "s":
    print(u * v)
  elif command.startswith("n"):
    n = int(command.split()[1])
    u.vynasob(n)
    v.vynasob(n)
  else:
    break
