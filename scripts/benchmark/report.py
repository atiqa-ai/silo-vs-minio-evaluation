#!/usr/bin/env python3
"""Real-evidence benchmark summaries and charts; never fabricate missing metrics."""
import argparse,csv,json,pathlib,statistics

def aggregate(paths):
    rows=[]
    for path in paths:
        d=json.loads(pathlib.Path(path).read_text())
        for run in d.get("runs",[]):
            m=run.get("metrics") or {}
            row={"mode":d["mode"],"operation":run.get("operation"),"object_size":run.get("object_size"),
                 "repetition":run.get("repetition"),"status":d["status"],"exit_code":run.get("exit_code")}
            for key in ("ops_per_second","throughput_mib_s","p50_ms","p95_ms","p99_ms"):
                row[key]=m.get(key)
            for direction in ("read","write"):
                row["fio_"+direction+"_iops"]=m.get(direction,{}).get("iops")
            rows.append(row)
    groups={}
    for row in rows:
        if row["status"]!="PASS" or row["exit_code"]!=0:continue
        key=(row["mode"],row["operation"],row["object_size"])
        groups.setdefault(key,[]).append(row)
    summaries=[]
    for (mode,op,size),items in groups.items():
        item={"mode":mode,"operation":op,"object_size":size,"repetitions":len(items)}
        for metric in ("ops_per_second","throughput_mib_s","p50_ms","p95_ms","p99_ms","fio_read_iops","fio_write_iops"):
            values=[x[metric] for x in items if isinstance(x.get(metric),(int,float))]
            item[metric+"_median"]=statistics.median(values) if len(values)==len(items) else None
        summaries.append(item)
    return {"run_count":len(rows),"rows":rows,"summaries":summaries,
            "benchmark_validated":bool(rows) and bool(summaries) and all(x["status"]=="PASS" and x["exit_code"]==0 for x in rows)
                                  and all(x["repetitions"]>=3 for x in summaries)
                                  and all((x["ops_per_second_median"] is not None and x["throughput_mib_s_median"] is not None
                                           and x["p50_ms_median"] is not None and x["p95_ms_median"] is not None
                                           and x["p99_ms_median"] is not None) for x in summaries if x["mode"]=="warp"),
            "note":"Metric availability depends on verified Warp JSON schema and real runs."}

def write_reports(result,out):
    out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=True)
    (out/"summary.json").write_text(json.dumps(result,indent=2)+"\n")
    fields=["mode","operation","object_size","repetition","status","exit_code","ops_per_second",
            "throughput_mib_s","p50_ms","p95_ms","p99_ms","fio_read_iops","fio_write_iops"]
    with (out/"runs.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(result["rows"])
    def fmt(v):return "N/A" if v is None else f"{v:.3f}"
    lines=["# DEV-910 benchmark results","",f"Validated: **{result['benchmark_validated']}**","",
           "| Operation | Size | Runs | Median MiB/s | Median ops/s | Median p95 ms |",
           "|---|---|---:|---:|---:|---:|"]
    for x in result["summaries"]:
        lines.append(f"| {x['operation'] or x['mode']} | {x['object_size'] or '-'} | {x['repetitions']} | "
                     f"{fmt(x['throughput_mib_s_median'])} | {fmt(x['ops_per_second_median'])} | {fmt(x['p95_ms_median'])} |")
    (out/"summary.md").write_text("\n".join(lines)+"\n")
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    for metric,title in (("throughput_mib_s_median","Throughput (MiB/s)"),
                         ("ops_per_second_median","Operations/s"),
                         ("p95_ms_median","p95 latency (ms)")):
        points=[x for x in result["summaries"] if x[metric] is not None]
        if not points:continue
        fig,ax=plt.subplots(figsize=(max(7,len(points)*0.65),4))
        labels=[str(x["operation"] or x["mode"])+" "+str(x["object_size"] or "") for x in points]
        ax.bar(labels,[x[metric] for x in points])
        ax.set_ylabel(title);ax.tick_params(axis="x",rotation=60)
        fig.tight_layout();fig.savefig(out/(metric+".png"),dpi=150);plt.close(fig)

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("manifests",nargs="+");p.add_argument("--out",required=True);a=p.parse_args()
    write_reports(aggregate(a.manifests),a.out)
