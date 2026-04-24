import argparse
import sys
from pathlib import Path
from typing import cast

from flask import Flask, request

from signal_storage._executor import FailureResult, GetSuccessResult, ListSuccessResult, StorageExecutor
from signal_storage._parser import parse
from signal_storage._signal import signal_batch_serialize_json

__version__ = "0.2.0"


def parse_configuration(argv: list[str]) -> argparse.Namespace:
  parser = argparse.ArgumentParser(prog="signal-storage")
  parser.add_argument(
    "--path", required=True, type=Path, help="Cesta do složky, kterou program využije jako kořenovou složku uložiště."
  )
  parser.add_argument("--host", type=str, default="localhost", help="Host, kde má být puštěn server.")
  parser.add_argument("--port", type=int, default=8080, help="Port, kde má být puštěn server.")
  parser.add_argument(
    "--production",
    default=False,
    action="store_true",
    help="Parametr pro zapnutí programu v produkčním režimu.",
  )

  configuration = parser.parse_args(args=argv)
  cast(Path, configuration.path).mkdir(parents=True, exist_ok=True)

  return configuration


def main():
  configuration = parse_configuration(sys.argv[1:])

  app = Flask(__name__)
  storage_executor = StorageExecutor(root_folder=configuration.path)

  @app.route("/status", methods=["GET"])
  def _status():
    return {"name": "signal-storage", "version": __version__}

  @app.route("/query", methods=["POST"])
  def _query():
    try:
      command = parse(request.get_data(as_text=True))
    except SyntaxError as error:
      return {"message": f"Syntax error: {str(error)}"}, 400

    match result := storage_executor.execute(command):
      case FailureResult():
        return {"message": result.message}, 500
      case GetSuccessResult():
        return {"message": result.message, "data": signal_batch_serialize_json(result.data)}, 200
      case ListSuccessResult():
        return {"message": result.message, "signal_ids": result.signal_ids}, 200
      case _:
        return {"message": result.message}, 200

  app.run(host=configuration.host, port=configuration.port, debug=not configuration.production)


if __name__ == "__main__":
  main()
# 67
