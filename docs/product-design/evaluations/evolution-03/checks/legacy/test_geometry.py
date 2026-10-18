import sys,tempfile,unittest
from pathlib import Path
from test_engineering_gate import CANDIDATE
sys.path.insert(0,str(CANDIDATE/'scripts'))
from compare_geometry import compare_parts
from build123d import Box,Pos,Compound,export_step,Align

class GeometryCases(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
  self.catalog={'project_root':str(self.root),'units':'mm','volume_tolerance_mm3':1e-5,'parts':{'p':{'before_pose':[0]*6,'after_pose':[0]*6}}}
 def step(self,name,shape):
  path=self.root/name;export_step(shape,str(path));return path
 def compare(self,a,b):return compare_parts({'p':self.step('a.step',a)},{'p':self.step('b.step',b)},self.catalog,.001)
 def test_reexport_not_redesign(self):
  r=self.compare(Box(20,20,10),Box(20,20,10));self.assertEqual(r['status'],'PASS');self.assertEqual(r['parts'][0]['shape_change'],'NOT_DETECTED')
 def test_same_volume_and_box_can_change_shape(self):
  base=Box(20,20,10,align=(Align.MIN,)*3)
  a=base-Pos(5,5,0)*Box(2,2,10,align=(Align.MIN,)*3);b=base-Pos(12,12,0)*Box(2,2,10,align=(Align.MIN,)*3)
  self.assertAlmostEqual(a.volume,b.volume);r=self.compare(a,b);self.assertEqual(r['parts'][0]['shape_change'],'DETECTED');self.assertGreater(r['parts'][0]['symmetric_difference_mm3'],79)
 def test_pose_change_is_not_reshape(self):
  self.catalog['parts']['p']['after_pose']=[10,0,0,0,0,0]
  r=self.compare(Box(20,20,10),Pos(10,0,0)*Box(20,20,10));self.assertEqual(r['parts'][0]['shape_change'],'NOT_DETECTED');self.assertTrue(r['parts'][0]['pose_changed'])
 def test_missing_frame_unknown(self):
  self.catalog['parts']['p'].pop('before_pose');self.assertEqual(self.compare(Box(2,2,2),Box(2,2,2))['status'],'NOT_EVALUATED')
 def test_located_compound_is_not_false_change(self):
  obj=Compound([Pos(30,0,0)*Box(4,4,4),Pos(0,30,0)*Box(4,4,4)])
  r=self.compare(obj,obj);self.assertEqual(r['status'],'PASS');self.assertEqual(r['parts'][0]['shape_change'],'NOT_DETECTED')
 def test_overlapping_compound_unknown(self):
  obj=Compound([Box(4,4,4),Pos(1,0,0)*Box(4,4,4)]);self.assertEqual(self.compare(obj,obj)['status'],'NOT_EVALUATED')
 def test_added_part_detected(self):
  path=self.step('a.step',Box(3,3,3));self.catalog['parts']['p'].pop('before_pose')
  r=compare_parts({}, {'p':path},self.catalog,.001);self.assertEqual(r['parts'][0]['shape_change'],'DETECTED');self.assertEqual(r['parts'][0]['change_type'],'ADDED')
 def test_unknown_units_block_comparison(self):
  self.catalog['units']='cm';self.assertEqual(self.compare(Box(2,2,2),Box(2,2,2))['status'],'NOT_EVALUATED')
if __name__=='__main__':unittest.main()
