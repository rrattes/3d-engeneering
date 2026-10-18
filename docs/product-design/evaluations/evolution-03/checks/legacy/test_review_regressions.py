import unittest
import test_engineering_gate as gate
import test_selection as selection
from evaluate_design import evaluate_design
def configuration_sha(before,after,catalog,tolerance):
 return canonical_sha({'before':before,'after':after,'catalog':catalog,'tolerance_mm':tolerance})
from pd_common import canonical_sha

class ReviewRegressions(unittest.TestCase):
 setUp=gate.GateCases.setUp
 put=gate.GateCases.put
 seal=gate.GateCases.seal
 def evaluate(self):return evaluate_design(self.contract,self.candidate,self.root)
 def test_baseline_values_must_support_validated_claim(self):
  record=dict(self.record,value=60)
  self.contract['baseline']=self.put('baseline.json',{'revision':'A','validation':{'status':'PASS','scope':'cad'},'metrics':{'air':record}})
  self.seal();self.candidate.update(contract_sha256=canonical_sha(self.contract),baseline_sha256=self.contract['baseline']['sha256'])
  result=self.evaluate();self.assertEqual(result['eligibility'],'BLOCKED');self.assertNotEqual(next(x for x in result['checks'] if x['id']=='air')['status'],'PASS')
 def test_changed_frame_config_invalidates_old_geometry(self):
  self.contract['mode']='redesign';self.seal();self.candidate.update(mode='redesign',contract_sha256=canonical_sha(self.contract))
  config={'before':{'shell':'before.step'},'after':{'shell':'after.step'},'tolerance_mm':0.001,'catalog':{'units':'mm','before_revision':'A','after_revision':'B','volume_tolerance_mm3':0.01,'parts':{'shell':{'before_pose':[0]*6,'after_pose':[0]*6}}}}
  source=self.put('dummy-source.json',{'fixture':True})
  report={'schema':'product-design-geometry-v1','status':'PASS','units':'mm','before_revision':'A','after_revision':'B','source_artifacts':[source],'configuration_sha256':configuration_sha(config['before'],config['after'],config['catalog'],config['tolerance_mm']),'volume_tolerance_mm3':0.01,'parts':[{'id':'shell','status':'PASS','shape_change':'DETECTED','symmetric_difference_mm3':1}]}
  self.candidate['geometry']=self.put('geometry.json',report);self.candidate['geometry_config']=self.put('config.json',config)
  self.assertEqual(self.evaluate()['eligibility'],'ELIGIBLE')
  config['catalog']['parts']['shell']['after_pose'][0]=10
  self.candidate['geometry_config']=self.put('config.json',config)
  self.assertEqual(self.evaluate()['eligibility'],'BLOCKED')
 def test_missing_geometry_config_blocks(self):
  self.contract['mode']='redesign';self.seal();self.candidate.update(mode='redesign',contract_sha256=canonical_sha(self.contract))
  source=self.put('dummy.json',{})
  self.candidate['geometry']=self.put('geometry.json',{'schema':'product-design-geometry-v1','status':'PASS','units':'mm','before_revision':'A','after_revision':'B','source_artifacts':[source],'volume_tolerance_mm3':0.01,'parts':[{'id':'shell','status':'PASS','shape_change':'DETECTED','symmetric_difference_mm3':1}]})
  self.assertEqual(self.evaluate()['eligibility'],'BLOCKED')

class VisualRegression(selection.SelectionCases):
 # Avoid rerunning inherited scenarios; they run in test_selection.
 pass
# Add only the review-specific scenario to the suite below.
def visual_failure(self):
 self.prepare();self.review['criteria'].append({'id':'extra','status':'FAIL','image_paths':[self.image['path']],'finding':'contradiction','resolution':'open'})
 self.review_ref=self.put('review.json',self.review);self.put('decision.json',dict(self.decision,visual_review_sha256=self.review_ref['sha256']))
 self.assertEqual(self.select()['selection'],'BLOCKED')
VisualRegression.test_known_visual_fail_cannot_hide_under_global_pass=visual_failure

def load_tests(loader,tests,pattern):
 suite=loader.loadTestsFromTestCase(ReviewRegressions)
 suite.addTest(VisualRegression('test_known_visual_fail_cannot_hide_under_global_pass'))
 return suite
if __name__=='__main__':unittest.main()
