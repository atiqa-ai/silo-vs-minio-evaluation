# DEV-906 — generated Dataset and Verification Toolkit

**Status:** Toolkit implemented and unit-tested; S3 integration and acceptance evidence OPEN.

## Goal
Generate generated objects, seed isolated MinIO/Silo buckets, capture per-version manifests and detect corruption or missing metadata.

## Environment
Profile B user-confirmed; actual Docker/S3 environment, pinned image digests and live test date not yet recorded.

## Prerequisites
Python 3.9+; `boto3` in an isolated environment for S3 operations; `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` supplied outside Git. Use a disposable test bucket only.

## Procedures (run from repository root)
1. Small deterministic smoke dataset:
   `python3 scripts/dataset/generate.py --output datasets/generated --sizes 1024,65536,1048576 --seed 906`
   Expected: 3 generated files and local SHA-256 inventory.
2. Optional S3 seed after Phase 6 lab validation:
   `python3 scripts/dataset/seed.py --data datasets/generated --bucket dev906-test --endpoint https://localhost:9000 --versions 2 --output artifacts/seed-results.json`
   Expected: 6 versioned uploads if bucket already exists. TLS CA must be trusted by the client.
3. Remote inventory (after seeding):
   `python3 scripts/verification/manifest.py --endpoint https://localhost:9000 --bucket dev906-test --hash-content --output artifacts/minio-manifest.json`
   Expected: version-level metadata, tags and SHA-256.
4. Compare two inventories:
   `python3 scripts/verification/compare.py artifacts/minio-manifest.json artifacts/silo-manifest.json`
   Expected: exit 0 only when matching identities and available comparable fields agree.
5. Unit tests:
   `python3 -m unittest discover -s tests/data-management -p 'test_*.py' -v`
   Expected: deterministic generation, no overwrite, missing object/version, altered bytes, tag mismatch, multipart ETag control all PASS.

## Coverage and limitations
- generated KB/MB objects and arbitrary explicit byte sizes; 1–5 GB objects are supported by streaming generation but have not been generated or benchmarked.
- Flat/deep keys, repeatable tags and metadata, versioned uploads.
- Manifest includes key, version ID, size, ETag, metadata, tags, optional SHA-256, retention and legal-hold fields, plus delete markers.
- ETags are **not** treated as MD5 content hashes. For actual byte-level verification use `--hash-content`.
- Object-lock retention/legal hold, lifecycle, notification, replication, STS/IAM and delete-marker seeding remain Phase 7 integration gaps; they require safe, scenario-specific setup and evidence.
- Comparing separately seeded versioned deployments needs a logical version mapping; raw S3 version IDs are product-generated and cannot be assumed equal.
- `mc diff` and Silo `mcli checksum verify` cross-checks are not yet executed.

## Results
Unit test output to be recorded after execution. No live MinIO/Silo integration PASS claimed.

## Findings
Phase 6 live lab validation remains OPEN. No 5–10 GB dataset generated to avoid unexpected SSD usage.

## Reproduce / cleanup
Generated data is ignored by Git. Remove it only after explicit approval. Do EXECUTION REQUIRED `docker compose down -v` without approval.
