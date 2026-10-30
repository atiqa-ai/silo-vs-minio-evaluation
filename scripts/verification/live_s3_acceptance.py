#!/usr/bin/env python3
"""Destructive-to-test-bucket-only live S3 acceptance; writes evidence, never fakes PASS."""
import argparse, hashlib, json, os, sys, uuid
from pathlib import Path

def execute(s3, bucket, size=6*1024*1024):
    key='acceptance/'+uuid.uuid4().hex
    payload=(b'option-b-minio-silo-parity\n' * ((size//26)+1))[:size]
    sha=hashlib.sha256(payload).hexdigest()
    checks={}
    evidence={'bucket':bucket,'key':key,'sha256_expected':sha,'checks':checks}
    try:
        s3.put_bucket_versioning(Bucket=bucket,VersioningConfiguration={'Status':'Enabled'})
        checks['versioning_enabled']=s3.get_bucket_versioning(Bucket=bucket).get('Status')=='Enabled'
        # Explicit multipart, not put_object's single request.
        upload=s3.create_multipart_upload(Bucket=bucket,Key=key,Metadata={'test':'option-b'},Tagging='test=option-b')
        upload_id=upload['UploadId'];parts=[]
        try:
            for index,part in enumerate((payload[:5*1024*1024],payload[5*1024*1024:]),1):
                result=s3.upload_part(Bucket=bucket,Key=key,UploadId=upload_id,PartNumber=index,Body=part)
                parts.append({'PartNumber':index,'ETag':result['ETag']})
            completed=s3.complete_multipart_upload(Bucket=bucket,Key=key,UploadId=upload_id,MultipartUpload={'Parts':parts})
        except Exception:
            s3.abort_multipart_upload(Bucket=bucket,Key=key,UploadId=upload_id)
            raise
        version=completed.get('VersionId')
        checks['immutable_version_id']=isinstance(version,str) and version not in ('','null')
        if not checks['immutable_version_id']: raise RuntimeError('Multipart upload returned no immutable version ID')
        req={'Bucket':bucket,'Key':key,'VersionId':version}
        got=s3.get_object(**req)
        try: body=got['Body'].read()
        finally: got['Body'].close()
        head=s3.head_object(**req)
        tags=s3.get_object_tagging(**req)['TagSet']
        checks.update({'multipart_two_parts':len(parts)==2,
                       'sha256_readback':hashlib.sha256(body).hexdigest()==sha,
                       'size':len(body)==len(payload)==head['ContentLength'],
                       'metadata':head.get('Metadata',{}).get('test')=='option-b',
                       'tags':{'Key':'test','Value':'option-b'} in tags,
                       'version_readback':got.get('VersionId')==version and head.get('VersionId')==version})
        evidence['version_id']=version
    except Exception as exc:
        evidence['error']=type(exc).__name__+': '+str(exc)
    evidence['status']='PASS' if checks and all(checks.values()) and 'error' not in evidence else 'FAIL'
    return evidence

def main():
    p=argparse.ArgumentParser();p.add_argument('--endpoint',required=True);p.add_argument('--bucket',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    from boto3 import client
    from botocore.config import Config
    if not os.getenv('AWS_ACCESS_KEY_ID') or not os.getenv('AWS_SECRET_ACCESS_KEY'):p.error('AWS credentials required')
    s3=client('s3',endpoint_url=a.endpoint,config=Config(s3={'addressing_style':'path'}))
    result=execute(s3,a.bucket)
    dest=Path(a.output);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'],dest)
    sys.exit(0 if result['status']=='PASS' else 1)
if __name__=='__main__':main()
