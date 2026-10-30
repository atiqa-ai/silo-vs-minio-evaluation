import sys,unittest,tempfile,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"scripts/testing"))
import s3_compatibility as c
import dev912_report as report
class CompatibilityTests(unittest.TestCase):
 def test_matching_error(self):
  a={"status":"EXPECTED_ERROR","http_status":404,"error_code":"NoSuchKey"}
  self.assertEqual(c.verdict(a,dict(a,error_message="backend specific")),"MATCH")
 def test_different_error(self):
  a={"status":"EXPECTED_ERROR","http_status":404,"error_code":"NoSuchKey"}
  b={"status":"EXPECTED_ERROR","http_status":403,"error_code":"AccessDenied"}
  self.assertEqual(c.verdict(a,b),"DIFFERENT_REVIEW")
 def test_missing(self):
  self.assertEqual(c.verdict(None,{"status":"OK"}),"NOT_RUN")
 def test_error(self):
  self.assertEqual(c.verdict({"status":"ERROR"},{"status":"OK"}),"INCOMPLETE")
 def test_compare(self):
  x=c.compare({"case":{"status":"OK"}},{"case":{"status":"OK"}})
  self.assertEqual(x[0]["verdict"],"MATCH")
 def test_report(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/"input.json";p.write_text(json.dumps({"status":"NOT_RUN","comparison":[]}))
   report.generate(p,Path(t)/"out")
   self.assertTrue((Path(t)/"out"/"compatibility.csv").exists())
   self.assertTrue((Path(t)/"out"/"compatibility.md").exists())
 def test_normalization(self):
  a={"status":"OK","body_sha256":"a","request_id":"x"}
  b={"status":"OK","body_sha256":"a","request_id":"y"}
  self.assertEqual(c.verdict(a,b),"MATCH")
if __name__=="__main__":unittest.main()
