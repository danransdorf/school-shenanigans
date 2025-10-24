name, surname = input().split(" ")
age = int(input())
gender = input()

if age < 18:
  print(f"Hello {name}!")
else:
  print(
    "Good morning",
    "Mr." if gender == "m" else "Mrs.",
    f"{surname}."
  )