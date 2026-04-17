"""

!!!

Disclaimer: The code was provided by the instructor as-is (intentionally cryptic names, bad practices, etc.).
  My only task was to write comments.

!!!


"""


class Graf:
  """
  Orientovaný graf.
  FIXME: !!! Metoda r() je špatně implementována kvůli neznámé třídě GrafSS !!!
  """

  def __init__(self, n):
    """
    Nastaví parametry nové instanci grafu.

    Args:
      n (int): Počet vrcholů
    """
    self.n = n
    self.seznam_sousedu = [[] for _ in range(n)]

  def __repr__(self):
    """Vrátí textovou reprezentaci grafu pro vývojáře."""
    return str(self.seznam_sousedu)

  def pridej_hranu(self, i, j):
    """
    Přidá do grafu orientovanou hranu.

    Args:
      i (int): Index vrcholu, ZE kterého vedeme hranu
      j (int): Index vrcholu, DO kterého vedeme hranu
    """
    self.seznam_sousedu[i].append(j)

  def x(self):
    """
    Získá počet vrcholů v grafu.

    Returns:
      int: počet vrcholů
    """
    return self.n

  def y(self, u):
    """
    Získá počet hran vedených ze specifikovaného vrcholu.

    Args:
      u (int): index chtěného vrcholu

    Raises:
      IndexError: při indexu mimo rozsah

    Returns:
      int: počet hran vedených z vrcholu
    """
    return len(self.seznam_sousedu[u])

  def p(self):
    """
    Získá počet hran v grafu.

    Returns:
      int: počet hran v grafu
    """
    return sum(len(self.seznam_sousedu[u]) for u in range(self.n))

  def mn(self):
    """
    Získá indexy vrcholů, ze kterých nevede žádná hrana.

    Returns:
      list[int]: indexy vrcholů
    """
    return [u for u in range(self.n) if len(self.seznam_sousedu[u]) == 0]

  def e(self, i, j):
    """
    Vrátí, zda existuje hrana mezi dvěma vrcholy.

    Args:
      i (int): index vrcholu, ZE kterého má hrana vést
      j (int): index vrcholu, DO kterého má hrana vést

    Returns:
      bool: zda hrana existuje
    """
    return j in self.seznam_sousedu[i]

  def k(self, u):
    """
    Vytiskne všechny sousední vrcholy vrcholu "u".
    (tj. všechny, do kterých vede z vrcholu "u" hrana).

    Args:
      u (int): Index vrcholu

    Raises:
      IndexError: při indexu mimo rozsah
    """
    for v in self.seznam_sousedu[u]:
      print(v)

  def s(self):
    """
    Vrátí všechny hrany v grafu jako dvojice.

    Returns:
      list[tuple[int,int]]: hrany jako dvojice indexů vrcholů (z, do)
    """
    hrany = []

    for u in range(self.n):
      for v in self.seznam_sousedu[u]:
        hrany.append((u, v))

    return hrany

  def ms(self):
    """
    Vrátí vrcholy, ze kterých vede nejvíce hran.

    Raises:
      ValueError: při self.n==0, kvůli prázdnému argumentu pro max()

    Returns:
      list[int]: indexy vrcholů
    """
    pm = max(len(self.seznam_sousedu[u]) for u in range(self.n))
    return [u for u in range(self.n) if len(self.seznam_sousedu[u]) == pm]

  def eo(self):
    """
    Vrátí, zda je graf symetrický. (tj. pro hranu (u,v) existuje hrana (v,u))

    Returns:
      bool: zda je graf symetrický
    """
    for u in range(self.n):
      for v in self.seznam_sousedu[u]:
        if u not in self.seznam_sousedu[v]:
          return False
    return True

  def mp(self):
    """
    Vrátí všechny vrcholy, do kterých nevede hrana.

    Returns:
      list[int]: indexy vrcholů
    """
    vstupni = [0] * self.n
    for u in range(self.n):
      for v in self.seznam_sousedu[u]:
        vstupni[v] += 1
    return [i for i in range(self.n) if vstupni[i] == 0]

  def r(self):
    """
    Vrátí graf s opačnou orientací hran.

    Raises:
      NameError: GrafSS aktuálně není definován

    Returns:
      GrafSS: graf s opačnou orientací hran
    """
    novy = GrafSS(self.n)  # FIXME: nedefinováno
    for u in range(self.n):
      for v in self.seznam_sousedu[u]:
        novy.pridej_hranu(v, u)
    return novy
