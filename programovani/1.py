from common import LessonPrinter

with LessonPrinter("Python jako kalkulačka") as p:
  p.item(24 + 15)
  p.item(4893847572 + 5879279532879827597387)
  p.item(4893847572 - 85375827)
  p.item(38742 * 38)
  p.text("Počítat s celými čísly není problém, ale co zlomky?")
  p.item(7 / 8)
  p.item(1 / 3)
  p.item(1 / 3 + 1 / 3 + 1 / 3)
  p.item(1 / 6 + 1 / 6 + 1 / 6 + 1 / 6 + 1 / 6 + 1 / 6, "← Nasčítání chyb může způsobit špatný výsledek")

  with p.subsection("Floor division") as sub:
    sub.item(14 // 3)
    sub.item(-14 // 3, "← Zaokrouhlení dolů - takže na -5")

  with p.subsection("Zbytek po dělení") as sub:
    sub.item(14 % 3)
    sub.item(14 % 7)

with LessonPrinter("Koncepty v programování") as p:
  with p.subsection("Boolean") as sub:
    sub.item(5 == 5)
    sub.item(5 == 5.0)
    sub.item(5 < 6 < 7)
    sub.item(5 != 5)
    sub.item(not True)

  with p.subsection("Variables") as sub:
    a = 14 + 3
    b = 14 - 3
    sub.item(a)
    sub.item(a + b)

  with p.subsection("If") as sub:
    if a > 5:
      sub.item("A > 5")

    if b < 5:
      sub.item("B < 5")
    else:
      sub.item("B >= 5")

  with p.subsection("While loop") as sub:
    x = 1
    while x <= 5:
      sub.item(x)
      x += 1

  with p.subsection("Comment") as sub:
    # Toto je komentář
    # sub.item("This won't print")
    sub.item("But this will print")

  with p.subsection("Input") as sub:
    sub.item(input("Zadej sem číslo a já to vytisknu: "))
    n = int(input("Zadej sem číslo a vytisknu všechny menší sudá čísla v N: "))

    x = 1
    while x < n:
      if x % 2 == 0:
        sub.item(x)
      x += 1
