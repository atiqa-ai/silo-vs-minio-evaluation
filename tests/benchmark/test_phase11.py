import importlib.util,json,tempfile,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[2]/"scripts/benchmark/phase11.py"
s=importlib.util.spec_from_file_location("phase11",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class TestPhase11(unittest.TestCase):
 def test_profile(self):
  self.assertEqual(m.load_profile(m.PROFILE)["repetitions"],3)
 def test_fio_percentiles(self):
  d={"jobs":[{"read":{"bw":100,"iops":10,"clat_ns":{"percentile":{"50.000000":1000000,"95.000000":2000000,"99.000000":3000000}}},"write":{"bw":50,"iops":5}}]}
  self.assertEqual(m.fio_metrics(d)["read"]["p95_ms"],2)
  self.assertIsNone(m.fio_metrics(d)["write"]["p99_ms"])
 def test_fio_directory_guard(self):
  with tempfile.TemporaryDirectory() as tmp:
   with self.assertRaises(ValueError):m.safe_dir(tmp)
   (Path(tmp)/".dev910-fio-approved").touch()
   self.assertEqual(m.safe_dir(tmp),Path(tmp).resolve())
   (Path(tmp)/"dev910-fio-test.bin").touch()
   with self.assertRaises(ValueError):m.safe_dir(tmp)
 def test_invalid_profile(self):
  with tempfile.TemporaryDirectory() as tmp:
   d=json.loads(m.PROFILE.read_text());d["concurrency"]=100
   f=Path(tmp)/"p.json";f.write_text(json.dumps(d))
   with self.assertRaises(ValueError):m.load_profile(f)
if __name__=="__main__":unittest.main()
