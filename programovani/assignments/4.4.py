list1 = list(map(int, input().split(" ")))

for k_th_iteration in range(1, len(list1)):
  # V k-té iteraci budeme mít složeno k-1 prvků, takže můžeme iterovat jen od 1 do n-(k-1)-1 prvku.
  pointer = 1
  while pointer <= len(list1) - (k_th_iteration-1) - 1:
    # Když (i-1)-tý prvek > i-tý, prohoď je
    if list1[pointer-1] > list1[pointer]:
      list1[pointer], list1[pointer-1] = list1[pointer-1], list1[pointer]
    pointer += 1

print(" ".join(map(str, list1)))