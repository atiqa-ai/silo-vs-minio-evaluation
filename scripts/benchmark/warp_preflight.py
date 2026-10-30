#!/usr/bin/env python3
"""Check real Warp binary version, help and analyze JSON fixture before benchmarking."""
import argparse, json, pathlib, subprocess, sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from warp_metrics import extract_metrics

def check(binary, sample):
    checks={}
    for args in (['--version'],['--help'],['analyze','--help']):
        proc=subprocess.run([binary,*args],capture_output=True,text=True,timeout=30)
        checks[' '.join(args)]={'exit_code':proc.returncode,'output':(proc.stdout+proc.stderr)[:12000]}
    if sample:
        checks['sample_metrics']=extract_metrics(json.loads(pathlib.Path(sample).read_text()))
    else:
        checks['sample_metrics']='NOT_VERIFIED: supply genuine warp analyze --json output'
    checks['status']='FIXTURE_PARSED_NOT_NATIVE_SCHEMA_VERIFIED' if sample and all(x['exit_code']==0 for x in checks.values() if isinstance(x,dict) and 'exit_code' in x) else 'BLOCKED'
    checks['reason']='Native Warp schema is not verified by a normalized fixture. Requires actual warp analyze --json capture and version-specific adapter.'
    return checks

def main():
    p=argparse.ArgumentParser();p.add_argument('--warp-bin',default='warp');p.add_argument('--sample');p.add_argument('--output',required=True);a=p.parse_args()
    result=check(a.warp_bin,a.sample)
    path=pathlib.Path(a.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'])
    if result['status']!='NATIVE_SCHEMA_VERIFIED':raise SystemExit(1)
if __name__=='__main__':main()
