def number_of_divisors(number: int) -> int:
  amount = 0
  for potential_divisor in range(1, number+1):
    if number % potential_divisor == 0:
      amount += 1
  
  return amount

start, end = [int(x) for x in input().split()]

divisors: dict[int, set[int]] = {}
"""dict[number of divisors, numbers]"""

for n in range(start, end+1):
  amount = number_of_divisors(n)
  divisors.setdefault(amount, set()).add(n)

for amount in range(1, max(divisors.keys())+1):
  print(amount, '->', *sorted(divisors[amount] if amount in divisors else []))