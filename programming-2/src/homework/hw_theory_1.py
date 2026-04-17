"""
Idea: Použít bucketing, jelikož největší mezera musí být velká alespoň "délka / počet mezer".
Jest:
  - počet mezer ← (začátek + poutače + konec) - 1
  - Rozděl délku dálnice na úseky (buckety) široké "délka / počet mezer".
  - Načítej pozice poutačů, přičemž udržuj min/max každého bucketu
  - Nejvzdálenější body najdi podle nejdelší mezery -- maximálního rozdílu "max - min následujícího neprázdného bucketu"
  - Vrať pozici přesně v půli mezi nejvzdálenějšími body

Technikálie: Nevěřme floatům, vstup jsou kilometry zaokrouhlené na 3 cifry, převeďme na metry (int)
"""

import sys
from pathlib import Path
from typing import cast

type Min = int
type Max = int
EMPTY = object()  # nahraďme None něčím deskriptivnějším
KM_TO_M = 1000

with Path("vstup.txt").open() as f:
  highway_length = int(f.readline()) * KM_TO_M  # km → m
  banner_amount = int(f.readline())

  if 0 == banner_amount:
    Path("vystup.txt").write_text(f"{(highway_length / 2 / KM_TO_M):.3f}")
    sys.exit(0)

  anchor_count = banner_amount + 2  # Poutače + začátek + konec
  space_count = anchor_count - 1  # n-1 mezer
  bucket_size = highway_length / space_count

  buckets: list[tuple[Min, Max] | object] = [EMPTY] * (space_count)
  for _ in range(banner_amount):
    banner_position = int(round(float(f.readline()) * KM_TO_M))
    if not 0 < banner_position < highway_length:  # Se začátkem a koncem dálnice počítáme na konci tak, či tak
      continue

    bucket_idx = int(banner_position // bucket_size)
    if bucket_idx == space_count:  # safeguard, kdyby banner_position cca == highway_length
      bucket_idx -= 1

    if buckets[bucket_idx] is EMPTY:
      buckets[bucket_idx] = banner_position, banner_position
      continue

    bucket_min, bucket_max = buckets[bucket_idx]  # ty: ignore[not-iterable] # buckets[bucket_idx]: tuple[Min, Max]
    buckets[bucket_idx] = min(bucket_min, banner_position), max(bucket_max, banner_position)

# nastav na začátek dálnice
gap_max_start = 0
gap_max = 0

prev_bucket_max = 0
for bucket in buckets:
  if bucket is EMPTY:  # Mezera neskončila, dokud nenajdeme neprázdný bucket
    continue
  bucket = cast(tuple[Min, Max], bucket)

  bucket_min, bucket_max = bucket
  gap = bucket_min - prev_bucket_max
  if gap > gap_max:
    gap_max = gap
    gap_max_start = prev_bucket_max
  prev_bucket_max = bucket_max

# Zkontroluj mezeru na konci dálnice
gap_final = highway_length - prev_bucket_max
if gap_final > gap_max:
  gap_max = gap_final
  gap_max_start = prev_bucket_max


Path("vystup.txt").write_text(f"{((gap_max_start + gap_max / 2) / KM_TO_M):.3f}")
