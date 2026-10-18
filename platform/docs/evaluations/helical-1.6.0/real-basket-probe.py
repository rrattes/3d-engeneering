"""Read-only probe of actual Rev C STEP delivery with the native evaluator."""
import json,sys,time
from pathlib import Path
sys.path.insert(0,'/opt/cad3d')
from build123d import import_step,Pos,Plane
from service_states import evaluate_steps
basket=Path('/basket');pointer=json.loads((basket/'build/delivery/current.json').read_text());out=basket/pointer['directory']
# One actual P8 pair from the validated assembly; no alternate/fictitious threads.
source={name:import_step(str(out/(name+'.step'))) for name in ('glass_bracket','mount_screw')}
placed={'screw':Pos(22,46,80)*source['mount_screw'],'support':source['glass_bracket']}
base={'id':'withdraw','moving_ids':['screw'],'samples':1,'allowed_contact_pairs':['screw::support'],'motion':{'type':'helical','axis_origin_mm':[22,46,80],'axis_direction':[0,1,0],'pitch_mm':3,'handedness':'right','travel_mm':-15}}
results=[]
for hand,mirror,expected in [('right',False,'PASS'),('left',False,'FAIL'),('left',True,'PASS')]:
 p={n:s.mirror(Plane.YZ) if mirror else s for n,s in placed.items()}
 step={**base,'motion':{**base['motion'],'handedness':hand,'axis_origin_mm':[-22 if mirror else 22,46,80]}}
 start=time.monotonic();r=evaluate_steps(p,[step])[0]
 results.append({'hand':hand,'mirrored':mirror,'expected':expected,'seconds':time.monotonic()-start,'result':r})
 print(hand,mirror,r['status'],flush=True)
 assert r['status']==expected
 if expected=='PASS':assert r['removal_proven']
report={'status':'PASS','source_basket_run':pointer['run_id'],'cases':results,'physical_validation':'NOT_EVALUATED'}
Path('/evidence/real-basket.json').write_text(json.dumps(report,indent=2)+'\n')
