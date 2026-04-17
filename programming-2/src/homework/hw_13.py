class Zvire:
  def __init__(self, nazev):
    self.nazev = nazev
    self.dalsi = None

  def prichazi_za_mne(self, zvire):
    self.dalsi = zvire

  def kousni_dalsiho(self):
    if self.dalsi is None:
      return f"{self.nazev}: nikdo za mnou neni"

    return f"{self.nazev}: {self.dalsi.nazev} ma ode me kousanec"

# zkus načíst první
first_phrase = input().strip()
if first_phrase == "konec":
  raise ValueError("Nic nepřišlo, tedy první zvíře nemůže odejít.")

prvni = Zvire(first_phrase)
posledni = prvni
while (phrase := input().strip()) != "konec":
  new = Zvire(phrase)
  posledni.prichazi_za_mne(new)
  posledni = new

# výtisk fronty
current = prvni
while current is not None:
  print(current.nazev)
  current = current.dalsi

# prvni odejde
prvni = prvni.dalsi

# přijde ptakopysk
ptakopysk = Zvire("ptakopysk")
ptakopysk.dalsi = prvni
prvni = ptakopysk

# přijde mravenec
mravenec = Zvire("mravenec")
mravenec.dalsi = prvni
prvni = mravenec

# zvířata se pokoušou
current = prvni
while current is not None:
  print(current.kousni_dalsiho())
  current = current.dalsi
