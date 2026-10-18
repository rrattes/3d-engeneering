"""Identical behavioral probes against the CLI actually shipped in each image."""
import contextlib,io,json,os,sys,tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
sys.path.insert(0,'/opt/cad3d')
import cad3d,yaml
from build123d import Box
result={'runtime':getattr(cad3d,'CAD3D_VERSION','unknown')}
with tempfile.TemporaryDirectory() as directory:
 os.chdir(directory);Path('.cad3d').mkdir();Path('out').mkdir()
 params={'printer':{'profile':'unknown-printer'},'material':{'profile':'pla'}}
 def validate():
  with patch.object(cad3d,'project_files',return_value=({},params,{'block':Box(10,10,10)},Path('out'))),contextlib.redirect_stdout(io.StringIO()):cad3d.validate(SimpleNamespace(assembly=None))
  return json.loads(Path('out/validation.json').read_text())
 r=validate();result['unknown_printer']={'profile_evidence':r.get('printer_profile'),'manufacturing_assessment':r['states']['manufacturing_assessment']}
 pc={'name':'Fixture','nozzle_diameter_mm':.4,'process_settings_sha256':'a'*64,'calibration_profile':'cal.yaml'}
 Path('.cad3d/printer.yaml').write_text(yaml.safe_dump(pc))
 identity={'printer':'Fixture','material':'pla','nozzle_diameter_mm':.4,'process_settings_sha256':'a'*64}
 Path('cal.yaml').write_text(yaml.safe_dump({'calibrated':True,'identity':identity,'min_wall_mm':1.6}))
 try:result['calibration_without_local_wall']={'result':'RETURNED','calibration_status':validate()['calibration_profile']['status']}
 except Exception as error:result['calibration_without_local_wall']={'result':'EXCEPTION','type':type(error).__name__,'message':str(error)}
 for f in Path('.cad3d').glob('*'):f.unlink()
 Path('model.py').write_text('from build123d import Box\ndef build(p):return {"support":Box(10,10,3),"fan":Box(8,8,4)}\n')
 Path('.cad3d/project.yaml').write_text(yaml.safe_dump({'project':{'name':'mixed-probe','model':'model.py','parameters':'params.yaml'}}));Path('.cad3d/params.yaml').write_text('{}')
 Path('.cad3d/assembly.yaml').write_text(yaml.safe_dump({'parts':{'support':{'kind':'manufactured','process':'fdm'},'fan':{'kind':'commercial','process':'none'}},'components':[{'id':'s1','part':'support'},{'id':'s2','part':'support','position_mm':[20,0,0]},{'id':'fan','part':'fan','position_mm':[40,0,0]}]}))
 with contextlib.redirect_stdout(io.StringIO()):cad3d.export(None)
 out=Path('build/outputs');result['mixed_exports']={'commercial_fan_stl_created':(out/'fan.stl').exists(),'support_stl_created':(out/'support.stl').exists(),'assembly_step_created':(out/'assembly.step').exists(),'bom_created':(out/'BOM.csv').exists()}
 result['checked_release_available']=callable(getattr(cad3d,'release',None))
print(json.dumps(result,indent=2))
