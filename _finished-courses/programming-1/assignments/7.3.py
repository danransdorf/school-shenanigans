phrase = input()
lengths = {}
for word in phrase.split():
  word_chars = set(word)
  for char in word_chars:
    lengths[char] = lengths.get(char, 0) + 1

print(*(f"{k}=>{v}" for k, v in lengths.items()), sep="\n")
