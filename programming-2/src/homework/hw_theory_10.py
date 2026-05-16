"""TODO: doc"""

count = int(input())
sequence = list(map(int, input().split()))

longest_starting_at: list[int] = [0] * (count)
memo_starting_with: list[int | None] = [None] * (count + 1)
"""Délky posloupnosti 0..k, na indexu `j` je nejvyšší číslo, kterým začíná `j` dlouhá nalezená podposloupnost"""
for idx in reversed(range(count)):
  largest_len = count
  while largest_len >= 0 and (
    memo_starting_with[largest_len] is None  # type: ignore
  ):
    largest_len -= 1

  largest_compatible = largest_len
  while largest_compatible >= 0 and (
    memo_starting_with[largest_compatible] is None or sequence[idx] > memo_starting_with[largest_compatible]  # type: ignore
  ):
    largest_compatible -= 1

  new_sequence_length = max(1, largest_compatible + 1)
  longest_starting_at[idx] = max(new_sequence_length, largest_len)
  current = memo_starting_with[new_sequence_length]
  memo_starting_with[new_sequence_length] = max(current, sequence[idx]) if current is not None else sequence[idx]  # type: ignore

# obdobně sestavme délky posloupností končících na indexu
longest_ending_at: list[int] = [0] * (count)
memo_ending_with: list[int | None] = [None] * (count + 1)
"""Délky posloupnosti 0..k, na indexu `j` je nejvyšší číslo, kterým začíná `j` dlouhá nalezená podposloupnost"""
for idx in range(count):
  largest_len = count
  while largest_len >= 0 and (
    memo_ending_with[largest_len] is None  # type: ignore
  ):
    largest_len -= 1

  largest_compatible = largest_len
  while largest_compatible >= 0 and (
    memo_ending_with[largest_compatible] is None or sequence[idx] < memo_ending_with[largest_compatible]  # type: ignore
  ):
    largest_compatible -= 1

  new_sequence_length = max(1, largest_compatible + 1)
  longest_ending_at[idx] = max(new_sequence_length, largest_len)
  current = memo_ending_with[new_sequence_length]
  memo_ending_with[new_sequence_length] = min(current, sequence[idx]) if current is not None else sequence[idx]  # type: ignore

# maximální "slepení" dvou podposloupností
maximum = max(longest_starting_at[0], longest_ending_at[count - 1])
for i in range(count - 1):
  maximum = max(longest_ending_at[i] + longest_starting_at[i + 1], maximum)

print(maximum)
