"""Matched-scope demonstration of CAD reuse after CMF-only change, not a universal benchmark."""
import json,shutil,subprocess,sys,time
import helpers as h
from impact_plan import plan_work,record_task
from pd_common import file_sha
ROOT=h.ROOT;demo=ROOT/'reports/product-design-evolution-02/productivity-demo';demo.mkdir(parents=True,exist_ok=True)
recipes=json.loads((h.CANDIDATE/'assets/feature_recipes.json').read_text())['recipes']
config_path=demo/'comparison.json';workflow_path=demo/'workflow.json'
def relative(p):return str(p.relative_to(ROOT))
def save(path,value):path.write_text(json.dumps(value,indent=2)+'\n')
def call(script,*args):
 run=subprocess.run([sys.executable,'-B',str(h.CANDIDATE/'scripts'/script),'--project',str(ROOT),*args],capture_output=True,text=True)
 if run.returncode:raise RuntimeError(script+': '+run.stdout+run.stderr)
 return run.stdout.strip()
inputs=[];outputs=[];cases=[]
for style,spec in recipes.items():
 path=demo/(style+'.json');save(path,spec);inputs.append(relative(path))
 folder=demo/'features'/style
 outputs.extend(relative(folder/('style-feature.'+ext)) for ext in ('step','json','md'))
 cases.append({'id':style,'label':style.upper(),'parts':[{'source':{'path':relative(folder/'style-feature.step'),'sha256':'pending-generation'},'pose':[0]*6}]})
config={'schema':'product-design-visual-comparison-v1','units':'mm','cases':cases,'views':[{'id':'iso','direction':[1,-1.2,.9],'up':[0,0,1]}]}
# Fill hashes only after the real feature CLI generation, before rendering.
environment={'cad_image_id':'sha256:81ff095d899a294b16b58435622b2a16555ba5c45ff4e1f1c7d3613f818cfa4a','vtk_window':'vtkEGLRenderWindow'}
workflow={'schema':'product-design-workflow-v1','tasks':[{'id':'features','kind':'cad','inputs':inputs+[relative(h.CANDIDATE/'scripts/style_geometry.py'),relative(h.CANDIDATE/'scripts/pd_common.py')],'outputs':outputs,'depends_on':[],'parameters':{},'environment':environment,'dependencies_complete':True},{'id':'render','kind':'render','inputs':[c['parts'][0]['source']['path'] for c in cases]+[relative(config_path),relative(h.CANDIDATE/'scripts/render_comparison.py'),relative(h.CANDIDATE/'scripts/pd_common.py'),'3d-engineering-evolution-20261017/cli/cad3d_visualization.py'],'outputs':[relative(demo/'comparison/comparison-iso.png'),relative(demo/'comparison/visual-comparison.json'),relative(demo/'comparison/visual-comparison.md')],'depends_on':['features'],'parameters':{},'environment':environment,'dependencies_complete':True}]}
start=time.perf_counter()
for style in recipes:call('style_geometry.py','--spec',relative(demo/(style+'.json')),'--output',relative(demo/'features'/style))
feature_seconds=time.perf_counter()-start
for case in cases:case['parts'][0]['source']['sha256']=file_sha(ROOT/case['parts'][0]['source']['path'])
save(config_path,config);save(workflow_path,workflow)
state=record_task(workflow,{},ROOT,'features')
start=time.perf_counter();call('render_comparison.py','--config',relative(config_path),'--output',relative(demo/'comparison'));render_seconds=time.perf_counter()-start
state=record_task(workflow,state,ROOT,'render');save(demo/'cache-before-cmf.json',state)
shutil.copy2(demo/'comparison/comparison-iso.png',demo/'before-cmf.png')
step_hashes={case['id']:file_sha(ROOT/case['parts'][0]['source']['path']) for case in cases}
for case in config['cases']:case['parts'][0]['color']='#526f83'
save(config_path,config)
plan=plan_work(workflow,state,ROOT);states={r['id']:r['state'] for r in plan['tasks']};assert states=={'features':'REUSE','render':'RUN'},states
start=time.perf_counter();call('render_comparison.py','--config',relative(config_path),'--output',relative(demo/'comparison'));cmf_seconds=time.perf_counter()-start
state=record_task(workflow,state,ROOT,'render');save(demo/'cache-after-cmf.json',state)
final={r['id']:r['state'] for r in plan_work(workflow,state,ROOT)['tasks']};assert final=={'features':'REUSE','render':'REUSE'},final
assert step_hashes=={case['id']:file_sha(ROOT/case['parts'][0]['source']['path']) for case in cases}
result={'scope':'Single five-feature demonstration; real CLI exports/renders; no physical claims','after_cmf_plan':states,'after_execution_plan':final,'cad_step_hashes_preserved':True,'baseline_commands':6,'cmf_only_commands':1,'elapsed_seconds':{'feature_stage_five_cli_calls':feature_seconds,'baseline_render_cli':render_seconds,'cmf_render_cli':cmf_seconds},'limits':['One local run; OS/library warming and changed render inputs are not controlled for causal timing comparison.','No percentage or token savings claim.','Cache does not grant engineering/visual/user acceptance.'],'step_sha256':step_hashes}
save(demo/'result.json',result);print(json.dumps(result),flush=True)
