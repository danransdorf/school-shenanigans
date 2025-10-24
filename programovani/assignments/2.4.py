
import sys


number = int(input())

if number == 1:
  print("ne")
  sys.exit(0)

if number == 2:
  print("ano")
  sys.exit(0)
  
if number % 2 == 0:
  print("ne")
  sys.exit(0)

potential_divisor = 3
while number >= potential_divisor**2:
  if number % potential_divisor == 0:
    print("ne")
    sys.exit(0)
  potential_divisor += 2 # posuň se na další liché číslo

print("ano")