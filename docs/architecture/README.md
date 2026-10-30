# Approved Phase 3 architecture

- Docker Compose only; shared network `migration-net`.
- Separate MinIO, Silo, proxy, workload and monitoring projects.
- Single-node and proposed 4-node × 1-drive distributed topologies (validate support before use).
- Dedicated local SSD volumes; localhost-only published proxy/console ports.
- One heavy environment at a time; no mixed-product clusters.
- MinIO-to-MinIO and Silo-to-Silo replication only.
- generated dataset 5–10 GB target subject to disk budget.
- Warp/Fio and repeatable identical benchmark profiles.
- Raw evidence and manifests for every PASS/FAIL.
- **DEV-910 deviation:** NFS-backed testing excluded by owner decision; local SSD only.
- Exact releases, digests, KMS/IdP and capacity need verification.
