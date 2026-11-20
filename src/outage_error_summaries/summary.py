import csv
from dataclasses import dataclass
from pathlib import Path

ERROR_SEVERITIES = frozenset({"ERROR", "FATAL"})


@dataclass
class ServiceErrors:
    service: str
    error_count: int
    first_error_time: str


@dataclass
class OutageSummary:
    outage_id: str
    services: list[ServiceErrors]

    @property
    def total(self) -> int:
        return sum(item.error_count for item in self.services)


def summarize(rows: list[dict[str, str]]) -> list[OutageSummary]:
    grouped: dict[str, dict[str, ServiceErrors]] = {}
    for row in rows:
        if row["severity"].strip().upper() not in ERROR_SEVERITIES:
            continue
        outage_id = row["outage_id"].strip()
        service = row["service"].strip()
        timestamp = row["timestamp"].strip()
        services = grouped.setdefault(outage_id, {})
        current = services.get(service)
        if current is None:
            services[service] = ServiceErrors(service, 1, timestamp)
            continue
        current.error_count += 1
        current.first_error_time = min(current.first_error_time, timestamp)
    return [
        OutageSummary(
            outage_id,
            sorted(services.values(), key=lambda item: (item.first_error_time, item.service)),
        )
        for outage_id, services in sorted(grouped.items())
    ]


def read_logs(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def render_markdown(summaries: list[OutageSummary]) -> str:
    lines = ["# Outage Error Summaries", ""]
    for outage in summaries:
        lines += [
            f"## {outage.outage_id}",
            "",
            "| # | service | error_count | first_error_time |",
            "|---|---|---|---|",
        ]
        for index, item in enumerate(outage.services, start=1):
            lines.append(f"| {index} | {item.service} | {item.error_count} | {item.first_error_time} |")
        lines += ["", f"Total: {outage.total}", ""]
    return "\n".join(lines)


def write_markdown(path: Path, summaries: list[OutageSummary]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(summaries), encoding="utf-8")
