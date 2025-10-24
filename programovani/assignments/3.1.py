import datetime

day = int(input())
month = int(input())
year = int(input())

try:
  datetime.datetime(abs(year),month,day)
  print(True)
except:
  print(False)