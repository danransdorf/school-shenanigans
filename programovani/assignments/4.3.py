phrase = input().replace(" ", "")

print("ANO" if phrase == phrase[::-1] else "NE")