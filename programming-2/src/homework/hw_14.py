"""

Note: This homework was completed using assigned template, hence the unstandard code style.

"""


# ruff: noqa # template


class Prvek:
  def __init__(self, x, dalsi):
    self.x = x
    self.dalsi = dalsi


def VytiskniLSS(p):
  print("LSS:", end=" ")
  while p != None:
    print(p.x, end=" ")
    p = p.dalsi
  print(".")


def NactiLSS():
  """cte cisla z radku, dokud nenacte prazdny radek"""
  prvni = None
  posledni = None
  r = input()
  while r != "":
    radek = r.split()
    if len(radek) == 0:  # protoze ten test r!="" v RCDX neukoncil cyklus!
      break
    for s in radek:
      p = Prvek(int(s), None)
      if prvni == None:
        prvni = p
      else:
        posledni.dalsi = p
      posledni = p
    r = input()
  return prvni


#################################################


def IntersectionDestruct(node1: Prvek | None, node2: Prvek | None):
  """destruktivni prunik dvou usporadanych seznamu
  * nevytvari zadne nove prvky, vysledny seznam bude poskladany z prvku puvodnich seznamu,
  * vysledek je MNOZINA, takze se hodnoty neopakuji"""

  # sem doplnte kod funkce, dalsi casti zdrojoveho kodu NEMENTE
  # ....................................................

  if node1 is None or node2 is None:
    return None

  # Vytvořme placeholder, abychom se vyhli zvláštnímu vložení prvního prvku
  sentinel: Prvek = Prvek(x=-1, dalsi=None)
  intersection_tail: Prvek = sentinel

  while node1 is not None and node2 is not None:
    if node1.x > node2.x:
      node2 = node2.dalsi
      continue
    if node1.x < node2.x:
      node1 = node1.dalsi
      continue

    # invariant: node1.x == node2.x
    intersection_tail.dalsi = node1
    intersection_tail = intersection_tail.dalsi
    node1 = node1.dalsi
    node2 = node2.dalsi

  intersection = sentinel.dalsi  # sentinel drží průnik počínaje druhým prvkem
  if intersection_tail is not None:
    intersection_tail.dalsi = None

  return intersection

  # ....................................................


#################################################

VytiskniLSS(IntersectionDestruct(NactiLSS(), NactiLSS()))
