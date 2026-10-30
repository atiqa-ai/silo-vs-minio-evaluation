# DEV-908: two-pool expansion on one Ubuntu host

Topology: pool 1 = `minio1..4` with one persistent volume each. Pool 2 = `minioexp1..4`, each with a fresh dedicated persistent volume. All eight processes receive the same two-pool startup arguments in `expanded.yaml`; four original processes use only pool 1 in `base.yaml`.

Run **base.yaml first**, seed/verify generated data, and capture cluster admin info. Verify erasure parity and new pool sizing against pinned release before expansion. Do EXECUTION REQUIRED the normal `compose/minio/distributed/compose.yaml` simultaneously with the expansion topology: these represent alternative ownership of pool-1 volumes.

The expansion script first validates both Compose files. It does not mutate anything unless `I_APPROVE_POOL_EXPANSION=YES`. It stops the old four processes and recreates eight with the new two-pool command; volumes are not deleted. This is a disruptive *lab* procedure and must not be described as a guaranteed zero-downtime production operation. Never roll one node at a time.

Commands:
```
docker compose --env-file .env -f compose/minio/expansion/base.yaml up -d
bash scripts/lab/dev908-expand-pool.sh
I_APPROVE_POOL_EXPANSION=YES bash scripts/lab/dev908-expand-pool.sh
```
Capture before/after `mc admin info`, `mc admin rebalance status` (if supported), cluster logs, SHA-256 inventory, and metrics. A second pool may be empty immediately after expansion; rebalancing is a separate explicitly approved operation. If release rejects 4-drive parity, **stop** and record NOT SUPPORTED rather than silently changing topology.

**Resource budget:** eight containers at default 768MiB limit reserve a potential 6GiB limit in aggregate; storage overhead, OS, and other processes need headroom. This is a local functional test, not production fault-domain isolation. Run no other heavy stack.

**Live acceptance:** EXECUTION REQUIRED. Startup, quorum, expansion and healing remain REVIEW REQUIRED until Ubuntu execution.
