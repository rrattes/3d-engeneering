"""Read pinned engineering evidence. No solver, inferred criteria or physical certification."""
from pd_common import artifact, number

ERRORS=(ValueError,OSError,KeyError,TypeError,IndexError,AttributeError)
FIELDS=('id','part','requirement_id','method','unit','expected_limit','coverage','calibration')
LIMITS=['Hashes bind local declarations, not their authenticity.',
        'Coverage is limited to the declared method, samples and calibration; no physical certification.']

def reference(ref):
    if not isinstance(ref,dict):raise ValueError('reference object required')
    result=dict(ref)
    if 'json_pointer' in result:
        pointer=result.pop('json_pointer')
        if 'pointer' in result and result['pointer']!=pointer:raise ValueError('conflicting JSON pointers')
        result['pointer']=pointer
    return result

def read(root,ref):return artifact(root,reference(ref),True)

def bounded(items):
    if not isinstance(items,list) or not items or len(items)>128:raise ValueError('nonempty bounded list required')
    return items

def validate_criterion(check):
    for key in FIELDS:
        if key not in check:raise ValueError('missing criterion '+key)
    for key in ('id','part','requirement_id','method','unit','calibration'):
        if not isinstance(check[key],str) or not check[key].strip():raise ValueError('nonempty '+key+' required')
    if not isinstance(check['coverage'],dict) or not check['coverage']:raise ValueError('explicit coverage required')
    limits=check['expected_limit']
    if not isinstance(limits,dict) or not limits or not set(limits)<={'min','max'}:raise ValueError('explicit min/max criterion required')
    for value in limits.values():number(value)
    if 'min' in limits and 'max' in limits and limits['min']>limits['max']:raise ValueError('reversed limits')
    if 'orientation' in check:
        ori=check['orientation']
        if not isinstance(ori,dict) or not isinstance(ori.get('datum'),str) or not ori['datum'].strip():raise ValueError('orientation requires a named engineering datum, not centroid')
        pose=ori.get('pose')
        if not isinstance(pose,list) or len(pose)!=6:raise ValueError('orientation requires XYZ/rotation transform')
        for x in pose:number(x)
        if ori.get('support') not in {'nominal','supports_required','measured'}:raise ValueError('explicit support scope required')

def read_policy(root,ref):
    policy=read(root,ref)
    if policy.get('schema')!='product-design-evidence-policy-v1':raise ValueError('unsupported policy')
    if not isinstance(policy.get('revision'),str) or not policy['revision']:raise ValueError('policy revision missing')
    for src in bounded(policy.get('source_refs')):artifact(root,src)
    artifact(root,policy.get('parameter_ref'))
    checks=bounded(policy.get('checks'));ids=set()
    for check in checks:
        validate_criterion(check)
        if check['id'] in ids:raise ValueError('duplicate criterion')
        ids.add(check['id'])
    return policy

def adapt_cad3d_report(report_ref,policy_ref,root):
    """Only the explicitly versioned interchange report is supported.

    Raw CAD3D command returns/thickness dictionaries lack provenance. Their producer
    must emit this envelope with actual method/coverage; this adapter never fills it.
    """
    try:
        policy=read_policy(root,policy_ref);ref=reference(report_ref);report=read(root,ref)
        if report.get('schema')!='cad3d-product-design-report-v1':raise ValueError('unsupported provider format; explicit interchange envelope required')
        if report.get('revision')!=policy['revision']:raise ValueError('report revision mismatch')
        for key in ('source_refs','parameter_ref'):
            if report.get(key)!=policy[key]:raise ValueError(key+' mismatch')
        checks=[]
        for i,check in enumerate(bounded(report.get('checks'))):
            validate_criterion(check)
            checks.append({**check,'criterion_ref':{'policy_id':check['id']},'artifact_ref':{**ref,'pointer':ref.get('pointer','')+'/checks/'+str(i)}})
        evidence={'schema':'product-design-engineering-evidence-v1','revision':report['revision'],
                  'policy_ref':reference(policy_ref),'report_ref':ref,'source_refs':report['source_refs'],'parameter_ref':report['parameter_ref'],'checks':checks}
        result=validate_engineering_evidence({'engineering_evidence':policy_ref},{'revision':report['revision'],'engineering_evidence_inline':evidence},root,_adapter=True)
        return {**evidence,'status':result['status'],'limits':LIMITS}
    except ERRORS as exc:return {'status':'NOT_EVALUATED','checks':[],'reason':str(exc),'limits':LIMITS}

def validate_engineering_evidence(contract,candidate,root,*,_adapter=False):
    checks=[]
    try:
        pref=contract.get('engineering_evidence');policy=read_policy(root,pref)
        ev=candidate.get('engineering_evidence_inline') if _adapter else read(root,candidate.get('engineering_evidence'))
        if ev.get('schema')!='product-design-engineering-evidence-v1':raise ValueError('unsupported evidence')
        if ev.get('revision')!=candidate.get('revision') or ev['revision']!=policy['revision']:raise ValueError('evidence/policy/candidate revision mismatch')
        if reference(ev.get('policy_ref'))!=reference(pref):raise ValueError('policy reference mismatch')
        for key in ('source_refs','parameter_ref'):
            if ev.get(key)!=policy[key]:raise ValueError(key+' differs from authority')
        report_ref=reference(ev.get('report_ref'));provider=read(root,report_ref)
        if provider.get('schema')!='cad3d-product-design-report-v1':raise ValueError('unsupported live provider envelope')
        for key in ('revision','source_refs','parameter_ref'):
            if provider.get(key)!=policy[key]:raise ValueError('live provider provenance mismatch: '+key)
        records=bounded(provider.get('checks'))
        provider_refs={record['id']:{**report_ref,'pointer':report_ref.get('pointer','')+'/checks/'+str(i)} for i,record in enumerate(records)}
        if len(provider_refs)!=len(records):raise ValueError('duplicate provider checks')
        items=bounded(ev.get('checks'));indexed={c['id']:c for c in items}
        if len(indexed)!=len(items) or set(indexed)!={c['id'] for c in policy['checks']}:raise ValueError('missing, duplicate or uncontracted checks')
        for criterion in policy['checks']:
            ident=criterion['id'];c=indexed[ident]
            try:
                validate_criterion(c)
                if reference(c.get('artifact_ref'))!=provider_refs.get(ident):raise ValueError('record is not from the pinned provider envelope')
                record=read(root,c.get('artifact_ref'))
                if c.get('criterion_ref')!={'policy_id':ident}:raise ValueError('criterion reference mismatch')
                for key in (*FIELDS,'orientation'):
                    if c.get(key)!=criterion.get(key) or record.get(key)!=criterion.get(key):raise ValueError('criterion/provider mismatch: '+key)
                if record.get('revision')!=candidate['revision'] or c.get('revision')!=candidate['revision']:raise ValueError('record revision mismatch')
                if c.get('status')!='PASS' or record.get('status')!='PASS':raise ValueError('provider status is not PASS')
                for key in ('observed_value','observed_interval'):
                    if record.get(key)!=c.get(key):raise ValueError('observation differs from source')
                if 'observed_interval' in c:
                    interval=c['observed_interval']
                    if not isinstance(interval,list) or len(interval)!=2:raise ValueError('two bounds required')
                    low,high=map(number,interval)
                else:low=high=number(c.get('observed_value'))
                if low>high:raise ValueError('reversed observed interval')
                limits=criterion['expected_limit'];status='PASS'
                if ('min' in limits and low<limits['min']) or ('max' in limits and high>limits['max']):status='FAIL'
                checks.append({**c,'status':status,'reason':'current criterion and recorded interval checked'})
            except ERRORS as exc:checks.append({**c,'status':'NOT_EVALUATED','reason':str(exc)})
    except ERRORS as exc:checks.append({'id':'evidence','status':'NOT_EVALUATED','reason':str(exc)})
    status='FAIL' if any(c['status']=='FAIL' for c in checks) else 'NOT_EVALUATED' if any(c['status']!='PASS' for c in checks) else 'PASS'
    return {'status':status,'checks':checks,'limits':LIMITS}
