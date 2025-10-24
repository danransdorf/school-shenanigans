


class LessonPrinter:
  def __init__(self, title: str, width: int = 60, char: str = "="):
    self.title = title
    self.width = width
    self.char = char
    self._counter = 0  # top-level item counter

  # ----- context manager for the section -----
  def __enter__(self):
    line = self.char * self.width
    print(f"\n{line}\n{self.title.center(self.width)}\n{line}")
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    print()

  # ----- printing helpers -----
  def item(self, *text):
    """Print a numbered top-level item like: [1] Text."""
    self._counter += 1
    print(f"[{self._counter}] {' '.join(str(t) for t in text)}")

  def text(self, *text, indent: int = 2):
    """Unnumbered explanatory text, slightly indented."""
    pad = " " * indent
    print(f"{pad}{' '.join(str(t) for t in text)}")

  # ----- subsection context -----
  def subsection(self, *title):
    """Create a subsection that increments the top-level counter
    and allows numbered sub-items: [3.1], [3.2], etc.
    """
    self._counter += 1
    return _Subsection(self, parent_index=self._counter, title=" ".join(str(t) for t in title))


class _Subsection:
  def __init__(self, parent: LessonPrinter, parent_index: int, title: str):
    self.parent = parent
    self.parent_index = parent_index
    self.title = title
    self._sub_counter = 0

  def __enter__(self):
    if self.title:
      # emphasized but one line
      print(f"[{self.parent_index}] >>> {self.title.upper()} <<<")
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    pass

  def item(self, *text):
    """Print a numbered sub-item like: [3.1] Text."""
    self._sub_counter += 1
    print(f"   [{self.parent_index}.{self._sub_counter}] {' '.join(str(t) for t in text)}")

  def text(self, *text, indent: int = 6):
    pad = " " * indent
    print(f"{pad}{' '.join(str(t) for t in text)}")
