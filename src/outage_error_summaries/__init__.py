import argparse
from pathlib import Path

from outage_error_summaries.summary import read_logs, summarize, write_summary

DEFAULT_INPUT = Path("data/replayed_outage_error_logs.csv")
DEFAULT_OUTPUT = Path("output/service_error_counts.csv")


def main() -> None:
    parser = argparse.ArgumentParser(prog="outage-error-summaries")
    parser.add_argument("input", nargs="?", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    summaries = summarize(read_logs(args.input))
    write_summary(args.output, summaries)

    for item in summaries:
        print(f"{item.service}\t{item.error_count}\t{item.first_error_time}")
    print(f"total\t{sum(item.error_count for item in summaries)}")
