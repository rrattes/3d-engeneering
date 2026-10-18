import copy,json,struct,unittest
import helpers as h
from build123d import Box,Pos,export_step
from pd_common import file_sha
from render_comparison import render_comparison,camera_for_bounds,unit,cross,dot
import itertools

class CameraCases(unittest.TestCase):
 def test_projected_corners_fit_image_and_annotation_margins(self):
  boxes=[[[100,200,-5],[600,250,90]],[[-90,-80,0],[100,300,400]]]
  for direction,up in [([1,-1,.8],[0,0,1]),([0,0,1],[0,1,0]),([-1,0,0],[0,0,1])]:
   aspect=800/680;c=camera_for_bounds(boxes,direction,up,aspect);normal=unit(direction);right=unit(cross(c['up'],normal));vertical=unit(c['up']);scale=c['parallel_scale_mm']
   for b in boxes:
    for point in itertools.product(*zip(*b)):
     offset=[point[i]-c['target'][i] for i in range(3)]
     self.assertLessEqual(abs(dot(offset,right)),scale*aspect);self.assertLessEqual(abs(dot(offset,vertical)),scale*.78)

class RenderCases(h.LocalProject):
 def setUp(self):
  super().setUp();export_step(Box(20,30,10),str(self.root/'a.step'));export_step(Pos(0,0,0)*Box(30,20,15),str(self.root/'b.step'))
  def part(path):return {'source':{'path':path,'sha256':file_sha(self.root/path)},'pose':[0]*6}
  self.config={'schema':'product-design-visual-comparison-v1','units':'mm','cases':[{'id':'before','parts':[part('a.step')]},{'id':'after','parts':[part('b.step')]}],'views':[{'id':'iso','direction':[1,-1,.8],'up':[0,0,1]}]}
 def render(self):return render_comparison(self.config,self.root,self.root/'reports/compare')
 def test_real_png_and_manifest_without_aesthetic_approval(self):
  result=self.render();self.assertEqual(result['status'],'PASS');self.assertEqual(result['actual_visual_review'],'NOT_EVALUATED');self.assertEqual(result['user_acceptance'],'PENDING')
  path=self.root/result['images'][0]['path'];data=path.read_bytes();self.assertEqual(data[:8],b'\x89PNG\r\n\x1a\n');self.assertEqual(struct.unpack('>II',data[16:24]),(1600,680));self.assertEqual(file_sha(path),result['images'][0]['sha256']);self.assertEqual(len(result['sources']),2)
 def test_stale_source_hash_rejected(self):
  self.config['cases'][0]['parts'][0]['source']['sha256']='0'*64
  with self.assertRaises(ValueError):self.render()
 def test_missing_display_pose_rejected(self):
  self.config['cases'][0]['parts'][0].pop('pose')
  with self.assertRaises(ValueError):self.render()
 def test_render_directory_confined(self):
  with self.assertRaises(ValueError):render_comparison(self.config,self.root,self.root/'outside_reports')
 def test_path_traversal_view_id_rejected(self):
  self.config['views'][0]['id']='../escape'
  with self.assertRaises(ValueError):self.render()
 def test_source_geometry_not_modified_by_render(self):
  original=[file_sha(self.root/x) for x in ('a.step','b.step')];self.render();self.assertEqual(original,[file_sha(self.root/x) for x in ('a.step','b.step')])
if __name__=='__main__':unittest.main()
