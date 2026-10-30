# Phase 6–8 six-blocker remediation status

This document distinguishes code readiness from actual Ubuntu execution.

1. **Images and Silo compatibility:** Verified upstream source release `minio/minio@RELEASE.2025-10-15T17-29-55Z` and PGSTY Silo server `RELEASE.2026-10-26T00-00-00Z`. The `pgsty/silo` classic container uses `server /data --console-address :9001` and MINIO_ROOT_* environment variables. `scripts/lab/resolve-images.sh` pulls tagged images and records actual immutable registry digests on Ubuntu. MinIO community official container availability has changed; proposed third-party build is not equivalent to an upstream-authenticated build. Review provenance before accepting it. No digest was fabricated. Silo distributed runtime support must be tested on Ubuntu.

2. **Compose validation:** All 8 files are parseable YAML, but only `docker compose config --quiet` on Ubuntu with actual `.env` verifies Compose semantics and interpolation. Run `scripts/lab/ubuntu-compose-validate.sh`. Container startup is a separate test.

3. **Monitoring:** Grafana datasource/dashboard provisioning and Prometheus alert rules added. Live metrics authentication and endpoint reachability still require configuration and test; a dashboard is not proof of real metrics. Verify Prometheus targets and alert firing in Ubuntu.

4. **Object Lock/lifecycle:** Disposable governance default-retention configuration and lifecycle rule readback implemented. Actual server-driven expiration and negative delete tests still require live elapsed-time observations. Never shorten compliance retention or claim early deletion is possible.

5. **Notifications/IAM/STS:** Notification event-file delivery verifier added, IAM/STS provisioning checklist created. Actual destination, credentials, policy enforcement and STS token issuance require live infrastructure. No PASS without delivered event and authorization evidence.

6. **Independent CLI checks:** `cli_crosscheck.sh` captures mc diff and mcli checksum verify versions, help, output and exit codes. Commands require actual compatible pinned CLIs and lab aliases; semantic diff review required.

**Decision: Not fully closed.** Local implementation and static tests do not replace Ubuntu execution. Do not mark DEV-905/906/907 PASS without real evidence.
