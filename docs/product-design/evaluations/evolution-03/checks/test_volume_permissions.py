from helpers import LocalProject
from pd_common import file_sha
from compare_geometry import compare_parts
from design_freedom import evaluate_freedom
from build123d import Box,Pos,export_step
class VolumePermissions(LocalProject):
 def step(self,name,shape):
  p=self.root/name;export_step(shape,str(p));return {'path':name,'sha256':file_sha(p)}
 def fixture(self,after=None):
  self.before=Box(10,10,10);self.after=after if after is not None else self.before+Pos(6,0,0)*Box(2,4,4)+Pos(-6,0,0)*Box(2,4,4)
  src=self.step('before.step',self.before);self.step('after.step',self.after)
  self.config={'before':{'body':'before.step'},'after':{'body':'after.step'},'catalog':{'units':'mm','before_revision':'b','after_revision':'a','volume_tolerance_mm3':0.001,'angular_tolerance_deg':0.000001,'parts':{'body':{'before_pose':[0]*6,'after_pose':[0]*6}}},'tolerance_mm':0.001}
  self.geo=compare_parts(self.config['before'],self.config['after'],dict(self.config['catalog'],project_root=str(self.root)),self.config['tolerance_mm'])
  reg=lambda name,shape:{'id':name,'source':self.step(name+'.step',shape),'pose':[0]*6}
  self.mapping={'schema':'product-design-freedom-v2','mode':'brep_regions','units':'mm','coordinate_frame':'comparison_local_mm','baseline_revision':'b','engineering_source':self.put('authority.json',{'owner':'engineering'}),'margin_mm':0.2,'margins_embedded':True,'comparison_policy':{'linear_tolerance_mm':.001,'volume_tolerance_mm3':.001,'angular_tolerance_deg':.000001},'parts':[{'id':'body','source':src,'before_pose':[0]*6,'after_pose':[0]*6,'locked':False,'pose_locked':True,'protected_material':[reg('core',Box(8,8,8))],'protected_void':[reg('void',Pos(0,0,8)*Box(4,4,4))],'editable_volumes':[reg('left',Pos(-6,0,0)*Box(4,6,6)),reg('right',Pos(6,0,0)*Box(4,6,6))]}]}
 def test_opposite_additions_pass(self):self.fixture();self.assertEqual(evaluate_freedom(self.mapping,self.geo,self.root,self.config)['status'],'PASS')
 def test_void_obstruction(self):
  self.fixture(Box(10,10,10)+Pos(0,0,6)*Box(2,2,6));r=evaluate_freedom(self.mapping,self.geo,self.root,self.config);self.assertEqual(r['status'],'FAIL')
 def test_core_removal(self):self.fixture(Box(10,10,10)-Box(2,2,2));self.assertEqual(evaluate_freedom(self.mapping,self.geo,self.root,self.config)['status'],'FAIL')
 def test_margin_missing(self):self.fixture();del self.mapping['margin_mm'];self.assertNotEqual(evaluate_freedom(self.mapping,self.geo,self.root,self.config)['status'],'PASS')
 def test_threshold_changed(self):self.fixture();self.config['catalog']['volume_tolerance_mm3']=1000;self.assertNotEqual(evaluate_freedom(self.mapping,self.geo,self.root,self.config)['status'],'PASS')
 def test_stale_region(self):self.fixture();self.step('core.step',Box(2,2,2));self.assertNotEqual(evaluate_freedom(self.mapping,self.geo,self.root,self.config)['status'],'PASS')
 def test_pose_stale(self):self.fixture();self.config['catalog']['parts']['body']['after_pose'][5]=180;self.assertNotEqual(evaluate_freedom(self.mapping,self.geo,self.root,self.config)['status'],'PASS')
 def test_added_outside_union(self):self.fixture(Box(10,10,10)+Pos(0,6,0)*Box(2,2,2));self.assertEqual(evaluate_freedom(self.mapping,self.geo,self.root,self.config)['status'],'FAIL')
 def test_invalid_boolean_fails_closed(self):
  from unittest.mock import patch
  self.fixture()
  with patch('design_freedom_brep.region_metrics',side_effect=RuntimeError('invalid boolean')):
   self.assertEqual(evaluate_freedom(self.mapping,self.geo,self.root,self.config)['status'],'NOT_EVALUATED')
 def test_mixed_topology_rejected(self):
  from build123d import Compound
  from compare_geometry import solid_fragments
  mixed=Compound(children=[Box(2,2,2),(Pos(10,0,0)*Box(2,2,2)).faces()[0]])
  with self.assertRaises(ValueError):solid_fragments(mixed)
