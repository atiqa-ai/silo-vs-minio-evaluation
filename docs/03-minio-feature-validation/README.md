# DEV-907 — MinIO single-node feature validation

**Status:** Partial implementation; live testing and full acceptance criteria OPEN.

## Goal
Evidence-backed validation of MinIO S3 capabilities on the Phase 6 single-node lab.

## Preconditions
- Phase 6 MinIO lab operational; actual image release and digest pinned and recorded.
- Endpoint reachable with trusted TLS certificate.
- Credentials supplied through environment, never committed.
- Disposable bucket only. Do EXECUTION REQUIRED on production endpoints.

## Run smoke suite
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install boto3
export AWS_ACCESS_KEY_ID='YOUR_LAB_KEY'
export AWS_SECRET_ACCESS_KEY='YOUR_LAB_SECRET'
python3 scripts/testing/minio_baseline.py --endpoint https://localhost:YOUR_PROXY_PORT --output artifacts/dev907-minio-smoke.json
python3 -m unittest discover -s tests/s3-core -p 'test_*.py' -v
```
The smoke suite creates a uniquely named bucket, enables versioning, tests PUT/GET/HEAD/LIST, metadata, tags, a second version, multipart upload, and delete markers. By default the disposable bucket remains available for inspection. `--cleanup` deletes ONLY the bucket created by that run; it is destructive and should be used only after explicit approval.

## Expected vs actual
| Test | Expected | Actual | Status | Evidence |
|---|---|---|---|---|
| Create bucket | Success | EXECUTION REQUIRED | NOT TESTED | — |
| Versioning | Enabled | EXECUTION REQUIRED | NOT TESTED | — |
| PUT/GET/HEAD/LIST | Success, SHA-256 match | EXECUTION REQUIRED | NOT TESTED | — |
| Metadata and tags | Preserved | EXECUTION REQUIRED | NOT TESTED | — |
| Multipart | Full SHA-256 match | EXECUTION REQUIRED | NOT TESTED | — |
| Delete marker | Present | EXECUTION REQUIRED | NOT TESTED | — |

## Full DEV-907 acceptance gaps
- S3 IAM policies and negative authorization tests.
- STS and temporary credentials.
- SSE-S3/SSE-KMS support and key-management dependencies.
- Object Lock, retention, legal hold and lifecycle policies.
- Bucket notifications and destination delivery.
- Prometheus/metrics, server logs, traces and observability.
- SDK and CLI interoperability and error-code conformance.
- Record release tags/digests, commands, exit codes, screenshots, raw results and cleanup.

**No live PASS claims:** Docker/S3 endpoints are not available in the assistant workspace.
