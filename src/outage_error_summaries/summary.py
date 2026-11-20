import csv
from dataclasses import dataclass
from pathlib import Path

ERROR_SEVERITIES = frozenset({"ERROR", "FATAL"})


@dataclass
class ServiceErrors:
    service: str
    error_count: int
    first_error_time: str


def summarize(rows: list[dict[str, str]]) -> list[ServiceErrors]:
    summaries: dict[str, ServiceErrors] = {}
    for row in rows:
        if row["severity"].strip().upper() not in ERROR_SEVERITIES:
            continue
        service = row["service"].strip()
        timestamp = row["timestamp"].strip()
        current = summaries.get(service)
        if current is None:
            summaries[service] = ServiceErrors(service, 1, timestamp)
            continue
        current.error_count += 1
        current.first_error_time = min(current.first_error_time, timestamp)
    return sorted(summaries.values(), key=lambda item: (item.first_error_time, item.service))


def read_logs(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_summary(path: Path, summaries: list[ServiceErrors]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["service", "error_count", "first_error_time"])
        for item in summaries:
            writer.writerow([item.service, item.error_count, item.first_error_time])
