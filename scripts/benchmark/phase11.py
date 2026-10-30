#!/usr/bin/env python3
"""DEV-910 local MinIO Warp/fio runner. Only real command outputs count as evidence."""
import argparse, datetime, hashlib, json, os, pathlib, re, shutil, subprocess, sys, time

ROOT = pathlib.Path(__file__).resolve().parents[2]
PROFILE = ROOT / "benchmarks/profiles/minio-local.json"
OPS = {"put", "get", "list", "delete", "mixed"}

def load_profile(path):
    p = json.loads(pathlib.Path(path).read_text())
    if not isinstance(p["repetitions"], int) or not 1 <= p["repetitions"] <= 10:
        raise ValueError("repetitions must be 1..10")
    if not 1 <= p["concurrency"] <= 8: raise ValueError("concurrency must be 1..8")
    if not 10 <= p["duration_seconds"] <= 600: raise ValueError("duration must be 10..600s")
    if not 0 <= p["warmup_seconds"] <= 120: raise ValueError("invalid warmup")
    if not set(p["operations"]).issubset(OPS): raise ValueError("unknown operation")
    if any(not re.fullmatch(r"[1-9][0-9]*(?:KiB|MiB|GiB)", s) for s in p["object_sizes"]):
        raise ValueError("invalid size")
    return p

def record_command(command, output, env=None):
    start = time.monotonic()
    with open(output, "w") as f:
        result = subprocess.run(command, stdout=f, stderr=subprocess.STDOUT, text=True, env=env)
    return {"command": command, "exit_code": result.returncode, "wall_seconds": round(time.monotonic()-start, 3),
            "output": str(output), "sha256": hashlib.sha256(output.read_bytes()).hexdigest()}

def safe_dir(path):
    resolved = pathlib.Path(path).resolve()
    if resolved == pathlib.Path("/") or not resolved.is_dir():
        raise ValueError("fio directory must be a pre-existing dedicated directory")
    if not (resolved / ".dev910-fio-approved").is_file():
        raise ValueError("Create .dev910-fio-approved marker in dedicated SSD test directory")
    if (resolved / "dev910-fio-test.bin").exists():
        raise ValueError("Refusing to overwrite existing fio test file")
    return resolved

def fio_command(profile, directory, output):
    f=profile["fio"]
    return ["fio", "--name=dev910-local-ssd", "--directory="+str(safe_dir(directory)),
            "--filename=dev910-fio-test.bin", "--size="+f["size"],
            "--runtime="+str(f["runtime_seconds"]), "--time_based=1",
            "--ioengine=libaio", "--direct=1", "--group_reporting=1",
            "--rw="+f["rw"], "--bs="+f["bs"], "--iodepth="+str(f["iodepth"]),
            "--numjobs="+str(f["numjobs"]), "--output-format=json", "--output="+str(output)]

def fio_metrics(data):
    jobs=data.get("jobs",[])
    if not jobs: raise ValueError("No fio jobs")
    result={}
    for direction in ("read","write"):
        vals=[j.get(direction,{}) for j in jobs]
        result[direction]={"bandwidth_KiB_s":sum(v.get("bw",0) for v in vals),
          "iops":sum(v.get("iops",0) for v in vals)}
        for pct in ("50.000000","95.000000","99.000000"):
            # fio may report clat_ns or clat_us; normalize to milliseconds.
            values=[]
            for v in vals:
                for unit,scale in (("clat_ns",1e-6),("clat_us",1e-3),("clat_ms",1)):
                    percentile=v.get(unit,{}).get("percentile",{})
                    if pct in percentile:
                        values.append(percentile[pct]*scale)
                        break
            result[direction]["p"+pct.split(".")[0]+"_ms"]=max(values) if values else None
    return result

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--profile",default=str(PROFILE))
    ap.add_argument("--out",required=True)
    ap.add_argument("--mode",choices=("plan","warp","fio"),default="plan")
    ap.add_argument("--endpoint",help="host:port, required for warp")
    ap.add_argument("--fio-dir",help="dedicated local SSD directory")
    ap.add_argument("--warp-bin",default="warp",help="path to verified Warp binary")
    ap.add_argument("--engine",choices=("minio","silo"),default="minio")
    ap.add_argument("--approve",action="store_true",help="approve temporary synthetic workload")
    a=ap.parse_args()
    p=load_profile(a.profile)
    out=pathlib.Path(a.out).resolve()
    if a.mode=="plan":
        print(json.dumps({"profile":p,"mode":"plan","estimated_warp_runs":p["repetitions"]*len(p["operations"])*len(p["object_sizes"]),
          "note":"No benchmarks executed"},indent=2))
        return
    if not a.approve:ap.error("--approve required for workload execution")
    if out.exists() and (not out.is_dir() or any(out.iterdir())):ap.error("output directory must be empty/new")
    out.mkdir(parents=True,exist_ok=True)
    result={"mode":a.mode,"engine":a.engine,"profile":p,"started_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "status":"INCOMPLETE","runs":[]}
    try:
        if a.mode=="fio":
            if not shutil.which("fio"):raise RuntimeError("fio missing")
            if not a.fio_dir:raise RuntimeError("--fio-dir required")
            # fio --output writes directly to JSON; do not overwrite by stdout redirect.
            safe_dir(a.fio_dir)
            for rep in range(1,p["repetitions"]+1):
                output=out/f"fio-{rep}.json"
                cmd=fio_command(p,a.fio_dir,output)
                # Fio overwrites its dedicated synthetic test file on repetitions.
                # User explicitly approved the dedicated directory and marker.
                cp=subprocess.run(cmd,capture_output=True,text=True)
                (out/f"fio-command-{rep}.txt").write_text(cp.stdout+"\\n"+cp.stderr)
                entry={"command":cmd,"exit_code":cp.returncode,"output":str(output),
                       "repetition":rep}
                if cp.returncode==0 and output.exists():
                    entry["metrics"]=fio_metrics(json.loads(output.read_text()))
                result["runs"].append(entry)
                if cp.returncode:raise RuntimeError("fio failed at repetition "+str(rep))
        else:
            if not shutil.which(a.warp_bin):raise RuntimeError("warp missing")
            if not a.endpoint:raise RuntimeError("--endpoint required")
            key=os.getenv("WARP_ACCESS_KEY");secret=os.getenv("WARP_SECRET_KEY")
            if not key or not secret:raise RuntimeError("WARP_ACCESS_KEY/WARP_SECRET_KEY missing")
            # Version-specific flags validated via CLI help at execution time.
            version=subprocess.run([a.warp_bin,"--version"],capture_output=True,text=True,check=True)
            (out/"warp-version.txt").write_text(version.stdout+version.stderr)
            helptext=subprocess.run([a.warp_bin,"--help"],capture_output=True,text=True,check=True).stdout
            (out/"warp-help.txt").write_text(helptext)
            for op in p["operations"]:
                ophelp=subprocess.run([a.warp_bin,op,"--help"],capture_output=True,text=True)
                (out/f"warp-{op}-help.txt").write_text(ophelp.stdout+ophelp.stderr)
                if ophelp.returncode:raise RuntimeError(f"warp {op} not supported by pinned CLI")
                required=("--host", "--duration", "--concurrent", "--benchdata", "--bucket")
                missing=[flag for flag in required if flag not in ophelp.stdout]
                if missing:raise RuntimeError(f"warp {op} unsupported options: {missing}")
                # Warp prepares objects for GET/LIST/DELETE/MIXED by default.
                # Each operation gets a unique disposable bucket, no --noclear.
                # Warmup is handled by Warp's normal preparation/stabilization;
                # never claim an exact warmup interval without version support.
                for size in p["object_sizes"]:
                    for rep in range(1,p["repetitions"]+1):
                        label=f"{op}-{size}-{rep}"
                        # Warp generates its own bucket/test data; use a disposable dedicated endpoint.
                        bucket="dev910-"+hashlib.sha256((a.engine+"-"+label+"-"+out.name).encode()).hexdigest()[:16]
                        benchdata=out/(label+".csv.zst")
                        cmd=[a.warp_bin,op,"--host="+a.endpoint,
                             "--duration="+str(p["duration_seconds"])+"s",
                             "--concurrent="+str(p["concurrency"]),
                             "--bucket="+bucket,"--benchdata="+str(benchdata),"--no-color"]
                        if "--obj.size" in ophelp.stdout:cmd.append("--obj.size="+size)
                        elif op in ("put","get","mixed"):raise RuntimeError("Object-size flag missing for "+op)
                        if "--no-color" not in ophelp.stdout:cmd.remove("--no-color")
                        # Warp credentials are inherited from WARP_ACCESS_KEY / WARP_SECRET_KEY.
                        # Never pass secrets in argv, manifest or shell history.
                        raw=out/(label+".log")
                        env=os.environ.copy()
                        entry=record_command(cmd,raw,env=env)
                        entry["label"]=label
                        entry["operation"]=op
                        entry["object_size"]=size
                        entry["repetition"]=rep
                        entry["bucket"]=bucket
                        entry["benchdata"]=str(benchdata)
                        entry["benchdata_present"]=benchdata.exists()
                        result["runs"].append(entry)
                        if entry["exit_code"]==0 and benchdata.exists():
                            analysis=out/(label+"-analysis.json")
                            analyze=[a.warp_bin,"analyze",str(benchdata),"--json"]
                            analyzed=subprocess.run(analyze,capture_output=True,text=True,env=env)
                            analysis.write_text(analyzed.stdout)
                            (out/(label+"-analysis.stderr")).write_text(analyzed.stderr)
                            entry["analysis_exit_code"]=analyzed.returncode
                            entry["analysis_json"]=str(analysis)
                            if analyzed.returncode==0:
                                try:
                                    from warp_metrics import extract_metrics
                                    entry["metrics"]=extract_metrics(json.loads(analyzed.stdout))
                                except (ValueError,KeyError,TypeError) as exc:
                                    entry["metrics_error"]=str(exc)
                        else:
                            entry["analysis_exit_code"]=None
                        if entry["exit_code"]:raise RuntimeError("warp failed at "+label)
                        if entry.get("analysis_exit_code")!=0 or not entry.get("metrics"):
                            raise RuntimeError("Warp analysis/metrics unavailable at "+label+"; preserve raw evidence")
        result["status"]="PASS" if result["runs"] and all(x["exit_code"]==0 for x in result["runs"]) else "FAIL"
        if a.mode=="warp" and result["status"]=="PASS":
            if not all(x.get("analysis_exit_code")==0 and x.get("metrics") for x in result["runs"]):
                result["status"]="INCOMPLETE"
                result["error"]="Warp analysis or metric extraction missing; inspect raw output"
    except Exception as exc:
        result["status"]="FAIL";result["error"]=str(exc)
    finally:
        result["finished_utc"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
        (out/"manifest.json").write_text(json.dumps(result,indent=2)+"\n")
    print(result["status"],out)
    if result["status"]!="PASS":sys.exit(1)

if __name__=="__main__":main()
