import ast
from collections.abc import Callable

expression = ast.parse(input(), mode="eval").body

BINARY_OPERATION: dict[ast.expr, Callable[[int | float, int | float], int]] = {
  ast.Add: lambda x, y: x + y,
  ast.Mult: lambda x, y: x * y,
}


def evaluate(node: ast.expr) -> int | float:
  match node:
    case ast.Constant():
      return node.value
    case ast.BinOp():
      return BINARY_OPERATION[type(node.op)](evaluate(node.left), evaluate(node.right))
    case ast.UnaryOp():
      if node.op is ast.UAdd:
        return evaluate(node.operand)
      elif node.op is ast.USub:
        return evaluate(node.operand)
      else:
        raise ValueError("Unknown operation")
    case _:
      raise ValueError("Unknown node:", node)


print(evaluate(expression))
