import json, subprocess, sys, unittest
import test_engineering_gate as fixtures
from test_engineering_gate import digest, CANDIDATE

class CliCases(unittest.TestCase):
 setUp=fixtures.GateCases.setUp
 put=fixtures.GateCases.put
 seal=fixtures.GateCases.seal
 metric=fixtures.GateCases.metric
 def run_cli(self,script,*args):return subprocess.run([sys.executable,str(CANDIDATE/'scripts'/script),'--project',str(self.root),*args],capture_output=True,text=True)
 def test_gate_cli_live_report_and_block_code(self):
  self.metric(value=60);self.put('contract.json',self.contract);self.put('candidate.json',self.candidate)
  run=self.run_cli('evaluate_design.py','--contract','contract.json','--candidate','candidate.json','--output','reports/evaluation')
  self.assertEqual(run.returncode,3,run.stdout+run.stderr);self.assertEqual(json.loads((self.root/'reports/evaluation/engineering-gate.json').read_text())['eligibility'],'BLOCKED')
 def test_exploratory_exit_zero_is_not_acceptance(self):
  self.contract.pop('authorization');self.contract['requirements']=[];self.candidate.update(contract_sha256=digest(self.contract),purpose='study');self.put('contract.json',self.contract);self.put('candidate.json',self.candidate)
  run=self.run_cli('evaluate_design.py','--contract','contract.json','--candidate','candidate.json','--output','reports/study')
  self.assertEqual(run.returncode,0,run.stdout+run.stderr);self.assertIn('EXPLORATORY',run.stdout)
 def test_selection_cli_block_preserves_existing_pointer(self):
  self.metric(value=60);self.put('contract.json',self.contract);self.put('candidate.json',self.candidate);self.put('review.json',{});self.put('decision.json',{});self.put('design/product-design/accepted.json',{'revision':'old'})
  before=(self.root/'design/product-design/accepted.json').read_bytes()
  run=self.run_cli('select_candidate.py','--contract','contract.json','--candidate','candidate.json','--visual-review','review.json','--user-decision','decision.json')
  self.assertEqual(run.returncode,3,run.stdout+run.stderr);self.assertEqual(before,(self.root/'design/product-design/accepted.json').read_bytes())
if __name__=='__main__':unittest.main()
