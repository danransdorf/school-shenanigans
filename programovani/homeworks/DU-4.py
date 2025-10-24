list1 = list(map(int, input().split(" ")))
list2 = list(map(int, input().split(" ")))
len1 = len(list1) 
len2 = len(list2) 

intersection = []

pointer1, pointer2 = 0, 0
while pointer1 < len1 and pointer2 < len2:
  if list1[pointer1] < list2[pointer2]: # prvek 1 je nízký, posuň pointer1 dopředu
    pointer1 += 1
  elif list1[pointer1] > list2[pointer2]: # prvek 2 je nízký, posuň pointer2 dopředu
    pointer2 += 1
  elif list1[pointer1] == list2[pointer2]: # rovnost, přidej prvek do průniku, posuň se dopředu
    intersection.append(list1[pointer1])
    pointer1 += 1
    pointer2 += 1
  else: # Should never happen
    raise NotImplemented

print(" ".join(map(str, intersection)))