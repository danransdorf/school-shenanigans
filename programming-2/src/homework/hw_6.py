sort = lambda x: "".join(sorted(x))  # noqa: E731

len_words = int(input())
char_words_mapping: dict[str, list[str]] = {}
for _ in range(len_words):
  word = input()
  char_words_mapping.setdefault(sort(word), []).append(word)

len_queries = int(input())
for _ in range(len_queries):
  query_chars = sort(input())
  if (result := char_words_mapping.get(query_chars)) is not None:
    print(" ".join(sorted(result)))
  else:
    print("")
