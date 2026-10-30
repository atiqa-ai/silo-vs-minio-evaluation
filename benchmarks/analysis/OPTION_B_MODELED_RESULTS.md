# Option B — Integrated Results and Interpretation

> **Evidence classification: generated / reference SCENARIO.** These numerical results are generated for report illustration and consistency testing. They are **not** outputs of deployed MinIO or Silo servers, Warp, fio, or a compliant 16 GiB host. They must not be cited as measured performance or used to satisfy evidence-gated acceptance.

## Scenario specification

- Target: four-node deployment where applicable; eight CPU cores; 16 GiB physical RAM; at least 100 GB SSD; 5–10 GiB dataset.
- Repetitions: three reference runs.
- Raw reference records: `documentation/scenario_results/three_run_scenario.csv`.
- Aggregates: `documentation/scenario_results/summary_scenario.csv`.

## reference aggregate comparison

| Metric | MinIO | Silo | Interpretation |
|---|---:|---:|---|
| PUT throughput | 185 MiB/s | 172 MiB/s | MinIO 7.56% higher |
| GET throughput | 245 MiB/s | 231 MiB/s | MinIO 6.06% higher |
| Mixed operations | 1,250 ops/s | 1,170 ops/s | MinIO 6.84% higher |
| PUT p95 latency | 42 ms | 48 ms | MinIO 12.50% lower |
| GET p95 latency | 28 ms | 31 ms | MinIO 9.68% lower |
| CPU utilization | 61% | 65% | MinIO 4 percentage points lower |
| Peak RAM | 7.8 GiB | 8.4 GiB | MinIO 0.6 GiB lower |
| Node recovery | 75 s | 94 s | MinIO 20.21% shorter |

### Calculation methodology

- Relative throughput improvement: `(MinIO - Silo) / Silo × 100`.
- Relative latency/recovery reduction: `(Silo - MinIO) / Silo × 100`.
- CPU comparison uses percentage-point difference, not a percentage relative to utilization.

## Functional validation and S3 compatibility

The project contains runnable MinIO/Silo S3 test suites and integrity/compatibility checks. Passing offline unit tests validate code paths and fixtures, **not** live S3 interoperability. No real API PASS/FAIL values are inferred from the reference performance table.

## Real acceptance gate

Only genuine timestamped runtime logs, raw Warp/fio outputs, actual host specifications, checksums and evidence-linked acceptance reports can change live functional, benchmark, and DEV-915 acceptance statuses to VERIFIED.
