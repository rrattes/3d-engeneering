import os
import hashlib,json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
CANDIDATE=Path(os.environ.get('PD_CANDIDATE',str(ROOT/'docs/product-design/candidates/evolution-03/product-design'))).resolve()
sys.path.insert(0,str(CANDIDATE/'scripts'))
from pd_common import canonical_sha

class LocalProject(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
 def put(self,name,data):
  p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True)
  p.write_text(json.dumps(data) if not isinstance(data,str) else data)
  return {'path':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
