#!/usr/bin/env bash
set -euo pipefail
[[ $# -eq 2 ]] || { echo "Usage: $0 <seconds> <output-dir>" >&2;exit 2; }
SECONDS="$1";OUT="$2"
[[ "$SECONDS" =~ ^[0-9]+$ ]] && (( SECONDS >= 1 && SECONDS <= 3600 )) || exit 2
mkdir -p "$OUT"
for ((i=0;i<SECONDS;i++)); do
  printf '%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$OUT/timestamps.txt"
  docker stats --no-stream --format '{{json .}}' >> "$OUT/docker-stats.jsonl" 2>> "$OUT/errors.log" || true
  if command -v iostat >/dev/null; then iostat -dx 1 1 >> "$OUT/iostat.txt" 2>> "$OUT/errors.log" || true; else sleep 1; fi
done
