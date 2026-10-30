# Option B requirements-to-evidence acceptance checklist

Source: supplied project specification. **PARTIAL is not PASS.** No Ubuntu runtime claims.

Option B: 8 CPU cores, 16 GiB RAM, 100 GB free SSD, 4 nodes × 1 drive plus load balancer, 5–10 GB generated data, all sub-tasks; benchmark results indicative. One heavy stack at a time.

| Task | Required acceptance | Status | Remaining evidence |
|---|---|---|---|
| DEV-904 | Repo, public GitHub board, secret scanning, task evidence folders | PARTIAL | Check GitHub board and gitleaks on Ubuntu |
| DEV-905 | Option B Compose lab, TLS, pinned digests, monitoring, rebuild time | PARTIAL | Pull images, inspect digest, docker compose config/up, TLS and health |
| DEV-906 | 5–10 GB generated data, SHA-256, versioning, metadata, retention, CLI cross-check | PARTIAL | Seed then download each version; run mc diff and mcli verify |
| DEV-907 | MinIO single-node S3, IAM/STS, object lock, ILM, notifications | EXECUTION REQUIRED | Execute and preserve raw results |
| DEV-908 | 4x1 distributed failure, healing, expansion | EXECUTION REQUIRED | Fault injection and admin evidence |
| DEV-909 | MinIO bucket, batch and site replication | EXECUTION REQUIRED | Backlog, recovery and raw logs |
| DEV-910 | MinIO Warp/fio repeated baseline, noise and system load | EXECUTION REQUIRED | Verify actual Warp JSON; 3+ repeats |
| DEV-911 | Silo unchanged parity suite | EXECUTION REQUIRED | Use same scripts, dataset and mc |
| DEV-912 | S3 edge cases and evidence for O01–O08 | EXECUTION REQUIRED | Write applies/does-not-apply evidence for each |
| DEV-913 | Silo/MinIO fair Warp comparison | EXECUTION REQUIRED | Same profile, sequential stacks, capture host load |
| DEV-914 | Security, licence, CVEs, SBOM, scans, exit plan | PARTIAL | Scan pinned images and test TLS/IAM |
| DEV-915 | 18-feature matrix, recommendation, evidence, cleanup | PARTIAL | Populate only from real raw evidence |

**Epic gates:** public repo/board; exact commands, expected and actual PASS/FAIL; raw logs and screenshots; image digests; no secrets; clean rebuild time; same mc and dataset; no mixed clusters; O01–O08 decisions; repeated Warp runs; final Go/No-Go. All require actual evidence.
