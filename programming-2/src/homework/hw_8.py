"""Vstupem jsou slova obsahující malá písmen a-z."""

from collections.abc import Iterable

Word = bytes
Char = int


ASCII_A = 97
ASCII_Z = 122

words: list[Word] = []
while True:
  line = input().strip()
  if line == "-end-":
    break

  words.append(bytes(line, encoding="ascii"))


def bucket_sort(words: list[Word], *, at_position: int = 0) -> Iterable[Word]:
  """at_position: aktuálně srovnávaná pozice znaku (úroveň rekurze)"""
  if 1 == len(words):
    yield words[0]
    return

  char_buckets: dict[Char, list[Word]] = {}  # Bucketing po charakterech
  for word in words:
    if at_position == len(word):  # Slovo již skončilo
      yield word  # Vraťme to, jelikož je kratší než ostatní
      continue
    char_buckets.setdefault(word[at_position], []).append(word)

  for char in range(ASCII_A, ASCII_Z + 1):  # Projdi postupně buckety od A do Z.
    if char in char_buckets:
      # Vrať seřazený bucket -- zvyš pozici znaku, dle kterého řadíš
      yield from bucket_sort(char_buckets[char], at_position=at_position + 1)


for word in bucket_sort(words):
  print(str(word, encoding="ascii"))

print("-end-")
