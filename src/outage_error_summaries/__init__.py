import argparse
from pathlib import Path

from outage_error_summaries.summary import read_logs, summarize, write_markdown

DEFAULT_INPUT = Path("data/replayed_outage_error_logs.csv")
DEFAULT_OUTPUT = Path("output/outage_summaries.md")


def main() -> None:
    parser = argparse.ArgumentParser(prog="outage-error-summaries")
    parser.add_argument("input", nargs="?", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    summaries = summarize(read_logs(args.input))
    write_markdown(args.output, summaries)

    for outage in summaries:
        print(f"{outage.outage_id}\t{len(outage.services)} services\t{outage.total} errors")
