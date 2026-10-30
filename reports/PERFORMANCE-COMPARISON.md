# Option B performance comparison

## Scope
This report consolidates DEV-904 engineering artifacts for Option B MinIO versus Silo assessment.

## Related task reports
- [DEV-910 — MinIO benchmark evaluation](../docs/taskwise-evaluation/DEV-910.md)
- [DEV-913 — Controlled MinIO–Silo benchmark comparison](../docs/taskwise-evaluation/DEV-913.md)

## Technical findings
The repository includes implementation scripts and a recorded offline test log showing **85 passed**. Individual S3 functionality, security, recovery and benchmark acceptance is established only by its corresponding raw test output.

## Option B comparison scenario

| Metric | Unit | MinIO | Silo | MinIO vs Silo |
|---|---|---:|---:|---:|
| PUT throughput | MiB/s | 185 | 172 | +7.56% |
| GET throughput | MiB/s | 245 | 231 | +6.06% |
| Mixed operations | ops/s | 1250 | 1170 | +6.84% |
| PUT p95 latency | ms | 42 | 48 | -12.50% |
| GET p95 latency | ms | 28 | 31 | -9.68% |
| CPU utilization | % | 61 | 65 | -6.15% |
| Peak RAM | GiB | 7.8 | 8.4 | -7.14% |
| Node recovery | s | 75 | 94 | -20.21% |

**Data origin:** The eight values are from `submission/documentation/OPTION_B_ILLUSTRATIVE_METRICS.csv` (three-run scenario); they are reference figures rather than raw Warp/fio execution measurements. The table is included for presentation and calculation validation, referencetime sign-off.

**Interpretation:** Under this comparison scenario, MinIO has higher PUT/GET throughput and lower p95 latency, CPU, memory and recovery values. These differences describe the supplied scenario only.

## Evidence and reproducibility
Use [Ubuntu execution guide](../UBUNTU-START-HERE.md) and [execution gates](../EXECUTION-GATES.md). Preserve exact commands, versions, timestamps, raw responses and hashes for runtime evidence.

## Conclusion
This report provides a linked engineering record and distinguishes available project evidence from results that require runtime collection.
