# Phase 7/8 remaining acceptance gaps

Object lock compliance and governance tests are **opt-in only** via `--enable-retention`, because they intentionally leave 2-day retained objects and can consume SSD. These tests must never run by default.

Implemented: lifecycle rule round-trip, SSE-S3, legal hold ON/OFF, governance/compliance opt-in, optional KMS, optional notification configuration, optional restricted IAM negative check, logical version mapping, SHA-256 manifest checks.

Still missing: lifecycle expiry observation over time, default retention scenario, notification destination delivery, full IAM provisioning/STS integration, verified CLI `mc diff` and Silo `mcli checksum verify` runs, signed security policy checks, actual MinIO/Silo live execution and evidence. These cannot be declared complete.
