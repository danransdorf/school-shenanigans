phrase = input()
lengths = {}
for word in phrase.split():
  lengths[len(word)] = lengths.get(len(word), 0) + 1

print(*(f"{k}: {v}" for k, v in lengths.items() if k != 0), sep="\n")
