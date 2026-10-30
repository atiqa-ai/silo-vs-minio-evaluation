import importlib.util,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"scripts/testing"))
import silo_advanced_parity as a
import dev911_gate as g
class AdvancedTests(unittest.TestCase):
 def test_core_scenarios_always_required(self):
  class Args:
   kms_key_minio=None;kms_key_silo=None
   retention_approval=False
   notification_arn_minio=None;notification_arn_silo=None
  self.assertEqual(a.scenario_plan(Args()),list(a.CORE))
 def test_gate_missing_is_incomplete(self):
  x=g.evaluate({})
  self.assertEqual(x["status"],"INCOMPLETE")
  self.assertEqual(x["checks"]["smoke"]["status"],"NOT_RUN")
 def test_fake_pass_without_evidence_rejected(self):
  x=g.evaluate({"smoke":{"status":"PASS","evidence_files":[]}})
  self.assertEqual(x["checks"]["smoke"]["status"],"INCOMPLETE")
 def test_nonexistent_evidence_rejected(self):
  x=g.evaluate({"smoke":{"status":"PASS","evidence_files":["/not-a-real-dev911-evidence"]}})
  self.assertEqual(x["checks"]["smoke"]["status"],"INCOMPLETE")
if __name__=="__main__":unittest.main()
