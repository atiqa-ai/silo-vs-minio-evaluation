# DEV-908 — MinIO distributed mode (Phase 9)

**Development status:** Cluster Compose exists; safe evidence, integrity and opt-in node-failure tooling implemented.
**Live acceptance status:** NOT TESTED.

## Design
Four MinIO server containers, one persistent Docker volume per node, shared `migration-net`, consistent MinIO image and credentials. The Compose uses `server http://minio{1...4}/data`. This topology's actual erasure-set support, quorum behavior and product-version compatibility must be verified against the pinned release on Ubuntu. No automatic assumption of a successful four-drive erasure layout.

## Preconditions
- Phase 6 image digests and Compose interpolation validated on Ubuntu.
- Cluster initialized successfully, API reachable through verified proxy/load balancer, TLS trusted.
- Sufficient free SSD, resource limits and one heavy stack at a time.
- A disposable DEV-908 bucket created by the operator; no production data.
- Do EXECUTION REQUIRED node-stop scenarios without explicit approval.

## Test procedure
1. Start only the distributed MinIO stack after validating its Compose config.
2. Capture baseline:
   `bash scripts/lab/minio-distributed-evidence.sh`
3. Seed a disposable bucket:
   `python3 scripts/testing/distributed_minio.py --endpoint https://localhost:PORT --mode seed --bucket YOUR_DEV908_BUCKET --output artifacts/dev908-seed.json`
4. Capture baseline integrity:
   `python3 scripts/testing/distributed_minio.py --endpoint https://localhost:PORT --mode verify --bucket YOUR_DEV908_BUCKET --output artifacts/dev908-before.json`
5. With explicit approval only, stop a node:
   `I_APPROVE_NODE_STOP=YES bash scripts/lab/minio-distributed-failure.sh minio4`
6. Capture cluster health, API errors and integrity results while node is down. Do **not** presume availability or quorum.
7. Restore node with `docker compose --env-file .env -f compose/minio/distributed/compose.yaml start minio4`.
8. Capture healing status, cluster health, logs and SHA-256 verification after recovery.
9. Record whether expansion/rebalance is supported by this pinned release; only execute documented supported operations on disposable volumes.

## Evidence requirements
For each step: UTC timestamp, release digest, exact command, expected result, actual exit code, health endpoint, logs, metrics, inventory and SHA-256 outcomes. Redact secrets before publishing.

## OPEN acceptance criteria
- Real four-node boot and cluster health.
- Failure-mode availability/quorum behavior and successful restart.
- Healing/repair evidence (not just object GET).
- Expansion/rebalance support and execution, or explicitly unsupported/not tested.
- Proxy/load-balancer behavior, Prometheus/Grafana evidence.
- All scenarios repeated with consistent data and a final evidence-backed PASS/FAIL matrix.

**No live execution has been performed in this workspace.**
