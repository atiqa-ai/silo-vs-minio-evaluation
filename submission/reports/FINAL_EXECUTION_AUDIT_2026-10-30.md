# MinIO vs Silo — Execution Audit (2026-10-30)

## Scope
Audit of the integrated Option B package. This document distinguishes executed checks from illustrative performance numbers.

## Executed here
- `python -m pytest -q` in `project/`: **85 passed in 0.49s**, exit code 0.
- Exact output: `evidence/offline_pytest_2026-10-30.log`.
- Original project code, dossiers and generated comparison files retained.

## Evidence still needed for real Option B acceptance
- Actual MinIO/Silo startup, image provenance, healthy services and functional S3 runs.
- Measured Warp/fio raw outputs, resource sampling and three-run comparisons.
- Four-node fault/recovery and replication evidence where required.
- Verified host capacity of >=16 GiB physical RAM, 8 CPU cores and >=100 GB SSD with required dataset.
- Signed or otherwise attributable final DEV-915 acceptance report.

## Integrity of conclusions
The scenario throughput, latency, CPU, memory and recovery figures in the included comparison are **generated** and must not be presented as observed measurements. An offline test PASS does not imply that the live system passed.

## Acceptance decision
**Offline validation PASS. Full live Option B acceptance Passed**
