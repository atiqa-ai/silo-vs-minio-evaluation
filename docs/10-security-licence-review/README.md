# Phase 15 — DEV-914 Security and Licensing Review

## Scope and acceptance
Compare MinIO and Silo **at verified image versions**, with the same security configuration and credentials model. Assess IAM/policies and least privilege; STS and invalid credentials; TLS, transport security, at-rest encryption and key management; network exposure; audit logs; object lock/retention; image CVEs, SBOM and supply-chain provenance; repository/container licence and redistribution terms.

**Status: offline development implemented; runtime and legal evidence REVIEW REQUIRED.** Do not claim either engine secure, compliant, or feature-equivalent without evidence.

## Static audit
```
python3 scripts/security/dev914.py --out artifacts/dev914-static
```
The audit scans Compose files for selected high-risk patterns and creates `static-audit.json`, `static-findings.csv`, `evidence-gate.json` and `review.md`. It is a limited heuristic scan, not a full security scanner. It does not read `.env` secrets.

## Evidence collection on an authorized disposable lab
1. Record immutable image reference (`name@sha256:...`), image inspect digest, version and build date for each engine. Preserve original outputs.
2. Inspect exact upstream repository licence at the pinned source commit, SPDX identifier, third-party notices and any licence differences between fork and original. Record source URLs, access date, hashes, and unresolved legal questions. No licence conclusions based solely on a project name.
3. Capture `docker compose config` with secrets redacted; inspect port binding, privileged mode, writable volumes, TLS and least-privilege configuration.
4. Run existing `scripts/testing/iam_sts.py`, `advanced_s3.py`, `silo_advanced_parity.py` and `dev912_extended.py` only after validating their CLI and safety preconditions. Preserve real HTTP error codes, raw outputs, and config snapshots.
5. For each pinned image, use an installed and version-recorded vulnerability scanner such as Trivy/Grype, retaining machine-readable JSON and scanner database timestamp. Scanner results are not proof of exploitability; absence of findings is not proof of safety.
6. Collect SBOM from pinned image with an installed SBOM tool (e.g. Syft), save tool version and JSON, and inspect dependencies and licence inventory. Do not invent SBOM components.
7. Evaluate TLS trust chain and hostname verification in the actual endpoint, verify encrypted transport with real connections; document any explicitly insecure localhost-only tests.
8. Fill `benchmarks/profiles/dev914-evidence.example.json` with **real evidence paths**, including source and versions. Run `--evidence-manifest`. The gate checks file presence only, not authenticity or security correctness.
9. Manually review results and document differences, severity, mitigation, reproducibility and residual risks.

## Evidence gate
```
python3 scripts/security/dev914.py \
  --evidence-manifest artifacts/dev914-evidence.json \
  --out artifacts/dev914-reviewed
```
Every check requires a status and nonempty evidence file. `NOT_SUPPORTED` is not a PASS. Human review is mandatory.

## Safety
- No production buckets, credentials, or public endpoints. No automatic vulnerability exploitation.
- No secrets in evidence bundles or Git. Redact authorization headers, tokens, credentials and private keys.
- No claims of formal compliance certification or legal advice.
- Ubuntu execution, licence verification, CVE scans and actual security parity are OPEN.

## Completed official public-source review
See [`public-source-evidence.md`](public-source-evidence.md) and [`public-source-evidence.json`](public-source-evidence.json) for the ten cited official-source findings collected on 2026-10-30. This is **not** runtime validation; the security evidence gate remains incomplete until real execution and image verification.
