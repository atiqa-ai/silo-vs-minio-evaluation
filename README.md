# MinIO vs Silo — S3 Storage Evaluation

**Epic DEV-904 | Option B evaluation | General technical comparison and documentation index**

## Executive overview
This repository provides Docker Compose lab configurations, Python S3 test suites, dataset integrity tools, benchmark workflows, security checks and task-by-task engineering reports for evaluating MinIO and Silo under a controlled local Option B profile.

## Evaluation configuration
| Requirement | Option B profile |
|---|---|
| CPU | 8 cores |
| RAM | 16 GiB physical |
| Disk | ≥100 GiB free SSD |
| Dataset | 5–10 GiB generated data |
| Benchmark repetitions | 3 per system |
| Execution | Sequential, same host and profile |
| Distributed testing | Four nodes where applicable |

## Illustrative comparison profile

The following values are supplied reference figures for discussing comparative metrics and calculation methods. They should be interpreted as a documentation example, rather than as measurements from a deployed storage environment.

## Comparative results
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

## Task-specific technical reports
- [DEV-905 — Lab and deployment configuration](docs/taskwise-evaluation/DEV-905.md)
- [DEV-906 — Dataset generation and integrity](docs/taskwise-evaluation/DEV-906.md)
- [DEV-907 — MinIO S3 functional assessment](docs/taskwise-evaluation/DEV-907.md)
- [DEV-908 — Distributed MinIO and recovery](docs/taskwise-evaluation/DEV-908.md)
- [DEV-909 — Replication assessment](docs/taskwise-evaluation/DEV-909.md)
- [DEV-910 — MinIO benchmark evaluation](docs/taskwise-evaluation/DEV-910.md)
- [DEV-911 — Silo S3 functional parity](docs/taskwise-evaluation/DEV-911.md)
- [DEV-912 — S3 compatibility and edge cases](docs/taskwise-evaluation/DEV-912.md)
- [DEV-913 — Controlled MinIO–Silo benchmark comparison](docs/taskwise-evaluation/DEV-913.md)
- [DEV-914 — Security and license assessment](docs/taskwise-evaluation/DEV-914.md)
- [DEV-915 — Final acceptance and recommendation](docs/taskwise-evaluation/DEV-915.md)

## Consolidated evaluation reports
- [Evaluation scope, acceptance and recommendation](reports/FINAL-EVALUATION-REPORT.md)
- [MinIO implementation and S3 execution](reports/MINIO-EXECUTION-REPORT.md)
- [Silo implementation and S3 execution](reports/SILO-EXECUTION-REPORT.md)
- [API compatibility and O01–O08 case matrix](reports/S3-COMPATIBILITY-MATRIX.md)
- [Dataset generation and checksums](reports/DATA-INTEGRITY-REPORT.md)
- [Distributed healing and replication](reports/DISTRIBUTED-REPLICATION-REPORT.md)
- [Option B performance comparison](reports/PERFORMANCE-COMPARISON.md)
- [Security controls and license provenance](reports/SECURITY-LICENSING-REVIEW.md)
- [CPU, RAM and recovery profile](reports/RESOURCE-UTILIZATION-REPORT.md)
- [Option B execution prerequisites](reports/OPTION-B-GAP-ANALYSIS.md)
- [Epic acceptance mapping](reports/DEV-904-ACCEPTANCE-MATRIX.md)
- [Evidence inventory and provenance](reports/EVIDENCE-INDEX.md)
- [Engineering risks and recommendation](reports/RISKS-AND-RECOMMENDATION.md)

## Documentation cross-verification

## Verification sources
- [Recorded offline pytest log](submission/evidence/offline_pytest_2026-10-30.log): 85 passed.
- [Option B scenario CSV](submission/documentation/OPTION_B_ILLUSTRATIVE_METRICS.csv): source for the comparison table.
- [Ubuntu setup](UBUNTU-START-HERE.md) and [execution gates](EXECUTION-GATES.md).

## Reproduce offline tests
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pytest
python -m pytest -q
```

## Project layout
- `compose/`: storage and monitoring deployments
- `scripts/`: test, verification, benchmarking and security utilities
- `tests/`: offline automated tests
- `benchmarks/`: profiles and analysis
- `docs/taskwise-evaluation/`: DEV-905 through DEV-915 reports
- `reports/`: consolidated technical reports
- `submission/`: supporting project records


## Repository navigation and evidence

- [Ubuntu setup](UBUNTU-START-HERE.md) · [Execution and acceptance gates](EXECUTION-GATES.md)
- [Task reports DEV-905–DEV-915](docs/taskwise-evaluation/README.md)
- [Consolidated reports](reports/README.md)
- [Offline test execution report](submission/reports/OFFLINE-TEST-EXECUTION-REPORT.md)
- [Repository cleanup record](REPOSITORY-CLEANUP.md)

**Results provenance:** Performance values in the comparison table are scenario/reference values, REFERENCE ONLY Warp/fio measurements. Runtime acceptance depends on preserved raw test evidence.

## DEV-905–DEV-915 — General Technical Comparison Reports

The following reports provide technical comparisons, architecture considerations, common behavior and reference workload analysis for the Option B evaluation. The numerical performance comparison is an illustrative reference dataset rather than a live benchmark measurement.

| Task | Technical report |
|---|---|
| DEV-905 | [DEV-905 — Deployment, Compose, and TLS](docs/taskwise-evaluation/DEV-905.md) |
| DEV-906 | [DEV-906 — Dataset Generation and Object Integrity](docs/taskwise-evaluation/DEV-906.md) |
| DEV-907 | [DEV-907 — MinIO S3 Functional Baseline](docs/taskwise-evaluation/DEV-907.md) |
| DEV-908 | [DEV-908 — Distributed Storage, Healing, and Recovery](docs/taskwise-evaluation/DEV-908.md) |
| DEV-909 | [DEV-909 — Replication and Consistency](docs/taskwise-evaluation/DEV-909.md) |
| DEV-910 | [DEV-910 — MinIO Throughput, Latency, and Resource Efficiency](docs/taskwise-evaluation/DEV-910.md) |
| DEV-911 | [DEV-911 — Silo S3 Functional Parity](docs/taskwise-evaluation/DEV-911.md) |
| DEV-912 | [DEV-912 — S3 API Compatibility and Edge Cases](docs/taskwise-evaluation/DEV-912.md) |
| DEV-913 | [DEV-913 — Option B Performance Comparison](docs/taskwise-evaluation/DEV-913.md) |
| DEV-914 | [DEV-914 — Security, Licensing, and Supply Chain](docs/taskwise-evaluation/DEV-914.md) |
| DEV-915 | [DEV-915 — Final Capability Matrix and Recommendation](docs/taskwise-evaluation/DEV-915.md) |

