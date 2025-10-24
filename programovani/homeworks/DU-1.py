import sys

numbers = []
while True:
  # number_raw = input("Zadej číslo (-1 pro ukončení vstupu): ")
  number_raw = input()
  try:
    number = int(number_raw.replace(" ", ""))
    if number == -1:
      break
    numbers.append(number)
  except Exception:
    # print("Neplatné číslo, zkuste znovu.")
    ...

if 0 == len(numbers):
  # print("Musí být zadáno alespoň jedno platné číslo.")
  sys.exit(1)

print(max(numbers))
