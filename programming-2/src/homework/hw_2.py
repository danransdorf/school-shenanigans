nums1 = list(map(int, input().split()))
nums2 = list(map(int, input().split()))


merged = []
p1, p2 = 0, 0
while p1 < len(nums1) or p2 < len(nums2):
  # oba listy nebyly večerpány
  if p1 < len(nums1) and p2 < len(nums2):
    if nums1[p1] > nums2[p2]:
      merged.append(nums2[p2])
      p2 += 1
    else:
      merged.append(nums1[p1])
      p1 += 1
  # nums2 byl vyčerpán
  elif p1 < len(nums1):
    merged.append(nums1[p1])
    p1 += 1
  # nums1 byl vyčerpán
  elif p2 < len(nums2):
    merged.append(nums2[p2])
    p2 += 1
  else:
    break

print(" ".join(map(str, merged)))
