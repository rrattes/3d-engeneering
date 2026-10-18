#!/usr/bin/env python3
"""Check declared engineering constraints and evidence; never certify physical performance."""
import argparse
from pathlib import Path
from pd_common import artifact,canonical_sha,load_json,local_path,number,write_outputs,safe_output

from compare_geometry import configuration_sha

MODES={'cmf_study','visual_review','refinement','redesign'}
SCOPES={'cad','simulation','physical_measurement','declaration'}

def _text(value):
    if not isinstance(value,str) or not value.strip():raise ValueError('nonempty text required')
    return value

def _validate(contract,candidate):
    if contract.get('schema')!='product-design-contract-v1' or candidate.get('schema')!='product-design-candidate-v1':raise ValueError('unsupported schema')
    _text(contract.get('id'));_text(candidate.get('revision'))
    if contract.get('mode') not in MODES or candidate.get('mode')!=contract['mode']:raise ValueError('invalid/mismatching mode')
    if contract.get('target_scope') not in {'cad_prototype','design_proposal','visual_study'}:raise ValueError('unsupported acceptance scope')
    if candidate.get('purpose') not in {'study','solution'}:raise ValueError('candidate purpose required')
    reqs=contract.get('requirements')
    if not isinstance(reqs,list) or len(reqs)>128:raise ValueError('bounded requirement list required')
    seen=set()
    for req in reqs:
        ident=_text(req.get('id'))
        if ident in seen:raise ValueError('duplicate requirement')
        seen.add(ident)
        for key in ['owner','metric','unit']:_text(req.get(key))
        if not isinstance(req.get('conditions'),dict):raise ValueError('conditions object required')
        if req.get('direction') not in {'minimum','maximum','range'} or req.get('preserve') not in {'none','nondecreasing','nonincreasing'}:raise ValueError('comparison rule required')
        limits=req.get('limits',{})
        for bound in ('min','max'):
            if bound in limits:number(limits[bound])
        if req['direction'] in {'minimum','range'} and 'min' not in limits:raise ValueError('minimum required')
        if req['direction'] in {'maximum','range'} and 'max' not in limits:raise ValueError('maximum required')
        if req['direction']=='range' and limits['min']>limits['max']:raise ValueError('reversed interval')
        scopes=req.get('evidence_scopes')
        if not isinstance(scopes,list) or not scopes or not set(scopes)<=SCOPES:raise ValueError('explicit evidence scopes required')
        if not isinstance(req.get('uncertainty_required'),bool):raise ValueError('uncertainty policy required')

def _record(record,req,revision):
    if not isinstance(record,dict):raise ValueError('metric record missing')
    if record.get('status')!='PASS':raise ValueError('metric not verified in its declared scope')
    for key in ['metric','unit','conditions']:
        if record.get(key)!=req[key]:raise ValueError(key+' mismatch')
    if record.get('revision')!=revision:raise ValueError('metric revision mismatch')
    if record.get('scope') not in req['evidence_scopes']:raise ValueError('scope not accepted for this requirement')
    _text(record.get('method'))
    value=number(record.get('value'))
    if req['uncertainty_required'] and 'uncertainty' not in record:raise ValueError('uncertainty missing')
    uncertainty=number(record.get('uncertainty',0))
    if uncertainty<0:raise ValueError('negative uncertainty')
    return value-uncertainty,value+uncertainty

def _minimum(low,high,bound):
    return 'PASS' if low>=bound else 'FAIL' if high<bound else 'NOT_EVALUATED'

def _maximum(low,high,bound):
    return 'PASS' if high<=bound else 'FAIL' if low>bound else 'NOT_EVALUATED'

def evaluate_design(contract,candidate,project_root):
    _validate(contract,candidate);root=Path(project_root).resolve();checks=[]
    def add(ident,status,reason,**data):checks.append({'id':ident,'status':status,'reason':reason,**data})
    try:
        if candidate.get('contract_sha256')!=canonical_sha(contract):raise ValueError('candidate contract digest mismatch')
        auth=contract.get('authorization')
        if contract['requirements'] or auth is not None:
            approval=artifact(root,auth,True)
            policy={k:v for k,v in contract.items() if k!='authorization'}
            if approval.get('decision')!='APPROVED' or approval.get('authority')!='engineering' or approval.get('policy_sha256')!=canonical_sha(policy):raise ValueError('engineering policy changed or unapproved')
        add('policy','PASS','policy integrity checked; authority is a local declaration, not authenticated')
    except (ValueError,OSError,KeyError,TypeError,IndexError) as exc:add('policy','NOT_EVALUATED',str(exc))
    baseline=None
    if contract['requirements']:
        try:
            ref=contract.get('baseline');baseline=artifact(root,ref,True)
            if candidate.get('baseline_sha256')!=ref['sha256']:raise ValueError('candidate baseline mismatch')
            _text(baseline.get('revision'))
            if baseline.get('validation',{}).get('status')!='PASS':raise ValueError('baseline not validated in declared scope')
            add('baseline','PASS','baseline statement integrity checked',declared_scope=baseline['validation'].get('scope'))
        except (ValueError,OSError,KeyError,TypeError,IndexError) as exc:add('baseline','NOT_EVALUATED',str(exc));baseline=None
    for req in contract['requirements']:
        try:
            artifact(root,req.get('source'))
            if baseline is None:raise ValueError('baseline unavailable')
            if baseline['validation'].get('scope') not in req['evidence_scopes']:raise ValueError('baseline validation scope incompatible')
            before=_record(baseline['metrics'][req['id']],req,baseline['revision'])
            after=_record(artifact(root,candidate.get('metrics',{}).get(req['id']),True),req,candidate['revision'])
            results=[];limits=req['limits']
            baseline_results=[]
            if req['direction'] in {'minimum','range'}:baseline_results.append(_minimum(*before,number(limits['min'])))
            if req['direction'] in {'maximum','range'}:baseline_results.append(_maximum(*before,number(limits['max'])))
            baseline_status='FAIL' if 'FAIL' in baseline_results else 'NOT_EVALUATED' if 'NOT_EVALUATED' in baseline_results else 'PASS'
            add('baseline:'+req['id'],baseline_status,'baseline absolute bounds checked separately',interval=before,unit=req['unit'])
            if baseline_status!='PASS':raise ValueError('baseline numbers do not demonstrate declared validation against current limits')
            if req['direction'] in {'minimum','range'}:results.append(_minimum(*after,number(limits['min'])))
            if req['direction'] in {'maximum','range'}:results.append(_maximum(*after,number(limits['max'])))
            if req['preserve']=='nondecreasing':results.append(_minimum(*after,before[1]))
            elif req['preserve']=='nonincreasing':results.append(_maximum(*after,before[0]))
            status='FAIL' if 'FAIL' in results else 'NOT_EVALUATED' if 'NOT_EVALUATED' in results else 'PASS'
            add(req['id'],status,'conservative interval comparison; unrelated metrics do not compensate',before_interval=before,after_interval=after,unit=req['unit'])
        except (ValueError,OSError,KeyError,TypeError,IndexError) as exc:add(req['id'],'NOT_EVALUATED',str(exc))
    if contract.get('design_freedom') is not None and contract['mode'] not in {'redesign','refinement'}:
        add('design_freedom_scope','NOT_EVALUATED','spatial map requires a geometric mode with full comparison provenance')
    if contract['mode'] in {'redesign','refinement'}:
        try:
            geometry=artifact(root,candidate.get('geometry'),True)
            if geometry.get('schema')!='product-design-geometry-v1' or geometry.get('status')!='PASS' or geometry.get('units')!='mm':raise ValueError('compatible CAD comparison required')
            if baseline is None or geometry.get('before_revision')!=baseline['revision'] or geometry.get('after_revision')!=candidate['revision']:raise ValueError('geometry revision provenance mismatch')
            config=artifact(root,candidate.get('geometry_config'),True)
            expected_config=configuration_sha(config['before'],config['after'],config['catalog'],config['tolerance_mm'])
            if geometry.get('configuration_sha256')!=expected_config:raise ValueError('geometry configuration changed; recompute comparison')
            refs=geometry.get('source_artifacts')
            if not isinstance(refs,list) or not refs:raise ValueError('CAD source provenance missing')
            for ref in refs:artifact(root,ref)
            parts=geometry.get('parts',[])
            if not parts or any(p.get('status')!='PASS' for p in parts):raise ValueError('partial geometry comparison')
            changed=[]
            for part in parts:
                if part.get('shape_change')=='DETECTED':
                    if number(part['symmetric_difference_mm3'])<=number(geometry['volume_tolerance_mm3']):raise ValueError('inconsistent geometry evidence')
                    changed.append(part['id'])
            if not changed:raise ValueError('no shape change demonstrated; color or pose alone is insufficient')
            add('geometry','PASS','fresh CAD comparison report; evaluator does not recompute BREP',changed_parts=changed)
        except (ValueError,OSError,KeyError,TypeError,IndexError) as exc:add('geometry','NOT_EVALUATED',str(exc))
    if contract.get('design_freedom') is not None:
        try:
            from design_freedom import evaluate_freedom
            mapping=artifact(root,contract['design_freedom'],True)
            comparison=artifact(root,candidate.get('geometry'),True)
            comparison_config=artifact(root,candidate.get('geometry_config'),True)
            permission=evaluate_freedom(mapping,comparison,root,comparison_config)
            add('design_freedom',permission['status'],'engineering-owned spatial permissions',details=permission)
        except (ValueError,OSError,KeyError,TypeError,IndexError) as exc:add('design_freedom','NOT_EVALUATED',str(exc))
    blocked=any(c['status']!='PASS' for c in checks)
    eligibility='BLOCKED' if blocked else 'EXPLORATORY' if candidate['purpose']=='study' or not contract['requirements'] else 'ELIGIBLE'
    return {'schema':'product-design-evaluation-v1','eligibility':eligibility,'target_scope':contract['target_scope'],
            'mode':contract['mode'],'candidate_revision':candidate['revision'],'contract_sha256':canonical_sha(contract),
            'candidate_sha256':canonical_sha(candidate),'checks':checks,'visual_review':'NOT_EVALUATED',
            'user_acceptance':'PENDING','physical_validation':'NOT_EVALUATED',
            'limits':['Local declarations and hashes are not authentication or independent physical verification.',
                      'Engineering eligibility is scoped to the supplied requirements and evidence; visual/user acceptance is separate.',
                      'This tool does not intercept external CAD publishers.']}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--project',type=Path,required=True)
    parser.add_argument('--contract',required=True);parser.add_argument('--candidate',required=True);parser.add_argument('--output',required=True)
    args=parser.parse_args()
    try:
        contract=load_json(local_path(args.project,args.contract));candidate=load_json(local_path(args.project,args.candidate))
        result=evaluate_design(contract,candidate,args.project)
        lines=['# Avaliação da proposta de design','',f'Estado: **{result["eligibility"]}**. Escopo: `{result["target_scope"]}`.','']
        lines.extend(f'- {c["id"]}: {c["status"]} — {c["reason"]}' for c in result['checks'])
        lines+=['','Revisão visual, aceitação do usuário e validação física não são inferidas por este comando.','']
        write_outputs(safe_output(args.project,args.output,'engineering-gate',[contract,candidate,{'path':args.contract},{'path':args.candidate}]),'engineering-gate',result,'\n'.join(lines));print(result['eligibility'])
        return 3 if result['eligibility']=='BLOCKED' else 0
    except (ValueError,OSError,KeyError,TypeError,IndexError) as exc:
        print('INVALID_INPUT: '+str(exc));return 2
if __name__=='__main__':raise SystemExit(main())
