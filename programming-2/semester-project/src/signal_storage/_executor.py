"""
Vrstva pro vykonání příkazů
"""

import datetime
import json
import pathlib
import shutil
from dataclasses import dataclass
from enum import StrEnum

import polars as pl
import pyarrow.parquet as pq

from signal_storage._signal import SIGNAL_SCHEMA, SignalRangeSpecification, SignalValues, SignalValuesRaw, empty_signal


class StorageError(Exception): ...


class PartitionGranularity(StrEnum):
  WEEK = "week"
  DAY = "day"
  HOUR = "hour"


@dataclass(frozen=True, slots=True)
class Command: ...


@dataclass(frozen=True, slots=True)
class GetCommand(Command):
  wanted: list[SignalRangeSpecification]


@dataclass(frozen=True, slots=True)
class ListCommand(Command): ...


@dataclass(frozen=True, slots=True)
class PutCommand(Command):
  batch: dict[str, SignalValuesRaw]
  """dict[signal_id, values]"""


@dataclass(frozen=True, slots=True)
class DeleteCommand(Command):
  wanted: list[SignalRangeSpecification]


@dataclass(frozen=True, slots=True)
class CommandResult:
  message: str


@dataclass(frozen=True, slots=True)
class SuccessResult(CommandResult): ...


@dataclass(frozen=True, slots=True)
class FailureResult(CommandResult): ...


@dataclass(frozen=True, slots=True)
class GetSuccessResult(CommandResult):
  data: dict[str, SignalValues]


@dataclass(frozen=True, slots=True)
class ListSuccessResult(CommandResult):
  signal_ids: list[str]


@dataclass(frozen=True, slots=True)
class PutSuccessResult(CommandResult): ...


@dataclass(frozen=True, slots=True)
class DeleteSuccessResult(CommandResult): ...


class StorageExecutor:
  """Singleton služba pro vykonávání příkazů."""

  PARTITION_THRESHOLD = 10_000
  DEFAULT_GRANULARITY = PartitionGranularity.WEEK

  def __init__(self, *, root_folder: pathlib.Path) -> None:
    self._root_dir = root_folder
    self._root_dir_resolved = self._root_dir.resolve()
    self._signal_metadata: dict[str, PartitionGranularity] = self._get_or_create_metadata()

  def execute(self, command: Command) -> CommandResult:
    try:
      match command:
        case GetCommand():
          return self._get(command.wanted)
        case ListCommand():
          return self._list()
        case PutCommand():
          return self._put(command.batch)
        case DeleteCommand():
          return self._delete(command.wanted)
        case _:
          raise RuntimeError(f"Invalid command provided: {type(command).__name__}")
    except StorageError as error:
      return FailureResult(message=f"Failed with error: {str(error)}")

  def _metadata_save(self) -> None:
    json.dump(self._signal_metadata, (self._root_dir / "metadata.json").open("w", encoding="utf-8"))

  def _metadata_add_signal(self, signal_id: str) -> None:
    self._signal_metadata[signal_id] = self.DEFAULT_GRANULARITY
    self._metadata_save()

  def _metadata_delete_signal(self, signal_id: str) -> None:
    del self._signal_metadata[signal_id]
    self._metadata_save()

  def _metadata_update_granularity(self, *, signal_id: str, new_granularity: PartitionGranularity) -> None:
    self._signal_metadata[signal_id] = new_granularity
    self._metadata_save()

  def _get_or_create_metadata(self) -> dict[str, PartitionGranularity]:
    path = self._root_dir / "metadata.json"
    if not path.exists():
      path.write_text("{}")
      return {}

    metadata_raw = json.load(path.open(encoding="utf-8"))
    return {key: PartitionGranularity(value) for key, value in metadata_raw.items()}

  def _ensure_signal_dir(self, signal_id: str, *, create: bool = False) -> pathlib.Path:
    signal_dir = self._root_dir / signal_id
    if not signal_dir.resolve().is_relative_to(self._root_dir_resolved):  # Zabrání escapu typu: "../../sensitive"
      raise StorageError("Path escape attempt detected.")
    if not signal_dir.exists():
      if not create:
        raise StorageError(f"Signal `{signal_id}` does not exist.")
      signal_dir.mkdir()
      self._metadata_add_signal(signal_id)

    return signal_dir

  def _get(self, wanted: list[SignalRangeSpecification]) -> GetSuccessResult:
    data: dict[str, SignalValues] = {}
    for spec in wanted:
      signal_dir = self._ensure_signal_dir(spec.signal_id)

      try:
        signal = pl.scan_parquet(signal_dir, hive_partitioning=True)
      except Exception:
        data[spec.signal_id] = empty_signal()
        continue

      if spec.date_from is not None:
        signal = signal.filter(pl.col("time") >= spec.date_from)
      if spec.date_to is not None:
        signal = signal.filter(pl.col("time") <= spec.date_to)

      data[spec.signal_id] = signal.drop("partition").collect()

    row_count = sum(signal.height for signal in data.values())
    return GetSuccessResult(data=data, message=f"{row_count} rows fetched.")

  def _list(self) -> ListSuccessResult:
    return ListSuccessResult(
      signal_ids=list(self._signal_metadata.keys()), message=f"{len(self._signal_metadata)} signals listed."
    )

  def _partition_key(self, granularity: PartitionGranularity) -> pl.Expr:
    match granularity:
      case PartitionGranularity.WEEK:
        return pl.col("time").dt.truncate("1w").cast(pl.Utf8).alias("partition")
      case PartitionGranularity.DAY:
        return pl.col("time").dt.truncate("1d").cast(pl.Utf8).alias("partition")
      case PartitionGranularity.HOUR:
        return pl.col("time").dt.truncate("1h").cast(pl.Utf8).alias("partition")

  def _dataframe_from_values_raw(self, values_raw: SignalValuesRaw) -> SignalValues:
    return pl.from_records(values_raw, orient="row", schema=SIGNAL_SCHEMA)

  def _finer_granularity(self, granularity: PartitionGranularity) -> PartitionGranularity | None:
    match granularity:
      case PartitionGranularity.WEEK:
        return PartitionGranularity.DAY
      case PartitionGranularity.DAY:
        return PartitionGranularity.HOUR
      case PartitionGranularity.HOUR:
        return None  # už jsme na nejjemnější granularitě

  def _repartition_signal(
    self, *, signal_id: str, signal_dir: pathlib.Path, new_granularity: PartitionGranularity
  ) -> None:
    try:
      all_data = pl.scan_parquet(signal_dir, hive_partitioning=True).drop("partition").collect()
    except Exception:
      all_data = empty_signal()

    for child in signal_dir.iterdir():
      if child.is_dir():
        shutil.rmtree(child)

    self._metadata_update_granularity(signal_id=signal_id, new_granularity=new_granularity)

    if all_data.height == 0:
      return

    repartitioned = all_data.with_columns(self._partition_key(new_granularity))
    pq.write_to_dataset(
      repartitioned.to_arrow(),
      root_path=signal_dir,
      partition_cols=["partition"],
    )

  def _put(self, batch: dict[str, SignalValuesRaw]) -> PutSuccessResult:
    row_count = 0
    for signal_id, values_raw in batch.items():
      incoming = self._dataframe_from_values_raw(values_raw)
      row_count += incoming.height

      needs_repartition = False
      signal_dir = self._ensure_signal_dir(signal_id, create=True)
      granularity = self._signal_metadata[signal_id]
      incoming_partitioned = incoming.with_columns(self._partition_key(granularity)).group_by("partition")
      for partition_path, partition_content in incoming_partitioned:
        partition_values = partition_content.drop("partition")
        try:
          existing = (
            pl.scan_parquet(signal_dir, hive_partitioning=True)
            .filter(pl.col("partition") == datetime.datetime.fromisoformat(partition_path[0]))
            .drop("partition")
            .collect()
          )
        except Exception:
          existing = empty_signal()

        merged = existing.update(partition_values.sort("time"), on="time", how="full")
        needs_repartition = needs_repartition or merged.height > self.PARTITION_THRESHOLD

        merged_partitioned = merged.with_columns(self._partition_key(granularity))

        pq.write_to_dataset(
          merged_partitioned.to_arrow(),
          root_path=signal_dir,
          partition_cols=["partition"],
          existing_data_behavior="delete_matching",
        )

      if needs_repartition:
        new_granularity = self._finer_granularity(granularity)
        if new_granularity is not None:
          self._repartition_signal(signal_id=signal_id, signal_dir=signal_dir, new_granularity=new_granularity)

    return PutSuccessResult(message=f"Upserted {row_count} rows.")

  def _delete(self, wanted: list[SignalRangeSpecification]) -> DeleteSuccessResult:
    for spec in wanted:
      signal_dir = self._ensure_signal_dir(spec.signal_id)

      if spec.date_from is None and spec.date_to is None:
        shutil.rmtree(signal_dir)  # nelze použít path.unlink(), protože nemaže složku včetně obsahu
        self._metadata_delete_signal(spec.signal_id)
        continue

      try:
        signal = pl.scan_parquet(signal_dir, hive_partitioning=True)
      except Exception:
        continue  # signál je prázdný, přeskoč

      discard = pl.lit(True)
      if spec.date_from is not None:
        discard &= pl.col("time") >= spec.date_from
      if spec.date_to is not None:
        discard &= pl.col("time") <= spec.date_to

      filtered = signal.filter(~discard).collect()

      for child in signal_dir.iterdir():  # smaž všechen obsah před vložením nového
        if child.is_dir():
          shutil.rmtree(child)

      pq.write_to_dataset(
        filtered.to_arrow(),
        root_path=signal_dir,
        partition_cols=["partition"],
      )

    return DeleteSuccessResult("Deletion successful.")
