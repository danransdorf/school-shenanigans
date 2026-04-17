import datetime
from dataclasses import dataclass

import polars as pl

type SignalValues = pl.DataFrame
type SignalValuesRaw = list[tuple[datetime.datetime, float]]

SIGNAL_SCHEMA = {"time": pl.Datetime("us", "UTC"), "value": pl.Float64}


@dataclass(frozen=True, slots=True)
class SignalRangeSpecification:
  signal_id: str
  date_from: datetime.datetime | None = None
  date_to: datetime.datetime | None = None


def signal_values_serialize_json(signal: SignalValues) -> dict:
  if 0 == signal.height:
    return {}

  dicts = signal.with_columns(
    time=pl.col("time").dt.to_string("iso:strict"), value=pl.col("value").cast(pl.String)
  ).to_dicts()
  time_value = {}
  for d in dicts:
    time_value[d["time"]] = d["value"]
  return time_value


def signal_batch_serialize_json(batch: dict[str, SignalValues]) -> dict:
  return {identifier: signal_values_serialize_json(signal) for identifier, signal in batch.items()}


def empty_signal() -> SignalValues:
  return pl.DataFrame(schema=SIGNAL_SCHEMA)
