# outage-error-summaries

Reads an outage log CSV and builds an error summary for each outage.

- Only `ERROR` and `FATAL` rows are counted. `WARN` and `INFO` rows are ignored.
- Rows are grouped by `outage_id`, then by `service` inside each outage.
- Each service gets one `error_count` and its `first_error_time`.
- Services are ordered by their first error time.

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

The input CSV needs at least the `outage_id`, `timestamp`, `service` and `severity` columns.

## Result

The bundled CSV contains only one outage, `OUT-01`, despite its original "Six Outages" name. The tool handles any number of outages in the input.

See [output/outage_summaries.md](output/outage_summaries.md) for the current report.
