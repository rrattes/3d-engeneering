"""Isolated real STEP/CAD/render smoke pilot; not new product qualification."""
import copy,json,shutil,time
from pathlib import Path
import helpers as h
from pd_common import file_sha
from compare_geometry import compare_parts
from render_comparison import render_comparison
from impact_plan import plan_work,record_task
from delivery_manifest import inspect_delivery,publish_manifest
ROOT=h.ROOT;out=ROOT/'docs/product-design/evaluations/evolution-03/pilot/run02';out.mkdir(parents=True,exist_ok=True)
started=time.monotonic();source_inventory={};results={}
def dump(path,data):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
for name in ('jewelry','console'):
 project=out/name;project.mkdir(exist_ok=True);parts=[]
 if name=='jewelry':
  origin=ROOT/'Porta_Joias_Duas_Gavetas_Cinco_Estilos_Rev_A'
  cfg=json.loads((origin/'docs/comparacao-abertos.json').read_text())
  originals=cfg['cases'][0]['parts']
 else:
  origin=ROOT/'BC250_Console_Rev_B'
  originals=[{'source':{'path':'manufacturing/step/'+part+'.step'},'pose':[0]*6} for part in ('lid_LF','lid_RF','lid_LR','lid_RR')]
 for index,item in enumerate(originals):
  src=origin/item['source']['path'];sha=file_sha(src);source_inventory[str(src.relative_to(ROOT))]=sha
  target=project/f'part-{index}.step';shutil.copyfile(src,target)
  parts.append({'source':{'path':target.name,'sha256':sha},'pose':item['pose'],'color':'#aab1b7'})
 before={f'p{i}':p['source']['path'] for i,p in enumerate(parts)}
 catalog={'units':'mm','before_revision':'copied','after_revision':'cmf-study','volume_tolerance_mm3':.01,'angular_tolerance_deg':.000001,'project_root':str(project),'parts':{k:{'before_pose':[0]*6,'after_pose':[0]*6} for k in before}}
 t=time.monotonic();geometry=compare_parts(before,before,catalog,.001);dump(project/'geometry.json',geometry)
 assert geometry['status']=='PASS',geometry
 assert all(p['shape_change']=='NOT_DETECTED' for p in geometry['parts'])
 config={'schema':'product-design-visual-comparison-v1','units':'mm','cases':[{'id':'gray','label':'REFERENCE - GRAY','parts':parts},{'id':'cmf','label':'CMF STUDY - SAME CAD','parts':copy.deepcopy(parts)}],'views':[{'id':'iso','direction':[1,-1,.8],'up':[0,0,1]}]}
 for item in config['cases'][1]['parts']:item['color']='#315668'
 dump(project/'render.json',config);render=render_comparison(config,project,project/'reports/comparison');dump(project/'reports/comparison/visual-comparison.json',render)
 env={'image':'sha256:81ff095d899a294b16b58435622b2a16555ba5c45ff4e1f1c7d3613f818cfa4a'}
 tasks=[{'id':'cad','kind':'cad','inputs':[],'outputs':list(before.values()),'depends_on':[],'parameters':{'source':'copied, immutable real product STEP'},'environment':env,'dependencies_complete':True},
 {'id':'render','kind':'render','inputs':list(before.values())+['render.json'],'outputs':[render['images'][0]['path']],'depends_on':['cad'],'parameters':{},'environment':env,'dependencies_complete':True}]
 workflow={'schema':'product-design-workflow-v1','tasks':tasks};state={}
 for ident in ('cad','render'):state=record_task(workflow,state,project,ident)
 unchanged=plan_work(workflow,state,project)
 config['cases'][1]['parts'][0]['color']='#725530';dump(project/'render.json',config)
 color_plan=plan_work(workflow,state,project);assert [r['state'] for r in color_plan['tasks']]==['REUSE','RUN']
 # Actually produce the changed-color image; record reuse only after successful work.
 render2=render_comparison(config,project,project/'reports/comparison');dump(project/'reports/comparison/visual-comparison.json',render2)
 assert all(file_sha(project/p['source']['path'])==p['source']['sha256'] for p in parts)
 state=record_task(workflow,state,project,'render')
 deps=[p['source'] for p in parts]+[{'path':'render.json','sha256':file_sha(project/'render.json')}]
 artifacts=[{'id':f'cad{i}','role':'cad','part':f'p{i}','variant':'chosen','source':p['source'],'dependencies':[]} for i,p in enumerate(parts)]
 artifacts.append({'id':'render','role':'render','part':'assembly','variant':'cmf','source':render2['images'][0],'dependencies':deps})
 manifest={'schema':'product-design-delivery-v1','revision':'cmf-study','previous_manifest_ref':None,'artifacts':artifacts}
 publication=publish_manifest(manifest,project,None);assert publication['consistency']=='CONSISTENT',publication
 # Interrupted next attempt: config edits make old image stale; retain actual prior pointer.
 pointer=project/'reports/product-design/delivery/current.json';old=pointer.read_bytes();previous=file_sha(pointer)
 config['cases'][1]['parts'][0]['color']='#ffffff';dump(project/'render.json',config)
 manifest['revision']='interrupted-next';manifest['previous_manifest_ref']={'path':str(pointer.relative_to(project)),'sha256':previous}
 failed=publish_manifest(manifest,project,previous);assert failed['consistency']=='STALE';assert pointer.read_bytes()==old
 results[name]={'elapsed_seconds':round(time.monotonic()-t,3),'real_step_parts':len(parts),'geometry':geometry['status'],'shape_change':'NOT_DETECTED',
 'unchanged_plan':unchanged,'color_plan':color_plan,'actual_renders':2,'incremental_cad_regenerations':0,'delivery_before_interruption':publication,'interrupted_delivery':failed,
 'previous_pointer_preserved':True,'images':render2['images'],'scope':'real STEP import/comparison and CMF render only; no new physical or motion qualification'}
for path,sha in source_inventory.items():assert file_sha(ROOT/path)==sha
results['elapsed_seconds']=round(time.monotonic()-started,3);dump(out/'source-inventory.json',source_inventory);dump(out/'RESULT.json',results)
print(json.dumps({'status':'PASS_SCOPED_PILOT','seconds':results['elapsed_seconds'],'products':['jewelry','console']},indent=2))
