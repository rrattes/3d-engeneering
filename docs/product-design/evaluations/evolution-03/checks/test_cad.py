import copy,json,unittest
from unittest.mock import patch
import helpers as h
from build123d import Box,Pos,Solid,export_step,import_step,Align
from compare_geometry import compare_parts
from style_geometry import make_feature
from design_freedom import evaluate_freedom
from pd_common import canonical_sha

class FeatureCases(unittest.TestCase):
 def test_five_recipes_produce_real_single_solids(self):
  recipes=json.loads((h.CANDIDATE/'assets/feature_recipes.json').read_text())['recipes']
  for style,spec in recipes.items():
   with self.subTest(style=style):
    shape=make_feature(spec);self.assertTrue(shape.is_valid);self.assertEqual(len(shape.solids()),1);self.assertGreater(shape.volume,0)
 def test_relief_is_real_and_rotated(self):
  shape=make_feature({'kind':'relief','length':30,'width':2,'height':1,'angle_deg':30,'z':3});self.assertAlmostEqual(shape.volume,60)
 def test_invalid_profile_rejected(self):
  with self.assertRaises(ValueError):make_feature({'kind':'frame','outer':{'kind':'rounded','width':10,'depth':10,'radius':8},'inner':{'kind':'rounded','width':4,'depth':4,'radius':1},'height':2})
 def test_frame_must_contain_inner_contour(self):
  with self.assertRaises(ValueError):make_feature({'kind':'frame','outer':{'kind':'rounded','width':20,'depth':20,'radius':9},'inner':{'kind':'rounded','width':19,'depth':19,'radius':1},'height':2})
 def test_duplicate_loft_level_rejected(self):
  section={'kind':'rounded','width':20,'depth':20,'radius':3,'z':0}
  with self.assertRaises(ValueError):make_feature({'kind':'loft','ruled':True,'sections':[section,section]})

class DeltaCases(h.LocalProject):
 def setUp(self):
  super().setUp();self.catalog={'project_root':str(self.root),'units':'mm','volume_tolerance_mm3':.01,'angular_tolerance_deg':1e-6,'include_delta_bounds':True,'before_revision':'A','after_revision':'B','parts':{'shell':{'before_pose':[0]*6,'after_pose':[0]*6}}}
 def compare(self,a,b):
  export_step(a,str(self.root/'before.step'));export_step(b,str(self.root/'after.step'))
  return compare_parts({'shell':'before.step'},{'shell':'after.step'},self.catalog,.001)
 def test_cut_delta_bounds_match_actual_removed_material(self):
  a=Box(20,20,10,align=(Align.MIN,)*3);b=a-Pos(2,2,0)*Box(2,2,10,align=(Align.MIN,)*3)
  r=self.compare(a,b);self.assertEqual(r['status'],'PASS',r);bounds=r['parts'][0]['delta_bounds_mm'];self.assertAlmostEqual(bounds[0][0],2,places=5);self.assertAlmostEqual(bounds[1][0],4,places=5);self.assertAlmostEqual(r['parts'][0]['symmetric_difference_mm3'],40,places=4)
 def test_added_material_delta_is_bounded(self):
  a=Box(20,20,10);b=a+Pos(11,0,0)*Box(4,4,4)
  r=self.compare(a,b);self.assertEqual(r['status'],'PASS',r);self.assertGreater(r['parts'][0]['delta_bounds_mm'][0][0],9.9)
 def test_rigid_motion_normalized_with_delta_enabled(self):
  self.catalog['parts']['shell']['after_pose']=[7,0,0,0,0,0];a=Box(10,10,10)
  r=self.compare(a,Pos(7,0,0)*a);self.assertEqual(r['status'],'PASS',r);self.assertIsNone(r['parts'][0]['delta_bounds_mm']);self.assertEqual(r['parts'][0]['shape_change'],'NOT_DETECTED')
 def test_removed_part_has_delta(self):
  export_step(Box(4,4,4),str(self.root/'before.step'))
  r=compare_parts({'shell':'before.step'},{},self.catalog,.001);self.assertEqual(r['status'],'PASS',r);self.assertIsNotNone(r['parts'][0]['delta_bounds_mm'])
 def test_invalid_delta_fragment_cannot_be_discarded(self):
  a=Box(20,20,10);b=a-Pos(9,0,0)*Box(4,4,12)
  export_step(a,str(self.root/'before.step'));export_step(b,str(self.root/'after.step'))
  class Fragment:
   is_valid=False
  class BrokenResult:
   is_valid=False
   def solids(self):return [Fragment()]
  with patch.object(Solid,'__sub__',return_value=BrokenResult()):
   r=compare_parts({'shell':'before.step'},{'shell':'after.step'},self.catalog,.001)
  self.assertEqual(r['status'],'NOT_EVALUATED',r);self.assertIn('invalid',r['parts'][0]['reason'])

if __name__=='__main__':unittest.main()
