length = int(input())
string = input()

memo = set()
for starting_position in range(len(string) - length + 1):
  current = string[starting_position : starting_position + length]
  if current not in memo:
    memo.add(current)
    print(current)
