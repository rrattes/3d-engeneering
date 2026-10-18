"""Optional BREP regions, using the installed CAD kernel; v1 remains separate."""
from pd_common import artifact,local_path,number
from compare_geometry import configuration_sha,region_metrics,compare_parts,solid_fragments


def evaluate_brep(mapping,geometry,root,config):
    checks=[]
    try:
        from build123d import import_step,Pos,Rot
        import sys,itertools
        if '/opt/cad3d' not in sys.path:sys.path.insert(0,'/opt/cad3d')
        from brep_pairs import common_volume
        if mapping.get('mode')!='brep_regions' or mapping.get('units')!='mm' or mapping.get('coordinate_frame')!='comparison_local_mm':raise ValueError('explicit BREP mode/mm/frame required')
        if number(mapping['margin_mm'])<0 or mapping.get('margins_embedded') is not True:raise ValueError('engineering margins must already be built into region volumes')
        artifact(root,mapping['engineering_source'])
        if geometry.get('status')!='PASS' or mapping.get('baseline_revision')!=geometry.get('before_revision'):raise ValueError('baseline/comparison mismatch')
        if geometry.get('configuration_sha256')!=configuration_sha(config['before'],config['after'],config['catalog'],config['tolerance_mm']):raise ValueError('stale comparison configuration')
        policy=mapping['comparison_policy']
        expected={'linear_tolerance_mm':number(config['tolerance_mm']),'volume_tolerance_mm3':number(config['catalog']['volume_tolerance_mm3']),'angular_tolerance_deg':number(config['catalog'].get('angular_tolerance_deg',1e-6))}
        if any(number(policy[k])!=v or v<=0 or geometry.get(k)!=v for k,v in expected.items()):raise ValueError('thresholds differ from engineering authority')
        tol=expected['volume_tolerance_mm3']
        for ref in geometry['source_artifacts']:artifact(root,ref)
        parts=mapping['parts']
        if not isinstance(parts,list) or not parts or len(parts)>32:raise ValueError('bounded map parts required')
        ids=[p['id'] for p in parts]
        if len(set(ids))!=len(ids) or set(ids)!=set(config['before']) or set(ids)!=set(config['after']):raise ValueError('v2 requires explicit same-part correspondence; additions/removals need an engineering remap')
        fresh=compare_parts(config['before'],config['after'],dict(config['catalog'],project_root=str(root)),config['tolerance_mm'])
        if fresh['status']!='PASS':raise ValueError('live BREP comparison inconclusive')
        if fresh['parts']!=geometry['parts'] or fresh['source_artifacts']!=geometry['source_artifacts']:raise ValueError('reported comparison differs from live geometry')
        refs=[];total_solids=0
        def pose(frame):
            if not isinstance(frame,list) or len(frame)!=6:raise ValueError('six-number pose required')
            frame=[number(x) for x in frame]
            return Pos(*frame[:3])*Rot(*frame[3:])
        def read(ref,frame):
            nonlocal total_solids
            artifact(root,ref);refs.append(ref)
            shape=pose(frame).inverse()*import_step(str(local_path(root,ref['path'])))
            solids=solid_fragments(shape,32);total_solids+=len(solids)
            if not shape.is_valid or not 0<len(solids)<=32 or total_solids>256 or any(not s.is_valid or number(s.volume)<=0 for s in solids):raise ValueError('invalid/empty/oversized region solid group')
            if any(common_volume(a,b)>tol for a,b in itertools.combinations(solids,2)):raise ValueError('overlapping solids in one STEP')
            return solids
        from pd_common import file_sha
        for part in parts:
            ident=part['id'];frames=config['catalog']['parts'][ident]
            if any(not isinstance(part.get(k),bool) for k in ('locked','pose_locked')):raise ValueError('explicit locks required')
            if part['source']['path']!=config['before'][ident]:raise ValueError('baseline source mismatch')
            if part['before_pose']!=frames['before_pose'] or part['after_pose']!=frames['after_pose']:raise ValueError('engineering frame mismatch')
            if part['pose_locked'] and part['before_pose']!=part['after_pose']:
                checks.append({'id':ident,'status':'FAIL','reason':'protected pose changed'});continue
            before=read(part['source'],part['before_pose'])
            after_ref={'path':config['after'][ident],'sha256':file_sha(local_path(root,config['after'][ident]))}
            after=read(after_ref,part['after_pose'])
            regions={}
            for kind in ('protected_material','protected_void','editable_volumes'):
                values=part[kind]
                if not isinstance(values,list) or len(values)>32:raise ValueError('bounded explicit region lists required')
                if len({v['id'] for v in values})!=len(values):raise ValueError('duplicate region ID')
                regions[kind]=[s for v in values for s in read(v['source'],v['pose'])]
                # Protected material volume sums must be disjoint; editable/void union may overlap.
                if kind=='protected_material' and any(common_volume(a,b)>tol for a,b in itertools.combinations(regions[kind],2)):raise ValueError('overlapping protected material regions')
            metrics=region_metrics(before,after,**regions,volume_tolerance=tol)
            if metrics['baseline_protected_material_missing_mm3']>tol or metrics['baseline_void_occupied_mm3']>tol:raise ValueError('region policy incompatible with baseline')
            changed=metrics['added_mm3']+metrics['removed_mm3']
            bad=any(metrics[k]>tol for k in ('protected_material_missing_mm3','protected_void_occupied_mm3','outside_editable_mm3')) or (part['locked'] and changed>tol)
            checks.append({'id':ident,'status':'FAIL' if bad else 'PASS','reason':'exact material retention, void occupancy and editable union checked','metrics':metrics})
        for ref in refs:artifact(root,ref)
    except (ImportError,ValueError,OSError,KeyError,TypeError,IndexError,AttributeError,RuntimeError) as exc:checks.append({'id':'map','status':'NOT_EVALUATED','reason':str(exc)})
    status='FAIL' if any(c['status']=='FAIL' for c in checks) else 'NOT_EVALUATED' if not checks or any(c['status']!='PASS' for c in checks) else 'PASS'
    return {'status':status,'checks':checks,'limits':['Exact kernel Booleans within declared numerical thresholds, not physical certification.',
            'Protected void/allowed volumes must include engineering-owned physical margins; numerical tolerance is not clearance.',
            'Explicit same-part mapping only; no fallback to AABB or weaker policy.']}
