from helpers import LocalProject
from delivery_manifest import inspect_delivery,publish_manifest
from pd_common import file_sha
class DeliveryTests(LocalProject):
 def fixture(self):
  src=self.put('cad.step','solid');render=self.put('image.png','pixels')
  return {'schema':'product-design-delivery-v1','revision':'r1','previous_manifest_ref':None,'artifacts':[{'id':'cad','role':'cad','part':'body','variant':'minimal','source':src,'dependencies':[]},{'id':'render','role':'render','part':'body','variant':'minimal','source':render,'dependencies':[src]}]}
 def test_consistent_not_engineering(self):
  m=self.fixture();r=inspect_delivery(m,self.root);self.assertEqual(r['consistency'],'CONSISTENT');self.assertEqual(r['engineering']['status'],'NOT_EVALUATED')
 def test_cad_changes_render_stale(self):
  m=self.fixture();self.put('cad.step','new');r=inspect_delivery(m,self.root);self.assertEqual(r['consistency'],'STALE');self.assertEqual(r['artifact_states']['render'],'STALE')
 def test_missing(self):
  m=self.fixture();(self.root/'image.png').unlink();self.assertEqual(inspect_delivery(m,self.root)['consistency'],'INCOMPLETE')
 def test_escape(self):
  m=self.fixture();m['artifacts'][0]['source']['path']='../bad';self.assertEqual(inspect_delivery(m,self.root)['consistency'],'INVALID')
 def test_publish_and_stale_preserves(self):
  m=self.fixture();r=publish_manifest(m,self.root,None);self.assertEqual(r['consistency'],'CONSISTENT');p=self.root/'reports/product-design/delivery/current.json';old=p.read_bytes();self.put('image.png','changed');m['previous_manifest_ref']={'path':str(p.relative_to(self.root)),'sha256':file_sha(p)};r=publish_manifest(m,self.root,file_sha(p));self.assertEqual(r['consistency'],'STALE');self.assertEqual(old,p.read_bytes())
 def test_compare_previous(self):
  m=self.fixture();publish_manifest(m,self.root,None);p=self.root/'reports/product-design/delivery/current.json';old=p.read_bytes();r=publish_manifest(m,self.root,None);self.assertEqual(r['consistency'],'INVALID');self.assertEqual(old,p.read_bytes())
 def test_previous_chain(self):
  m=self.fixture();publish_manifest(m,self.root,None);p=self.root/'reports/product-design/delivery/current.json';sha=file_sha(p);m['revision']='r2';m['previous_manifest_ref']={'path':str(p.relative_to(self.root)),'sha256':sha};self.assertEqual(publish_manifest(m,self.root,sha)['consistency'],'CONSISTENT')
 def test_no_source_overwrite(self):
  m=self.fixture();m['artifacts'][0]['source']=self.put('reports/product-design/delivery/current.json','input');self.assertEqual(publish_manifest(m,self.root,None)['consistency'],'INVALID')
 def test_shared_helper_invalidates(self):
  m=self.fixture();ref=self.put('helper.py','v1');m['artifacts'][0]['dependencies']=[ref];m['artifacts'][1]['dependencies'].append(ref);self.put('helper.py','v2');r=inspect_delivery(m,self.root);self.assertTrue(all(s=='STALE' for s in r['artifact_states'].values()))
 def test_pointer_warning_preserved(self):
  m=self.fixture();r=self.put('technical.json',{'result':{'revision':'r1','status':'WARNING'}});m['engineering_ref']={**r,'json_pointer':'/result'};self.assertEqual(inspect_delivery(m,self.root)['engineering']['status'],'WARNING')
 def test_stale_visual_record(self):
  m=self.fixture();r=self.put('review.json',{'revision':'r1'});m['visual_review_ref']=r;self.put('review.json',{});self.assertNotEqual(inspect_delivery(m,self.root)['consistency'],'CONSISTENT')
 def test_missing_acceptance(self):
  m=self.fixture();m['acceptance_ref']={'path':'absent.json','sha256':'0'*64};self.assertNotEqual(inspect_delivery(m,self.root)['consistency'],'CONSISTENT')
 def test_review_revision(self):
  m=self.fixture();m['visual_review_ref']=self.put('review.json',{'revision':'old'});self.assertNotEqual(inspect_delivery(m,self.root)['consistency'],'CONSISTENT')
 def test_current_visual_coverage(self):
  m=self.fixture();m.update(contract_sha256='a'*64,candidate_sha256='b'*64)
  m['visual_review_ref']=self.put('review.json',{'schema':'product-design-visual-review-v1','revision':'r1','contract_sha256':'a'*64,'candidate_sha256':'b'*64,'images':[m['artifacts'][1]['source']],'variants':['minimal']})
  result=inspect_delivery(m,self.root);self.assertEqual(result['consistency'],'CONSISTENT');self.assertEqual(result['review_coverage']['count'],1)
 def test_review_binding_mismatch(self):
  m=self.fixture();m.update(contract_sha256='a'*64,candidate_sha256='b'*64)
  m['visual_review_ref']=self.put('review.json',{'schema':'product-design-visual-review-v1','revision':'r1','contract_sha256':'x'*64,'candidate_sha256':'b'*64,'images':[m['artifacts'][1]['source']]})
  self.assertNotEqual(inspect_delivery(m,self.root)['consistency'],'CONSISTENT')
