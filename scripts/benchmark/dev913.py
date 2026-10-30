#!/usr/bin/env python3
"""DEV-913 evidence-driven Silo vs MinIO performance comparison.
No synthetic numbers, no automatic runtime claims.
"""
import argparse, csv, hashlib, json, pathlib, statistics, sys

METRICS=("ops_per_second","throughput_mib_s","p50_ms","p95_ms","p99_ms")
LOWER_IS_BETTER={"p50_ms","p95_ms","p99_ms"}
EXPECTED={"minio","silo"}

def fingerprint(profile):
    # Canonical JSON avoids false differences from whitespace/key ordering.
    return hashlib.sha256(json.dumps(profile,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def load_manifest(path):
    data=json.loads(pathlib.Path(path).read_text())
    if not isinstance(data,dict) or data.get("mode")!="warp" or not isinstance(data.get("runs"),list):
        raise ValueError("Expected DEV-910 Warp manifest: "+str(path))
    return data

def group_runs(data):
    groups={}
    for run in data["runs"]:
        key=(run.get("operation"),run.get("object_size"))
        if not all(isinstance(x,str) and x for x in key):
            raise ValueError("Missing workload identifiers")
        groups.setdefault(key,[]).append(run)
    return groups

def compare(minio,silo,metadata):
    issues=[]
    if minio.get("engine") not in (None,"minio") or silo.get("engine") not in (None,"silo"):
        issues.append("Engine manifest identity mismatch")
    if minio.get("status")!="PASS" or silo.get("status")!="PASS":
        issues.append("Both engine manifests must have PASS status")
    if fingerprint(minio.get("profile"))!=fingerprint(silo.get("profile")):
        issues.append("Different benchmark profiles")
    for name in ("warp_version","hardware_id","client_version","filesystem","disk_id"):
        a=metadata.get("minio",{}).get(name)
        b=metadata.get("silo",{}).get(name)
        if not a or not b or a!=b:
            issues.append("Missing or unequal "+name)
    for engine in EXPECTED:
        meta=metadata.get(engine,{})
        if not meta.get("image_digest") or "@sha256:" not in meta["image_digest"]:
            issues.append("Missing pinned image digest for "+engine)
        evidence=meta.get("resource_evidence",[])
        if not isinstance(evidence,list) or not evidence or not all(pathlib.Path(x).is_file() and pathlib.Path(x).stat().st_size for x in evidence):
            issues.append("Missing resource evidence for "+engine)
    mg,sg=group_runs(minio),group_runs(silo)
    if set(mg)!=set(sg):issues.append("Workload coverage differs")
    rows=[]
    for key in sorted(set(mg)|set(sg)):
        left=mg.get(key,[]);right=sg.get(key,[])
        if len(left)<3 or len(right)<3 or len(left)!=len(right):
            issues.append("Missing/unequal repetitions: "+repr(key))
        for engine,runs in (("minio",left),("silo",right)):
            if len({r.get("repetition") for r in runs})!=len(runs):
                issues.append("Duplicate/missing repetition IDs: "+engine+" "+repr(key))
            if any(r.get("exit_code")!=0 or r.get("analysis_exit_code")!=0 for r in runs):
                issues.append("Unsuccessful benchmark or analysis: "+engine+" "+repr(key))
        for metric in METRICS:
            def vals(runs):
                numbers=[r.get("metrics",{}).get(metric) for r in runs]
                if len(numbers)!=len(runs) or not numbers or any(type(v) not in (float,int) or v<0 for v in numbers):
                    return None
                return numbers
            a,b=vals(left),vals(right)
            if a is None or b is None:
                issues.append("Missing measured "+metric+" for "+repr(key))
                rows.append({"operation":key[0],"size":key[1],"metric":metric,"minio_median":None,
                             "silo_median":None,"silo_delta_pct":None,"silo_improvement_pct":None})
                continue
            av,bv=statistics.median(a),statistics.median(b)
            delta=100*(bv-av)/av if av else None
            improvement=(-delta if metric in LOWER_IS_BETTER else delta) if delta is not None else None
            rows.append({"operation":key[0],"size":key[1],"metric":metric,
                         "minio_median":av,"silo_median":bv,
                         "silo_delta_pct":delta,"silo_improvement_pct":improvement})
    return {"status":"READY_FOR_MANUAL_REVIEW" if not issues and rows else "INCOMPLETE",
            "issues":sorted(set(issues)),"rows":rows,
            "warning":"Differences are descriptive, not statistically significant claims. Review raw runs, cache effects, cleanup, resource data and workload semantics."}

def write_report(result,out):
    out=pathlib.Path(out)
    if out.exists() and any(out.iterdir()):raise ValueError("Output directory must be empty/new")
    out.mkdir(parents=True,exist_ok=True)
    (out/"comparison.json").write_text(json.dumps(result,indent=2)+"\n")
    fields=("operation","size","metric","minio_median","silo_median","silo_delta_pct","silo_improvement_pct")
    with (out/"comparison.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(result["rows"])
    def fmt(v):return "N/A" if v is None else f"{v:.3f}"
    lines=["# DEV-913 MinIO vs Silo performance","",f"**Status:** {result['status']}","",
           "| Operation | Size | Metric | MinIO median | Silo median | Silo improvement % |",
           "|---|---|---|---:|---:|---:|"]
    for row in result["rows"]:
        lines.append(f"| {row['operation']} | {row['size']} | {row['metric']} | {fmt(row['minio_median'])} | {fmt(row['silo_median'])} | {fmt(row['silo_improvement_pct'])} |")
    lines+=["","## Evidence gaps"]+[f"- {x}" for x in result["issues"]]
    lines+=["","*No statistical significance claim; review real system measurements and resource captures.*"]
    (out/"comparison.md").write_text("\n".join(lines)+"\n")
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:return
    for metric in METRICS:
        rows=[r for r in result["rows"] if r["metric"]==metric and r["minio_median"] is not None and r["silo_median"] is not None]
        if not rows:continue
        fig,ax=plt.subplots(figsize=(max(7,len(rows)*.75),4.5))
        xs=list(range(len(rows)))
        ax.bar([x-.18 for x in xs],[r["minio_median"] for r in rows],width=.36,label="MinIO")
        ax.bar([x+.18 for x in xs],[r["silo_median"] for r in rows],width=.36,label="Silo")
        ax.set_xticks(xs,[r["operation"]+" "+r["size"] for r in rows],rotation=65,ha="right")
        ax.set_ylabel(metric);ax.legend();fig.tight_layout()
        fig.savefig(out/(metric+".png"),dpi=150);plt.close(fig)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--mode",choices=("plan","compare"),default="plan")
    p.add_argument("--minio-manifest",type=pathlib.Path)
    p.add_argument("--silo-manifest",type=pathlib.Path)
    p.add_argument("--metadata",type=pathlib.Path)
    p.add_argument("--out",type=pathlib.Path)
    a=p.parse_args()
    if a.mode=="plan":
        print(json.dumps({"status":"NOT_RUN","required_engines":sorted(EXPECTED),
                          "same_profile":True,"min_repetitions":3,
                          "evidence":"DEV-910 Warp manifests + pinned image digests + matching hardware/tool versions + resource captures"},indent=2))
        return 0
    if not all((a.minio_manifest,a.silo_manifest,a.metadata,a.out)):
        p.error("compare requires both manifests, metadata and --out")
    result=compare(load_manifest(a.minio_manifest),load_manifest(a.silo_manifest),
                   json.loads(a.metadata.read_text()))
    write_report(result,a.out)
    print(result["status"])
    return 0 if result["status"]=="READY_FOR_MANUAL_REVIEW" else 2
if __name__=="__main__":sys.exit(main())
