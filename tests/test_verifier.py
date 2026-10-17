import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from cusp_lifts import certificate
from verify import verify
class VerifierTests(unittest.TestCase):
 def test_valid_edge_cases(self):
  for args in [(1,1,0),(4,2,1),(819,3,1),(3600,60,29),(4096,64,63)]:
   with self.subTest(args=args):self.assertTrue(verify(certificate(*args)))
 def test_reject_finite_index_kernel(self):
  c=certificate(819,3,1);c['kernel_basis'][1]=[2*x for x in c['kernel_basis'][1]]
  self.assertFalse(verify(c))
 def test_reject_nonintegral_transport(self):
  c=certificate(819,3,1);c['P'][0][0]=1.0
  self.assertFalse(verify(c))
 def test_reject_wrong_isometry(self):
  c=certificate(819,3,1);c['Q'][0][0]+=1
  self.assertFalse(verify(c))
 def test_reject_wrong_norm(self):
  c=certificate(819,3,1);c['c'][0]+=1
  self.assertFalse(verify(c))
 def test_reject_wrong_parameter(self):
  c=certificate(819,3,1);c['d']+=1
  self.assertFalse(verify(c))
 def test_invalid_label(self):
  for args in [(10,3,1),(36,6,2),(0,1,0),(1,0,1)]:
   with self.assertRaises(ValueError):certificate(*args)
 def test_truncated_certificate(self):
  c=certificate(819,3,1);c.pop('kernel_basis')
  self.assertFalse(verify(c))
if __name__=='__main__':unittest.main()
