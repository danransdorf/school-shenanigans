from common import LessonPrinter

with LessonPrinter("Stringy") as p:
  greeting = "Hello"
  name = "Daniel"
  p.item(f"{greeting}, {name}")

  with p.subsection("Aggregating digit input") as sub:
    program = input("Enter program (digit_agg/digit_sum):")

    match program:
      case "digit_agg":
        acc = 0
        while -1 != (num := int(input("Enter digit: "))):
          acc = 10 * acc + num
        sub.item(f"Aggregated: {acc}")
      case "digit_sum":
        sub.item(f"Digit sum: {sum([int(x) for x in input('Enter number: ')])}")
      case _:
        pass
