#!/usr/bin/env python3
"""DEV-914: offline configuration risk inventory and evidence-gated security review.
Findings are potential risks, not verified vulnerabilities or runtime test outcomes.
"""
import argparse, hashlib, json, pathlib, re, csv
ROOT=pathlib.Path(__file__).resolve().parents[2]
CHECKS=("identity_and_iam","tls_transport","encryption_at_rest","secret_management",
        "network_exposure","audit_logging","object_lock_retention","image_vulnerabilities",
        "licence_provenance","supply_chain_integrity")
def audit(repo):
    repo=pathlib.Path(repo)
    findings=[]
    paths=sorted((repo/"compose").rglob("*.yaml"))+sorted((repo/"compose").rglob("*.yml"))
    for p in paths:
        text=p.read_text()
        rel=str(p.relative_to(repo))
        if re.search(r"(?m)^\s*privileged:\s*true\s*$",text):
            findings.append({"file":rel,"rule":"privileged_container","severity":"HIGH","detail":"Privileged container requested"})
        if re.search(r"(?m)^\s*network_mode:\s*host\s*$",text):
            findings.append({"file":rel,"rule":"host_network","severity":"MEDIUM","detail":"Host networking requested"})
        if re.search(r"(?m)^\s*-\s*0\.0\.0\.0:",text):
            findings.append({"file":rel,"rule":"wildcard_host_binding","severity":"MEDIUM","detail":"Explicit wildcard host port binding"})
        if re.search(r"(?m)^\s*read_only:\s*false\s*$",text):
            findings.append({"file":rel,"rule":"writable_rootfs","severity":"INFO","detail":"Writable container filesystem explicitly enabled"})
        if re.search(r"(?m)^\s*image:\s*[^#\n]+:latest\s*$",text):
            findings.append({"file":rel,"rule":"mutable_latest_tag","severity":"MEDIUM","detail":"Mutable latest image tag"})
    env=repo/".env.example"
    if env.exists():
        data=env.read_text()
        for name in ("MINIO_IMAGE","SILO_IMAGE"):
            if name not in data:findings.append({"file":".env.example","rule":"missing_image_pin","severity":"MEDIUM","detail":name+" absent"})
        if "REPLACE_ME" in data:
            findings.append({"file":".env.example","rule":"template_credentials","severity":"INFO","detail":"Credential placeholders present; expected in template, not evidence of runtime values"})
    return {"kind":"STATIC_CONFIGURATION_AUDIT","runtime_executed":False,
            "files_scanned":len(paths),"findings":findings,
            "warning":"Regex audit is incomplete and may miss issues; not a vulnerability scan."}
def evidence_gate(manifest):
    items=manifest.get("checks",{})
    result={}
    for check in CHECKS:
        entry=items.get(check,{})
        paths=entry.get("evidence_paths",[])
        status=entry.get("status","NOT_RUN")
        valid=status in ("PASS","FAIL","NOT_SUPPORTED","NOT_APPLICABLE") and isinstance(paths,list) and bool(paths) and all(pathlib.Path(p).is_file() and pathlib.Path(p).stat().st_size>0 for p in paths)
        result[check]={"status":status if valid else "NOT_VERIFIED","evidence_paths":paths if valid else []}
    return {"status":"REVIEW_READY" if all(v["status"]!="NOT_VERIFIED" for v in result.values()) else "INCOMPLETE",
            "checks":result,"note":"File presence is not authenticity or technical correctness verification. A human must review evidence."}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--repo",default=str(ROOT))
    p.add_argument("--out",required=True)
    p.add_argument("--evidence-manifest")
    a=p.parse_args()
    out=pathlib.Path(a.out)
    if out.exists() and any(out.iterdir()):p.error("Output directory must be empty")
    out.mkdir(parents=True,exist_ok=True)
    audit_result=audit(a.repo)
    (out/"static-audit.json").write_text(json.dumps(audit_result,indent=2)+"\n")
    with (out/"static-findings.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=("file","rule","severity","detail"))
        writer.writeheader();writer.writerows(audit_result["findings"])
    gate=evidence_gate(json.loads(pathlib.Path(a.evidence_manifest).read_text())) if a.evidence_manifest else evidence_gate({})
    (out/"evidence-gate.json").write_text(json.dumps(gate,indent=2)+"\n")
    lines=["# DEV-914 Security and licence review","",
           "**Static analysis only — no live engine execution.**","",
           "Compose files scanned: "+str(audit_result["files_scanned"]),
           "Potential findings: "+str(len(audit_result["findings"])),"",
           "## Runtime/security evidence gate","",
           "| Check | Status |","|---|---|"]
    lines.extend("| "+k+" | "+v["status"]+" |" for k,v in gate["checks"].items())
    lines+=["","**Gate:** "+gate["status"],"",
            "Do not infer license obligations, vulnerability absence, or security feature parity without exact source/image evidence.",
            "No CVE, scanner or licence outcome is asserted by this report."]
    (out/"review.md").write_text("\n".join(lines)+"\n")
    print(json.dumps({"static_files_scanned":audit_result["files_scanned"],"potential_findings":len(audit_result["findings"]),"evidence_status":gate["status"]}))
if __name__=="__main__":main()
