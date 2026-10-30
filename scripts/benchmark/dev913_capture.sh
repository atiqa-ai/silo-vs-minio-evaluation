#!/usr/bin/env bash
set -euo pipefail
[[ $# -eq 2 ]] || { echo "Usage: $0 minio|silo NEW_OUTPUT_DIR" >&2;exit 2; }
ENGINE="$1";OUT="$2"
[[ "$ENGINE" == minio || "$ENGINE" == silo ]] || exit 2
[[ ! -e "$OUT" ]] || { echo "Output path already exists" >&2;exit 2; }
mkdir -p "$OUT"
date -u +%Y-%m-%dT%H:%M:%SZ > "$OUT/timestamp.txt"
uname -a > "$OUT/uname.txt"
{ command -v lscpu >/dev/null && lscpu; } > "$OUT/cpu.txt" 2>&1 || true
{ command -v free >/dev/null && free -h; } > "$OUT/memory.txt" 2>&1 || true
{ command -v lsblk >/dev/null && lsblk -o NAME,SIZE,MODEL,ROTA,TYPE,MOUNTPOINTS; } > "$OUT/disks.txt" 2>&1 || true
{ command -v docker >/dev/null && docker version; } > "$OUT/docker-version.txt" 2>&1 || true
{ command -v docker >/dev/null && docker stats --no-stream; } > "$OUT/docker-stats.txt" 2>&1 || true
{ command -v warp >/dev/null && warp --version; } > "$OUT/warp-version.txt" 2>&1 || true
{ command -v fio >/dev/null && fio --version; } > "$OUT/fio-version.txt" 2>&1 || true
echo "Collected available host/tool evidence for $ENGINE. Verify image digest, filesystem and runtime isolation manually."
