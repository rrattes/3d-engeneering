import json,subprocess,sys,unittest
import helpers as h
from pd_common import canonical_sha

class NewCliCases(h.LocalProject):
 def run_cli(self,name,*args):return subprocess.run([sys.executable,'-B',str(h.CANDIDATE/'scripts'/name),*args],capture_output=True,text=True)
 def test_style_cli_writes_selected_brief(self):
  run=self.run_cli('style_brief.py','--style','gamer','--variant','discreto','--project',str(self.root),'--output','reports/brief');self.assertEqual(run.returncode,0,run.stdout+run.stderr)
  data=json.loads((self.root/'reports/brief/style-brief.json').read_text());self.assertEqual(list(data['variants']),['discreto'])
 def test_invalid_style_cli_returns_input_code(self):self.assertEqual(self.run_cli('style_brief.py','--style','unknown').returncode,2)
 def workflow(self):
  self.put('source.json',{'geometry':'synthetic'});self.put('output.step','synthetic output, no CAD assertion')
  config={'schema':'product-design-workflow-v1','tasks':[{'id':'cad','kind':'cad','inputs':['source.json'],'outputs':['output.step'],'depends_on':[],'parameters':{},'environment':{'kernel':'synthetic'},'dependencies_complete':True}]}
  self.put('workflow.json',config)
 def cache_cli(self,action,*extra):return self.run_cli('impact_plan.py',action,'--project',str(self.root),'--config','workflow.json','--state','reports/cache.json',*extra)
 def test_cache_cli_records_then_reuses_and_invalidates(self):
  self.workflow();run=self.cache_cli('record','--task','cad');self.assertEqual(run.returncode,0,run.stdout+run.stderr)
  run=self.cache_cli('plan','--output','reports/plan');self.assertEqual(run.returncode,0,run.stdout+run.stderr);self.assertEqual(json.loads(run.stdout)['counts']['REUSE'],1)
  self.put('source.json',{'geometry':'changed'});run=self.cache_cli('plan','--output','reports/plan');self.assertEqual(json.loads(run.stdout)['counts']['RUN'],1)
 def test_cache_state_cannot_overwrite_source(self):
  self.workflow();before=(self.root/'source.json').read_bytes()
  run=self.run_cli('impact_plan.py','record','--project',str(self.root),'--config','workflow.json','--state','source.json','--task','cad')
  self.assertEqual(run.returncode,2);self.assertEqual(before,(self.root/'source.json').read_bytes())
 def test_cache_output_cannot_overwrite_config(self):
  self.workflow();config=json.loads((self.root/'workflow.json').read_text());self.put('reports/plan/work-plan.json',config);before=(self.root/'reports/plan/work-plan.json').read_bytes()
  run=self.run_cli('impact_plan.py','plan','--project',str(self.root),'--config','reports/plan/work-plan.json','--state','reports/cache.json','--output','reports/plan')
  self.assertEqual(run.returncode,2);self.assertEqual(before,(self.root/'reports/plan/work-plan.json').read_bytes())
 def test_custom_brief_cannot_overwrite_input(self):
  self.put('reports/brief/style-brief.json',{'form':'custom','criteria':['one']});before=(self.root/'reports/brief/style-brief.json').read_bytes()
  run=self.run_cli('style_brief.py','--style','custom','--custom',str(self.root/'reports/brief/style-brief.json'),'--project',str(self.root),'--output','reports/brief')
  self.assertEqual(run.returncode,2);self.assertEqual(before,(self.root/'reports/brief/style-brief.json').read_bytes())
 def test_summary_cli_has_live_scoped_result(self):
  contract={'schema':'product-design-contract-v1','id':'visual-fixture','mode':'cmf_study','target_scope':'visual_study','requirements':[]}
  candidate={'schema':'product-design-candidate-v1','revision':'B','mode':'cmf_study','purpose':'study','contract_sha256':canonical_sha(contract),'metrics':{}}
  self.put('contract.json',contract);self.put('candidate.json',candidate);self.put('changes.json',{'schema':'product-design-changes-v1','revision':'B','changes':[]})
  run=self.run_cli('design_summary.py','--project',str(self.root),'--contract','contract.json','--candidate','candidate.json','--changes','changes.json','--output','reports/summary')
  self.assertEqual(run.returncode,0,run.stdout+run.stderr);data=json.loads((self.root/'reports/summary/design-summary.json').read_text());self.assertEqual(data['engineering']['eligibility'],'EXPLORATORY');self.assertEqual(data['user_acceptance'],'PENDING')

 def test_renderer_invalid_config_returns_input_code(self):
  self.put('invalid.json',[])
  run=self.run_cli('render_comparison.py','--project',str(self.root),'--config','invalid.json','--output','reports/images')
  self.assertEqual(run.returncode,2,run.stdout+run.stderr)

if __name__=='__main__':unittest.main()
