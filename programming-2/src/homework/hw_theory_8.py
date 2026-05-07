"""
Idea: výhra:=1, remíza:=0, prohra:=-1. Výsledek stavu když táhneme my je výsledek našeho nejlepšího tahu.
  Výsledek, když tahne oponent, je výsledek jeho nejlepšího tahu z jeho pohledu (čili otáčíme znaménko).
  Použijme tedy negamaxing.

Technická rozhodnutí:
  1. Zploštěme hrací desku do jednodimenzionální posloupnosti.
  2. Volíme předávání desky funkcím místo globálního stavu hlavně kvůli jednoduchosti memoizace.
  3. Kvůli přehlednosti natvrdo nastavme výherní kombinace místo implementace pěti funkcí s magickými čísly.
  4. Vždy kontrolujme "hloupě" celou desku, zda někdo nevyhrál.
    Dá se kontrolovat chytřeji, pomocí pamatování předchozího tahu, ale museli bychom upravovat memoizaci.
    Dále není ani jasné, zda se vyplatí zjišťovat, které kontroly vykonat.
"""

from enum import IntEnum
from functools import cache
from typing import Literal, cast

type Player = Literal["X", "O"]
type Winner = Player | None
type FieldValue = Player | Literal["."]
type Board = tuple[FieldValue, ...]


class GameResult(IntEnum):
  WIN = 1
  DRAW = 0
  LOSS = -1


WINNING_LINES: tuple[tuple[int, int, int], ...] = (
  # řady
  (0, 1, 2),
  (3, 4, 5),
  (6, 7, 8),
  # sloupce
  (0, 3, 6),
  (1, 4, 7),
  (2, 5, 8),
  # diagonály
  (0, 4, 8),
  (2, 4, 6),
)


def find_winners(board: Board) -> set[Player]:
  winners = set()
  for a, b, c in WINNING_LINES:
    if (representant := board[a]) == board[b] == board[c]:
      if representant == ".":
        continue
      winners.add(representant)

  return winners


def check_all(board: Board) -> Winner:
  winners = find_winners(board)
  match len(winners):
    case 0:
      return None
    case 1:
      return next(iter(winners))
    case _:
      raise AssertionError("Nečekaný stav, vítěz není jednoznačný.")


def find_empty_fields(board: Board) -> tuple[int, ...]:
  return tuple(pos for pos in range(9) if board[pos] == ".")


@cache
def evaluate(board: Board, player: Player, /) -> GameResult:  # zakažme kw-argumenty pro kompaktní cache
  opponent = "O" if player == "X" else "X"
  check = check_all(board)
  if check == player:
    return GameResult.WIN
  if check == opponent:
    return GameResult.LOSS

  # invariant: nemáme vítěze

  empty_fields = find_empty_fields(board)
  if not empty_fields:
    return GameResult.DRAW  # dohraná hra bez vítěze

  best = GameResult.LOSS
  for pos in empty_fields:
    opponent_result = evaluate(
      board[:pos] + (player,) + board[pos + 1 :],  # aktuální hráč zahraje na pozici
      opponent,
    )

    result = GameResult(-opponent_result)
    if result == GameResult.WIN:
      return GameResult.WIN  # máme výherní tah => není, co lepšího hledat

    best = max(best, result)

  return best


###
# MAIN
###
rows = list(input().strip()), list(input().strip()), list(input().strip())
start_player = input().strip()
board = (*rows[0], *rows[1], *rows[2])

if not (set(rows[0]) | set(rows[1]) | set(rows[2])).issubset({".", "X", "O"}):
  raise ValueError("Neznámé znaky v popisu stavu.")
if not len(rows[0]) == len(rows[1]) == len(rows[2]) == 3:
  raise ValueError("Neznámý formát stavu.")
if start_player not in ("X", "O"):
  raise ValueError(f"Neznámý hráč `{start_player}`.")
if len(find_winners(cast(Board, board))) >= 2:
  raise ValueError("Neplatný stav hry, vítěz není jednoznačný.")


match evaluate(cast(Board, board), cast(Player, start_player)):
  case GameResult.WIN:
    print("VYHRAJE")
  case GameResult.DRAW:
    print("REMIZUJE")
  case GameResult.LOSS:
    print("PROHRAJE")
