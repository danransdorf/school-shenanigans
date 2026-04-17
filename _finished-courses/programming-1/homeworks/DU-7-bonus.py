print(
  *(
    "\n".join(
      [" ".join([f"{((number1 * number2) % n):>{len(str(n - 1))}}" for number2 in range(n)]) for number1 in range(n)]
    )
    for n in [int(input())]
  )
)
