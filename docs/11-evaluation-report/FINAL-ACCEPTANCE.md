# DEV-915 / Epic Definition of Done — Acceptance Tracker

| Epic acceptance requirement | Evidence needed | Current status |
|---|---|---|
| Rebuildable local Docker Compose lab, rebuild time recorded | `docker compose up`, `ps`, image digest, timed rebuild logs | REVIEW REQUIRED |
| MinIO baseline for S3, object lock, lifecycle, resilience, replication | Raw command logs, manifests, tests and screenshots | REVIEW REQUIRED |
| Same tests rerun unchanged on Silo, differences categorized and severity assigned | Matching run IDs, versions, raw MinIO/Silo outputs | REVIEW REQUIRED |
| Silo compatibility conditions O01–O08 applicability decisions | Exact official wording, configuration and test evidence | REVIEW REQUIRED |
| Warp performance comparison under identical conditions | Pinned Warp version, raw JSON, repetition data, resource captures | REVIEW REQUIRED |
| Security, licence and maintenance assessment, exit plan | Public-source review present; runtime CVE/SBOM/TLS evidence missing | PARTIAL |
| Single capability matrix and defensible recommendation | Generator present; all runtime rows currently REVIEW REQUIRED | PARTIAL |
| Public repo with evidence, clean history and no secrets | Git remote, history scan, screenshots, review | REVIEW REQUIRED |

## Decision policy
- **GO:** Every mandatory feature is verified, no unacceptable regression, security/licensing reviewed, owner approves.
- **GO WITH CONDITIONS:** Evidence complete, known limitations bounded, documented mitigations and acceptance owner sign-off.
- **NO-GO:** Critical verified failures or unacceptable risks; also **NO-GO for unconditional replacement** when required evidence is absent.
- A static unit test or generated dataset is never proof of real MinIO/Silo behavior.

## Completion boundary
All report-generation code may be complete while the epic Definition of Done remains open. Do not relabel unexecuted requirements as passed.

## Development audit (2026-10-30)

Offline code audit and 78 unit tests passed. See `docs/governance/DEVELOPMENT-AUDIT.md`. This does not change any runtime acceptance status above.


## Integrated Option B scenario result (2026-10-30)

DEV-915: reference comparison favors MinIO in this illustrative scenario; real Option B runtime acceptance remains OPEN until required evidence is obtained.

See `documentation/scenario_results/INTEGRATED_RESULTS.md` in the submission root.
