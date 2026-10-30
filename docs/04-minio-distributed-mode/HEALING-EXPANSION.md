# Phase 9 — Healing, expansion and rebalance acceptance

Added `scripts/lab/minio-healing-evidence.sh` to capture version, cluster info and dry-run healing output.
Added `scripts/lab/minio-expansion-check.sh` for non-destructive rebalance command discovery and cluster info.

**Important:** Distributed expansion requires adding a supported server pool; simply adding a fifth
drive/node to the existing four-node erasure set is not a valid assumed procedure. The supported
topology and pinned-release behavior must be checked against the actual server release.
The local 8-core/16GB lab cannot assume an additional four-node pool is feasible.

Acceptance: before/after failure and recovery SHA-256 inventories, cluster health,
server-side healing logs and status, pool-layout evidence, and an actual supported expansion
run (or explicit NOT SUPPORTED/NOT TESTED with rationale). No healing or rebalance success is claimed.
