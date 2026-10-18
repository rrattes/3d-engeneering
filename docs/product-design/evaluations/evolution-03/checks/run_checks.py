"""Explicit groups; assert tested imports come from the selected candidate."""
import argparse, importlib, sys, unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE),str(HERE/'legacy')]
import helpers
GROUPS={'legacy':['test_engineering_gate','test_geometry','test_integrity','test_selection','test_cli','test_review_regressions'],
'host':['test_host','test_new_cli','test_engineering_evidence','test_delivery_manifest','test_summary_parity','test_style_extensions'],
'cad':['test_cad','test_render','test_volume_permissions'],'integration':['test_integration']}
p=argparse.ArgumentParser();p.add_argument('--group',choices=[*GROUPS,'all'],default='all');p.add_argument('--historical',action='store_true');a=p.parse_args()
names=sum(GROUPS.values(),[]) if a.group=='all' else GROUPS[a.group]
if a.historical:names=[n for n in names if n not in {'test_engineering_evidence','test_delivery_manifest','test_summary_parity','test_style_extensions','test_volume_permissions'}]
suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromName(n) for n in names)
for name,module in list(sys.modules.items()):
 if name in {'evaluate_design','compare_geometry','design_freedom','pd_common','style_brief','impact_plan','design_summary','render_comparison','style_geometry','select_candidate','engineering_evidence','delivery_manifest'}:
  assert Path(module.__file__).resolve().is_relative_to(helpers.CANDIDATE), (name,module.__file__)
print('CANDIDATE:',helpers.CANDIDATE,flush=True)
r=unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(0 if r.wasSuccessful() else 1)
