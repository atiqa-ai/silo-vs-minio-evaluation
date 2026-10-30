# DEV-909 provisioning automation and live gates

## Implemented
- `scripts/lab/replication-workflow.py`: gated bucket rule creation and site replication initialization with version/feature command discovery and JSON command evidence. Bucket versioning and rule readback included. **Separate distributed site deployments are required for site mode**; the two single-node containers in `compose/minio/replication` must not be used for site replication.
- `scripts/lab/batch-replication.py`: CLI-generated batch YAML template, explicit reviewed-file submission and job status query. Generated YAML requires manual verification of source/target credentials and pinned-server syntax before submission; credentials must not be committed.
- `scripts/testing/replication_audit.py`: read-only version-content comparison and lag polling.
- `scripts/lab/replication-failure.sh`: opt-in destination outage and recovery.

## Examples (commands are not executed automatically)
```bash
python3 scripts/lab/replication-workflow.py bucket --source-alias source --target-alias target --source-bucket dev909-source --target-bucket dev909-target --output artifacts/bucket-dry-run.json
python3 scripts/lab/replication-workflow.py bucket --source-alias source --target-alias target --source-bucket dev909-source --target-bucket dev909-target --execute --approve-disposable-lab --output artifacts/bucket-setup.json
python3 scripts/lab/batch-replication.py generate --alias source --job-file artifacts/reviewed-batch.yaml --execute --approve-disposable-lab --output artifacts/batch-template.json
python3 scripts/lab/batch-replication.py start --alias source --job-file artifacts/reviewed-batch.yaml --execute --approve-disposable-lab --output artifacts/batch-submit.json
python3 scripts/lab/batch-replication.py status --alias source --job-id JOB_ID --output artifacts/batch-status.json
```

## Release constraints
Documentation consulted describes **MinIO AIStor**. The project pins an earlier MinIO community release. Command presence and feature behavior must be checked with the *actual installed `mc` version and server* before marking a scenario supported. Site replication is mutually exclusive with bucket replication on the same deployments. Site replication requires separate distributed deployments and one empty site at initial setup. Batch replication job format is server-version specific. CLI exit 0 is not proof that objects replicated.

## Required live acceptance
- Record image digests and exact server/client versions.
- Capture bucket replication rule, readback and actual object/version/delete-marker synchronization.
- Capture batch job ID, terminal success state and independent object verification.
- Initialize isolated distributed site replication, record site status and object/IAM sync.
- Stop target, create source writes, restore target, verify catch-up and lag with server status and SHA-256.
- Mark unsupported operations explicitly; never report a pass on a dry run.
