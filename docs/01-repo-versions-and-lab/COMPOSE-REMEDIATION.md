# Phase 6 static remediation — 2026-10-30

Implemented: independent Silo credentials; distinct single-node console ports; fail-closed digest/credential preflight; removed misleading disabled health checks; opt-in storage startup (`restart: no`); Prometheus scrape target definitions (requires live metrics authentication and server verification).

**Not fixed/verified:** immutable image digests are unknown; Silo command syntax and four-node topology REVIEW REQUIRED; metrics may require bearer token or public metrics configuration; no Docker Compose CLI available in this workspace; no container healthcheck until a verified executable inside each pinned image is known; proxy and TLS end-to-end not tested; replication configuration and complete monitoring dashboard/alerting remain outstanding.

**Gate:** DO NOT deploy until `python3 scripts/lab/preflight.py --env-file .env` succeeds and Docker Compose config plus server readiness checks pass on Ubuntu.
