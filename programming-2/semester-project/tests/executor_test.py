import datetime

import pytest

from signal_storage._executor import (
  DeleteSuccessResult,
  FailureResult,
  GetSuccessResult,
  ListSuccessResult,
  PartitionGranularity,
  PutSuccessResult,
  StorageExecutor,
)
from signal_storage._parser import parse


@pytest.fixture
def executor(tmp_path):  # tmp_path zajistí izolaci testů, pro každý běh testu vytvoří složku
  return StorageExecutor(root_folder=tmp_path)


def test_new_signal_starts_at_week_granularity(executor):
  executor.execute(parse("PUT signal1 VALUES ((2026-01-01T00:00:00Z, 1.0))"))
  assert executor._signal_metadata["signal1"] == PartitionGranularity.WEEK


def test_repartition_week_to_day(executor, monkeypatch):
  monkeypatch.setattr(StorageExecutor, "PARTITION_THRESHOLD", 2)  # pro test nastav limit na 2
  # 3 body v týdnu (přes limit), očekáváme přeuspořádání
  executor.execute(
    parse("PUT signal1 VALUES ((2026-01-01T00:00:00Z, 1.0),(2026-01-01T01:00:00Z, 2.0),(2026-01-01T02:00:00Z, 3.0))")
  )
  assert executor._signal_metadata["signal1"] == PartitionGranularity.DAY

  # zkontroluj data
  get_result = executor.execute(parse("GET signal1"))
  assert isinstance(get_result, GetSuccessResult)
  assert get_result.data["signal1"].height == 3
  assert sorted(get_result.data["signal1"]["time"].to_list()) == [
    datetime.datetime(2026, 1, 1, hour, tzinfo=datetime.UTC) for hour in [0, 1, 2]
  ]
  assert sorted(get_result.data["signal1"]["value"].to_list()) == [1.0, 2.0, 3.0]


def test_repartition_granular_does_not_throw_error(executor, monkeypatch):
  monkeypatch.setattr(StorageExecutor, "PARTITION_THRESHOLD", 1)
  # Donuťme executor provést přeuspořádání WEEK => DAY => HOUR
  for i in range(3):
    executor.execute(parse(f"PUT signal1 VALUES ((2026-01-01T00:00:0{i}Z, {i}))"))
  assert executor._signal_metadata["signal1"] == PartitionGranularity.HOUR

  executor.execute(
    parse("PUT signal1 VALUES ((2026-01-01T00:00:10Z, 10.0),(2026-01-01T00:00:11Z, 11.0),(2026-01-01T00:00:12Z, 12.0))")
  )
  # Další překročení limitu nesmí ani selhat, ani změnit granularitu
  assert executor._signal_metadata["signal1"] == PartitionGranularity.HOUR

  get_result = executor.execute(parse("GET signal1"))
  assert isinstance(get_result, GetSuccessResult)
  assert get_result.data["signal1"].height == 6


def test_list_empty(executor):
  result = executor.execute(parse("LIST"))
  assert isinstance(result, ListSuccessResult)
  assert result.signal_ids == []


def test_list_after_puts(executor):
  executor.execute(
    parse("PUT signalA VALUES ((2026-01-01T00:00:00Z, 1.0)), signalB VALUES ((2026-01-01T00:00:00Z, 2.0))")
  )
  result = executor.execute(parse("LIST"))
  assert isinstance(result, ListSuccessResult)
  assert sorted(result.signal_ids) == ["signalA", "signalB"]


def test_put_then_get(executor):
  put_result = executor.execute(parse("PUT signal1 VALUES ((2026-01-01T00:00:00Z, 42.0))"))
  assert isinstance(put_result, PutSuccessResult)

  get_result = executor.execute(parse("GET signal1"))
  assert isinstance(get_result, GetSuccessResult)
  assert get_result.data["signal1"].height == 1
  assert get_result.data["signal1"]["time"][0] == datetime.datetime(2026, 1, 1, tzinfo=datetime.UTC)
  assert get_result.data["signal1"]["value"][0] == 42.0


def test_put_multiple_points(executor):
  executor.execute(
    parse("PUT signal1 VALUES ((2026-01-01T00:00:00Z, 1.0), (2026-01-02T00:00:00Z, 2.0), (2026-01-03T00:00:00Z, 3.0))")
  )
  get_result = executor.execute(parse("GET signal1"))
  assert isinstance(get_result, GetSuccessResult)
  assert get_result.data["signal1"].height == 3


def test_put_multiple_signals(executor):
  executor.execute(
    parse("PUT signal1 VALUES ((2026-01-01T00:00:00Z, 1.0)), signal2 VALUES ((2026-01-01T00:00:00Z, 2.0))")
  )
  get_result = executor.execute(parse("GET signal1, signal2"))
  assert isinstance(get_result, GetSuccessResult)
  assert get_result.data["signal1"]["value"][0] == 1.0
  assert get_result.data["signal2"]["value"][0] == 2.0


def test_delete_entire_signal(executor):
  executor.execute(parse("PUT signal1 VALUES ((2026-01-01T00:00:00Z, 1.0))"))
  delete_result = executor.execute(parse("DELETE signal1"))
  assert isinstance(delete_result, DeleteSuccessResult)

  get_result = executor.execute(parse("GET signal1"))
  assert isinstance(get_result, FailureResult)


def test_delete_with_date_range(executor):
  executor.execute(
    parse("PUT signal1 VALUES ((2026-01-01T00:00:00Z, 1.0),(2026-01-02T00:00:00Z, 2.0),(2026-01-03T00:00:00Z, 3.0))")
  )
  executor.execute(parse("DELETE signal1 FROM 2026-01-02T00:00:00Z TO 2026-01-02T00:00:00Z"))
  get_result = executor.execute(parse("GET signal1"))
  assert isinstance(get_result, GetSuccessResult)
  assert get_result.data["signal1"].height == 2
  values = get_result.data["signal1"]["value"].to_list()
  assert 2.0 not in values
  assert 1.0 in values
  assert 3.0 in values
