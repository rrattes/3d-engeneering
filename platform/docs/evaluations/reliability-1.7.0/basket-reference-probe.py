"""Read-only actual bracket STEP: datum points replace failed centroid assumptions."""
import sys,json
from pathlib import Path
sys.path.insert(0,'/opt/cad3d')
from build123d import import_step
from validation import select_face,local_thickness,pair_check
root=Path('/basket');p=json.loads((root/'build/delivery/current.json').read_text());out=root/p['directory'];shape=import_step(str(out/'glass_bracket.step'))
selectors=[{'ref':'side','surface':'plane','point_mm':[35,55,85],'normal':[1,0,0],'point_tolerance_mm':.01},{'ref':'bridge','surface':'plane','point_mm':[0,60,116],'normal':[0,0,1],'point_tolerance_mm':.01}]
selection=[select_face(shape,s)[1] for s in selectors]
assert all(r['status']=='PASS' for r in selection),selection
thickness=local_thickness(shape,1.2,samples_per_axis=2,face_selectors=selectors)
assert thickness['status'] in ('PASS','WARNING') and thickness['measured_samples']>0,thickness
from build123d import Pos,Axis
screw=Pos(22,46,80)*import_step(str(out/'mount_screw.step'))
wrong=screw.rotate(Axis((22,46,80),(0,1,0)),180)
collision=pair_check(wrong,shape,intentional_contact=True)
assert collision['status']=='FAIL' and collision['intersection_volume_mm3']>0,collision
report={'status':'PASS','source_run':p['run_id'],'selectors':selection,'scoped_thickness':thickness,'wrong_phase_static_collision':collision,'physical_validation':'NOT_EVALUATED','delivery_modified':False}
Path('/evidence/basket-reference.json').write_text(json.dumps(report,indent=2)+'\n')
print('Actual bracket: point selectors resolved; scoped thickness',thickness['status'],'; wrong-phase static collision FAIL as expected.')
