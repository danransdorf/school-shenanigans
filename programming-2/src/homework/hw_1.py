data: list[tuple[str, list[str]]] = []
while True:
  line = input()
  if line == "---":
    break
  key, values_str = line.split(": ", maxsplit=1)  # rozděl podle :
  values = list(values_str.split(", "))  # rozděl hodnoty podle , a ignoruj mezery
  data.append((key, values))

# dualně použijme sety a listy, sety kvůli unikátnosti, listy kvůli zachování pořadí
inverse_data: dict[str, set[str]] = {}
inverse_data_ordered: dict[str, list[str]] = {}
for key, values in data:
  for value in values:
    if value not in inverse_data or key not in inverse_data[value]:
      inverse_data.setdefault(value, set()).add(key)
      inverse_data_ordered.setdefault(value, []).append(key)

for key in sorted(inverse_data_ordered.keys()):  # seřaď klíče dle abecedy
  values = inverse_data_ordered[key]
  print(f"{key}: {', '.join(sorted(values))}")

print("---")
