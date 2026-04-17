relations = {}
wanted_keys = []
while True:
  phrase = input()
  if phrase == "!":
    break
  if " " in phrase:
    a, b = phrase.split()
    relations.setdefault(a, set()).add(b)
    relations.setdefault(b, set()).add(a)
  else:
    wanted_keys.append(phrase)

for key in wanted_keys:
  print(*sorted(relations.get(key, [])))
