# DEV-905 — Repository, pinned versions and local Compose lab

## Goal
Provide repeatable, isolated MinIO and Silo local lab topologies.

## Phase 6 implementation status
**Configuration authored; runtime REVIEW REQUIRED.** Docker is unavailable in the authoring environment. No image digests have been verified, no container has been started, and no PASS has been recorded.

## Environment
Profile B user-confirmed (8 CPU / 16 GB RAM / 100 GB SSD). Actual hardware/OS/Docker evidence OPEN.

## Prerequisites
Verified MinIO and Silo immutable image digests, Compose v2, Docker, OpenSSL, local SSD, secrets stored in ignored `.env`.

## Procedure
See `scripts/lab/README.md`. Capture exact commands and outputs before changing status.

## Results
| Check | Expected | Actual | Status |
|---|---|---|---|
| YAML syntax | All compose YAML parses | Static parser only | Static check |
| Docker compose config | All selected files pass | EXECUTION REQUIRED | Not tested |
| Image provenance | Verified release/digest | OPEN | Not tested |
| Single-node startup | Healthy API/console | OPEN | Not tested |
| 4-node startup | Healthy cluster | OPEN | Not tested |
| Restart persistence | Manifest unchanged | OPEN | Not tested |
| TLS | Trusted HTTPS client succeeds | OPEN | Not tested |
| Proxy | S3 API accessible on localhost | OPEN | Not tested |
| Monitoring | Metrics available | OPEN | Not tested |
| Replication | Same-product source/target healthy | OPEN | Not tested |

## Findings and problems
- No Docker daemon in authoring environment.
- Image digests, Silo entrypoint, metrics endpoints and 4-node topology support need live verification.
- Proxy backend uses HTTP internally; HTTPS is terminated at localhost proxy only. Full internal TLS requires additional design approval if demanded.

## Conclusion
Phase 6 artifacts drafted; acceptance OPEN live validation.

## Reproduce and safe cleanup
See `scripts/lab/README.md`. Never run `docker compose down -v` without approval.
