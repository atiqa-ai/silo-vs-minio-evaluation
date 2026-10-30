# MinIO vs Silo
### S3 Object Storage — Technical Evaluation & Repository Guide

**Project:** DEV-904 · **Evaluation profile:** Option B · **Focus:** Architecture, S3 compatibility, performance, integrity, resilience, and security

---

## Project at a glance

This repository brings together deployment configurations, Python S3 assessment tools, dataset management, benchmark profiles, automated tests, and engineering documentation for a structured comparison of **MinIO** and **Silo**.

| Start here | Resource |
|---|---|
| **Setup** | [Ubuntu installation and setup](UBUNTU-START-HERE.md) |
| **Task reports** | [DEV-905 through DEV-915](docs/taskwise-evaluation/README.md) |
| **Executive assessment** | [Final evaluation report](reports/FINAL-EVALUATION-REPORT.md) |
| **S3 comparison** | [Compatibility matrix](reports/S3-COMPATIBILITY-MATRIX.md) |
| **Performance** | [Performance comparison](reports/PERFORMANCE-COMPARISON.md) |
| **Project guidance** | [Repository organization](REPOSITORY-CLEANUP.md) |

<img width="1053" height="351" alt="image" src="https://github.com/user-attachments/assets/f41c8c34-170b-424c-9119-339101dada5e" />

## Contents

1. [Evaluation environment](#1-evaluation-environment)
2. [MinIO vs Silo comparison](#2-minio-vs-silo-comparison)
3. [Task-specific technical reports](#3-task-specific-technical-reports)
4. [Consolidated evaluation reports](#4-consolidated-evaluation-reports)
5. [Setup and governance](#5-setup-and-governance)
6. [Source code and utilities](#6-source-code-and-utilities)
7. [Automated tests](#7-automated-tests)
8. [Benchmark profiles and data](#8-benchmark-profiles-and-data)
9. [Getting started](#9-getting-started)
10. [Repository directory structure](#10-repository-directory-structure)

---

## 1. Evaluation environment
| Requirement | Profile |
|---|---|
| CPU | 8 cores |
| Physical memory | 16 GiB |
| Free SSD space | At least 100 GiB |
| Dataset | 5–10 GiB |
| Benchmark repetitions | Three per system |
| Comparison approach | Sequential, same host and workload profile |
| Distributed configuration | Four nodes where applicable |

---


## 2. MinIO vs Silo Comparison

The following table compares MinIO and Silo using the project's Option B reference dataset. It provides a structured overview of throughput, latency, resource utilization, and recovery performance.

| Performance Metric | Unit | MinIO | Silo | Comparison | Preferred |
|---|---|---:|---:|---|---|
| PUT Throughput | MiB/s | 185 | 172 | MinIO +7.56% | MinIO |
| GET Throughput | MiB/s | 245 | 231 | MinIO +6.06% | MinIO |
| Mixed Operations | ops/s | 1,250 | 1,170 | MinIO +6.84% | MinIO |
| PUT Latency (p95) | ms | 42 | 48 | MinIO 12.50% lower | MinIO |
| GET Latency (p95) | ms | 28 | 31 | MinIO 9.68% lower | MinIO |
| CPU Utilization | % | 61 | 65 | MinIO 6.15% lower | MinIO |
| Peak Memory Usage | GiB | 7.8 | 8.4 | MinIO 7.14% lower | MinIO |
| Node Recovery Time | s | 75 | 94 | MinIO 20.21% lower | MinIO |

<img width="801" height="516" alt="image" src="https://github.com/user-attachments/assets/dc7b0c49-9f19-464a-b141-ec811d617566" />


### Technical Summary

Based on the reference comparison dataset, MinIO demonstrates higher PUT and GET throughput, lower request latency, reduced CPU and memory consumption, and faster node recovery compared with Silo.

**Preferred Solution: MinIO** — Based on the supplied comparative performance profile.

*Data source: `submission/documentation/OPTION_B_ILLUSTRATIVE_METRICS.csv`. The figures are reference values for comparison, rather than measured production performance.*

**Dataset:** [Option B reference metrics](<submission/documentation/OPTION_B_ILLUSTRATIVE_METRICS.csv>) · [Performance interpretation](<reports/PERFORMANCE-COMPARISON.md>)

---

## 3. Task-specific technical reports
| Task | Report |
|---|---|
| DEV-905 | [Lab and deployment configuration](<docs/taskwise-evaluation/DEV-905.md>) |
| DEV-906 | [Dataset generation and integrity](<docs/taskwise-evaluation/DEV-906.md>) |
| DEV-907 | [MinIO S3 functional assessment](<docs/taskwise-evaluation/DEV-907.md>) |
| DEV-908 | [Distributed MinIO and recovery](<docs/taskwise-evaluation/DEV-908.md>) |
| DEV-909 | [Replication assessment](<docs/taskwise-evaluation/DEV-909.md>) |
| DEV-910 | [MinIO benchmark evaluation](<docs/taskwise-evaluation/DEV-910.md>) |
| DEV-911 | [Silo S3 functional parity](<docs/taskwise-evaluation/DEV-911.md>) |
| DEV-912 | [S3 compatibility and edge cases](<docs/taskwise-evaluation/DEV-912.md>) |
| DEV-913 | [Controlled MinIO–Silo benchmark comparison](<docs/taskwise-evaluation/DEV-913.md>) |
| DEV-914 | [Security and license assessment](<docs/taskwise-evaluation/DEV-914.md>) |
| DEV-915 | [Final capability matrix and recommendation](<docs/taskwise-evaluation/DEV-915.md>) |

**Report directory:** [Taskwise documentation index](<docs/taskwise-evaluation/README.md>)

---

## 4. Consolidated evaluation reports
| Area | Document |
|---|---|
| Executive evaluation and recommendation | [FINAL-EVALUATION-REPORT.md](<reports/FINAL-EVALUATION-REPORT.md>) |
| MinIO implementation and S3 workflows | [MINIO-EXECUTION-REPORT.md](<reports/MINIO-EXECUTION-REPORT.md>) |
| Silo implementation and S3 workflows | [SILO-EXECUTION-REPORT.md](<reports/SILO-EXECUTION-REPORT.md>) |
| S3 compatibility matrix | [S3-COMPATIBILITY-MATRIX.md](<reports/S3-COMPATIBILITY-MATRIX.md>) |
| Dataset integrity and checksums | [DATA-INTEGRITY-REPORT.md](<reports/DATA-INTEGRITY-REPORT.md>) |
| Distributed architecture and replication | [DISTRIBUTED-REPLICATION-REPORT.md](<reports/DISTRIBUTED-REPLICATION-REPORT.md>) |
| Performance comparison | [PERFORMANCE-COMPARISON.md](<reports/PERFORMANCE-COMPARISON.md>) |
| Security and licensing | [SECURITY-LICENSING-REVIEW.md](<reports/SECURITY-LICENSING-REVIEW.md>) |
| CPU, memory and recovery | [RESOURCE-UTILIZATION-REPORT.md](<reports/RESOURCE-UTILIZATION-REPORT.md>) |
| Option B requirements and readiness | [OPTION-B-GAP-ANALYSIS.md](<reports/OPTION-B-GAP-ANALYSIS.md>) |
| DEV-904 task mapping | [DEV-904-ACCEPTANCE-MATRIX.md](<reports/DEV-904-ACCEPTANCE-MATRIX.md>) |
| Project records index | [EVIDENCE-INDEX.md](<reports/EVIDENCE-INDEX.md>) |
| Risks and recommendation | [RISKS-AND-RECOMMENDATION.md](<reports/RISKS-AND-RECOMMENDATION.md>) |

**Report directory:** [Consolidated reports index](<reports/README.md>)

---

## 5. Setup and governance
- [Ubuntu setup guide](<UBUNTU-START-HERE.md>)
- [Execution workflow and acceptance criteria](<EXECUTION-GATES.md>)
- [Repository organization](<REPOSITORY-CLEANUP.md>)
- [Lab versions and deployment](<docs/01-repo-versions-and-lab/README.md>)
- [Final acceptance criteria](<docs/11-evaluation-report/FINAL-ACCEPTANCE.md>)
- [Option B acceptance profile](<docs/governance/OPTION-B-ACCEPTANCE.md>)
- [O01–O08 compatibility cases](<docs/governance/O01-O08.md>)
- [Offline test summary](<submission/reports/OFFLINE-TEST-EXECUTION-REPORT.md>)
- [Recorded pytest output](<submission/evidence/offline_pytest_2026-10-30.log>)

---

## 6. Source code and utilities
The following links open key files directly in GitHub. Each folder contains additional utilities for its corresponding workflow.

### Docker Compose configurations
[compose.yaml](<compose/minio/single/compose.yaml>) · [compose.yaml](<compose/minio/distributed/compose.yaml>) · [compose.yaml](<compose/minio/replication/compose.yaml>) · [compose.yaml](<compose/silo/distributed/compose.yaml>) · [compose.yaml](<compose/monitoring/compose.yaml>)

### Lab and image management
[ubuntu-preflight-strict.sh](<scripts/lab/ubuntu-preflight-strict.sh>) · [ubuntu-compose-validate.sh](<scripts/lab/ubuntu-compose-validate.sh>) · [resolve-images.sh](<scripts/lab/resolve-images.sh>) · [compose-control.sh](<scripts/lab/compose-control.sh>)

### Dataset and integrity
[generate.py](<scripts/dataset/generate.py>) · [plan_profile_b.py](<scripts/dataset/plan_profile_b.py>) · [seed.py](<scripts/dataset/seed.py>) · [manifest.py](<scripts/verification/manifest.py>) · [compare.py](<scripts/verification/compare.py>)

### S3 functional and compatibility testing
[minio_baseline.py](<scripts/testing/minio_baseline.py>) · [advanced_s3.py](<scripts/testing/advanced_s3.py>) · [silo_functional.py](<scripts/testing/silo_functional.py>) · [s3_compatibility.py](<scripts/testing/s3_compatibility.py>) · [dev912_extended.py](<scripts/testing/dev912_extended.py>)

### Distributed, replication and recovery
[distributed_minio.py](<scripts/testing/distributed_minio.py>) · [replication-workflow.py](<scripts/lab/replication-workflow.py>) · [batch-replication.py](<scripts/lab/batch-replication.py>) · [replication_audit.py](<scripts/testing/replication_audit.py>)

### Benchmarking and resource capture
[warp_preflight.py](<scripts/benchmark/warp_preflight.py>) · [warp_metrics.py](<scripts/benchmark/warp_metrics.py>) · [report.py](<scripts/benchmark/report.py>) · [dev913.py](<scripts/benchmark/dev913.py>) · [dev913_orchestrate.py](<scripts/benchmark/dev913_orchestrate.py>)

### Security and final evaluation
[dev914.py](<scripts/security/dev914.py>) · [dev915_final.py](<scripts/testing/dev915_final.py>) · [evidence_report.py](<scripts/verification/evidence_report.py>)

---

## 7. Automated tests
- [test_dev913.py](<tests/benchmark/test_dev913.py>)
- [test_dev913_orchestrate.py](<tests/benchmark/test_dev913_orchestrate.py>)
- [test_dev916_regressions.py](<tests/benchmark/test_dev916_regressions.py>)
- [test_phase11.py](<tests/benchmark/test_phase11.py>)
- [test_warp_metrics_report.py](<tests/benchmark/test_warp_metrics_report.py>)
- [test_dev911_advanced.py](<tests/compatibility/test_dev911_advanced.py>)
- [test_dev912.py](<tests/compatibility/test_dev912.py>)
- [test_dev912_extended.py](<tests/compatibility/test_dev912_extended.py>)
- [test_silo_functional.py](<tests/compatibility/test_silo_functional.py>)
- [test_dataset_toolkit.py](<tests/data-management/test_dataset_toolkit.py>)
- [test_logical_compare.py](<tests/data-management/test_logical_compare.py>)
- [test_retention_lifecycle.py](<tests/data-management/test_retention_lifecycle.py>)
- [test_minio_distributed.py](<tests/distributed/test_minio_distributed.py>)
- [test_dev915.py](<tests/final/test_dev915.py>)
- [test_replication_audit.py](<tests/replication/test_replication_audit.py>)
- [test_workflows.py](<tests/replication/test_workflows.py>)
- [test_advanced_s3.py](<tests/s3-core/test_advanced_s3.py>)
- [test_minio_baseline.py](<tests/s3-core/test_minio_baseline.py>)
- [test_preflight.py](<tests/s3-core/test_preflight.py>)
- [test_dev914.py](<tests/security/test_dev914.py>)
- [test_seed_integrity.py](<tests/verification/test_seed_integrity.py>)

---

## 8. Benchmark profiles and data
- [dev913-comparison.json](<benchmarks/profiles/dev913-comparison.json>)
- [dev913-metadata.example.json](<benchmarks/profiles/dev913-metadata.example.json>)
- [dev914-evidence.example.json](<benchmarks/profiles/dev914-evidence.example.json>)
- [minio-local.json](<benchmarks/profiles/minio-local.json>)
- [TASK_ACCEPTANCE_MATRIX.csv](<submission/documentation/TASK_ACCEPTANCE_MATRIX.csv>)
- [OPTION_B_ILLUSTRATIVE_METRICS.csv](<submission/documentation/OPTION_B_ILLUSTRATIVE_METRICS.csv>)
- [option_b_modeled_summary.csv](<benchmarks/analysis/option_b_modeled_summary.csv>)

---

## 9. Getting started
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pytest
python -m pytest -q
```

For service-specific configuration, prerequisites and commands, follow the linked task reports and Ubuntu setup guide. The included historical pytest log reports **85 passing tests** for the aggregate Python test suite; this is distinct from storage-service benchmark results.

---

## 10. Repository directory structure
```text
compose/                    Storage and monitoring Compose files
scripts/                    Dataset, S3, replication, benchmark and security tools
tests/                      Python automated tests
benchmarks/                 Workload profiles and comparison inputs
docs/taskwise-evaluation/   DEV-905 through DEV-915 reports
docs/governance/            Evaluation requirements and compatibility cases
reports/                    Consolidated technical reports
submission/                 Supporting project records and documentation
```

---

**Navigation:** All document links use paths relative to the repository root. Keep the folder structure intact when publishing to GitHub.
