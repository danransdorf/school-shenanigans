numbers = []
while True:
  number = int(input())
  if number == -1:
    break
  numbers.append(number)

sorted_numbers = sorted(numbers)
min_gap = min(b - a for a, b in zip(sorted_numbers, sorted_numbers[1:]))
print(min_gap)