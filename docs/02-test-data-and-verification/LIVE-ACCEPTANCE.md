# DEV-906 — Live acceptance checklist (not yet executed)

## Preconditions
- Phase 6 lab starts successfully with verified pinned MinIO and Silo images.
- Actual host CPU/RAM/disk, Docker/Compose versions and image digests recorded.
- Disposable test buckets, local SSD storage budget, and TLS trust configured.
- Environment credentials supplied securely; do not save in evidence.
- Run against MinIO and Silo **separately**.

## A. Profile B dataset (5–10 GiB)
1. `python3 scripts/dataset/plan_profile_b.py --gib 5 --write-plan artifacts/profile-b-plan.json`
2. Check free SSD for source data + version copies + both product stores + replication + benchmark scratch; reduce concurrent usage, not the agreed dataset target.
3. Generate only after budget approval:
   `python3 scripts/dataset/generate.py --output datasets/generated --sizes "$(python3 -c 'import json;print(",".join(map(str,json.load(open("artifacts/profile-b-plan.json"))["sizes"])))')" --seed 906`
4. Independently recompute all local SHA-256 values and capture output.

## B. Live uploads and version mapping
1. Create isolated buckets and enable versioning before seeding.
2. Run `seed.py` separately for MinIO and Silo, with `--versions 2`, using same source data.
3. Save separate seed receipts (`artifacts/minio-seed.json`, `artifacts/silo-seed.json`).
4. Capture both remote manifests with `manifest.py --hash-content`.
5. Compare logical revisions:
   `python3 scripts/verification/logical_compare.py artifacts/minio-seed.json artifacts/minio-manifest.json artifacts/silo-seed.json artifacts/silo-manifest.json --output artifacts/logical-comparison.json`
6. PASS only when all logical revisions and SHA-256 match; product-generated version IDs are not expected to match.

## C. Required remaining scenarios
- Generate delete markers and prove ListObjectVersions and restoration behavior.
- Configure metadata, tags, lifecycle and versioning; verify expiration timing with recorded wait.
- Object lock governance/compliance, legal hold and retention must use isolated disposable buckets; never assume compliance-locked objects can be removed early.
- IAM policies, service accounts, STS and notification/replication fixtures are required where supported and available.
- Exercise negative controls: missing object, corrupted bytes, missing version, changed tag.
- Run `mc diff` and Silo `mcli checksum verify` using **verified supported syntax** from the pinned CLI versions; record command output, exit codes and screenshots.
- Capture exact release tags/digests, server logs, bucket config, object counts, command outputs and cleanup procedures.

## Pass criteria
No missing logical object/version, no unexpected metadata/tag/retention mismatch, full byte hashes verified, negative controls detected, all applicable fixture scenarios executed, independent CLI checks recorded, and raw evidence linked in DEV-906 README.

**Status: BLOCKED — live Docker/S3 environment unavailable in the assistant workspace. No server-side PASS asserted.**
