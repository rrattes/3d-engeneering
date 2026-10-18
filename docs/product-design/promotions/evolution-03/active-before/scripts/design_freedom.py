"""Conservative engineering-owned spatial permissions; AABBs are not surface certification."""
from pd_common import artifact,number


def bounds(value):
    if not isinstance(value,list) or len(value)!=2 or any(not isinstance(v,list) or len(v)!=3 for v in value):
        raise ValueError('bounds must be two XYZ triples')
    low,high=([number(x) for x in v] for v in value)
    if any(a>=b for a,b in zip(low,high)):raise ValueError('bounds require positive extents')
    return low,high


def contained(inner,outer,margin):
    return all(a>=c+margin and b<=d-margin for a,b,c,d in zip(inner[0],inner[1],outer[0],outer[1]))


def intersects(first,second,margin):
    return all(a<=d+margin and b>=c-margin for a,b,c,d in zip(first[0],first[1],second[0],second[1]))


def evaluate_freedom(mapping,geometry,root,config):
    checks=[]
    def add(ident,status,reason):checks.append({'id':ident,'status':status,'reason':reason})
    try:
        if not all(isinstance(v,dict) for v in (mapping,geometry,config)):raise ValueError('map, geometry and config objects required')
        if mapping.get('schema')!='product-design-freedom-v1' or mapping.get('units')!='mm' or mapping.get('coordinate_frame')!='comparison_local_mm':
            raise ValueError('explicit map schema, mm units and comparison-local frame required')
        if geometry.get('status')!='PASS' or mapping.get('baseline_revision')!=geometry.get('before_revision'):
            raise ValueError('map baseline/comparison mismatch')
        artifact(root,mapping.get('engineering_source'))
        from compare_geometry import configuration_sha
        if geometry.get('configuration_sha256')!=configuration_sha(config['before'],config['after'],config['catalog'],config['tolerance_mm']):
            raise ValueError('map requires the current comparison configuration')
        policy=mapping.get('comparison_policy',{})
        if not isinstance(policy,dict):raise ValueError('comparison policy object required')
        expected={'linear_tolerance_mm':number(policy['linear_tolerance_mm']),
                  'volume_tolerance_mm3':number(policy['volume_tolerance_mm3']),
                  'angular_tolerance_deg':number(policy['angular_tolerance_deg'])}
        actual={'linear_tolerance_mm':number(config['tolerance_mm']),
                'volume_tolerance_mm3':number(config['catalog']['volume_tolerance_mm3']),
                'angular_tolerance_deg':number(config['catalog'].get('angular_tolerance_deg',1e-6))}
        if any(value<=0 for value in expected.values()) or expected!=actual or any(geometry.get(k)!=v for k,v in expected.items()):
            raise ValueError('comparison thresholds differ from engineering-owned policy')
        non_detection=policy.get('non_detection_policy')
        if non_detection not in {'require_identical_source','accept_approved_thresholds'}:raise ValueError('explicit non-detection policy required')
        margin=number(mapping.get('margin_mm'))
        if margin<0:raise ValueError('negative permission margin')
        parts=mapping.get('parts')
        if not isinstance(parts,list) or not parts or len(parts)>128:raise ValueError('bounded part list required')
        if any(not isinstance(part,dict) for part in parts):raise ValueError('part objects required')
        indexed={part['id']:part for part in parts}
        if len(indexed)!=len(parts):raise ValueError('duplicate map part')
        # Check every declaration, including unchanged parts, for stale sources/invalid regions.
        for ident,part in indexed.items():
            if not isinstance(part.get('locked'),bool) or not isinstance(part.get('pose_locked'),bool):raise ValueError('explicit locks required')
            artifact(root,part.get('source'))
            if geometry.get('model_files',{}).get('before',{}).get(ident)!=part['source']['path']:
                raise ValueError('map part source does not match compared before model')
            frame=part.get('before_pose')
            if not isinstance(frame,list) or len(frame)!=6:raise ValueError('engineering-owned before_pose required')
            frame=[number(x) for x in frame]
            declared=config['catalog']['parts'][ident]['before_pose']
            if frame!=declared:raise ValueError('comparison reference frame differs from approved map')
            for key in ('editable_regions','protected_regions'):
                regions=part.get(key)
                if not isinstance(regions,list) or len(regions)>128:raise ValueError('explicit bounded regions required')
                region_ids=set()
                for region in regions:
                    if not isinstance(region,dict):raise ValueError('region object required')
                    if not isinstance(region.get('id'),str) or not region['id'] or region['id'] in region_ids:raise ValueError('unique region IDs required')
                    region_ids.add(region['id']);bounds(region.get('bounds_mm'))
                    if key=='protected_regions' and not region.get('reason'):raise ValueError('protected region needs engineering reason')
        for change in geometry.get('parts',[]):
            if not isinstance(change,dict):raise ValueError('change object required')
            if change.get('status')!='PASS':raise ValueError('incomplete geometric evidence')
            difference=number(change.get('symmetric_difference_mm3'))
            if difference<0 or change.get('shape_change')!=('DETECTED' if difference>expected['volume_tolerance_mm3'] else 'NOT_DETECTED'):
                raise ValueError('shape detection is inconsistent with the approved volume threshold')
            ident=change['id'];part=indexed.get(ident)
            if part is None:add(ident,'NOT_EVALUATED','changed part not authorized by map');continue
            frames=config['catalog']['parts'][ident]
            after_frame=frames.get('after_pose') if ident in config['after'] else None
            if after_frame is not None:
                if not isinstance(after_frame,list) or len(after_frame)!=6:raise ValueError('explicit after frame required')
                after_frame=[number(x) for x in after_frame]
            raw_pose_change=after_frame is not None and after_frame!=part['before_pose']
            if raw_pose_change and part['pose_locked']:
                add(ident,'FAIL','protected pose changed');continue
            if change.get('shape_change')!='DETECTED':
                if non_detection=='require_identical_source':
                    after_path=config['after'].get(ident)
                    from pd_common import local_path,file_sha
                    if after_path is None or file_sha(local_path(root,after_path))!=part['source']['sha256']:
                        add(ident,'NOT_EVALUATED','non-detection does not prove identical material; strict source policy requires identical STEP bytes');continue
                    add(ident,'PASS','identical source bytes; pose checked separately')
                else:
                    add(ident,'PASS','no detected change above explicitly engineering-approved thresholds; smaller changes remain outside coverage')
                continue
            if part['locked']:
                add(ident,'FAIL','engineering-locked part reshaped');continue
            if change.get('delta_frame')!='comparison_local_mm':raise ValueError('delta coordinate frame missing or incompatible')
            delta=bounds(change.get('delta_bounds_mm'))
            hits=[r['id'] for r in part['protected_regions'] if intersects(delta,bounds(r['bounds_mm']),margin)]
            if hits:
                add(ident,'FAIL','delta bounding region touches protected region(s): '+', '.join(hits));continue
            if not any(contained(delta,bounds(r['bounds_mm']),margin) for r in part['editable_regions']):
                add(ident,'NOT_EVALUATED','delta not contained in one explicitly editable region');continue
            add(ident,'PASS','conservative delta bounds fit editable region and avoid protected boxes')
        if not geometry.get('parts'):raise ValueError('comparison parts missing')
    except (ValueError,OSError,KeyError,TypeError,IndexError) as exc:add('map','NOT_EVALUATED',str(exc))
    status='FAIL' if any(c['status']=='FAIL' for c in checks) else 'NOT_EVALUATED' if any(c['status']!='PASS' for c in checks) else 'PASS'
    return {'status':status,'checks':checks,'limits':['Conservative delta AABB may reject distant separate changes whose combined bounds cross a protected region.',
            'PASS is a scoped declared permission check, not fit, strength, clearance, exact surface matching or physical validation.',
            'Map authority is a local engineering declaration pinned by the enclosing approved contract; non-detection is qualified by its explicit threshold/source policy.']}
