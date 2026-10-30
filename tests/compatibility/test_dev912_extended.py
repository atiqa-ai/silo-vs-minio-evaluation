import sys,unittest,tempfile,pathlib
from unittest.mock import Mock
ROOT=pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/testing'))
import dev912_extended as m
from s3_compatibility import compare
class TestExtended(unittest.TestCase):
 def test_cases_unique(self):self.assertEqual(len(m.CASES),len(set(m.CASES)))
 def test_expected_error(self):
  from botocore.exceptions import ClientError
  def bad():raise ClientError({'Error':{'Code':'NoSuchKey','Message':'missing'},'ResponseMetadata':{'HTTPStatusCode':404}},'GetObject')
  self.assertEqual(m.expect_error(bad)['error_code'],'NoSuchKey')
 def test_unexpected_success(self):self.assertEqual(m.expect_error(lambda:None)['status'],'UNEXPECTED_SUCCESS')
 def test_difference(self):
  a={'case':{'status':'EXPECTED_ERROR','error_code':'NoSuchKey','http_status':404}}
  b={'case':{'status':'EXPECTED_ERROR','error_code':'AccessDenied','http_status':403}}
  self.assertEqual(compare(a,b)[0]['verdict'],'DIFFERENT_REVIEW')
 def test_plan_no_network(self):
  class Args:mode='plan'
  self.assertEqual(m.run(Args())['status'],'NOT_RUN')
if __name__=='__main__':unittest.main()
