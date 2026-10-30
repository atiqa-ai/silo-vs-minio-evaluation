#!/usr/bin/env python3
"""Generate reproducible sequential benchmark run instructions; never execute without live lab."""
import argparse,json,pathlib,shlex,sys
from phase11 import load_profile
from dev913 import fingerprint
ROOT=pathlib.Path(__file__).resolve().parents[2]
def plan(profile, minio_endpoint, silo_endpoint):
    p=load_profile(profile)
    commands=[]
    for engine,endpoint in (("minio",minio_endpoint),("silo",silo_endpoint)):
        commands.append({"engine":engine,"action":"STOP_OTHER_STACK_AND_VERIFY_ACTIVE_ENGINE",
          "command":["python3","scripts/benchmark/phase11.py","--engine",engine,"--mode","warp",
                     "--profile",str(profile),"--endpoint",endpoint,"--approve",
                     "--out","artifacts/dev913-"+engine+"-warp"],
          "expected_manifest":"artifacts/dev913-"+engine+"-warp/manifest.json"})
    return {"status":"PLAN_ONLY_NOT_EXECUTED","profile_sha256":fingerprint(p),
            "repetitions":p["repetitions"],"workloads":len(p["operations"])*len(p["object_sizes"]),
            "total_runs_per_engine":p["repetitions"]*len(p["operations"])*len(p["object_sizes"]),
            "steps":commands,"warning":"Start/stop stacks manually, validate Warp flags, TLS and credentials; never execute on production."}
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--profile",default=str(ROOT/"benchmarks/profiles/minio-local.json"))
    ap.add_argument("--minio-endpoint",default="127.0.0.1:9000")
    ap.add_argument("--silo-endpoint",default="127.0.0.1:9900")
    ap.add_argument("--out")
    a=ap.parse_args()
    data=plan(a.profile,a.minio_endpoint,a.silo_endpoint)
    if a.out:
        path=pathlib.Path(a.out)
        if path.exists():ap.error("Refusing to overwrite plan")
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(data,indent=2)+"\\n")
    print(json.dumps(data,indent=2))
if __name__=="__main__":main()
