import sys

count = int(input().strip())
numbers = list(map(int, input().strip().split()))

right_anchor_idx = count - 1
while right_anchor_idx > 0:
  current_idx = right_anchor_idx - 1
  if numbers[current_idx] >= numbers[right_anchor_idx]:
    right_anchor_idx = current_idx
    continue
  if numbers[current_idx] < numbers[right_anchor_idx]:
    # najdi nejmenší větší číslo vpravo
    min_idx = right_anchor_idx
    for idx in range(
      count - 1, right_anchor_idx, -1
    ):  # minimum nalezneme procházením zprava, protože ocas je klesající
      if numbers[idx] > numbers[current_idx]:
        min_idx = idx
        break
    # extrakce prvku a sort ocasu
    part1 = numbers[:current_idx]
    part2 = [numbers[min_idx]]
    part3_1 = numbers[current_idx + 1 : min_idx]
    part3_2 = numbers[min_idx + 1 :]
    part3 = list(reversed(part3_1 + [numbers[current_idx]] + part3_2))  # nemusíme řadit, tato část je klesající
    result = part1 + part2 + part3
    print(*result)
    sys.exit(0)

print("NEEXISTUJE")
