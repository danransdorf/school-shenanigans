# V odevzdání #2 je verze na jednom řádku dle zadání, toto je zformátované pro čitelnost
print(*("even" if (x[-1] in "02468") else "odd" for x in input().split() if x.isdigit()), sep=" ")
