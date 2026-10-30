# Evidence-based technical gates — 2026-10-30

## Verified against upstream publications (not local execution)
- MinIO last upstream release: `RELEASE.2025-10-15T17-29-55Z` source commit short `9e49d5e`, official GitHub release: https://github.com/minio/minio/releases . Release instructions require a source-built container; **no official Docker image digest has been verified here**.
- Silo selected release: `RELEASE.2026-10-26T00-00-00Z` source `c3ad836aed0d8a7d23c2e44a5eaa3009d08525e3`: https://github.com/pgsty/silo/releases . The published standard manifest digest is in `.env.example`; it still requires local pull/inspect and architecture verification.
- Warp documentation confirms `warp analyze <benchmark.csv.zst> --json`, https://docs.min.io/warp/reference/cli/analyze/ . This **does not establish the output JSON schema**. Existing `warp_metrics.py` only accepts normalized metrics and must fail closed on native schema until a real sample is tested.

## Runtime gates on Ubuntu
1. Populate `.env` with non-committed credentials and *real* `@sha256:` references for all images. For MinIO, build from verified upstream tag and record Git SHA, Dockerfile, base-image digest, image ID, architecture, build logs and `docker image inspect` result; local image IDs are not equivalent to published manifest digests.
2. Export `.env` variables to shell and run `python3 scripts/lab/verify_runtime.py --output artifacts/runtime-preflight.json --compose compose/minio/single/compose.yaml --compose compose/minio/distributed/compose.yaml --compose compose/silo/single/compose.yaml --compose compose/silo/distributed/compose.yaml --compose compose/proxy/compose.yaml --compose compose/monitoring/compose.yaml`. The script **fails closed** if an image lacks digest or cannot be pulled or Compose config fails. Local source-built MinIO needs an explicit separate provenance policy before this gate can pass.
3. Run `warp --version`, `warp analyze --help`, then capture a genuine `warp analyze <raw.csv.zst> --json` output. Save raw and add a version-specific adapter with fixture and negative controls. Do not substitute a hand-authored normalized sample.
4. Seed test data, run `scripts/verification/seed_integrity.py` for MinIO and Silo, and record raw SHA-256, metadata, tags and version-ID checks. Retention, legal hold, multipart, `mc diff` and `mcli checksum verify` are **separate mandatory acceptance cases**, not implied by seed integrity.
5. For every PASS/FAIL retain raw commands, outputs, image digests, run environment and SHA-256 evidence. Mark unrun cases EXECUTION REQUIRED.

## Gate status
- Public release metadata: SOURCE_VERIFIED.
- Silo published digest: SOURCE_VERIFIED, LOCAL_PULL_REVIEW_REQUIRED.
- MinIO image: BLOCKED (source build/provenance required).
- Supporting image digests: BLOCKED (pull/inspect required).
- Warp native JSON adapter: BLOCKED (real output sample required).
- Compose config against actual pulled images: BLOCKED (Docker unavailable in authoring environment).
- Live S3 metadata/tags/retention/multipart/mc/mcli: EXECUTION REQUIRED.

Do not treat a unit test as a live storage acceptance test.
