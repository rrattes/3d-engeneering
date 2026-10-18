import unittest, tempfile, sys
from pathlib import Path
from test_engineering_gate import digest
import test_engineering_gate as fixtures
from test_engineering_gate import CANDIDATE
sys.path.insert(0,str(CANDIDATE/'scripts'))
from pd_common import safe_output, number
from evaluate_design import evaluate_design
from compare_geometry import configuration_sha

class IntegrityCases(unittest.TestCase):
 setUp=fixtures.GateCases.setUp
 put=fixtures.GateCases.put
 seal=fixtures.GateCases.seal
 def test_output_cannot_target_delivery(self):
  with self.assertRaises(ValueError):safe_output(self.root,'build/delivery','engineering-gate',[])
 def test_output_cannot_overwrite_evidence(self):
  ref=self.put('reports/x/engineering-gate.json',{})
  with self.assertRaises(ValueError):safe_output(self.root,'reports/x','engineering-gate',[ref])
 def test_output_may_be_reused_report_directory(self):self.assertEqual(safe_output(self.root,'reports/eval','engineering-gate',[]),self.root/'reports/eval')
 def test_huge_number_rejected_cleanly(self):
  with self.assertRaises(ValueError):number(10**10000)
 def geometry(self):
  self.contract['mode']='redesign';self.seal();self.candidate.update(mode='redesign',contract_sha256=digest(self.contract))
  source=self.put('cad.json',{'synthetic':True})
  config={'before':{'shell':'a.step'},'after':{'shell':'b.step'},'catalog':{'units':'mm','before_revision':'A','after_revision':'B','volume_tolerance_mm3':0.01,'parts':{'shell':{'before_pose':[0]*6,'after_pose':[0]*6}}},'tolerance_mm':0.001}
  self.candidate['geometry_config']=self.put('config.json',config)
  config_sha=configuration_sha(config['before'],config['after'],config['catalog'],config['tolerance_mm'])
  return {'schema':'product-design-geometry-v1','status':'PASS','units':'mm','before_revision':'A','after_revision':'B','source_artifacts':[source],'configuration_sha256':config_sha,'volume_tolerance_mm3':0.01,'parts':[{'id':'shell','status':'PASS','shape_change':'DETECTED','symmetric_difference_mm3':1}]}
 def test_geometry_from_other_revision_blocks(self):
  data=self.geometry();data['after_revision']='unrelated';self.candidate['geometry']=self.put('geometry.json',data)
  self.assertEqual(evaluate_design(self.contract,self.candidate,self.root)['eligibility'],'BLOCKED')
 def test_geometry_bound_to_expected_revisions(self):
  self.candidate['geometry']=self.put('geometry.json',self.geometry())
  self.assertEqual(evaluate_design(self.contract,self.candidate,self.root)['eligibility'],'ELIGIBLE')
if __name__=='__main__':unittest.main()
