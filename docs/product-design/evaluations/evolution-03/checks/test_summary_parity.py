from helpers import LocalProject
from design_summary import render_summary_markdown
class SummaryParity(LocalProject):
 def test_all_facts_and_escape(self):
  result={'revision':'r|1','engineering':{'eligibility':'BLOCKED','checks':[{'id':'wall','status':'NOT_EVALUATED','unit':'mm','expected_limit':{'min':2},'observed_value':1.2,'coverage':{'scope':'sampled'},'artifact_ref':{'path':'old.json'},'reason':'stale'}]},'parts':[{'part':'body|x','feature':'rim','affected_requirements':['wall'],'evidence_status':'NOT_EVALUATED','volume_after_mm3':None}], 'notes':['old metrics'],'visual_review':'NOT_EVALUATED','user_acceptance':'PENDING','physical_validation':'NOT_EVALUATED','delivery':{'consistency':'STALE'}}
  md=render_summary_markdown(result)
  for text in ['rim','wall','sampled','old.json','1.2','min','2','mm','STALE','PENDING','null']:self.assertIn(text,md)
  self.assertIn('body\\|x',md)
