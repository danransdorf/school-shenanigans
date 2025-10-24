sum_accumulated = 0
max_number = None

while True:
  number = int(input())
  if number == -1:
    break
  
  sum_accumulated += number
  if max_number is None:
    max_number = number
  else:
    max_number = max(number, max_number)

sum_expected = max_number * (max_number+1) // 2
print(
  # Když rozdíl 0 : vypiš max+1, protože tedy chybí číslo n
  (sum_expected - sum_accumulated) or max_number+1 
)