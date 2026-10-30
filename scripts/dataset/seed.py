#!/usr/bin/env python3
"""Seed synthetic files to an S3-compatible endpoint; no production data."""
import argparse, json, os, hashlib
from pathlib import Path

def client(endpoint):
    try:
        import boto3
        from botocore.config import Config
    except ImportError as e:
        raise SystemExit("Install boto3 in an isolated virtualenv to seed S3") from e
    for name in ("AWS_ACCESS_KEY_ID","AWS_SECRET_ACCESS_KEY"):
        if not os.getenv(name):
            raise SystemExit(f"Missing {name}; provide credentials outside Git")
    return boto3.client("s3",endpoint_url=endpoint,
        region_name=os.getenv("AWS_DEFAULT_REGION","us-east-1"),
        config=Config(s3={"addressing_style":"path"}))

def seed(base, bucket, endpoint, versions=1, create_bucket=False):
    base=Path(base)
    inventory=json.loads((base/"local-manifest.json").read_text())
    s3=client(endpoint)
    if create_bucket:
        s3.create_bucket(Bucket=bucket)
    if versions > 1:
        s3.put_bucket_versioning(Bucket=bucket,VersioningConfiguration={"Status":"Enabled"})
    if versions > 1:
        status=s3.get_bucket_versioning(Bucket=bucket).get('Status')
        if status!='Enabled': raise RuntimeError('Bucket versioning not confirmed enabled')
    results=[]
    for obj in inventory["objects"]:
        path=base/obj["key"]
        for v in range(versions):
            with path.open("rb") as stream:
                response=s3.put_object(Bucket=bucket,Key=obj["key"],Body=stream,
                    Metadata={**obj["metadata"],"synthetic-revision":str(v)},
                    Tagging="dataset=dev906&group="+obj["tags"]["group"])
            version_id=response.get("VersionId")
            if versions>1 and (not version_id or version_id=='null'):
                raise RuntimeError('S3 did not return a usable version ID for '+obj['key'])
            results.append({"key":obj["key"],"version_id":version_id,
                            "etag":response.get("ETag"),"source_sha256":obj["sha256"],
                            "revision":v})
    return results

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--data",default="datasets/generated")
    p.add_argument("--bucket",required=True)
    p.add_argument("--endpoint",required=True)
    p.add_argument("--versions",type=int,default=2)
    p.add_argument("--create-bucket",action="store_true")
    p.add_argument("--output",default="artifacts/seed-results.json")
    a=p.parse_args()
    if a.versions < 1: p.error("--versions must be >= 1")
    results=seed(a.data,a.bucket,a.endpoint,a.versions,a.create_bucket)
    dest=Path(a.output);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps({"bucket":a.bucket,"objects":results},indent=2)+"\n")
    print(f"Seeded {len(results)} object versions; receipt: {dest}")

if __name__=="__main__": main()
