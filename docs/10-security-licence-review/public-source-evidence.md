# DEV-914 — Public-source security and licence evidence

**Research date:** 2026-10-30  
**Evidence class:** Official public documentation and repository statements, **not** local Ubuntu runtime evidence.  
**Review scope:** Open-source `minio/minio` and independent fork `pgsty/silo`. Statements below are release/repository scoped, not an assertion about unpinned Docker images.

## Verified findings

| ID | Subject | Finding supported by public source | Evidence | Limitations |
|---|---|---|---|---|
| PS-01 | Upstream status | `minio/minio` repository states it was archived on 2026-04-25 and is no longer maintained. | https://github.com/minio/minio | Does not describe commercial MinIO/AIStor offerings. |
| PS-02 | MinIO licensing | MinIO's open-source source code is under GNU AGPLv3. | https://github.com/minio/minio ; https://github.com/minio/minio/blob/master/COMPLIANCE.md | Compliance obligations depend on usage and distribution; seek qualified legal review. |
| PS-03 | Silo identity | Silo is an independent PGSTY-maintained MinIO fork, not affiliated with MinIO, Inc. | https://github.com/pgsty/silo | Compatibility claims require independent testing. |
| PS-04 | Silo licensing | Silo server, console, mcli and shared packages are described as AGPL-3.0-or-later; project documentation is CC BY 4.0. | https://silo.pgsty.com/about/license/ | Review exact source tree, dependencies and redistributed artifacts before compliance conclusions. |
| PS-05 | Silo release | Project documents `RELEASE.2026-10-26T00-00-00Z`, source `c3ad836aed0d`, Console v2.5.1, silo-pkg v3.15.2, Go 1.27.3. | https://github.com/pgsty/silo | Release metadata is a maintainer statement; no image digest or local binary verified. |
| PS-06 | MinIO security policy | Upstream published a security policy describing supported latest releases and vulnerability reporting process. | https://github.com/minio/minio/blob/master/SECURITY.md | Archived repository status limits inference about ongoing updates. |
| PS-07 | MinIO advisories | GitHub repository publishes security advisories including 2026 authentication, replication, S3 Select and storage REST findings. | https://github.com/minio/minio/security/advisories | Advisory existence does not establish whether any specific image is affected. |
| PS-08 | Silo security policy | Fork maintains separate reporting and a supported current release line. | https://github.com/pgsty/silo/blob/main/SECURITY.md | Not proof that all vulnerabilities are known or resolved. |
| PS-09 | Silo advisory ledger | Official ledger documents CVEs and fork-local `SN-2026-*` security findings, fixes and release boundaries; SN IDs are not CVEs. | https://silo.pgsty.com/about/security-advisories/ | Fix applicability requires exact version/commit verification. |
| PS-10 | Silo supply chain | Project states releases include checksums, SPDX SBOMs, signed manifests and build attestations. | https://github.com/pgsty/silo | Claimed availability only; actual artifact signature/SBOM has not been downloaded and verified. |

## Concrete advisory examples

- MinIO upstream: `GHSA-hv4r-mvr4-25vw` (unsigned-trailer query-string authentication bypass), `GHSA-9c4q-hq6p-c237` (Snowball auto-extract authentication bypass), `GHSA-xh8f-g2qw-gcm7` (storage REST path traversal). See https://github.com/minio/minio/security/advisories/ .
- Silo: official ledger identifies `CVE-2026-41145` (unsigned-trailer authentication), `CVE-2026-40344` (Snowball authentication), `CVE-2026-42600` (storage REST path traversal), and fork-local `SN-2026-015` / `SN-2026-016` (object retention/lock authorization). See https://silo.pgsty.com/about/security-advisories/ .
- These are **published advisory records**, not independently reproduced vulnerabilities or proof of patch status for unpinned images. Silo's October release documentation and advisory ledger describe fix boundaries; confirm source commit and image digest before applying them to a deployment.

## Evidence-based comparison

1. **Maintenance:** Public evidence favors Silo for an actively maintained open-source release line relative to the archived `minio/minio` repository. This is not a performance or security ranking.
2. **Licence:** Both open-source server codebases have AGPL obligations. Silo documentation identifies `AGPL-3.0-or-later` and distinguishes documentation licensing; legal compliance must be assessed for the actual distribution scenario.
3. **Security:** Both have public advisory records; Silo publishes a detailed fork-specific ledger. Comparing advisory counts is not a valid measure of relative security.
4. **Supply chain:** Silo publicly describes SBOM/signing/attestation artifacts, but cryptographic verification and vulnerability scans remain undone.

## REVIEW REQUIRED — cannot be represented as completed

- Actual MinIO and Silo image digests, source-to-image reproducibility and deployed versions.
- Container vulnerability scanner findings, image SBOM contents and verified signatures.
- TLS endpoint handshake, IAM/STS enforcement, encryption at rest, audit logs and object-lock enforcement.
- Live exposure, privilege escalation, security regression or patch effectiveness.
- Full AGPL compliance analysis or legal opinion.

**Public-source review status:** COMPLETE for the ten scoped official-source findings above. **Phase 15 full runtime evidence gate:** INCOMPLETE. Do not convert source evidence into runtime PASS values.
