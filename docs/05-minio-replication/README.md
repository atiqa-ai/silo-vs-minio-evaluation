# Phase 10 / DEV-909 — MinIO replication

## Scope and development artifacts
Existing Compose supplies independent source/target MinIO services. `scripts/testing/replication_audit.py`
polls full S3 version histories and verifies SHA-256 contents plus delete markers without assuming identical version IDs.
`replication-snapshot.sh` collects logs/config/ps; `replication-failure.sh` requires explicit opt-in.

## Mandatory Ubuntu live runbook
1. Resolve and approve immutable image digests; validate Compose and start both servers.
2. Verify separate source and target S3 endpoints (e.g. via isolated localhost bindings or approved proxy).
3. Create two disposable buckets, enable versioning and configure a supported replication rule using a version-matched `mc` CLI.
4. Capture the actual `mc replicate add`/`mc replicate ls` commands, version and redacted output.
5. Seed several objects, versions, metadata, tags, and delete markers. Use independent target credentials.
6. Run `replication_audit.py` with source/target endpoints, bucket names and output JSON. Record lag from first observation; it is a polling approximation, not a server-side replication metric.
7. Stop destination with opt-in script, write additional source versions, verify lag/failure, restart destination and re-audit.
8. For existing objects, run a documented version-compatible batch replication procedure and capture status.
9. Site replication is a distinct admin mechanism: verify prerequisites and supported CLI syntax before configuring. Do not equate bucket replication with site replication.
10. Record explicit PASS/FAIL/NOT TESTED for bucket, batch, site, delete-marker, lag and recovery scenarios.

## Constraints
No live replication rule, site replication or batch job has been configured in this environment.
`replication_audit.py` compares content/version multisets and cannot independently prove that replication
(not a separate upload) created the target objects. Save server-side replication rule/status evidence too.
No automatic deletion, no fake evidence, no NFS.
