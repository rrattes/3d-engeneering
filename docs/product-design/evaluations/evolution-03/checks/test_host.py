import copy,unittest
import helpers as h
from style_brief import make_brief
from impact_plan import ordered,plan_work,record_task
from design_freedom import evaluate_freedom
from compare_geometry import configuration_sha
from render_comparison import camera_for_bounds

class VocabularyCases(unittest.TestCase):
 def test_ten_substyles_and_references_are_scoped(self):
  profiles={'minimalista':['domestico','preciso'],'gamer':['discreto','expressivo'],'industrial':['precisao','robusto'],'organico':['seixo','fluido'],'retro':['art_deco','anos_1950']}
  for style,variants in profiles.items():
   for variant in variants:
    result=make_brief(style,variant);self.assertEqual(list(result['variants']),[variant]);self.assertTrue(result['references']);self.assertTrue(all(r['visual_assessment']=='NOT_EVALUATED' for r in result['references']))
 def test_custom_direction_is_allowed(self):self.assertEqual(make_brief('custom',custom={'form':'hexagonal','criteria':['legible']})['style'],'custom')
 def test_custom_needs_form_and_criteria(self):
  with self.assertRaises(ValueError):make_brief('custom',custom={'form':'round'})
 def test_unknown_substyle_is_not_silently_selected(self):
  with self.assertRaises(ValueError):make_brief('gamer','unknown')
 def test_camera_fits_wide_tall_and_offcenter_bounds(self):
  boxes=[[[100,200,-5],[600,250,90]],[[-90,-80,0],[100,300,400]]]
  for direction,up in [([1,-1,.8],[0,0,1]),([0,0,1],[0,1,0])]:
   camera=camera_for_bounds(boxes,direction,up,800/680);self.assertGreater(camera['parallel_scale_mm'],0);self.assertEqual(len(camera['target']),3)
 def test_degenerate_camera_rejected(self):
  with self.assertRaises(ValueError):camera_for_bounds([[[0,0,0],[1,1,1]]],[0,0,1],[0,0,1],1)

class CacheCases(h.LocalProject):
 def setUp(self):
  super().setUp()
  for name in ['geometry.json','cmf.json','model.py','cad.step','image.png']:self.put(name,name)
  self.config={'schema':'product-design-workflow-v1','tasks':[{'id':'cad','kind':'cad','inputs':['geometry.json','model.py'],'outputs':['cad.step'],'depends_on':[],'parameters':{},'environment':{'kernel':'existing-image'},'dependencies_complete':True},{'id':'render','kind':'render','inputs':['cad.step','cmf.json'],'outputs':['image.png'],'depends_on':['cad'],'parameters':{},'environment':{'renderer':'v1'},'dependencies_complete':True}]}
 def warmed(self):
  state=record_task(self.config,{},self.root,'cad');return record_task(self.config,state,self.root,'render')
 def states(self,state):return {r['id']:r['state'] for r in plan_work(self.config,state,self.root)['tasks']}
 def test_current_artifacts_reused(self):self.assertEqual(self.states(self.warmed()),{'cad':'REUSE','render':'REUSE'})
 def test_cmf_change_preserves_cad_reuse(self):
  state=self.warmed();self.put('cmf.json','new color');self.assertEqual(self.states(state),{'cad':'REUSE','render':'RUN'})
 def test_geometry_change_invalidates_downstream(self):
  state=self.warmed();self.put('geometry.json','new shape');self.assertEqual(self.states(state),{'cad':'RUN','render':'RUN'})
 def test_corrupted_output_is_not_reused(self):
  state=self.warmed();self.put('cad.step','corrupted');self.assertEqual(self.states(state),{'cad':'RUN','render':'RUN'})
 def test_changed_tool_invalidates_only_relevant_task(self):
  state=self.warmed();self.config['tasks'][1]['environment']['renderer']='v2';self.assertEqual(self.states(state),{'cad':'REUSE','render':'RUN'})
 def test_rerecorded_changed_parent_output_still_invalidates_child(self):
  state=self.warmed();self.put('cad.step','new actual output');state=record_task(self.config,state,self.root,'cad');self.assertEqual(self.states(state),{'cad':'REUSE','render':'RUN'})
 def test_record_requires_current_upstream(self):
  with self.assertRaises(ValueError):record_task(self.config,{},self.root,'render')
 def test_record_requires_output(self):
  (self.root/'cad.step').unlink()
  with self.assertRaises(ValueError):record_task(self.config,{},self.root,'cad')
 def test_missing_dependency_completeness_blocks(self):
  self.config['tasks'][0]['dependencies_complete']=False;self.assertEqual(self.states({})['cad'],'BLOCKED')
 def test_missing_external_input_blocks(self):
  (self.root/'model.py').unlink();self.assertEqual(self.states({})['cad'],'BLOCKED')
 def test_cycle_rejected(self):
  self.config['tasks'][0]['depends_on']=['render']
  with self.assertRaises(ValueError):ordered(self.config,self.root)
 def test_missing_producer_edge_rejected(self):
  self.config['tasks'][1]['depends_on']=[]
  with self.assertRaises(ValueError):ordered(self.config,self.root)
 def test_duplicate_producer_rejected(self):
  self.config['tasks'][1]['outputs']=['cad.step']
  with self.assertRaises(ValueError):ordered(self.config,self.root)
 def test_external_path_rejected(self):
  self.config['tasks'][0]['inputs']=['../escape']
  with self.assertRaises(ValueError):ordered(self.config,self.root)
 def test_no_engineering_acceptance_from_cache(self):self.assertEqual(plan_work(self.config,self.warmed(),self.root)['engineering_acceptance'],'NOT_EVALUATED')
 def test_malformed_task_cache_rejected_cleanly(self):
  with self.assertRaises(ValueError):plan_work(self.config,{'schema':'product-design-cache-v1','tasks':[]},self.root)

 def test_malformed_cache_record_rejected_cleanly(self):
  with self.assertRaises(ValueError):plan_work(self.config,{'schema':'product-design-cache-v1','tasks':{'cad':'invalid record'}},self.root)

class FreedomCases(h.LocalProject):
 def setUp(self):
  super().setUp();source=self.put('before.step','synthetic source, no CAD import in host cases');self.put('after.step','different synthetic bytes')
  self.config={'before':{'shell':'before.step'},'after':{'shell':'after.step'},'tolerance_mm':.001,'catalog':{'units':'mm','volume_tolerance_mm3':.01,'angular_tolerance_deg':1e-6,'parts':{'shell':{'before_pose':[0]*6,'after_pose':[0]*6}}}}
  self.part={'id':'shell','source':source,'before_pose':[0]*6,'locked':False,'pose_locked':True,'editable_regions':[{'id':'outside','bounds_mm':[[0,0,0],[10,10,10]]}],'protected_regions':[{'id':'interface','bounds_mm':[[5,5,5],[6,6,6]],'reason':'engineering contact'}]}
  self.map={'schema':'product-design-freedom-v1','units':'mm','coordinate_frame':'comparison_local_mm','baseline_revision':'A','engineering_source':self.put('requirements.json',{'source':'synthetic test only'}),'margin_mm':0,'comparison_policy':{'linear_tolerance_mm':.001,'volume_tolerance_mm3':.01,'angular_tolerance_deg':1e-6,'non_detection_policy':'require_identical_source'},'parts':[self.part]}
  self.change={'id':'shell','status':'PASS','shape_change':'DETECTED','symmetric_difference_mm3':1,'delta_frame':'comparison_local_mm','delta_bounds_mm':[[2,2,2],[3,3,3]],'pose_changed':False}
  self.geometry={'status':'PASS','before_revision':'A','model_files':{'before':{'shell':'before.step'}},'linear_tolerance_mm':.001,'volume_tolerance_mm3':.01,'angular_tolerance_deg':1e-6,'parts':[self.change]}
 def evaluate(self):
  self.geometry['configuration_sha256']=configuration_sha(self.config['before'],self.config['after'],self.config['catalog'],self.config['tolerance_mm']);return evaluate_freedom(self.map,self.geometry,self.root,self.config)
 def test_editable_change_passes(self):self.assertEqual(self.evaluate()['status'],'PASS')
 def test_locked_part_blocks(self):self.part['locked']=True;self.assertEqual(self.evaluate()['status'],'FAIL')
 def test_protected_region_blocks(self):self.change['delta_bounds_mm']=[[4.9,4.9,4.9],[5.1,5.1,5.1]];self.assertEqual(self.evaluate()['status'],'FAIL')
 def test_unpermitted_space_unknown(self):self.change['delta_bounds_mm']=[[11,11,11],[12,12,12]];self.assertEqual(self.evaluate()['status'],'NOT_EVALUATED')
 def test_missing_bounds_unknown(self):self.change.pop('delta_bounds_mm');self.assertEqual(self.evaluate()['status'],'NOT_EVALUATED')
 def test_mismatching_frame_unknown(self):self.change['delta_frame']='world';self.assertEqual(self.evaluate()['status'],'NOT_EVALUATED')
 def test_shift_both_frames_cannot_move_permissions(self):
  self.config['catalog']['parts']['shell']={'before_pose':[20,0,0,0,0,0],'after_pose':[20,0,0,0,0,0]};self.assertEqual(self.evaluate()['status'],'NOT_EVALUATED')
 def test_increased_volume_threshold_not_permitted(self):
  self.config['catalog']['volume_tolerance_mm3']=.5;self.geometry['volume_tolerance_mm3']=.5;self.assertEqual(self.evaluate()['status'],'NOT_EVALUATED')
 def test_increased_linear_threshold_not_permitted(self):
  self.config['tolerance_mm']=1;self.geometry['linear_tolerance_mm']=1;self.assertEqual(self.evaluate()['status'],'NOT_EVALUATED')
 def test_increased_angular_threshold_not_permitted(self):
  self.config['catalog']['angular_tolerance_deg']=1;self.geometry['angular_tolerance_deg']=1;self.assertEqual(self.evaluate()['status'],'NOT_EVALUATED')
 def test_subthreshold_pose_move_still_blocks(self):
  self.config['catalog']['parts']['shell']['after_pose'][0]=.0001;self.assertEqual(self.evaluate()['status'],'FAIL')
 def test_strict_non_detection_requires_same_bytes(self):
  self.change.update(shape_change='NOT_DETECTED',symmetric_difference_mm3=.001);self.assertEqual(self.evaluate()['status'],'NOT_EVALUATED')
 def test_strict_identical_source_passes(self):
  self.put('after.step',(self.root/'before.step').read_text());self.change.update(shape_change='NOT_DETECTED',symmetric_difference_mm3=0);self.assertEqual(self.evaluate()['status'],'PASS')
 def test_approved_threshold_policy_reports_limit(self):
  self.map['comparison_policy']['non_detection_policy']='accept_approved_thresholds';self.change.update(shape_change='NOT_DETECTED',symmetric_difference_mm3=.001);r=self.evaluate();self.assertEqual(r['status'],'PASS');self.assertIn('outside coverage',r['checks'][0]['reason'])
 def test_stale_source_blocks(self):self.put('before.step','changed');self.assertEqual(self.evaluate()['status'],'NOT_EVALUATED')
 def test_duplicate_map_part_rejected(self):self.map['parts'].append(copy.deepcopy(self.part));self.assertEqual(self.evaluate()['status'],'NOT_EVALUATED')
 def test_missing_engineering_authority_unknown(self):self.map.pop('engineering_source');self.assertEqual(self.evaluate()['status'],'NOT_EVALUATED')
 def test_inconsistent_detection_unknown(self):self.change['shape_change']='NOT_DETECTED';self.assertEqual(self.evaluate()['status'],'NOT_EVALUATED')

if __name__=='__main__':unittest.main()
