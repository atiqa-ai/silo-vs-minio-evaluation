#!/usr/bin/env python3
"""Profile B deterministic dataset plan; dry-run by default."""
import argparse, json, shutil
from pathlib import Path
def plan(gib=5,output="datasets/generated"):
    if not 5<=gib<=10: raise ValueError("Profile B dataset must be 5–10 GiB")
    total=int(gib*1024**3)
    # Four 1 GiB objects exercise multipart-sized transfers; remaining data in mixed sizes.
    sizes=[1024**3]*min(4,total//(1024**3))
    remainder=total-sum(sizes)
    choices=[1024,64*1024,1024**2,16*1024**2,64*1024**2]
    i=0
    while remainder:
        size=min(choices[i%len(choices)],remainder)
        sizes.append(size);remainder-=size;i+=1
    free=shutil.disk_usage(Path(output).parent if Path(output).parent.exists() else ".").free
    return {"profile":"B","total_bytes":total,"objects":len(sizes),
            "sizes":sizes,"available_bytes":free,
            "warning":"Capacity is NOT approved until versions, replicas, benchmark temporary data and volumes are budgeted."}
def main():
    p=argparse.ArgumentParser();p.add_argument("--gib",type=float,default=5)
    p.add_argument("--output",default="datasets/generated");p.add_argument("--write-plan")
    a=p.parse_args();result=plan(a.gib,a.output)
    data=json.dumps(result,indent=2)+"\n"
    if a.write_plan:
        f=Path(a.write_plan);f.parent.mkdir(parents=True,exist_ok=True);f.write_text(data)
    print(data,end="")
if __name__=="__main__":main()
