"""Inspect delivery integrity; publish only an owned manifest, never CAD or acceptance."""
import json, os, tempfile, uuid
from pathlib import Path
from pd_common import local_path,file_sha,artifact,load_json
from engineering_evidence import read,reference,ERRORS

LIMITS=['Consistency does not qualify engineering, aesthetics or physical manufacture.',
        'Dependency completeness is a producer declaration; hashes do not authenticate execution.',
        'Owned manifest writers are serialized; external artifact writers are not in an atomic transaction.']

def _refs(item):
    deps=item.get('dependencies')
    if not isinstance(deps,list) or len(deps)>128:raise ValueError('bounded explicit dependencies required')
    return [item['source'],*deps]

def inspect_delivery(manifest,root):
    findings=[];states={};engineering={'status':'NOT_EVALUATED'};review_coverage={'status':'NOT_EVALUATED','variants':None}
    try:
        if manifest.get('schema')!='product-design-delivery-v1':raise ValueError('unsupported delivery schema')
        if not isinstance(manifest.get('revision'),str) or not manifest['revision']:raise ValueError('revision required')
        items=manifest.get('artifacts')
        if not isinstance(items,list) or not items or len(items)>512:raise ValueError('bounded artifact list required')
        for item in items:
            ident=item['id']
            if not isinstance(ident,str) or not ident or ident in states:raise ValueError('unique artifact ID required')
            for key in ('role','part','variant'):
                if not isinstance(item.get(key),str) or not item[key]:raise ValueError(key+' required')
            state='CURRENT'
            for ref in _refs(item):
                # Reject path violations before treating missing/changed evidence as stale.
                path=local_path(root,ref.get('path'))
                if not isinstance(ref.get('sha256'),str) or len(ref['sha256'])!=64:raise ValueError('explicit digest required')
                if not path.is_file():state='INCOMPLETE';findings.append(ident+': missing '+ref['path'])
                else:
                    try:artifact(root,ref)
                    except ERRORS:
                        if state!='INCOMPLETE':state='STALE'
                        findings.append(ident+': changed '+ref['path'])
            states[ident]=state
        if manifest.get('engineering_ref') is not None:
            try:
                engineering=read(root,manifest['engineering_ref'])
                if not isinstance(engineering,dict) or engineering.get('revision')!=manifest['revision'] or engineering.get('status') not in {'PASS','FAIL','WARNING','NOT_EVALUATED'}:raise ValueError('engineering revision/status mismatch')
            except ERRORS as exc:
                engineering={'status':'NOT_EVALUATED','reason':str(exc)};states['engineering']='STALE'
        for key in ('visual_review_ref','acceptance_ref'):
            if manifest.get(key) is not None:
                try:
                    record=read(root,manifest[key])
                    if not isinstance(record,dict) or record.get('revision')!=manifest['revision']:raise ValueError('record revision mismatch')
                    schema='product-design-visual-review-v1' if key=='visual_review_ref' else 'product-design-acceptance-record-v1'
                    if record.get('schema')!=schema:raise ValueError('unsupported review/decision schema')
                    for binding in ('contract_sha256','candidate_sha256'):
                        digest=manifest.get(binding)
                        if not isinstance(digest,str) or len(digest)!=64 or record.get(binding)!=digest:raise ValueError('review/decision binding mismatch')
                    if key=='visual_review_ref':
                        images=record.get('images')
                        if not isinstance(images,list) or not images or len(images)>128:raise ValueError('review image evidence required')
                        for image in images:artifact(root,image)
                        variants=record.get('variants')
                        if variants is not None:
                            if not isinstance(variants,list) or len(variants)>128 or any(not isinstance(v,str) or not v for v in variants) or len(set(variants))!=len(variants):raise ValueError('explicit unique reviewed variants required')
                            delivered={item['variant'] for item in items}
                            if not set(variants)<=delivered:raise ValueError('reviewed variant absent from delivery')
                            review_coverage={'status':'DECLARED_CURRENT','variants':variants,'count':len(variants)}
                    states[key]='CURRENT'
                except ERRORS as exc:
                    states[key]='STALE';findings.append(key+': '+str(exc))
        consistency='INCOMPLETE' if 'INCOMPLETE' in states.values() else 'STALE' if 'STALE' in states.values() else 'CONSISTENT'
        if consistency!='CONSISTENT':
            engineering={**engineering,'status':'NOT_EVALUATED','reason':'delivery sources are not current'}
            review_coverage={'status':'NOT_EVALUATED','variants':None}
    except ERRORS as exc:consistency='INVALID';findings.append(str(exc));engineering={'status':'NOT_EVALUATED'}
    return {'consistency':consistency,'findings':findings,'artifact_states':states,'engineering':engineering,'review_coverage':review_coverage,'limits':LIMITS}

def _write_new(path,data):
    with path.open('x',encoding='utf-8') as stream:
        json.dump(data,stream,ensure_ascii=False,indent=2,allow_nan=False);stream.write('\n');stream.flush();os.fsync(stream.fileno())

def publish_manifest(manifest,root,expected_previous_sha=None):
    root=Path(root).resolve();folder=local_path(root,'reports/product-design/delivery')
    result=inspect_delivery(manifest,root);attempt={'manifest':manifest,'inspection':result}
    # Own the entire output namespace; an input inside it could be replaced by publication.
    try:
        def protect(value):
            if isinstance(value,dict):
                if 'path' in value and local_path(root,value['path']).is_relative_to(folder):
                    # Previous pointer is checked separately and never treated as input artifact.
                    raise ValueError('source overlaps owned delivery namespace')
                for child in value.values():protect(child)
            elif isinstance(value,list):
                for child in value:protect(child)
        protect({k:v for k,v in manifest.items() if k!='previous_manifest_ref'})
        folder.mkdir(parents=True,exist_ok=True)
        current=local_path(root,'reports/product-design/delivery/current.json')
        lock=local_path(root,'reports/product-design/delivery/.publish.lock')
        fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    except (OSError,ValueError,TypeError) as exc:return {**result,'consistency':'INVALID','findings':result['findings']+[str(exc)]}
    try:
        os.close(fd)
        actual=file_sha(current) if current.exists() else None
        if actual!=expected_previous_sha:raise ValueError('previous manifest changed')
        previous=manifest.get('previous_manifest_ref')
        if actual is None:
            if previous is not None:raise ValueError('unexpected previous reference')
        elif not isinstance(previous,dict) or previous.get('path')!='reports/product-design/delivery/current.json' or previous.get('sha256')!=actual:raise ValueError('previous pointer reference required')
        # Retain immutable previous payload so a mutable current path is not the only history.
        if actual is not None:
            archive=folder/('history-'+actual+'.json')
            if not archive.exists():_write_new(archive,load_json(current))
        result=inspect_delivery(manifest,root)
        attempt={'manifest':manifest,'inspection':result}
        _write_new(folder/('attempt-'+uuid.uuid4().hex+'.json'),attempt)
        if result['consistency']!='CONSISTENT':return result
        with tempfile.NamedTemporaryFile('w',encoding='utf-8',dir=folder,prefix='.next-',delete=False) as stream:
            temp=Path(stream.name);json.dump(manifest,stream,ensure_ascii=False,indent=2,allow_nan=False);stream.write('\n');stream.flush();os.fsync(stream.fileno())
        try:
            result=inspect_delivery(manifest,root)
            if result['consistency']!='CONSISTENT':
                _write_new(folder/('attempt-'+uuid.uuid4().hex+'.json'),{'manifest':manifest,'inspection':result})
                return result
            if (file_sha(current) if current.exists() else None)!=expected_previous_sha:raise ValueError('previous pointer changed during preparation')
            temp.replace(current)
        finally:temp.unlink(missing_ok=True)
        return result
    except ERRORS as exc:
        result={**result,'consistency':'INVALID','findings':result['findings']+[str(exc)]}
        _write_new(folder/('attempt-'+uuid.uuid4().hex+'.json'),{'manifest':manifest,'inspection':result})
        return result
    finally:lock.unlink(missing_ok=True)
