import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"scripts/benchmark"))
from dev913_orchestrate import plan
class TestPlan(unittest.TestCase):
 def test_sequential_plan(self):
  x=plan(ROOT/"benchmarks/profiles/minio-local.json","localhost:9000","localhost:9900")
  self.assertEqual(x["status"],"PLAN_ONLY_NOT_EXECUTED")
  self.assertEqual(x["total_runs_per_engine"],45)
  self.assertEqual([s["engine"] for s in x["steps"]],["minio","silo"])
  self.assertNotEqual(x["steps"][0]["expected_manifest"],x["steps"][1]["expected_manifest"])
if __name__=="__main__":unittest.main()
