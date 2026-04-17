"""Dle zadání => tvořeno kopií šablony a implementováním"""

# ruff: noqa: N802 # nestandardní jmenování je součástí zadání


class Clovek:
  def __init__(self, vek, dalsi=None):
    # věk člověka
    self.vek = vek
    # další člověk ve frontě
    self.dalsi = dalsi


class Fronta:
  def __init__(self):
    # Ze standardního vstupu přečte seznam NEZÁPORNÝCH čísel.
    # Na každém řádku je jedno číslo, na posledním řádku je -1
    # (seznam může být i prázdný, pak je na vstupu jen -1).
    # Každé číslo představuje věk člověka ve frontě, první číslo
    # odpovídá věku člověka na začátku fronty (tj. prvního ve frontě).
    # Vytvoří frontu objektů typu Clovek v podobě spojového seznamu, kde
    # každý člověk ví, kdo je ZA NÍM ve frontě (tj. obráceně než je to u
    # fronty lidí obvyklé).

    # První člověk ve frontě.
    self.prvni = None
    current = None
    while True:
      number = int(input())
      if -1 == number:
        break
      if current is None:
        self.prvni = Clovek(number, None)
        current = self.prvni
      else:
        current.dalsi = Clovek(number, None)
        current = current.dalsi

  def vypis(self):
    # Postupně vypíše věky všech lidí ve frontě, od prvního do posledního,
    # a to na jeden řádek; za každým věkem bude mezera.
    # Pozor, není povoleno použít list, takže vypisujte věky průběžně
    # pomocí print(vek, end=" ")
    # Je-li fronta prázdná, vypíše místo toho slovo PRAZDNY

    current = self.prvni
    if current is None:
      print("PRAZDNY")
      return

    while current is not None:
      print(current.vek, end=" ")
      current = current.dalsi

    print()

  def vyhodNejstarsi(self):
    # Z fronty vyhodí nejstaršího člověka, respektive všechny nejstarší
    # lidi (ve frontě může být i více lidí stejného věku).
    if self.prvni is None:
      return

    current = self.prvni
    max_age = current.vek
    while current is not None:
      if current.vek > max_age:
        max_age = current.vek
      current = current.dalsi

    nova_prvni = None
    nova_posledni = None

    current = self.prvni
    while current is not None:
      dalsi = current.dalsi
      current.dalsi = None

      if current.vek != max_age:
        if nova_prvni is None:
          nova_prvni = current
          nova_posledni = current
        else:
          nova_posledni.dalsi = current
          nova_posledni = current

      current = dalsi

    self.prvni = nova_prvni

  def nejstarsiDozadu(self):
    # Nejstaršího člověka (respektive všechny nejstarší lidi) přesune na
    # konec fronty.
    if self.prvni is None:
      return

    current = self.prvni
    max_age = current.vek
    while current is not None:
      if current.vek > max_age:
        max_age = current.vek
      current = current.dalsi

    ostatni_prvni = None
    ostatni_posledni = None
    stari_prvni = None
    stari_posledni = None

    current = self.prvni
    while current is not None:
      dalsi = current.dalsi
      current.dalsi = None

      if current.vek == max_age:
        if stari_prvni is None:
          stari_prvni = current
          stari_posledni = current
        else:
          stari_posledni.dalsi = current
          stari_posledni = current
      else:
        if ostatni_prvni is None:
          ostatni_prvni = current
          ostatni_posledni = current
        else:
          ostatni_posledni.dalsi = current
          ostatni_posledni = current

      current = dalsi

    if ostatni_prvni is None:
      self.prvni = stari_prvni
    else:
      ostatni_posledni.dalsi = stari_prvni
      self.prvni = ostatni_prvni

  def zdvojVsechny(self):
    # Zdvojí všechny lidi, tj. za každého člověka se ve frontě postaví
    # ještě jeden nový stejně starý člověk.
    current = self.prvni
    while current is not None:
      current.dalsi = Clovek(vek=current.vek, dalsi=current.dalsi)
      current = current.dalsi.dalsi

  def zdvojNejmladsi(self):
    # Zdvojí nemladšího člověka (resp. všechny nejmladší lidi): za
    # každého člověka s nejnižším věkem se postaví ještě jeden nový
    # stejně starý člověk.
    if self.prvni is None:
      return

    current = self.prvni
    min_age = None
    while current is not None:
      if min_age is None or current.vek < min_age:
        min_age = current.vek
      current = current.dalsi

    current = self.prvni
    while current is not None:
      if current.vek == min_age:
        current.dalsi = Clovek(vek=current.vek, dalsi=current.dalsi)
        current = current.dalsi.dalsi
      else:
        current = current.dalsi

  def vyhodTriPosledni(self):
    # Vyhodí tři poslední lidi z fronty (pokud je ve frontě méně než 3
    # lidi, tak po této operaci bude fronta prázdná).
    current = self.prvni
    if current is None or current.dalsi is None or current.dalsi.dalsi is None or current.dalsi.dalsi.dalsi is None:
      self.prvni = None
      return

    while current.dalsi.dalsi.dalsi.dalsi is not None:
      current = current.dalsi

    current.dalsi = None

  def licheSude(self):
    # Přerovná frontu tak, aby v ní nejprve stáli všichni lidi s lichým
    # věkem (se zachováním jejich původního vzájemného pořadí)
    # a následně všichni lidé se sudým věkem (opět se zachováním jejich
    # původního vzájemného pořadí)
    if self.prvni is None:
      return

    liche_prvni = None
    liche_posledni = None
    sude_prvni = None
    sude_posledni = None

    current = self.prvni
    while current is not None:
      dalsi = current.dalsi
      current.dalsi = None

      if current.vek % 2 == 1:
        if liche_prvni is None:
          liche_prvni = current
          liche_posledni = current
        else:
          liche_posledni.dalsi = current
          liche_posledni = current
      else:
        if sude_prvni is None:
          sude_prvni = current
          sude_posledni = current
        else:
          sude_posledni.dalsi = current
          sude_posledni = current

      current = dalsi

    if liche_prvni is None:
      self.prvni = sude_prvni
    else:
      liche_posledni.dalsi = sude_prvni
      self.prvni = liche_prvni

  def zrus(self):
    # Zruší frontu (po této operaci bude fronta prázdná).
    self.prvni = None


fronta = Fronta()
fronta.vypis()
fronta.vyhodNejstarsi()
fronta.vypis()
fronta.nejstarsiDozadu()
fronta.vypis()
fronta.vyhodTriPosledni()
fronta.vypis()
fronta.licheSude()
fronta.vypis()
fronta.zdvojNejmladsi()
fronta.vypis()
fronta.zdvojVsechny()
fronta.vypis()
fronta.zrus()
fronta.vypis()
fronta.vyhodNejstarsi()
fronta.vypis()
