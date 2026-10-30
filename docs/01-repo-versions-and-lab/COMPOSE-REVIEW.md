# Phase 6 Docker Compose review — static findings

**Scope:** reviewed all six storage Compose files, proxy, monitoring, `.env.example` and Prometheus scrape config. Docker CLI unavailable in review workspace; `docker compose config` and container runtime checks remain OPEN.

## Findings
1. **BLOCKER** All images are placeholders; real immutable digests not pinned. Do not launch until validated.
2. **BLOCKER** Storage Compose files disable health checks. Readiness and recovery cannot be evidenced.
3. **BLOCKER** MinIO and Silo both default to `127.0.0.1:19001` console mapping; running both simultaneously collides. This is consistent with one-heavy-stack-at-a-time but must be documented/enforced.
4. **BLOCKER** Only console is host-published; S3 API must use proxy. Proxy target config and TLS files must be created/verified before testing.
5. **HIGH** Silo startup command and distributed erasure topology require validation against the actual pinned Silo release. Do not assume fork parity.
6. **HIGH** Distributed and replication stacks have no load balancer or target-specific API endpoints wired into the lab control scripts. Replication is **not** configured by merely starting two containers.
7. **HIGH** Monitoring Prometheus config only scrapes itself; no MinIO/Silo metrics, Grafana dashboards or alerting are wired. No real-time storage observability yet.
8. **HIGH** Proxy and monitoring need verified credentials, health checks, TLS trust and an actual startup smoke test.
9. **MEDIUM** Shared network `migration-net` allows container-to-container reachability; test isolation and stable DNS names must be reviewed.
10. **MEDIUM** Resource budget must be measured under Profile B; 4×2 GiB nodes plus monitoring and workloads could pressure 16 GiB RAM.

## Acceptance gates
- Run `docker compose --env-file .env -f <compose path> config -q` for all 8 Compose projects.
- Verify images with `docker image inspect`, exact digests, startup commands and Silo feature support.
- Verify S3 and console through TLS proxy, no non-loopback published ports, persistence and health.
- Verify distributed quorum, separate volumes, and source-target replication.
- Verify Prometheus product scrape targets, Grafana dashboards, logs and alerts.
- Capture real outputs before any PASS.
