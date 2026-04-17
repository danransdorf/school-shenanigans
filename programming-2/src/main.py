from __future__ import annotations

import ast
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VALID_CATEGORIES = ("homework", "junk")
HELP_ALIASES = {"-h", "--help", "help"}
LIST_ALIASES = {"list", "ls"}


def print_category_usage(command_name: str, category: str) -> None:
  print(f"Usage: {command_name} <task-id|list> [task-args...]")
  print(f"Example: {command_name} 4.1")
  print(f"Runs tasks from: src/{category}/")


def print_root_usage() -> None:
  print("Usage: python src/main.py <homework|junk> <task-id|list> [task-args...]")
  print("Examples:")
  print("  python src/main.py homework 4.1")
  print("  homework 4.1")
  print("  hw 4.1")
  print("  junk tryout")


def category_dir(category: str) -> Path:
  return ROOT / category


def available_tasks(category: str) -> list[str]:
  task_dir = category_dir(category)
  if not task_dir.exists():
    return []

  tasks: list[str] = []
  for file in sorted(task_dir.glob("*.py")):
    if file.name.startswith("_"):
      continue

    task_id = file.stem
    for prefix in ("task_", "hw_", "homework_", "junk_"):
      if task_id.startswith(prefix):
        task_id = task_id.removeprefix(prefix)
        break

    task_id = task_id.replace("_", ".")
    tasks.append(f"{task_id} ({file.name})")

  return tasks


def task_candidates(category: str, task_id: str) -> list[str]:
  raw = task_id.strip()
  normalized = raw.replace(".", "_").replace("-", "_")

  names: list[str] = []
  for name in (
    raw,
    normalized,
    f"task_{normalized}",
    f"hw_{normalized}",
    f"{category}_{normalized}",
  ):
    if not name:
      continue

    candidate = name if name.endswith(".py") else f"{name}.py"
    if candidate not in names:
      names.append(candidate)

  return names


def resolve_task_file(category: str, task_id: str) -> Path | None:
  task_dir = category_dir(category)
  if not task_dir.exists():
    return None

  for filename in task_candidates(category, task_id):
    candidate = task_dir / filename
    if candidate.exists() and candidate.is_file():
      return candidate

  return None


def has_main_guard(task_file: Path) -> bool:
  try:
    tree = ast.parse(task_file.read_text(encoding="utf-8"))
  except OSError, SyntaxError:
    return False

  for node in tree.body:
    if not isinstance(node, ast.If):
      continue

    test = node.test
    if not isinstance(test, ast.Compare):
      continue
    if len(test.ops) != 1 or not isinstance(test.ops[0], ast.Eq):
      continue
    if len(test.comparators) != 1:
      continue

    left = test.left
    right = test.comparators[0]
    left_is_name = isinstance(left, ast.Name) and left.id == "__name__"
    right_is_name = isinstance(right, ast.Name) and right.id == "__name__"
    left_is_main = isinstance(left, ast.Constant) and left.value == "__main__"
    right_is_main = isinstance(right, ast.Constant) and right.value == "__main__"

    if (left_is_name and right_is_main) or (right_is_name and left_is_main):
      return True

  return False


def run_task(task_file: Path, args: list[str]) -> int:
  main_guard = has_main_guard(task_file)

  old_argv = sys.argv
  sys.argv = [task_file.name, *args]
  try:
    namespace = runpy.run_path(str(task_file), run_name="__main__")
    if not main_guard:
      entrypoint = namespace.get("main")
      if callable(entrypoint):
        entrypoint()
    return 0
  except SystemExit as exc:
    if exc.code is None:
      return 0
    if isinstance(exc.code, int):
      return exc.code

    print(exc.code, file=sys.stderr)
    return 1
  finally:
    sys.argv = old_argv


def run_category(category: str, args: list[str], command_name: str) -> int:
  if len(args) == 1 and args[0] in HELP_ALIASES:
    print_category_usage(command_name, category)
    return 0

  if not args:
    print("Missing task id.", file=sys.stderr)
    print_category_usage(command_name, category)
    return 1

  task_id = args[0]
  if task_id in LIST_ALIASES:
    tasks = available_tasks(category)
    if not tasks:
      print(f"No tasks found in {category}.")
      return 0

    print(f"Available {category} tasks:")
    for task in tasks:
      print(f"- {task}")
    return 0

  task_file = resolve_task_file(category, task_id)
  if task_file is None:
    print(f"Task '{task_id}' not found in '{category}'.", file=sys.stderr)
    tasks = available_tasks(category)
    if tasks:
      print(f"\nAvailable {category} tasks:", file=sys.stderr)
      for task in tasks:
        print(f"- {task}", file=sys.stderr)
    return 1

  return run_task(task_file, args[1:])


def homework(argv: list[str] | None = None) -> int:
  args = argv if argv is not None else sys.argv[1:]
  command_name = Path(sys.argv[0]).name or "homework"
  return run_category("homework", args, command_name)


def junk(argv: list[str] | None = None) -> int:
  args = argv if argv is not None else sys.argv[1:]
  command_name = Path(sys.argv[0]).name or "junk"
  return run_category("junk", args, command_name)


def main(argv: list[str] | None = None) -> int:
  args = argv if argv is not None else sys.argv[1:]

  if len(args) == 1 and args[0] in HELP_ALIASES:
    print_root_usage()
    return 0

  if len(args) < 2:
    print("Missing required arguments.", file=sys.stderr)
    print_root_usage()
    return 1

  category = args[0].lower()
  if category not in VALID_CATEGORIES:
    print(f"Unknown category: {category}", file=sys.stderr)
    print_root_usage()
    return 1

  return run_category(category, args[1:], category)


if __name__ == "__main__":
  raise SystemExit(main())
