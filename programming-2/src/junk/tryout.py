import sys


def main() -> None:
  print("junk/tryout.py")
  if len(sys.argv) > 1:
    print("args:", ", ".join(sys.argv[1:]))


if __name__ == "__main__":
  main()
