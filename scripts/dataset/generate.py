#!/usr/bin/env python3
"""Generate reproducible synthetic objects and a local SHA-256 inventory."""
import argparse, hashlib, json, os, random
from pathlib import Path

def make_bytes(seed, count):
    rng = random.Random(seed)
    while count:
        block = rng.randbytes(min(count, 1024 * 1024))
        yield block
        count -= len(block)

def generate(root, sizes, seed, force=False):
    root = Path(root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    records = []
    for index, size in enumerate(sizes):
        if size < 0:
            raise ValueError("Object size cannot be negative")
        key = f"deep/level-{index % 3}/object-{index:04d}.bin" if index % 2 else f"flat/object-{index:04d}.bin"
        dest = root / key
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists() and not force:
            raise FileExistsError(f"{dest} exists; use --force to overwrite")
        digest = hashlib.sha256()
        with dest.open("wb") as out:
            for block in make_bytes(seed + index, size):
                out.write(block)
                digest.update(block)
        records.append({"key":key,"size":size,"sha256":digest.hexdigest(),
                        "metadata":{"dataset-id":"dev906-synthetic"},
                        "tags":{"dataset":"dev906","group":str(index % 3)}})
    manifest = root / "local-manifest.json"
    manifest.write_text(json.dumps({"schema":1,"seed":seed,"objects":records},indent=2)+"\n")
    return manifest

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",default="datasets/generated")
    p.add_argument("--sizes",default="1024,65536,1048576",help="Comma-separated sizes in bytes")
    p.add_argument("--seed",type=int,default=906)
    p.add_argument("--force",action="store_true")
    args=p.parse_args()
    sizes=[int(s.strip()) for s in args.sizes.split(",")]
    print(generate(args.output,sizes,args.seed,args.force))

if __name__=="__main__":
    main()
