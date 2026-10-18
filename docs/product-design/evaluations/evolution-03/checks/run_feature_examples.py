"""Exercise feature CLI exports in an isolated reports tree; no product files changed."""
import json,subprocess,sys
import helpers as h
ROOT=h.ROOT
recipes=json.loads((h.CANDIDATE/'assets/feature_recipes.json').read_text())['recipes']
folder=ROOT/'reports/product-design-evolution-02/features';folder.mkdir(parents=True,exist_ok=True)
records=[]
for style,spec in recipes.items():
 source=folder/(style+'.json');source.write_text(json.dumps(spec,indent=2)+'\n')
 run=subprocess.run([sys.executable,'-B',str(h.CANDIDATE/'scripts/style_geometry.py'),'--project',str(ROOT),'--spec',str(source.relative_to(ROOT)),'--output',str((folder/style).relative_to(ROOT))],capture_output=True,text=True)
 if run.returncode:raise RuntimeError(style+': '+run.stdout+run.stderr)
 result=json.loads((folder/style/'style-feature.json').read_text());records.append(dict(style=style,**result));print(style+': '+result['status'],flush=True)
(folder/'catalog.json').write_text(json.dumps(records,indent=2)+'\n')
