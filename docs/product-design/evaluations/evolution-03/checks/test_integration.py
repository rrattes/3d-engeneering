import base64,copy,hashlib,json,sys,unittest
import helpers as h
sys.path.insert(0,str(h.Path(__file__).parent/'legacy'))
import test_engineering_gate as legacy
from build123d import Box,Pos,export_step,Align
from compare_geometry import compare_parts
from pd_common import canonical_sha,file_sha
from evaluate_design import evaluate_design
from select_candidate import select_candidate
from design_summary import summarize

class MapIntegrationCases(unittest.TestCase):
 def setUp(self):
  self.fixture=legacy.GateCases();self.fixture.setUp();self.addCleanup(self.fixture.doCleanups);self.root=self.fixture.root;self.put=self.fixture.put
  self.contract=self.fixture.contract;self.candidate=self.fixture.candidate
  shape=Box(20,20,10,align=(Align.MIN,)*3);changed=shape-Pos(2,2,0)*Box(2,2,10,align=(Align.MIN,)*3)
  export_step(shape,str(self.root/'before.step'));export_step(changed,str(self.root/'after.step'))
  self.config={'before':{'shell':'before.step'},'after':{'shell':'after.step'},'tolerance_mm':.001,'catalog':{'units':'mm','before_revision':'A','after_revision':'B','include_delta_bounds':True,'volume_tolerance_mm3':.01,'angular_tolerance_deg':1e-6,'parts':{'shell':{'before_pose':[0]*6,'after_pose':[0]*6}}}}
  report=compare_parts(self.config['before'],self.config['after'],dict(self.config['catalog'],project_root=str(self.root)),.001)
  self.assertEqual(report['status'],'PASS',report)
  self.mapping={'schema':'product-design-freedom-v1','units':'mm','coordinate_frame':'comparison_local_mm','baseline_revision':'A','engineering_source':self.fixture.source,'margin_mm':0,'comparison_policy':{'linear_tolerance_mm':.001,'volume_tolerance_mm3':.01,'angular_tolerance_deg':1e-6,'non_detection_policy':'require_identical_source'},'parts':[{'id':'shell','source':{'path':'before.step','sha256':file_sha(self.root/'before.step')},'before_pose':[0]*6,'locked':False,'pose_locked':True,'editable_regions':[{'id':'exterior','bounds_mm':[[-1,-1,-1],[21,21,11]]}],'protected_regions':[{'id':'interface','bounds_mm':[[10,0,0],[12,20,10]],'reason':'synthetic protected interface'}]}]}
  self.contract.update(mode='redesign',visual_criteria=['silhouette']);self.contract['design_freedom']=self.put('map.json',self.mapping)
  self.fixture.seal();self.candidate.update(mode='redesign',contract_sha256=canonical_sha(self.contract),geometry=self.put('geometry.json',report),geometry_config=self.put('config.json',self.config))
 def gate(self):return evaluate_design(self.contract,self.candidate,self.root)
 def update_map(self):
  self.contract['design_freedom']=self.put('map.json',self.mapping);self.fixture.seal();self.candidate['contract_sha256']=canonical_sha(self.contract)
 def review(self):
  path=self.root/'fixture.png';path.write_bytes(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jmZkAAAAASUVORK5CYII='));ref={'path':'fixture.png','sha256':file_sha(path)}
  review={'schema':'product-design-visual-review-v1','status':'PASS','revision':'B','reviewer':'SYNTHETIC TEST RECORD','contract_sha256':canonical_sha(self.contract),'candidate_sha256':canonical_sha(self.candidate),'images':[ref],'criteria':[{'id':'silhouette','status':'PASS','finding':'synthetic case only','resolution':'synthetic case only','image_paths':['fixture.png']}]}
  review_ref=self.put('review.json',review);decision_ref=self.put('decision.json',{'authority':'user','decision':'APPROVED','contract_sha256':canonical_sha(self.contract),'candidate_sha256':canonical_sha(self.candidate),'visual_review_sha256':review_ref['sha256'],'target_scope':self.contract['target_scope'],'notice':'SYNTHETIC UNIT/INTEGRATION FIXTURE, not real product approval'})
  return review_ref,decision_ref
 def test_real_delta_passes_live_map_gate(self):
  result=self.gate();self.assertEqual(result['eligibility'],'ELIGIBLE',result);self.assertEqual(next(c for c in result['checks'] if c['id']=='design_freedom')['status'],'PASS')
 def test_protected_delta_blocks_full_gate(self):
  self.mapping['parts'][0]['protected_regions'][0]['bounds_mm']=[[1,1,-1],[5,5,11]];self.update_map();self.assertEqual(self.gate()['eligibility'],'BLOCKED')
 def test_missing_map_evidence_blocks(self):
  (self.root/'map.json').unlink();self.assertEqual(self.gate()['eligibility'],'BLOCKED')
 def test_unauthorized_map_removal_blocks(self):
  self.contract.pop('design_freedom');self.candidate['contract_sha256']=canonical_sha(self.contract);self.assertEqual(self.gate()['eligibility'],'BLOCKED')
 def test_changed_config_frames_do_not_relocate_permissions(self):
  self.config['catalog']['parts']['shell']['before_pose'][0]=20;self.config['catalog']['parts']['shell']['after_pose'][0]=20
  report=compare_parts(self.config['before'],self.config['after'],dict(self.config['catalog'],project_root=str(self.root)),.001)
  self.candidate.update(geometry=self.put('geometry.json',report),geometry_config=self.put('config.json',self.config));self.assertEqual(self.gate()['eligibility'],'BLOCKED')
 def test_synthetic_selection_accepts_permitted_geometry(self):
  review,decision=self.review();self.assertEqual(select_candidate(self.contract,self.candidate,self.root,review,decision)['selection'],'ACCEPTED')
 def test_blocked_map_preserves_pointer_despite_visual_and_user_records(self):
  pointer=self.root/'design/product-design/accepted.json';pointer.parent.mkdir(parents=True);pointer.write_text('{"revision":"old-fixture"}');old=pointer.read_bytes()
  self.mapping['parts'][0]['locked']=True;self.update_map();review,decision=self.review()
  result=select_candidate(self.contract,self.candidate,self.root,review,decision);self.assertEqual(result['selection'],'BLOCKED');self.assertEqual(pointer.read_bytes(),old)
 def test_summary_uses_live_gate_not_prior_pass(self):
  changes={'schema':'product-design-changes-v1','revision':'B','changes':[{'part':'shell','feature':'outer relief','intent':'synthetic','affected_requirements':['air']}]}
  self.assertEqual(summarize(self.contract,self.candidate,changes,self.root)['engineering']['eligibility'],'ELIGIBLE')
  (self.root/'map.json').write_text('{}');self.assertEqual(summarize(self.contract,self.candidate,changes,self.root)['engineering']['eligibility'],'BLOCKED')
 def test_stale_geometry_not_shown_as_current_part_pass(self):
  changes={'schema':'product-design-changes-v1','revision':'B','changes':[]};(self.root/'before.step').write_text('changed')
  result=summarize(self.contract,self.candidate,changes,self.root);self.assertEqual(result['engineering']['eligibility'],'BLOCKED');self.assertEqual(result['parts'][0]['evidence_status'],'NOT_EVALUATED')
if __name__=='__main__':unittest.main()

class BREPIntegration(unittest.TestCase):
 def test_v2_gate_summary_selector_and_protected_void(self):
  f=MapIntegrationCases();f.setUp();self.addCleanup(f.doCleanups)
  def region(name,shape):
   path=f.root/(name+'.step');export_step(shape,str(path));return {'id':name,'source':{'path':path.name,'sha256':file_sha(path)},'pose':[0]*6}
  p=f.mapping['parts'][0]
  f.mapping.update(schema='product-design-freedom-v2',mode='brep_regions',margins_embedded=True)
  p.update(after_pose=[0]*6,protected_material=[region('core',Pos(10,5,2)*Box(2,2,2,align=(Align.MIN,)*3))],protected_void=[region('void',Pos(30,30,30)*Box(2,2,2))],editable_volumes=[region('editable',Box(50,50,50))])
  f.update_map();self.assertEqual(f.gate()['eligibility'],'ELIGIBLE')
  changes={'schema':'product-design-changes-v1','revision':'B','changes':[{'part':'shell','feature':'relief','affected_requirements':['air']}]}
  self.assertEqual(summarize(f.contract,f.candidate,changes,f.root)['engineering']['eligibility'],'ELIGIBLE')
  review,decision=f.review();self.assertEqual(select_candidate(f.contract,f.candidate,f.root,review,decision)['selection'],'ACCEPTED')
  # A protected material patch including the removed relief is violated.
  p['protected_material']=[region('changed-core',Pos(2,2,1)*Box(2,2,2,align=(Align.MIN,)*3))];f.update_map()
  self.assertEqual(f.gate()['eligibility'],'BLOCKED')
