import importlib.util, tempfile, unittest
from pathlib import Path
root=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('workflow',root/'scripts/lab/replication-workflow.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Tests(unittest.TestCase):
 def test_alias_injection_rejected(self):
  with self.assertRaises(ValueError):m.valid('test;rm -rf /',m.ALIAS,'alias')
 def test_bucket_validation(self):
  with self.assertRaises(ValueError):m.valid('A_BAD_BUCKET',m.BUCKET,'bucket')
 def test_mutation_requires_approval(self):
  with self.assertRaises(PermissionError):m.run(['mc','replicate','add'],[],'test',mutates=True,approved=False)
