# Phase 13 — DEV-912 S3 Compatibility and Edge Cases

## Development scope
The identical `s3_compatibility.probe()` is executed against MinIO and Silo, sequentially, using disposable unique buckets. It checks missing object and missing bucket errors, PUT/GET byte integrity and metadata, ETag properties, versioning/delete markers, multipart abort, and bounded concurrent overwrites. The same boto3 client configuration is used for both. `dev912_report.py` produces CSV, JSON, Markdown reports. The comparison preserves HTTP status and S3 error code, while excluding server-generated request IDs and version IDs.

**Development checks are not live test results.** No Silo/MinIO API requests were made during static development.

## Execution prerequisites
- Pin and validate MinIO and Silo images, Docker Compose, boto3/botocore versions and endpoint TLS.
- Use isolated lab credentials and disposable buckets only. generated data, no production endpoints.
- Run one heavy stack at a time; preserve same test configuration for each.
- Supply `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`, `SILO_ACCESS_KEY`, `SILO_SECRET_KEY` through the local environment, never source code.
- Do not infer an S3 standards violation solely from different errors or ETags. Verify the AWS S3 API specification and relevant configuration.
- The script retains created buckets for evidence. Clean only the generated buckets after verifying object versions and required evidence.

## Dry plan
```
python3 scripts/testing/s3_compatibility.py --mode plan --out artifacts/dev912-plan
```

## Live parity
```
python3 scripts/testing/s3_compatibility.py --mode run --approve \
  --minio-endpoint http://127.0.0.1:9000 \
  --silo-endpoint http://127.0.0.1:9900 \
  --allow-insecure-http --workers 4 --out artifacts/dev912-run001
python3 scripts/testing/dev912_report.py \
  --input artifacts/dev912-run001/result.json --out artifacts/dev912-report001
```

## Acceptance
- Each engine must execute the same cases and produce raw JSON evidence.
- MATCH means the normalized observed protocol fields agree, not that all AWS S3 behaviors are proven.
- DIFFERENT_REVIEW requires manual investigation; ERROR/EXECUTION REQUIRED is never counted as success.
- HTTP status and error code are compared; server-generated request IDs, timing, version IDs are not.
- Extended scenarios (invalid signature, malformed XML, conditional requests, pagination, copy-object, multipart completion failure, simultaneous readers/writers, IAM) remain outside this initial suite and must be closed before claiming complete DEV-912 coverage.
- Ubuntu runtime execution and real outputs remain OPEN.

## Extended edge-case suite (development closure)

`dev912_extended.py` adds 12 bounded scenarios: intentionally incorrect signing secret,
unsigned requests, conditional GET/PUT, paginated listing, server-side copy,
invalid multipart completion, valid multipart completion and byte verification,
parallel readers/writers, range GET, prefix filtering, and invalid part number.
The identical probe implementation executes against both endpoints and stores separate
raw results. The suite uses a disposable unique bucket per engine and does not remove
objects automatically. It does not claim that every possible S3 edge case is covered.

```bash
python3 scripts/testing/dev912_extended.py --mode plan --out artifacts/dev912-ext-plan
python3 scripts/testing/dev912_extended.py --mode run --approve \
  --minio-endpoint http://127.0.0.1:9000 \
  --silo-endpoint http://127.0.0.1:9900 \
  --allow-insecure-http --workers 4 --out artifacts/dev912-ext-run001
python3 scripts/testing/dev912_report.py \
  --input artifacts/dev912-ext-run001/result.json --out artifacts/dev912-ext-report001
```

### Important acceptance conditions

- Static development is distinct from live S3 compatibility acceptance.
- Error-code differences are classified `DIFFERENT_REVIEW`, not automatically noncompliant.
- A `MATCH` where both engines return `UNEXPECTED_SUCCESS` is not a successful test:
  the overall gate must reject unexpected successes.
- Verify both baseline and extended suites, pinned SDK and server versions, actual
  HTTP statuses, errors, object integrity, and evidence before claiming acceptance.
- Malformed raw XML requests are not covered by boto3 because the SDK validates/serializes
  them; a separate raw HTTP harness would be required for strict malformed-wire testing.
