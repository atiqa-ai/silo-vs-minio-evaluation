# DEV-907 advanced S3 scenarios — Ubuntu live execution

**Not executed in this workspace.** Run only on isolated, disposable MinIO/Silo test endpoints after Phase 6 is validated. This suite intentionally leaves retained objects for later inspection. Do not assume buckets can be deleted immediately.

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install boto3
export AWS_ACCESS_KEY_ID='LAB_ACCESS_KEY'
export AWS_SECRET_ACCESS_KEY='LAB_SECRET_KEY'
python3 scripts/testing/advanced_s3.py --endpoint https://localhost:19443 --output artifacts/minio-advanced.json
```

- Scenarios: version history/delete markers, SSE-S3, governance/compliance retention, legal hold, lifecycle rule round-trip.
- Optional `--kms-key`: SSE-KMS requires configured KMS.
- Optional `--notification-arn`: configures a destination, **does not** verify delivery.
- Set `DEV907_RESTRICTED_ACCESS_KEY` and `DEV907_RESTRICTED_SECRET_KEY` in the shell for IAM negative controls; never put secrets in CLI arguments.
- `scripts/testing/iam_sts.py` tests pre-issued scoped STS credentials; obtaining credentials from an IdP remains a prerequisite.
- Lifecycle **expiry** requires a later scheduled verification, not just configuration.
- No live PASS is claimed without real JSON output and raw CLI evidence.
- Object Lock compliance uses two-day retention; avoid this test unless SSD retention is acceptable. Never run on production buckets.
