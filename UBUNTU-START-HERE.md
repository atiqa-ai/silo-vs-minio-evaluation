# Ubuntu execution — controlled preflight (Option B)

This archive contains a development snapshot, **not** completed live acceptance evidence.
Do not execute destructive cleanup (`docker compose down -v`) on data you need.

## 1. Inspect and prepare

```bash
sudo apt update
sudo apt install -y python3 python3-venv git jq openssl
python3 -m venv .venv
. .venv/bin/activate
python -m pip install boto3 PyYAML
cp .env.example .env
```

Install Docker Engine + Compose v2 following the official Docker Ubuntu guide, then verify:

```bash
docker version
docker compose version
```

## 2. Resolve image references before deployment

`.env.example` intentionally contains REVIEW REQUIRED digest placeholders. Do not replace them with guessed values. Inspect `scripts/lab/resolve-images.sh` and `docs/governance/IMAGE-PROVENANCE.md`. Verify upstream releases, pull/build images, and record the actual immutable digests. Keep secrets out of Git.

```bash
set -a; . ./.env; set +a
python3 scripts/lab/verify_runtime.py --output artifacts/option-b-runtime-preflight.json --compose compose/minio/single/compose.yaml
```

For all Compose files run `bash scripts/lab/ubuntu-compose-validate.sh`. The preflight must fail until all immutable image references have been verified. A failing preflight means **do not** record PASS.

## 3. Dataset integrity

For version-specific verification use `--versions 2` when seeding. `seed_integrity.py` now rejects absent/null version IDs. It checks content SHA-256, length, tags, metadata and version identity. Object Lock, retention, multipart and mc/mcli remain independent live acceptance cases.

## 4. Warp

`warp_preflight.py` intentionally fails closed until real Warp binary + native JSON schema have been validated. Do not report generated throughput as benchmark evidence.

## 5. Completion

Follow `docs/governance/OPTION-B-ACCEPTANCE.md` for DEV-904 through DEV-915. Every runtime PASS needs raw outputs, timestamps, exact versions and comparable MinIO/Silo runs.
