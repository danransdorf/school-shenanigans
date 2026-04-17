decimal_part = input().split(".")[1][::2].rstrip("0")

if decimal_part:
  print("0." + decimal_part)
else:
  print("0")
