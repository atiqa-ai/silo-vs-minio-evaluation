# DEV-911 — Silo Functional Validation

## Development status
Implemented: same Python S3 smoke suite reused unchanged for MinIO and Silo, deterministic generated content, disposable unique buckets, side-by-side PASS/FAIL/EXECUTION REQUIRED matrix, isolated localhost Silo API port, same `mc` binary/command parity workflow, safe evidence retention, unit tests and runbook. **No live Silo functional results.**

## Strict comparison protocol
1. Use verified pinned MinIO and Silo image digests, verified Silo runtime support, identical S3 client (`mc` binary, boto3 version), matching hardware/resources, dataset specification, endpoint TLS settings, and command sequence.
2. Run one heavy stack at a time on Ubuntu (8 CPU/16GB RAM). Capture `docker compose config`, `ps`, logs, image digests and version strings. If both servers cannot coexist under the resource budget, preserve an identical test protocol and run sequentially. Never claim identical wall-clock performance from sequential functional runs.
3. `compose/silo/single/compose.yaml` publishes Silo S3 API to localhost port 9900 by default; MinIO endpoint must be established from its own verified configuration.
4. Python runner imports **the existing `minio_baseline.py` module**, invoking the same `run()` function for both endpoints. Same fixed bytes, metadata/tags and operations; unique bucket names prevent collision. Credentials are separate environment variables.
5. CLI parity uses the same `mc` binary for both, same command sequence, same payload; alias and disposable bucket name are the only changes. Do not use `mcli` as the comparison client. `mcli checksum verify` is a separate Silo-specific supplemental check.
6. Compare `PASS/PASS` = SAME_PASS, `PASS/FAIL` = SILO_REGRESSION, `FAIL/PASS` = SILO_PASS_MINIO_FAIL, `FAIL/FAIL` = BOTH_FAIL, missing = INCOMPLETE. Failures are not silently treated as unsupported features.

## Dry plan
```
python3 scripts/testing/silo_functional.py --mode plan --out artifacts/dev911-plan
```

## Real smoke parity (requires live, independently reachable endpoints)
```
export MINIO_ACCESS_KEY=... MINIO_SECRET_KEY=...
export SILO_ACCESS_KEY=... SILO_SECRET_KEY=...
python3 scripts/testing/silo_functional.py --mode run --approve \
  --minio-endpoint http://127.0.0.1:9000 \
  --silo-endpoint http://127.0.0.1:9900 \
  --allow-insecure-http --out artifacts/dev911-smoke-001
```
`--cleanup` is optional; it only deletes newly created disposable buckets and may fail on retained versions. Default retains evidence.

## Same mc client parity
Preconfigure `DEV911_MINIO_ALIAS` and `DEV911_SILO_ALIAS` in local `mc` configuration. Verify alias endpoints and ensure dedicated lab credentials; the script does not configure aliases or print secrets.
```
I_APPROVE_DEV911_MC=YES DEV911_MINIO_ALIAS=minio-lab DEV911_SILO_ALIAS=silo-lab \
  bash scripts/lab/dev911-mc-parity.sh
```
Inspect raw command output and compare actual payload SHA-256; the script does not automatically assert hashes equal.

## Required feature coverage matrix
| DEV-907 capability | Silo counterpart | Evidence state |
|---|---|---|
| Basic S3 CRUD, listing, metadata, tags, multipart | `minio_baseline.run` identical | EXECUTION REQUIRED |
| Bucket/object versioning, delete markers | `minio_baseline.run` identical | EXECUTION REQUIRED |
| SSE-S3 / SSE-KMS | `advanced_s3.py` identical CLI parameters | EXECUTION REQUIRED |
| Object lock governance / compliance / legal hold | `advanced_s3.py`, explicit retention approval | EXECUTION REQUIRED |
| Lifecycle rules and actual expiration | `advanced_s3.py`, timed observation required | EXECUTION REQUIRED |
| IAM policy, users, service accounts, STS | Existing `iam_sts.py` and provisioning checklist | EXECUTION REQUIRED |
| Notifications configuration and delivery | Existing notification verification + live sink | EXECUTION REQUIRED |
| Metrics/health/console and logs | Silo runtime-specific evidence | EXECUTION REQUIRED |
| Distributed, healing, expansion | Silo distributed Compose + safe failure/recovery | EXECUTION REQUIRED |
| Bucket/batch/site replication | Silo replication Compose + topology checks | EXECUTION REQUIRED |
| CLI `mc` parity, checksum verification | `dev911-mc-parity.sh`, supplemental `mcli` | EXECUTION REQUIRED |

**No unsupported capability may be labelled PASS without evidence.** Advanced tests may create 2-day compliance-locked objects; run only with explicit opt-in and adequate cleanup plan. Never test production data.

## Known blockers
- Image provenance, runtime support and Silo feature compatibility require Ubuntu execution.
- Advanced feature parity requires separate identical configuration and test fixtures on both systems; smoke success alone does not establish full DEV-907 equivalence.
- Live Docker validation and acceptance evidence unavailable in the authoring environment.

## Advanced feature parity runner
The same `advanced_s3.Runner` functions are invoked for both engines, not rewritten with weaker assertions. Execute only on disposable, verified lab endpoints:
```
python3 scripts/testing/silo_advanced_parity.py --mode plan --out artifacts/dev911-advanced-plan
python3 scripts/testing/silo_advanced_parity.py --mode run --approve \\
  --minio-endpoint http://127.0.0.1:9000 --silo-endpoint http://127.0.0.1:9900 \\
  --allow-insecure-http --out artifacts/dev911-advanced-001
```
KMS and notifications are opt-in only when both sides have configured equivalents. Retention requires `--retention-approval` plus `I_ACCEPT_2_DAY_OBJECT_RETENTION=YES`. This intentionally leaves compliance-retained objects for two days. STS, actual lifecycle expiration, delivery, monitoring, healing, expansion and replication require independent evidence and cannot be inferred from advanced suite success.

## Mandatory phase completion gate
`python3 scripts/testing/dev911_gate.py --input artifacts/dev911-evidence-index.json --output artifacts/dev911-gate.json`

Input is a user-maintained mapping of required scenario names to `{"status":"PASS","evidence_files":["path/to/real-output"]}`. All required categories must be evidenced. The gate only checks presence of evidence and stated status; manual inspection of actual outputs is mandatory. An empty index returns INCOMPLETE, never PASS.

**Development limitation:** The existing Silo distributed/replication Compose files are unvalidated scaffolds. Full implementation requires pinned Silo version support and live Ubuntu testing. This work must not be called 100% complete before those gates.
