size = int(input())

for dot_amount in range(-size + 1, size):
  print("." * abs(dot_amount) + "*" * abs(2 * (size - abs(dot_amount)) - 1) + "." * abs(dot_amount))
