# Phase 11 / DEV-910 — MinIO performance baseline

**Development:** Benchmark profiles, guarded Warp/fio execution, host/container resource capture, structured manifests, fio percentile parser, unit tests, and reporting skeleton implemented.
**Live results:** NONE. Do not label this phase performance-validated.

## Scope
Single-node MinIO and, if supported, distributed MinIO, tested separately on local SSD. NFS, remote storage, and production data excluded. Same profiles later used for Silo (DEV-913). Ubuntu machine: 8 CPU cores, 16GB RAM, ~100GB free SSD. One heavy stack at a time.

## Prerequisites
- Complete Phase 6 runtime validation and verified immutable MinIO image.
- Pin `warp --version`, `fio --version`, Docker version, OS, CPU, RAM and SSD model.
- Start only MinIO and monitoring; verify actual S3 endpoint and isolated disposable credentials.
- Ensure enough disk space for Warp-generated objects, fio test file, MinIO volumes, logs and OS reserve.
- Warp CLI options vary by version. Runner checks supported options using `warp <operation> --help` and fails closed when incompatible. Review the pinned Warp CLI's bucket naming, cleanup, TLS and mixed workload semantics before running.
- Some Warp operations need pre-existing objects. Execute the setup/seed workload required by the pinned CLI; never interpret an empty-bucket GET/LIST/DELETE failure as a storage regression.
- Use a disposable bucket and never share credentials or production endpoints.

## Commands
Dry-run plan (does not need Warp):
```
python3 scripts/benchmark/phase11.py --mode plan --out artifacts/dev910-plan
```
Warp (requires installed CLI, `WARP_ACCESS_KEY`, `WARP_SECRET_KEY`, dedicated endpoint):
```
python3 scripts/benchmark/phase11.py --mode warp --approve --endpoint 127.0.0.1:9000 --out artifacts/dev910-warp-run1
```
Fio (dedicated SSD test directory only, never MinIO's live data directory):
```
mkdir -p /path/to/dedicated-test-dir
touch /path/to/dedicated-test-dir/.dev910-fio-approved
python3 scripts/benchmark/phase11.py --mode fio --approve --fio-dir /path/to/dedicated-test-dir --out artifacts/dev910-fio-run1
```
Container/host metrics collection in another terminal:
```
bash scripts/benchmark/capture_resources.sh 300 artifacts/dev910-resources
```
Aggregate actual run manifests:
```
python3 scripts/benchmark/report.py artifacts/dev910-fio-run1/manifest.json --out artifacts/dev910-summary.json
```

## Metrics and acceptance
Record object size, operation, concurrency, repetition, warmup, duration, raw CLI output, exit code, p50/p95/p99 (when supported and correctly parsed), throughput, ops/s, CPU, memory, disk I/O and networking. fio JSON latency fields are converted to milliseconds. Warp output is **retained raw**, not falsely parsed into percentiles; pinned-version parser must be verified after obtaining an actual sample. Report summary marks those values unavailable.

Acceptance requires 3 valid repetitions for each supported profile, consistent configuration, recorded warmup, actual resource evidence, disk capacity gate, safe bucket cleanup, and documented errors. Do not claim latency/throughput without actual data. A zero exit code alone is not a performance PASS.

## Known development gaps
- Warp CLI flag compatibility and per-operation object preparation depend on installed version; runner fails closed on missing flags but does not automate all operation-specific preconditions.
- Warp `analyze --json` parser intentionally recognizes only an explicit normalized schema; actual Warp releases may use a different nested schema. Until a pinned-version sample is captured and adapter unit-tested, real Warp runs will be marked INCOMPLETE rather than reporting invented percentiles.
- No live benchmark data, charts, or measured Silo deltas exist.


## Implementation update
- Each Warp operation/size/repetition receives a unique disposable bucket and explicit `--benchdata` artifact. Warp normally prepares GET/LIST/DELETE workloads itself; confirm behavior with the pinned CLI. Never use `--noclear` against a shared bucket.
- Credentials are inherited from `WARP_ACCESS_KEY` and `WARP_SECRET_KEY`, never included in process arguments or manifests.
- `warp --version` and `warp <operation> --help` are recorded. Unsupported options cause fail-closed errors.
- `warp analyze <benchdata> --json` is captured for each successful benchmark. Metrics are accepted only when a tested schema adapter recognizes their units and fields.
- Fio performs three repetitions and extracts read/write bandwidth, IOPS and latency.
- `scripts/benchmark/report.py` produces summary JSON, CSV, Markdown, and PNG charts only when actual numeric metrics exist.
- A complete development acceptance gate requires a real Warp JSON sample and tested adapter; **not yet achieved**. Do not mark Phase 11 fully complete until this gate and Ubuntu run pass.


## Integrated Option B scenario result (2026-10-30)

DEV-910: reference MinIO PUT/GET 185/245 MiB/s, p95 42/28 ms. These are generated illustration values, not Warp output.

See `documentation/scenario_results/INTEGRATED_RESULTS.md` in the submission root.
