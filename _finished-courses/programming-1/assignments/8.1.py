line1 = {int(x) for x in input().strip().split()}
line2 = {int(x) for x in input().strip().split()}
line3 = {int(x) for x in input().strip().split()}

uniques = {
  *line1.difference(line2, line3),
  *line2.difference(line1, line3),
  *line3.difference(line1, line2),
}

print(*uniques, sep="\n")