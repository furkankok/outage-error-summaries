# outage-error-summaries

A small Python command-line tool that reads an outage log CSV and builds an error summary for each outage.

- Only `ERROR` and `FATAL` rows are counted. `WARN` and `INFO` rows are ignored.
- Rows are grouped by `outage_id`, then by `service` inside each outage.
- Each service gets one `error_count` and its `first_error_time`.
- Inside each outage, services are ordered by their first error time.
- The result is written as one Markdown table per outage.

## Requirements

- [uv](https://docs.astral.sh/uv/)
- Python 3.14 (uv installs it if missing)

## Run

Run from the repository root. The default paths are relative to it.

```sh
uv run outage-error-summaries
```

This reads `data/replayed_outage_error_logs.csv` and writes `output/outage_summaries.md`. The file is overwritten on every run.

Use another input file or output path:

```sh
uv run outage-error-summaries path/to/logs.csv -o path/to/report.md
```

The input CSV needs at least the `outage_id`, `timestamp`, `service` and `severity` columns. Outage ids and service names are read from the data, so any number of outages works.

## Project layout

```
data/replayed_outage_error_logs.csv     input log data
src/outage_error_summaries/__init__.py  command-line entry point
src/outage_error_summaries/summary.py   filtering, grouping, ordering, Markdown output
output/outage_summaries.md              generated report
```

## Prompt

The prompt I used for the summaries:

> Read the Replayed Outage Error Logs CSV in the data folder. Cover every outage_id in the file (OUT-01 to OUT-06), not just one or two. Count only ERROR and FATAL rows and ignore WARN and INFO. First group by outage_id, then by service inside each outage. Give each service one error_count and order the services by their first error time. Write one summary table per outage to output/outage_summaries.md, update summary.py to match, then commit and push to the repo.

## Ordering

Inside each outage, services are ordered by their first error time (the first `ERROR` or `FATAL` row). That shows which service failed first.

## What I checked

The original CSV has 179 rows, and all of them are `OUT-01`. So the output has one table: see [output/outage_summaries.md](output/outage_summaries.md). The script still groups by `outage_id`, so a file with more outages gives one table per outage.

## What was done

1. **First count.** Read the CSV, kept only `ERROR` and `FATAL` rows, counted them per service and ordered the services by first error time.
2. **Project setup.** Created this uv Python package, moved the CSV into `data/` with a name without spaces, and turned the count into the `outage-error-summaries` command.
3. **Per-outage report.** Changed the grouping to outage first, then service. The tool now writes one Markdown table per outage to `output/outage_summaries.md`. The logic was also checked on a small two-outage test file.
4. **Documentation.** Added this README.
