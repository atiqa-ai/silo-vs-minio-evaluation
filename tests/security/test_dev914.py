import sys,unittest,tempfile,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"scripts/security"))
from dev914 import audit,evidence_gate,CHECKS
class TestSecurity(unittest.TestCase):
 def test_unverified_without_evidence(self):
  result=evidence_gate({})
  self.assertEqual(result["status"],"INCOMPLETE")
  self.assertEqual(len(result["checks"]),len(CHECKS))
 def test_does_not_accept_pass_without_file(self):
  result=evidence_gate({"checks":{"tls_transport":{"status":"PASS","evidence_paths":["/nonexistent"]}}})
  self.assertEqual(result["checks"]["tls_transport"]["status"],"NOT_VERIFIED")
 def test_complete_evidence_presence(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"evidence.txt";p.write_text("synthetic fixture, not real evidence")
   m={"checks":{k:{"status":"FAIL","evidence_paths":[str(p)]} for k in CHECKS}}
   self.assertEqual(evidence_gate(m)["status"],"REVIEW_READY")
 def test_detect_privileged(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"compose"/"demo";p.mkdir(parents=True)
   (p/"compose.yaml").write_text("services:\n  x:\n    privileged: true\n")
   result=audit(d)
   self.assertIn("privileged_container",[x["rule"] for x in result["findings"]])
 def test_repo_audit(self):
  self.assertGreaterEqual(audit(ROOT)["files_scanned"],1)
if __name__=="__main__":unittest.main()
