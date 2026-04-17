"""
Vrstva pro převod textových dotazů do interního příkazu.
---
Idea: Tokenizace vstupu a následný LL-parsing do interního příkazu.

Ukázka toku:
  Query          -- "GET signal1 FROM 2025-01 TO ..."
    ↓  `lex()`
  Token stream   -- [GetKW, Name(signal1), FromKW, Timestamp(2025-01), ToKW, Ellipsis]
    ↓  `Parser.parse_command()`
  Příkaz         -- Get("signal1", from=2025-01, to=None)

Užitečné odkazy:
- Lexical Analysis: https://en.wikipedia.org/wiki/Lexical_analysis
- LL-parser: https://en.wikipedia.org/wiki/LL_parser
"""

__all__ = ["parse"]

import datetime
from dataclasses import dataclass

from signal_storage._executor import Command, DeleteCommand, GetCommand, ListCommand, PutCommand
from signal_storage._signal import SignalRangeSpecification, SignalValuesRaw


@dataclass(frozen=True, slots=True)
class Token: ...


@dataclass(frozen=True, slots=True)
class Number(Token):
  value: float


@dataclass(frozen=True, slots=True)
class Name(Token):
  value: str


@dataclass(frozen=True, slots=True)
class Timestamp(Token):
  value: datetime.datetime


class EllipsisToken(Token): ...


############
# Special Characters
############
class SpecialCharacter(Token): ...


class ParenOpen(SpecialCharacter): ...


class ParenClose(SpecialCharacter): ...


class Comma(SpecialCharacter): ...


SPECIAL_CHARACTERS: dict[str, type[SpecialCharacter]] = {
  "(": ParenOpen,
  ")": ParenClose,
  ",": Comma,
}


##########
# Keywords
##########
class Keyword(Token): ...


class GetKW(Keyword): ...


class ListKW(Keyword): ...


class PutKW(Keyword): ...


class DeleteKW(Keyword): ...


class ValuesKW(Keyword): ...


class FromKW(Keyword): ...


class ToKW(Keyword): ...


KEYWORDS: dict[str, type[Keyword]] = {
  "get": GetKW,
  "list": ListKW,
  "put": PutKW,
  "delete": DeleteKW,
  "values": ValuesKW,
  "from": FromKW,
  "to": ToKW,
}


def _is_word_character(char: str) -> bool:
  return char.isalnum() or char == "_"


def _is_numeric_char(char: str) -> bool:
  EXTRA_CHARS = "+-.:TZ"  # Znaky z ISO8601, zároveň pokrývá znaménko mínus a desetinnou tečku.
  return char.isdigit() or char in EXTRA_CHARS


def _lex_number_or_timestamp(query: str, start: int, length: int) -> tuple[Token, int]:
  end_exclusive = start
  while end_exclusive < length and _is_numeric_char(query[end_exclusive]):
    end_exclusive += 1

  raw = query[start:end_exclusive]

  try:
    value = datetime.datetime.fromisoformat(raw)
    if value.tzinfo is None:
      value = value.replace(tzinfo=datetime.UTC)
    else:
      value = value.astimezone(datetime.UTC)
    return Timestamp(value=value), end_exclusive
  except ValueError:
    pass

  try:
    return Number(value=float(raw)), end_exclusive
  except ValueError as error:
    raise SyntaxError(f"Invalid number or ISO datetime `{raw}` at position {start}") from error


def lex(query: str) -> list[Token]:
  tokens: list[Token] = []

  idx = 0
  query_length = len(query)
  while idx < query_length:
    if query[idx].isdigit() or query[idx] == "-":
      token, idx = _lex_number_or_timestamp(query, idx, query_length)
      tokens.append(token)
      continue

    if _is_word_character(query[idx]):
      word_start, word_end_exclusive = idx, idx
      while word_end_exclusive < query_length and _is_word_character(query[word_end_exclusive]):
        word_end_exclusive += 1

      word = query[word_start:word_end_exclusive]
      idx = word_end_exclusive

      keyword_type = KEYWORDS.get(word.lower())
      if keyword_type is not None:
        tokens.append(keyword_type())
        continue

      tokens.append(Name(value=word))
      continue

    special_character = SPECIAL_CHARACTERS.get(query[idx].lower())
    if special_character is not None:
      tokens.append(special_character())
      idx += 1
      continue

    if query[idx] == ".":
      if query[idx : idx + 3] != "...":
        raise SyntaxError(
          f"Unexpected characters following `.` at position: {idx}, expected: `...`, got: `{query[idx : idx + 3]}`"
        )
      tokens.append(EllipsisToken())
      idx += 3
      continue

    if query[idx].isspace():
      idx += 1
      continue

    raise SyntaxError(f"Unexpected character `{query[idx]}` at position: {idx}")

  return tokens


class Parser:
  """Implementace LL-parseru převod tokenů do příkazu."""

  def __init__(self, tokens: list[Token]) -> None:
    self._tokens = tokens
    self._position = 0

  @property
  def position(self) -> int:
    return self._position

  def _peek_next(self) -> Token | None:
    if self._position < len(self._tokens):
      return self._tokens[self._position]
    return None

  def _advance(self) -> Token:
    if self._position >= len(self._tokens):
      raise SyntaxError("Unexpected end of query.")
    token = self._tokens[self._position]
    self._position += 1
    return token

  def _assert_advance[T: Token](self, expected_type: type[T]) -> T:
    token = self._advance()
    if not isinstance(token, expected_type):
      raise SyntaxError(f"Expected {expected_type}, got {token}.")

    return token

  def _parse_from_to(self) -> tuple[datetime.datetime | None, datetime.datetime | None]:
    date_from: datetime.datetime | None
    date_to: datetime.datetime | None

    self._assert_advance(FromKW)
    match self._advance():
      case Timestamp() as timestamp:
        date_from = timestamp.value
      case EllipsisToken():
        date_from = None
      case unexpected:
        raise SyntaxError(f"Unexpected token `{unexpected}` found after FROM keyword.")

    self._assert_advance(ToKW)
    match self._advance():
      case Timestamp() as timestamp:
        date_to = timestamp.value
      case EllipsisToken():
        date_to = None
      case unexpected:
        raise SyntaxError(f"Unexpected token `{unexpected}` found after TO keyword.")

    return date_from, date_to

  def _parse_signal_range_specifications(self) -> list[SignalRangeSpecification]:
    specifications: list[SignalRangeSpecification] = []
    while True:
      signal_id = self._assert_advance(Name).value
      match self._peek_next():
        case None | Comma():
          specifications.append(SignalRangeSpecification(signal_id=signal_id))
        case FromKW():
          date_from, date_to = self._parse_from_to()
          specifications.append(SignalRangeSpecification(signal_id=signal_id, date_from=date_from, date_to=date_to))
          # bez _advance(), protože pozice je posunuta díky _parse_from_to()
        case unexpected:
          raise SyntaxError(f"Unexpected usage of {unexpected}, expecting `FROM` or `,` after specifying signal ID.")

      match self._peek_next():
        case None:
          break
        case Comma():
          self._advance()
          continue
        case unexpected:
          raise SyntaxError(f"Unexpected token {unexpected}, separate your statements with commas.")
    return specifications

  def _parse_values(self) -> SignalValuesRaw:
    self._assert_advance(ValuesKW)
    self._assert_advance(ParenOpen)
    if isinstance(self._peek_next(), ParenClose):
      raise SyntaxError("No values provided in VALUES (..) statement.")

    signal_values: SignalValuesRaw = []
    while True:
      match self._peek_next():
        case None:
          raise SyntaxError("Values opening parenthesis was left open.")  # velká závorka neukončena
        case ParenClose():
          self._advance()
          break  # velká závorka ukončena
        case Comma():
          self._advance()
          continue
        case ParenOpen():
          self._advance()
          time = self._assert_advance(Timestamp).value
          self._assert_advance(Comma)
          value = self._assert_advance(Number).value
          self._assert_advance(ParenClose)

          signal_values.append((time, value))
          continue
        case unexpected:
          raise SyntaxError(
            f"Unexpected token {unexpected} in Values specification, expected tuples ((time, value), (time,value), ...)"
          )

    return signal_values

  def _parse_get(self) -> GetCommand:
    self._assert_advance(GetKW)
    return GetCommand(wanted=self._parse_signal_range_specifications())

  def _parse_put(self) -> PutCommand:
    self._assert_advance(PutKW)
    batch: dict[str, SignalValuesRaw] = {}
    while True:
      signal_id = self._assert_advance(Name).value
      if signal_id in batch:
        raise SyntaxError(
          f"Cannot specify a signal multiple times in a PUT command, found multiple occurences of `{signal_id}`"
        )
      batch[signal_id] = self._parse_values()

      match self._peek_next():
        case None:
          break
        case Comma():
          self._advance()
          continue
        case unexpected:
          raise SyntaxError(f"Unexpected token `{unexpected}` found among values specification.")

    return PutCommand(batch)

  def _parse_delete(self) -> DeleteCommand:
    self._assert_advance(DeleteKW)
    return DeleteCommand(wanted=self._parse_signal_range_specifications())

  def parse_command(self) -> Command:
    match self._peek_next():
      case GetKW():
        return self._parse_get()
      case ListKW():
        self._advance()
        return ListCommand()
      case PutKW():
        return self._parse_put()
      case DeleteKW():
        return self._parse_delete()
      case None:
        raise SyntaxError("No valid tokens found.")
      case unexpected:
        raise SyntaxError(f"Unexpected token {unexpected} at the beginning.")


def parse(query: str) -> Command:
  tokens = lex(query)
  parser = Parser(tokens)
  command = parser.parse_command()
  if parser.position < len(tokens):
    raise SyntaxError(f"Unexpected token {tokens[parser.position]} after complete command.")

  return command
