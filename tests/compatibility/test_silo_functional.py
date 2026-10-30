import importlib.util, pathlib, tempfile, unittest, json
ROOT=pathlib.Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location("silo_functional",ROOT/"scripts/testing/silo_functional.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class SiloFunctionalTests(unittest.TestCase):
 def test_same_pass(self):
  rows=m.comparison({"put":{"status":"PASS"}},{"put":{"status":"PASS"}})
  self.assertEqual(rows[0]["comparison"],"SAME_PASS")
 def test_regression(self):
  rows=m.comparison({"put":{"status":"PASS"}},{"put":{"status":"FAIL"}})
  self.assertEqual(rows[0]["comparison"],"SILO_REGRESSION")
 def test_missing_not_pass(self):
  rows=m.comparison({"put":{"status":"PASS"}},{})
  self.assertEqual(rows[0]["comparison"],"INCOMPLETE")
 def test_both_fail_not_parity_success(self):
  rows=m.comparison({"put":{"status":"FAIL"}},{"put":{"status":"FAIL"}})
  self.assertEqual(rows[0]["comparison"],"BOTH_FAIL")
 def test_smoke_parser(self):
  with tempfile.TemporaryDirectory() as d:
   p=pathlib.Path(d)/"test.json"
   p.write_text(json.dumps({"checks":[{"test":"create_bucket","status":"PASS"}]}))
   self.assertEqual(m.parse_smoke(p)["create_bucket"]["status"],"PASS")
if __name__=="__main__":unittest.main()
