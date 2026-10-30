# Option B execution gates — evidence, not assumptions

## Verified in this authoring environment

- Python compilation and Bash syntax checks passed.
- Offline suite: 85 tests, zero failures/errors (2026-10-30).
- Added a strict live multipart S3 parity probe (`scripts/verification/live_s3_acceptance.py`) with explicit two-part multipart upload, versioning, SHA-256 GET readback, size, metadata, tags, and immutable version ID verification.
- `scripts/lab/ubuntu-preflight-strict.sh` checks digest-pinned images and all Compose files. It **does not** assert that containers are healthy.

## REVIEW REQUIRED (must be executed on actual Ubuntu host)

1. Verified source/build provenance and immutable digests for MinIO, Silo, Nginx, Prometheus, Grafana. The `.env.example` intentionally retains placeholders rather than inventing hashes.
2. Actual Docker pull, Compose network/volume configuration, startup and health checks.
3. Native Warp binary version and genuine `warp analyze --json` output. Current parser supports normalized metrics only; **do not claim Warp PASS** until an adapter is tested against real output.
4. Actual S3 parity on both products, Object Lock retention/legal hold, multipart, lifecycle, notifications, STS, replication, `mc diff`, `mcli checksum verify`, distributed failure and healing.
5. Real DEV-905–DEV-915 evidence, logs, screenshots, measured Warp/fio metrics, and acceptance sign-off.

## Ubuntu commands

```bash
cp .env.example .env
# Edit .env with verified image digests and credentials; do not commit.
python3 -m venv .venv && source .venv/bin/activate
pip install boto3 PyYAML
bash scripts/lab/ubuntu-preflight-strict.sh
# Only after deployment and creating a dedicated disposable test bucket:
export AWS_ACCESS_KEY_ID=... AWS_SECRET_ACCESS_KEY=...
python3 scripts/verification/live_s3_acceptance.py --endpoint http://127.0.0.1:9000 --bucket YOUR_TEST_BUCKET --output artifacts/minio-live-multipart.json
# Repeat with verified Silo endpoint, separate test bucket and credentials.
```

**Important:** The example MinIO endpoint is not published by default in every Compose stack; inspect the actual proxy or temporary test override before running. Do not treat this example as a guaranteed endpoint.

## Verdict

Pre-execution code safeguards are improved. Actual deployment, integration tests, benchmarks, and acceptance evidence cannot be honestly completed without an accessible Docker host and running services. All such gates remain BLOCKED until real outputs exist.
