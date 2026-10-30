# DEV-908 healing and expansion workflow

`healing-rebalance-workflow.py` provides `heal-status`, `rebalance-status`, and guarded `rebalance-start` commands, with evidence and exit codes. `minio-distributed-failure.sh` stops a single node only with approval. `distributed_minio.py` verifies seeded object SHA-256 before/during/after failure.

Rebalance **requires a real second server pool**; no such second pool is included in the current four-node Compose. The script refuses to start a rebalance without `--execute --approve-disposable-lab --multi-pool-confirmed`. No unsupported topology is silently added. Expansion must be performed according to the verified pinned MinIO server's documented mechanism. Current AIStor hot-reload expansion instructions require releases newer than the project's historical community release; they cannot be assumed compatible.

Live acceptance requires: health baseline, failure behavior, after-recovery healing status and logs, integrity checks, then (if supported) second-pool expansion with new pool topology, rebalance status progression and after-rebalance integrity. On a constrained 16 GB Ubuntu machine, adding a second pool may be infeasible; record `NOT TESTED` with reason instead of inventing a PASS.
