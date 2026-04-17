import datetime

import pytest

from signal_storage._executor import DeleteCommand, GetCommand, ListCommand, PutCommand
from signal_storage._parser import parse
from signal_storage._signal import SignalRangeSpecification

d1 = datetime.datetime(2026, 1, 1, tzinfo=datetime.UTC)
d1_iso = d1.isoformat()
d2 = datetime.datetime(2027, 1, 1, tzinfo=datetime.UTC)
d2_iso = d2.isoformat()
d3 = datetime.datetime(2028, 1, 1, tzinfo=datetime.UTC)
d3_iso = d3.isoformat()


# GET


@pytest.mark.parametrize(
  "query,wanted",
  [
    ("GET signal1", [SignalRangeSpecification("signal1")]),
    ("Get signal1", [SignalRangeSpecification("signal1")]),
    ("get signal1", [SignalRangeSpecification("signal1")]),
    (
      "GET signal1, signal2, signal3",
      [SignalRangeSpecification("signal1"), SignalRangeSpecification("signal2"), SignalRangeSpecification("signal3")],
    ),
    (
      "    GET      signal1,      signal2,     signal3      ",
      [SignalRangeSpecification("signal1"), SignalRangeSpecification("signal2"), SignalRangeSpecification("signal3")],
    ),
    (
      f"GET signal1 FROM {d1_iso} TO {d2_iso}",
      [SignalRangeSpecification("signal1", date_from=d1, date_to=d2)],
    ),
    (
      f"GET signal1 FROM ... TO {d2_iso}",
      [SignalRangeSpecification("signal1", date_from=None, date_to=d2)],
    ),
    (
      f"GET signal1 FROM {d1_iso} TO ...",
      [SignalRangeSpecification("signal1", date_from=d1, date_to=None)],
    ),
    (
      f"GET signal1 FROM {d1_iso} TO {d2_iso}, signal2 FROM {d2_iso} TO {d3_iso}",
      [
        SignalRangeSpecification("signal1", date_from=d1, date_to=d2),
        SignalRangeSpecification("signal2", date_from=d2, date_to=d3),
      ],
    ),
  ],
)
def test_get_successful(query, wanted):
  result = parse(query)
  assert result == GetCommand(wanted=wanted)


@pytest.mark.parametrize(
  "query",
  [
    "GET signal1,",
    "GET signal1 FROM",
    f"GET signal1 FROM {d1_iso}",
    f"GET signal1 FROM {d1_iso} TO",
    f"GET signal1 FROM {d1_iso} TO abcd",
    f"GET signal1 FROM {d1_iso} TO 111",
    f"GET signal1 FROM abcd TO {d1_iso}",
    f"GET signal1 FROM 111 TO {d1_iso}",
    f"GET signal1 FROM {d1_iso} TO {d1_iso}, ",
    "GET signal1 VALUES",
    f"GET signal1 VALUES (({d1_iso}, 15), ({d2_iso}, 10))",
  ],
)
def test_get_failure(query):
  with pytest.raises(SyntaxError):
    parse(query)


# LIST


def test_list_successful():
  assert isinstance(parse("LIST"), ListCommand)


def test_list_case_insensitive():
  assert isinstance(parse("list"), ListCommand)


def test_list_trailing_tokens():
  with pytest.raises(SyntaxError):
    parse("LIST something")


# PUT


@pytest.mark.parametrize(
  "query,expected_batch",
  [
    (
      f"PUT sig1 VALUES (({d1_iso}, 1.0))",
      {"sig1": [(d1, 1.0)]},
    ),
    (
      f"PUT sig1 VALUES (({d1_iso}, 1.0), ({d2_iso}, 2.0))",
      {"sig1": [(d1, 1.0), (d2, 2.0)]},
    ),
    (
      f"PUT sig1 VALUES (({d1_iso}, 1.0)), sig2 VALUES (({d2_iso}, 2.0))",
      {"sig1": [(d1, 1.0)], "sig2": [(d2, 2.0)]},
    ),
    (
      f"PUT sig1 VALUES (({d1_iso}, -3.14))",
      {"sig1": [(d1, -3.14)]},
    ),
  ],
)
def test_put_successful(query, expected_batch):
  result = parse(query)
  assert result == PutCommand(batch=expected_batch)


@pytest.mark.parametrize(
  "query",
  [
    "PUT",
    "PUT sig1",
    "PUT sig1 VALUES",
    "PUT sig1 VALUES (",
    "PUT sig1 VALUES ()",
    f"PUT sig1 VALUES (({d1_iso}))",
    f"PUT sig1 VALUES (({d1_iso}, ))",
    "PUT sig1 VALUES ((, 1.0))",
    f"PUT sig1 VALUES ({d1_iso}, 1.0)",
    f"PUT sig1 VALUES (({d1_iso}, 1.0)",
    f"PUT sig1 VALUES ({d1_iso}, 1.0))",
    f"PUT sig1 VALUES (({d1_iso}, 1.0)),",
    f"PUT sig1 VALUES (({d1_iso}, 1.0)), sig1 VALUES (({d2_iso}, 2.0))",
  ],
)
def test_put_failure(query):
  with pytest.raises(SyntaxError):
    parse(query)


# DELETE


@pytest.mark.parametrize(
  "query,wanted",
  [
    ("DELETE signal1", [SignalRangeSpecification("signal1")]),
    (
      "DELETE signal1, signal2",
      [SignalRangeSpecification("signal1"), SignalRangeSpecification("signal2")],
    ),
    (
      f"DELETE signal1 FROM {d1_iso} TO {d2_iso}",
      [SignalRangeSpecification("signal1", date_from=d1, date_to=d2)],
    ),
    (
      f"DELETE signal1 FROM ... TO {d2_iso}",
      [SignalRangeSpecification("signal1", date_from=None, date_to=d2)],
    ),
    (
      f"DELETE signal1 FROM {d1_iso} TO ...",
      [SignalRangeSpecification("signal1", date_from=d1, date_to=None)],
    ),
  ],
)
def test_delete_successful(query, wanted):
  result = parse(query)
  assert result == DeleteCommand(wanted=wanted)


@pytest.mark.parametrize(
  "query",
  [
    "DELETE",
    "DELETE signal1,",
    "DELETE signal1 FROM",
    f"DELETE signal1 FROM {d1_iso}",
    f"DELETE signal1 FROM {d1_iso} TO",
  ],
)
def test_delete_failure(query):
  with pytest.raises(SyntaxError):
    parse(query)


# Ostatní


@pytest.mark.parametrize(
  "query",
  [
    "",
    "   ",
    "INVALID signal1",
    "123",
    "FROM signal1",
  ],
)
def test_nonsense_queries(query):
  with pytest.raises(SyntaxError):
    parse(query)
