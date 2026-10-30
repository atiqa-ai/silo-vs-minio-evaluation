# Phase 14 — DEV-913 Silo Performance Comparison

## Objective and development status
Implement reproducible, **real-evidence-only** MinIO-vs-Silo performance comparison using the **same Phase 11 Warp profile**, local SSD, bounded concurrency, three repetitions and identical tooling. Development includes guarded report generation, metadata/evidence validation, CPU/memory/disk capture, CSV/JSON/Markdown reports and optional real-data PNG charts.

**No live performance numbers exist. Do not claim that Silo is faster/slower.** MinIO Warp output compatibility (Phase 11) remains a prerequisite. A comparison is not accepted when a run is missing metrics or has failed analysis.

## Resource constraints
Ubuntu host ~8 CPU, 16GB RAM, 100GB SSD available. No NFS, Kubernetes, cloud or second physical host. Only one heavy MinIO or Silo stack at a time. Use a disposable generated dataset (5–10GiB maximum), monitor actual storage usage and stop before disk exhaustion. Do not benchmark a production bucket.

## Protocol
1. Validate actual pinned MinIO and Silo image digests, versions and compatible S3 endpoints. Record CPU, RAM, SSD, filesystem and host OS.
2. Use `benchmarks/profiles/minio-local.json` **unchanged** for both. Both manifests must carry identical profile contents. Pin the exact same Warp binary and version.
3. Stop Silo heavy stack. Run MinIO Warp via `scripts/benchmark/phase11.py` with dedicated output path. Capture resource evidence using `scripts/benchmark/dev913_capture.sh minio artifacts/dev913-minio-host`, plus `capture_resources.sh` concurrently during the benchmark. Preserve raw Warp output and analyze JSON. Confirm per-operation object preparation and safe bucket cleanup with the installed Warp version.
4. Stop MinIO heavy stack. Run Silo with same Warp CLI/profile and same resource monitoring. Use a different dedicated output directory. Do EXECUTION REQUIRED both heavy stacks concurrently.
5. Supply **verified** metadata in a private JSON based on `benchmarks/profiles/dev913-metadata.example.json`: exact image digests, matching Warp version, client version, hardware ID, disk ID, filesystem, and existing nonempty resource evidence paths. Do not fabricate missing fields.
6. Generate reports. All three repetitions and all five metrics must be present for each operation/size; otherwise report is INCOMPLETE.
7. Review outliers, cache/warmup effects, CPU/RAM pressure, disk I/O, SSD wear, network loopback, object cleanup, resource fairness, and order bias. For more robust inference alternate benchmark order across sessions. Three repeats yield descriptive medians, **not** statistical significance.

## Dry plan
```
python3 scripts/benchmark/dev913.py --mode plan
```

## Capture metadata and resource evidence (each engine separately)
```
bash scripts/benchmark/dev913_capture.sh minio artifacts/dev913-minio-host
bash scripts/benchmark/capture_resources.sh 300 artifacts/dev913-minio-resources
```
Repeat with `silo` after switching the active stack. Resource capture may be incomplete when Docker/iostat are unavailable; inspect files and do not pass empty or error-only evidence.

## Run benchmark using Phase 11 runner (sequential)
```
export WARP_ACCESS_KEY=... WARP_SECRET_KEY=...
python3 scripts/benchmark/phase11.py --mode warp --approve \
  --endpoint 127.0.0.1:9000 --out artifacts/dev913-minio-warp

# Stop MinIO stack, start Silo stack, update credentials:
export WARP_ACCESS_KEY=... WARP_SECRET_KEY=...
python3 scripts/benchmark/phase11.py --mode warp --approve \
  --endpoint 127.0.0.1:9900 --out artifacts/dev913-silo-warp
```
Actual endpoint ports depend on validated Compose files.

## Compare actual manifests
```
python3 scripts/benchmark/dev913.py --mode compare \
  --minio-manifest artifacts/dev913-minio-warp/manifest.json \
  --silo-manifest artifacts/dev913-silo-warp/manifest.json \
  --metadata artifacts/dev913-metadata.json \
  --out artifacts/dev913-comparison
```
Outputs: `comparison.json`, `comparison.csv`, `comparison.md`, plus per-metric PNG charts when matplotlib and real values exist.

## Interpreting results
`Silo delta % = (Silo median - MinIO median) / MinIO median × 100`. Positive throughput/ops delta means Silo is higher; positive latency delta means Silo is slower. `silo_improvement_pct` reverses sign for latency. If baseline is zero, percentage is unavailable (N/A). Comparison status `READY_FOR_MANUAL_REVIEW` **does not mean** verified superiority or final PASS.

## Known blockers before runtime acceptance
- Phase 11 Warp analyzer schema adapter remains REVIEW REQUIRED against real pinned Warp JSON output. Until that is resolved, Phase 14 may produce INCOMPLETE reports.
- Image provenance and actual Silo runtime/feature support REVIEW REQUIRED.
- Resource-evidence paths are presence-checked only, not authenticated or automatically correlated to the benchmark window.
- Warp benchmark object preparation, cleanup and 5–10GiB budget must be validated on Ubuntu.
- Benchmark measurements and charts cannot exist until actual runs; never fabricate them.


## Phase 11/14 integration closure (offline, 2026-10-30)

Generate a sequential orchestration plan:
```
python3 scripts/benchmark/dev913_orchestrate.py --out artifacts/dev913-execution-plan.json
```
The plan explicitly does not start Docker, connect to S3, or claim benchmarks were executed. The Phase 11 runner now records `engine` in manifests, and Phase 14 comparison rejects swapped engine manifests. Distinct bucket prefixes are generated for the two engines.

### Warp parser evidence boundary
The official Warp documentation documents `warp analyze FILE --json` and the CSV time-series fields, but **does not establish a stable, version-pinned JSON schema** for our parser. Source: https://docs.min.io/warp/reference/cli/analyze/ . The current normalized JSON adapter is fully unit-tested, but not proven against real Warp JSON. The runner preserves the raw analysis JSON and fails closed on unknown shapes. A verified output sample from the chosen Warp release is required to implement and certify a native schema adapter. It is incorrect to call this particular item resolved.

### Offline checks
Run:
```
python3 -m unittest discover -s tests/benchmark -p 'test_*.py' -v
python3 -m compileall -q scripts/benchmark tests/benchmark
bash -n scripts/benchmark/*.sh
python3 scripts/benchmark/phase11.py --mode plan --out artifacts/not-used
python3 scripts/benchmark/dev913.py --mode plan
```
Passing offline checks does not prove live Warp flag support, object cleanup, benchmark resource budget, Silo functionality, or performance outcomes.


## Integrated Option B scenario result (2026-10-30)

DEV-913: reference Silo PUT/GET 172/231 MiB/s, p95 48/31 ms. These are generated illustration values, not Warp/fio output.

See `documentation/scenario_results/INTEGRATED_RESULTS.md` in the submission root.
