# Full repository file inventory and static review

Reviewed **248** non-Git files; **39** flagged for follow-up. Every file in the distribution has an entry in `FULL-FILE-AUDIT.json` with path, bytes, SHA-256 and checks.

## Audit boundaries

- Static checks are not semantic verification of every function or requirement.
- No live Ubuntu/Docker/MinIO/Silo/Warp execution occurred.
- No real image digest, S3 feature, or benchmark results can be certified from this audit.
- Git history and remote GitHub project board are not audited.

Git internal files excluded from source review: 18 (the Git history requires a separate security/history audit).

## Unit tests

- benchmark: 18 tests; exit 0
- compatibility: 21 tests; exit 0
- data-management: 9 tests; exit 0
- distributed: 3 tests; exit 0
- final: 7 tests; exit 0
- replication: 6 tests; exit 0
- s3-core: 9 tests; exit 0
- security: 5 tests; exit 0
- verification: 5 tests; exit 0

## Files flagged for follow-up

- `.env.example`: Contains unresolved verified-image placeholder
- `docs/01-repo-versions-and-lab/evidence/.gitkeep`: Evidence file present: provenance must be checked
- `docs/01-repo-versions-and-lab/evidence/remediation-check-1.txt`: Evidence file present: provenance must be checked
- `docs/01-repo-versions-and-lab/evidence/remediation-check-2.txt`: Evidence file present: provenance must be checked
- `docs/01-repo-versions-and-lab/evidence/remediation-check-3.txt`: Evidence file present: provenance must be checked
- `docs/01-repo-versions-and-lab/evidence/remediation-check-4.txt`: Evidence file present: provenance must be checked
- `docs/01-repo-versions-and-lab/evidence/remediation-static-checks.txt`: Evidence file present: provenance must be checked
- `docs/02-test-data-and-verification/evidence/.gitkeep`: Evidence file present: provenance must be checked
- `docs/02-test-data-and-verification/evidence/syntax-check.txt`: Evidence file present: provenance must be checked
- `docs/02-test-data-and-verification/evidence/unit-tests.txt`: Evidence file present: provenance must be checked
- `docs/03-minio-feature-validation/evidence/.gitkeep`: Evidence file present: provenance must be checked
- `docs/03-minio-feature-validation/evidence/data-management-unit-tests.txt`: Evidence file present: provenance must be checked
- `docs/03-minio-feature-validation/evidence/s3-core-unit-tests.txt`: Evidence file present: provenance must be checked
- `docs/03-minio-feature-validation/evidence/syntax-check.txt`: Evidence file present: provenance must be checked
- `docs/03-minio-feature-validation/evidence/unit-tests.txt`: Evidence file present: provenance must be checked
- `docs/04-minio-distributed-mode/evidence/.gitkeep`: Evidence file present: provenance must be checked
- `docs/04-minio-distributed-mode/evidence/static-checks.txt`: Evidence file present: provenance must be checked
- `docs/04-minio-distributed-mode/evidence/unit-tests.txt`: Evidence file present: provenance must be checked
- `docs/05-minio-replication/evidence/.gitkeep`: Evidence file present: provenance must be checked
- `docs/05-minio-replication/evidence/development-gate.json`: Evidence file present: provenance must be checked
- `docs/05-minio-replication/evidence/static-check-1.txt`: Evidence file present: provenance must be checked
- `docs/05-minio-replication/evidence/static-check-2.txt`: Evidence file present: provenance must be checked
- `docs/05-minio-replication/evidence/static-check-3.txt`: Evidence file present: provenance must be checked
- `docs/05-minio-replication/evidence/static-check-4.txt`: Evidence file present: provenance must be checked
- `docs/06-minio-performance-baseline/evidence/.gitkeep`: Evidence file present: provenance must be checked
- `docs/06-minio-performance-baseline/evidence/development-check-1.txt`: Evidence file present: provenance must be checked
- `docs/06-minio-performance-baseline/evidence/development-check-2.txt`: Evidence file present: provenance must be checked
- `docs/06-minio-performance-baseline/evidence/development-check-3.txt`: Evidence file present: provenance must be checked
- `docs/06-minio-performance-baseline/evidence/development-check-4.txt`: Evidence file present: provenance must be checked
- `docs/06-minio-performance-baseline/evidence/final-development-check-1.txt`: Evidence file present: provenance must be checked
- `docs/06-minio-performance-baseline/evidence/final-development-check-2.txt`: Evidence file present: provenance must be checked
- `docs/06-minio-performance-baseline/evidence/final-development-check-3.txt`: Evidence file present: provenance must be checked
- `docs/07-silo-functional-validation/evidence/.gitkeep`: Evidence file present: provenance must be checked
- `docs/07-silo-functional-validation/evidence/dev911-empty-index.json`: Evidence file present: provenance must be checked
- `docs/07-silo-functional-validation/evidence/dev911-gate-static.json`: Evidence file present: provenance must be checked
- `docs/08-compatibility-diff/evidence/.gitkeep`: Evidence file present: provenance must be checked
- `docs/09-silo-performance-comparison/evidence/.gitkeep`: Evidence file present: provenance must be checked
- `docs/10-security-licence-review/evidence/.gitkeep`: Evidence file present: provenance must be checked
- `docs/11-evaluation-report/evidence/.gitkeep`: Evidence file present: provenance must be checked
