import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[2]/"scripts/testing/replication_audit.py"
spec=importlib.util.spec_from_file_location("repl",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Stream:
 def __init__(self,data):self.data=data
 def iter_chunks(self,chunk_size):yield self.data
 def close(self):pass
class Paginator:
 def paginate(self,Bucket):return [{"Versions":[{"Key":"a","VersionId":"v1","Size":3}],"DeleteMarkers":[]}]
class S3:
 def __init__(self,version,data):self.version=version;self.data=data
 def get_paginator(self,name):return self
 def paginate(self,Bucket):return [{"Versions":[{"Key":"a","VersionId":self.version,"Size":len(self.data)}]}]
 def get_object(self,**kwargs):return {"Body":Stream(self.data)}
class Tests(unittest.TestCase):
 def test_version_id_difference_allowed(self):
  self.assertEqual(m.audit(S3("v1",b"abc"),S3("other",b"abc"),"s","t")["status"],"PASS")
 def test_content_mismatch_detected(self):
  self.assertEqual(m.audit(S3("v1",b"abc"),S3("v2",b"bad"),"s","t")["status"],"FAIL")
 def test_poll_immediate_success(self):
  self.assertEqual(m.poll(lambda:{"status":"PASS"},0,1)["attempts"],1)
if __name__=="__main__":unittest.main()
