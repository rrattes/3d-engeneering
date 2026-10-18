import copy
from helpers import LocalProject,canonical_sha
from engineering_evidence import validate_engineering_evidence,adapt_cad3d_report
class EvidenceTests(LocalProject):
 def fixture(self):
  self.source=self.put('part.step','solid');self.params=self.put('params.json',{'wall':2})
  self.criterion={'id':'wall','part':'body','requirement_id':'W','method':'sampled','unit':'mm','expected_limit':{'min':2},'coverage':{'scope':'sampled','locations':100},'calibration':'c1'}
  self.policy={'schema':'product-design-evidence-policy-v1','revision':'r1','source_refs':[self.source],'parameter_ref':self.params,'checks':[self.criterion]}
  self.pref=self.put('policy.json',self.policy)
  self.record={**self.criterion,'revision':'r1','status':'PASS','observed_value':2.2}
  self.rref=self.put('report.json',{'schema':'cad3d-product-design-report-v1','revision':'r1','source_refs':[self.source],'parameter_ref':self.params,'checks':[self.record]})
  self.evidence=adapt_cad3d_report(self.rref,self.pref,self.root)
  self.contract={'engineering_evidence':self.pref};self.candidate={'revision':'r1','engineering_evidence':self.put('evidence.json',self.evidence)}
 def check(self):
  self.candidate['engineering_evidence']=self.put('evidence.json',self.evidence)
  return validate_engineering_evidence(self.contract,self.candidate,self.root)['status']
 def test_current(self):self.fixture();self.assertEqual(self.check(),'PASS')
 def test_weaker_limit(self):
  self.fixture();self.record['expected_limit']={'min':1.2};self.rref=self.put('report.json',{'x':self.record});self.evidence['checks'][0]['artifact_ref']={**self.rref,'pointer':'/x'};self.assertNotEqual(self.check(),'PASS')
 def test_stale_source(self):self.fixture();self.put('part.step','changed');self.assertNotEqual(self.check(),'PASS')
 def test_missing_candidate(self):self.fixture();self.candidate.pop('engineering_evidence');self.assertNotEqual(validate_engineering_evidence(self.contract,self.candidate,self.root)['status'],'PASS')
 def test_revision(self):self.fixture();self.candidate['revision']='r2';self.assertNotEqual(self.check(),'PASS')
 def test_calibration(self):
  self.fixture();self.evidence['checks'][0]['calibration']='c2';self.assertNotEqual(self.check(),'PASS')
 def test_missing_coverage(self):self.fixture();self.evidence['checks'][0].pop('coverage');self.assertNotEqual(self.check(),'PASS')
 def test_unknown_provider(self):
  self.fixture();r=self.put('other.json',{'status':'PASS','exit_code':0});self.assertEqual(adapt_cad3d_report(r,self.pref,self.root)['status'],'NOT_EVALUATED')
 def test_json_pointer_alias(self):
  self.fixture();r=self.put('nested.json',{'report':{'schema':'cad3d-product-design-report-v1','revision':'r1','source_refs':[self.source],'parameter_ref':self.params,'checks':[self.record]}})
  self.assertEqual(adapt_cad3d_report({**r,'json_pointer':'/report'},self.pref,self.root)['status'],'PASS')
 def test_orientation_requires_datum(self):
  self.fixture();self.policy['checks'][0]['orientation']={'pose':[0,0,0,0,0,0]};self.pref=self.put('policy.json',self.policy);self.contract['engineering_evidence']=self.pref;self.evidence['policy_ref']=self.pref;self.assertNotEqual(self.check(),'PASS')
 def test_orientation_conflict(self):
  self.fixture();self.policy['checks'][0]['orientation']={'datum':'base','pose':[0,0,0,0,0,0],'support':'nominal'};self.pref=self.put('policy.json',self.policy);self.contract['engineering_evidence']=self.pref;self.evidence['policy_ref']=self.pref;self.evidence['checks'][0]['orientation']={'datum':'base','pose':[0,0,0,0,0,180],'support':'nominal'};self.assertNotEqual(self.check(),'PASS')
 def test_provider_envelope_wrong_source_even_if_repinned(self):
  self.fixture();wrong=self.put('wrong.step','different');r=self.put('report.json',{'schema':'cad3d-product-design-report-v1','revision':'r1','source_refs':[wrong],'parameter_ref':self.params,'checks':[self.record]});self.evidence['report_ref']=r;self.evidence['checks'][0]['artifact_ref']={**r,'pointer':'/checks/0'};self.assertNotEqual(self.check(),'PASS')
 def test_provider_envelope_wrong_parameters_even_if_repinned(self):
  self.fixture();wrong=self.put('wrong.json',{'wall':1.2});r=self.put('report.json',{'schema':'cad3d-product-design-report-v1','revision':'r1','source_refs':[self.source],'parameter_ref':wrong,'checks':[self.record]});self.evidence['report_ref']=r;self.evidence['checks'][0]['artifact_ref']={**r,'pointer':'/checks/0'};self.assertNotEqual(self.check(),'PASS')
 def test_live_gate_cannot_omit_contracted_evidence(self):
  from evaluate_design import evaluate_design
  self.fixture();contract={'schema':'product-design-contract-v1','id':'evidence','mode':'cmf_study','target_scope':'visual_study','requirements':[],'engineering_evidence':self.pref}
  contract['authorization']=self.put('approval.json',{'authority':'engineering','decision':'APPROVED','policy_sha256':canonical_sha(contract)})
  candidate={**self.candidate,'schema':'product-design-candidate-v1','mode':'cmf_study','purpose':'study','contract_sha256':canonical_sha(contract)}
  self.assertEqual(evaluate_design(contract,candidate,self.root)['eligibility'],'EXPLORATORY')
  candidate.pop('engineering_evidence');self.assertEqual(evaluate_design(contract,candidate,self.root)['eligibility'],'BLOCKED')
