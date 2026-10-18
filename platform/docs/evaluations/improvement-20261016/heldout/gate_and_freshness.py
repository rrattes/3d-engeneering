import sys,json,os,hashlib
from pathlib import Path
sys.path.insert(0,'/candidate/cli')
import yaml
from cad3d import require_product_architecture,ProductArchitectureGateError
from product_engineering import validate_architecture
from source_fingerprint import project_fingerprint
root=Path('/fixture/scenario_project');(root/'.cad3d').mkdir(parents=True,exist_ok=True)
(root/'.cad3d/project.yaml').write_text(yaml.safe_dump({'project':{'model':'model.py','parameters':'parameters.json','output':'build/outputs'}}))
(root/'model.py').write_text('from geometry import build\n')
(root/'geometry.py').write_text('def build(params): return {}\n')
(root/'.cad3d/parameters.json').write_text('{"width": 10}\n')
(root/'.cad3d/assembly.yaml').write_text(yaml.safe_dump({'components':[{'id':'fan','part':'fan'},{'id':'support','part':'support'}]}))
eng={'workflow_level':'product','model_gate':True,'project':{'name':'synthetic-gate','class':'assembly','purpose':'fan fixture','units':'mm'},'mechanical_architecture':{'components':[{'id':'fan','part':'fan','function':'cooling'},{'id':'support','part':'support','function':'support'}]}}
results={}
os.chdir(root)
for gate_value in (True,False):
 eng['model_gate']=gate_value
 (root/'.cad3d/engineering.yaml').write_text(yaml.safe_dump({'engineering':eng}))
 arch=validate_architecture(root)
 try:
  require_product_architecture(); gate={'status':'UNEXPECTED_UNBLOCKED'}
 except ProductArchitectureGateError as e:gate=e.payload
 results['gate_'+str(gate_value)]={'gate':gate,'architecture':arch}
a=project_fingerprint(root);mh=hashlib.sha256((root/'model.py').read_bytes()).hexdigest()
(root/'geometry.py').write_text('def build(params): return {"changed": params["width"]}\n')
(root/'.cad3d/parameters.json').write_text('{"width": 12}\n')
b=project_fingerprint(root)
results['freshness']={'old':a,'new':b,'model_py_unchanged':mh==hashlib.sha256((root/'model.py').read_bytes()).hexdigest(),'inventory_changed':a['sha256']!=b['sha256'],'changed_files':[r['path'] for r in b['files'] if r not in a['files']]}
Path('/fixture/gate_freshness_results.json').write_text(json.dumps(results,indent=2))
print(json.dumps({'gates':{k:v['gate'] for k,v in results.items() if k.startswith('gate')},'freshness':{k:v for k,v in results['freshness'].items() if k not in ('old','new')}},indent=2))
