#!/usr/bin/env python3
"""Compact part-level report from a live engineering gate, never a cached acceptance."""
import argparse
from pathlib import Path
from evaluate_design import evaluate_design
from pd_common import artifact,canonical_sha,load_json,local_path,safe_output,write_outputs


def summarize(contract,candidate,changes,root):
    gate=evaluate_design(contract,candidate,root)
    if not isinstance(changes,dict):raise ValueError('change report object required')
    if changes.get('schema')!='product-design-changes-v1' or changes.get('revision')!=candidate['revision']:
        raise ValueError('changes must identify the current candidate revision')
    items=changes.get('changes')
    if not isinstance(items,list) or len(items)>128:raise ValueError('bounded change list required')
    if any(not isinstance(item,dict) for item in items):raise ValueError('change item objects required')
    indexed={item['part']:item for item in items}
    if len(indexed)!=len(items):raise ValueError('one change summary per part')
    geometry=None;notes=[]
    if candidate.get('geometry'):
        try:geometry=artifact(root,candidate['geometry'],True)
        except (ValueError,OSError,KeyError,TypeError) as exc:notes.append('Geometry unavailable: '+str(exc))
    geometry_current=any(c['id']=='geometry' and c['status']=='PASS' for c in gate['checks'])
    if geometry is not None and not geometry_current:notes.append('Part comparison is not currently verified by the live geometry gate; values are reference data only.')
    actual=geometry.get('parts',[]) if geometry else []
    rows=[]
    for part in actual:
        item=indexed.pop(part['id'],{})
        rows.append({'part':part['id'],'change_type':part.get('change_type','UNKNOWN'),'shape_change':part.get('shape_change'),
                     'volume_before_mm3':part.get('before_volume_mm3'),'volume_after_mm3':part.get('after_volume_mm3'),
                     'symmetric_difference_mm3':part.get('symmetric_difference_mm3'),'delta_bounds_mm':part.get('delta_bounds_mm'),
                     'intent':item.get('intent','NOT_DOCUMENTED'),'feature':item.get('feature','NOT_DOCUMENTED'),
                     'affected_requirements':item.get('affected_requirements',[]),'evidence_status':part.get('status','NOT_EVALUATED') if geometry_current else 'NOT_EVALUATED'})
    for ident,item in indexed.items():rows.append({'part':ident,'intent':item.get('intent'),'feature':item.get('feature'),'evidence_status':'NOT_EVALUATED','reason':'no corresponding current CAD part comparison'})
    return {'schema':'product-design-summary-v1','revision':candidate['revision'],'contract_sha256':canonical_sha(contract),
            'candidate_sha256':canonical_sha(candidate),'engineering':gate,'parts':rows,'notes':notes,
            'visual_review':'NOT_EVALUATED','user_acceptance':'PENDING','physical_validation':'NOT_EVALUATED',
            'limits':['Engineering state is live, but narrative intent and impact lists are caller declarations.',
                      'Part values inherit the geometry report provenance and limits; no beauty or physical-quality score.']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--project',type=Path,required=True)
    for name in ('contract','candidate','changes','output'):p.add_argument('--'+name,required=True)
    a=p.parse_args()
    try:
        contract=load_json(local_path(a.project,a.contract));candidate=load_json(local_path(a.project,a.candidate));changes=load_json(local_path(a.project,a.changes))
        result=summarize(contract,candidate,changes,a.project)
        lines=['# Alterações de design','',f'Revisão: {result["revision"]}; engenharia: **{result["engineering"]["eligibility"]}**.','',
               '| Peça | Intenção | Evidência CAD |','|---|---|---|']
        for row in result['parts']:
            intent=str(row.get('intent','')).replace('|','/').replace('\n',' ');lines.append('| '+str(row['part'])+' | '+intent+' | '+str(row['evidence_status'])+' |')
        lines+=['','## Pendências técnicas','']+[c['id']+': '+c['status']+' — '+c['reason'] for c in result['engineering']['checks'] if c['status']!='PASS']
        lines+=['','Revisão visual, decisão do usuário e físico permanecem separados.','']
        directory=safe_output(a.project,a.output,'design-summary',[contract,candidate,{'path':a.contract},{'path':a.candidate},{'path':a.changes}])
        write_outputs(directory,'design-summary',result,'\n'.join(lines));print(result['engineering']['eligibility']);return 3 if result['engineering']['eligibility']=='BLOCKED' else 0
    except (ValueError,OSError,KeyError,TypeError,IndexError) as exc:print('INVALID_INPUT: '+str(exc));return 2
if __name__=='__main__':raise SystemExit(main())
