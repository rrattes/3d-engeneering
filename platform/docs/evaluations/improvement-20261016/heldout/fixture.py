import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,'/candidate/cli')
from build123d import Box,Cylinder,Pos,export_step
from validation import pair_check,assembly_path_check
out=Path('/fixture')
# Independent, intentionally small geometries; all dimensions are assumed millimetres.
head=Pos(0,0,1.5)*Cylinder(3,3)
shank=Pos(0,0,-3)*Cylinder(1.5,6)
sink_bad=Pos(3,0,1.5)*Box(4,12,3)
sink_good=Pos(7,0,1.5)*Box(4,12,3)
# Driver shaft + handle envelope, deliberately checked independently from installed hardware.
tool=(Pos(0,0,9)*Cylinder(2,12)).fuse(Pos(0,0,19)*Cylinder(4,8))
bridge_bad=Pos(0,0,12)*Box(3,12,2)
bridge_good=Pos(10,0,12)*Box(3,12,2)
panel=Pos(0,0,30)*Box(20,20,2)
fan=Pos(0,0,37)*Box(8,8,4)
# Additional anchors remain installed in both service configurations.
anchor=Pos(-15,15,30)*Box(3,3,3)
shapes=dict(head=head,shank=shank,sink_bad=sink_bad,sink_good=sink_good,tool=tool,bridge_bad=bridge_bad,bridge_good=bridge_good,panel=panel,fan=fan,anchor=anchor)
checks={
 'head_sink_negative':pair_check(head,sink_bad,pair_id='head::sink'),
 'head_sink_corrected':pair_check(head,sink_good,min_clearance=0.5,pair_id='head::sink'),
 'head_bridge_installed':pair_check(head,bridge_bad,min_clearance=0.5,pair_id='head::bridge'),
 'tool_bridge_negative':pair_check(tool,bridge_bad,pair_id='driver::bridge'),
 'tool_bridge_corrected':pair_check(tool,bridge_good,min_clearance=0.5,pair_id='driver::bridge'),
 'panel_fan_installed':pair_check(panel,fan,min_clearance=0.5,pair_id='panel::fan'),
}
placed={'panel':panel,'fan':fan,'anchor':anchor}
for name,mover,direction,travel in [('panel_path_negative','panel',[0,0,-1],15),('panel_path_corrected','panel',[-1,0,0],30),('fan_path_corrected','fan',[0,0,-1],15)]:
 checks[name]=assembly_path_check(placed,dict(id=name,moving_component=mover,direction_mm=direction,travel_mm=travel,samples=60))
female=(10.4-.15,10.4+.15);male=(10-.10,10+.10)
clearance=(female[0]-male[1],female[1]-male[0])
checks['signed_tolerance']={'female_bounds_mm':female,'male_bounds_mm':male,'clearance_bounds_mm':clearance,'required_min_mm':.2,'nominal_clearance_mm':.4,'status':'PASS' if clearance[0]>=.2 else 'FAIL','deficit_mm':.2-clearance[0]}
checks['fixture_scope']={'kind':'synthetic_BREP_regression','dimensions':'assumed; not vendor qualified','valid_solids':{k:bool(v.is_valid) for k,v in shapes.items()},'retention_strength':'NOT_EVALUATED','physical_validation':'NOT_EVALUATED','sampling':'61 poses inclusive; panel corrected spacing 0.5 mm; other paths 0.25 mm; continuous motion not proven','service_prerequisites':'release own fasteners; other item remains installed; anchors remain; cables/grip/thread engagement not represented'}
for k,v in shapes.items():export_step(v,str(out/(k+'.step')))
(out/'results.json').write_text(json.dumps(checks,indent=2))
print(json.dumps(checks,indent=2))
