input()  # flush nepotřebného řádku

numbers1 = list(map(int, input().strip().split()))
numbers2 = list(map(int, input().strip().split()))

ptr1, ptr2 = 0, 0
result1 = []
result2 = []

while True:
  if ptr1 == len(numbers1) and ptr2 == len(numbers2):
    break

  if ptr1 == len(numbers1):
    result2.append(ptr1 + ptr2 + 1)
    ptr2 += 1
    continue
  if ptr2 == len(numbers2):
    result1.append(ptr1 + ptr2 + 1)
    ptr1 += 1
    continue

  if numbers1[ptr1] < numbers2[ptr2]:
    result1.append(ptr1 + ptr2 + 1)
    ptr1 += 1
  else:
    result2.append(ptr1 + ptr2 + 1)
    ptr2 += 1


print(" ".join(map(str, result1)))
print(" ".join(map(str, result2)))
