# Immutable image pinning and verification

Silo standard image selected from official 2026-10-26 release: `docker.io/pgsty/silo:RELEASE.2026-10-26T00-00-00Z@sha256:7bb2aff6b89efe1cb1303c10fc21d579447434ed06649ac9ec05a5e2dbf30ad7`. Source: https://silo.pgsty.com/blog/release/silo-20261026/ . **Published digest is not locally pulled/verified**.

MinIO and supporting images remain **BLOCKED** until a genuine immutable digest and image provenance are established; do not replace with fabricated sha256 values. MinIO CE may need a reproducible source build; record source tag/commit, base image, build logs and resulting digest.

On Ubuntu: `docker pull "$SILO_IMAGE"`; `docker image inspect "$SILO_IMAGE" --format "{{json .RepoDigests}}"`; preserve output. Repeat for every image. `docker compose config` must succeed with actual `.env` values. Never use `latest`.
