import sys, unittest
import test_engineering_gate as gate_cases
from test_engineering_gate import digest
from select_candidate import select_candidate

class SelectionCases(unittest.TestCase):
 setUp=gate_cases.GateCases.setUp
 put=gate_cases.GateCases.put
 seal=gate_cases.GateCases.seal
 metric=gate_cases.GateCases.metric
 def prepare(self):
  self.contract['visual_criteria']=['silhouette'];self.seal();self.candidate['contract_sha256']=digest(self.contract)
  self.image=self.put('images/view.json',{'synthetic':'image reference only, not an aesthetic evaluation'})
  self.review={'schema':'product-design-visual-review-v1','revision':'B','contract_sha256':digest(self.contract),'candidate_sha256':digest(self.candidate),'reviewer':'fixture','status':'PASS','images':[self.image],'criteria':[{'id':'silhouette','status':'PASS','image_paths':[self.image['path']],'finding':'synthetic fixture','resolution':'synthetic fixture'}]}
  self.review_ref=self.put('review.json',self.review)
  self.decision={'authority':'user','decision':'APPROVED','contract_sha256':digest(self.contract),'candidate_sha256':digest(self.candidate),'visual_review_sha256':self.review_ref['sha256'],'target_scope':'cad_prototype'}
  self.put('decision.json',self.decision)
 def select(self):return select_candidate(self.contract,self.candidate,self.root,self.review_ref,{'path':'decision.json','sha256':__import__('hashlib').sha256((self.root/'decision.json').read_bytes()).hexdigest()})
 def test_acceptance_updates_only_own_pointer(self):
  self.prepare();self.assertEqual(self.select()['selection'],'ACCEPTED');self.assertTrue((self.root/'design/product-design/accepted.json').is_file())
 def test_block_preserves_prior_pointer(self):
  self.prepare();self.put('design/product-design/accepted.json',{'old':'preserve'});before=(self.root/'design/product-design/accepted.json').read_bytes();self.metric(value=60)
  self.assertEqual(self.select()['selection'],'BLOCKED');self.assertEqual(before,(self.root/'design/product-design/accepted.json').read_bytes())
 def test_study_cannot_be_selected(self):
  self.candidate['purpose']='study';self.prepare();self.assertEqual(self.select()['selection'],'BLOCKED')
 def test_stale_decision_blocks(self):
  self.prepare();self.put('decision.json',dict(self.decision,candidate_sha256='0'*64));self.assertEqual(self.select()['selection'],'BLOCKED')
 def test_stale_image_blocks(self):
  self.prepare();(self.root/self.image['path']).write_text('{}');self.assertEqual(self.select()['selection'],'BLOCKED')
 def test_missing_visual_criterion_blocks(self):
  self.prepare();self.review['criteria']=[];self.review_ref=self.put('review.json',self.review);self.put('decision.json',dict(self.decision,visual_review_sha256=self.review_ref['sha256']));self.assertEqual(self.select()['selection'],'BLOCKED')
 def test_symlink_pointer_blocked(self):
  self.prepare();self.put('innocent.json',{'preserve':1});directory=self.root/'design/product-design';directory.mkdir(parents=True);(directory/'accepted.json').symlink_to(self.root/'innocent.json');self.assertEqual(self.select()['selection'],'BLOCKED');self.assertIn('preserve',(self.root/'innocent.json').read_text())
 def test_visual_revision_mismatch_blocks(self):
  self.prepare();self.review['revision']='A';self.review_ref=self.put('review.json',self.review);self.put('decision.json',dict(self.decision,visual_review_sha256=self.review_ref['sha256']));self.assertEqual(self.select()['selection'],'BLOCKED')

if __name__=='__main__':unittest.main()
