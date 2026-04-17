"""
Program je naivní, při neplatném vstupu se někde v procesu vyhodí výjimka
(buď při int(), nebo kvůli indexu mimo rozsah)
"""


def evaluate(expression: list[str]) -> int:
  def _mult(a: int, b: int) -> int:
    return a * b

  def _add(a: int, b: int) -> int:
    return a + b

  def _subtract(a: int, b: int) -> int:
    return a - b

  idx = 0

  def _evaluate() -> int:
    nonlocal idx

    current_idx = idx
    idx += 1

    match expression[current_idx]:
      case "*":
        return _mult(_evaluate(), _evaluate())
      case "+":
        return _add(_evaluate(), _evaluate())
      case "-":
        return _subtract(_evaluate(), _evaluate())
      case hopefully_number:
        return int(hopefully_number)

  return _evaluate()


expression = input().strip().split()
print(evaluate(expression))
