import os
import copy, hashlib, importlib.util, json, sys, tempfile, unittest
from pathlib import Path
CANDIDATE=Path(os.environ.get('PD_CANDIDATE',str(Path(__file__).resolve().parents[4]/'candidates/evolution-03/product-design'))).resolve()
sys.path.insert(0,str(CANDIDATE/'scripts'))
from evaluate_design import evaluate_design

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()

class GateCases(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
  self.source=self.put('requirements.json',{'owner':'engineering','minimum_area_mm2':100})
  self.record={'metric':'inlet_area','unit':'mm2','conditions':{'plane':'inlet'},'scope':'cad','method':'BREP section','status':'PASS','revision':'A','value':100,'uncertainty':0}
  self.baseline=self.put('baseline.json',{'revision':'A','validation':{'status':'PASS','scope':'cad'},'metrics':{'air':self.record}})
  self.contract={'schema':'product-design-contract-v1','id':'demo','mode':'cmf_study','target_scope':'cad_prototype','baseline':self.baseline,'requirements':[{'id':'air','source':self.source,'owner':'engineering','metric':'inlet_area','unit':'mm2','conditions':{'plane':'inlet'},'direction':'minimum','limits':{'min':100},'preserve':'nondecreasing','evidence_scopes':['cad'],'uncertainty_required':True}]}
  self.seal();self.candidate={'schema':'product-design-candidate-v1','revision':'B','mode':'cmf_study','contract_sha256':digest(self.contract),'baseline_sha256':self.baseline['sha256'],'purpose':'solution','metrics':{'air':self.put('candidate-area.json',dict(self.record,revision='B',value=110))}}
 def put(self,name,data):
  file=self.root/name;file.parent.mkdir(parents=True,exist_ok=True);file.write_text(json.dumps(data));return {'path':name,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()}
 def seal(self):
  policy={k:v for k,v in self.contract.items() if k!='authorization'}
  self.contract['authorization']=self.put('approval.json',{'decision':'APPROVED','authority':'engineering','policy_sha256':digest(policy)})
 def evaluate(self):return evaluate_design(self.contract,self.candidate,self.root)
 def metric(self,**changes):
  record=dict(self.record,revision='B',value=110);record.update(changes);self.candidate['metrics']['air']=self.put('candidate-area.json',record)
 def test_compatible_candidate_eligible(self):self.assertEqual(self.evaluate()['eligibility'],'ELIGIBLE')
 def test_reduction_blocks_and_no_offsetting_other_metric(self):
  self.metric(value=60);self.candidate['metrics']['other']={'value':10000};self.assertEqual(self.evaluate()['eligibility'],'BLOCKED')
 def test_missing_evidence_blocks(self):self.candidate['metrics']={};self.assertEqual(self.evaluate()['eligibility'],'BLOCKED')
 def test_stale_hash_blocks(self):(self.root/'candidate-area.json').write_text('{}');self.assertEqual(self.evaluate()['eligibility'],'BLOCKED')
 def test_unit_mismatch_blocks(self):self.metric(unit='cm2');self.assertEqual(self.evaluate()['eligibility'],'BLOCKED')
 def test_conditions_mismatch_blocks(self):self.metric(conditions={'plane':'outlet'});self.assertEqual(self.evaluate()['eligibility'],'BLOCKED')
 def test_revision_mismatch_blocks(self):self.metric(revision='old');self.assertEqual(self.evaluate()['eligibility'],'BLOCKED')
 def test_unvalidated_baseline_blocks(self):
  self.contract['baseline']=self.put('baseline.json',{'revision':'A','validation':{'status':'NOT_EVALUATED','scope':'cad'},'metrics':{'air':self.record}});self.seal();self.candidate['contract_sha256']=digest(self.contract);self.candidate['baseline_sha256']=self.contract['baseline']['sha256'];self.assertEqual(self.evaluate()['eligibility'],'BLOCKED')
 def test_limits_change_cannot_be_hidden_by_candidate_digest(self):self.contract['requirements'][0]['limits']['min']=1;self.candidate['contract_sha256']=digest(self.contract);self.assertEqual(self.evaluate()['eligibility'],'BLOCKED')
 def test_omitted_requirement_changes_policy(self):self.contract['requirements']=[];self.candidate['contract_sha256']=digest(self.contract);self.assertEqual(self.evaluate()['eligibility'],'BLOCKED')
 def test_nan_cannot_pass(self):self.metric(value=float('nan'));self.assertEqual(self.evaluate()['eligibility'],'BLOCKED')
 def test_declaration_cannot_satisfy_cad_scope(self):self.metric(scope='declaration');self.assertEqual(self.evaluate()['eligibility'],'BLOCKED')
 def test_uncertainty_overlap_is_not_proof(self):self.metric(value=100,uncertainty=1);self.assertEqual(self.evaluate()['eligibility'],'BLOCKED')
 def test_render_only_does_not_satisfy_redesign(self):
  self.contract['mode']='redesign';self.seal();self.candidate.update(mode='redesign',contract_sha256=digest(self.contract));self.assertEqual(self.evaluate()['eligibility'],'BLOCKED')
 def test_study_stays_exploratory_even_when_numbers_pass(self):self.candidate['purpose']='study';self.assertEqual(self.evaluate()['eligibility'],'EXPLORATORY')
 def test_cannot_infer_user_or_physical_approval(self):
  result=self.evaluate();self.assertEqual(result['user_acceptance'],'PENDING');self.assertEqual(result['physical_validation'],'NOT_EVALUATED')
 def test_outside_reference_blocks(self):self.candidate['metrics']['air']={'path':'../outside.json','sha256':'0'*64};self.assertEqual(self.evaluate()['eligibility'],'BLOCKED')
 def test_boolean_value_is_not_number(self):self.metric(value=True);self.assertEqual(self.evaluate()['eligibility'],'BLOCKED')
 def test_missing_uncertainty_blocks(self):
  record=dict(self.record,revision='B',value=110);record.pop('uncertainty');self.candidate['metrics']['air']=self.put('candidate-area.json',record);self.assertEqual(self.evaluate()['eligibility'],'BLOCKED')
if __name__=='__main__':unittest.main()
