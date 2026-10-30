# Ubuntu live execution and evidence collection

**Status:** Runner created; actual Ubuntu Docker/S3 testing OPEN.

## Step 1 — Prerequisites

On your Ubuntu host, install Docker Engine + Compose plugin and Python 3 with venv, following the official vendor instructions. Ensure your user can run Docker, or use a controlled privileged session. The project does not automatically install system packages.

## Step 2 — Extract project

Unzip the latest project archive into a new local working directory and enter `minio-vs-silo-evaluation/`. Do not overwrite previous evidence or secrets.

## Step 3 — Preflight and unit evidence

```bash
bash scripts/lab/ubuntu-evidence-runner.sh
```

Inspect `artifacts/runs/<UTC_TIMESTAMP>/EVIDENCE-REPORT.md` and command stdout/stderr. Docker absence or failures are recorded, not hidden.

## Step 4 — Live MinIO smoke (only after Phase 6 server validation)

Install `boto3` in a venv. Set `S3_ENDPOINT`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` from local protected environment configuration, not Git. Then:

```bash
RUN_LIVE_S3=1 bash scripts/lab/ubuntu-evidence-runner.sh
```

The runner creates a uniquely named disposable test bucket, which remains for inspection; no automatic destructive cleanup. Use a trusted HTTPS endpoint. For explicitly isolated local HTTP testing, set `ALLOW_INSECURE_LOCAL_HTTP=1`.

## Evidence integrity rules

- Never fabricate logs, screenshots, dashboards, S3 outputs or PASS labels.
- Preserve raw command output, return codes, UTC timestamps, image digests and environment information.
- Review captured stdout/stderr for sensitive data before publication.
- Unit-test PASS does not imply S3 integration PASS.
- MinIO smoke tests are not Silo validation.
- Before any final report, separately execute and capture distributed, replication, object-lock, lifecycle, IAM/STS, monitoring and performance tests.
- Do EXECUTION REQUIRED destructive cleanup or publish GitHub artifacts without explicit approval.
