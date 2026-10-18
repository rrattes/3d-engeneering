#!/usr/bin/env python3
"""Optional atomic BREP comparison in an existing CAD environment, with explicit frames."""
import argparse
import itertools
from pathlib import Path
from pd_common import file_sha,load_json,local_path,number,write_outputs,safe_output,canonical_sha


def configuration_sha(before,after,catalog,tolerance_mm):
    return canonical_sha({'before':{k:str(v) for k,v in before.items()},
                          'after':{k:str(v) for k,v in after.items()},
                          'catalog':{k:v for k,v in catalog.items() if k!='project_root'},
                          'tolerance_mm':tolerance_mm})


def compare_parts(before,after,catalog,tolerance_mm):
    result={'schema':'product-design-geometry-v1','status':'NOT_EVALUATED','units':catalog.get('units'),
            'parts':[],'source_artifacts':[],'limits':['Volumetric difference only; no general registration or exhaustive Hausdorff bound.',
            'NOT_DETECTED means no volumetric change above the declared threshold, not certified geometric equivalence.']}
    try:
        linear=number(tolerance_mm);volume_tol=number(catalog.get('volume_tolerance_mm3'));angular=number(catalog.get('angular_tolerance_deg',1e-6))
        if linear<=0 or volume_tol<=0 or angular<=0 or catalog.get('units')!='mm':raise ValueError('explicit positive tolerances and mm units required')
        if not isinstance(before,dict) or not isinstance(after,dict):raise ValueError('part maps required')
        ids=sorted(set(before)|set(after))
        if not ids or len(ids)>128:raise ValueError('part budget exceeded or empty')
        root=Path(catalog['project_root']).resolve(strict=True)
        result.update(linear_tolerance_mm=linear,volume_tolerance_mm3=volume_tol,angular_tolerance_deg=angular,
                      before_revision=catalog.get('before_revision'),after_revision=catalog.get('after_revision'),
                      catalog_sha256=canonical_sha({k:v for k,v in catalog.items() if k!='project_root'}),
                      configuration_sha256=configuration_sha(before,after,catalog,tolerance_mm),
                      model_files={'before':{k:str(v) for k,v in before.items()},'after':{k:str(v) for k,v in after.items()}})
        from build123d import import_step,Pos,Rot
        import sys
        if '/opt/cad3d' not in sys.path:sys.path.insert(0,'/opt/cad3d')
        from brep_pairs import common_volume
        budget=0
        def read(mapping,ident,frame_key):
            nonlocal budget
            if ident not in mapping:return None,None
            path=Path(mapping[ident])
            if not path.is_absolute():path=local_path(root,str(path))
            path=path.resolve()
            if not path.is_relative_to(root):raise ValueError('STEP reference escapes project')
            sha=file_sha(path)
            spec=catalog.get('parts',{}).get(ident,{})
            frame=spec.get(frame_key)
            if not isinstance(frame,list) or len(frame)!=6:raise ValueError('explicit six-number frame required')
            frame=[number(x) for x in frame]
            shape=import_step(str(path))
            pose=Pos(*frame[:3])*Rot(*frame[3:])
            shape=pose.inverse()*shape
            solids=list(shape.solids())
            if not shape.is_valid or not 0<len(solids)<=64 or any(not s.is_valid or number(s.volume)<=0 for s in solids):raise ValueError('invalid, empty or oversized solid group')
            for a,b in itertools.combinations(solids,2):
                budget+=1
                if budget>8192:raise ValueError('BREP pair budget exceeded')
                if common_volume(a,b)>volume_tol:raise ValueError('overlapping solids cannot be summed as a disjoint part')
            result['source_artifacts'].append({'path':path.relative_to(root).as_posix(),'sha256':sha})
            return solids,frame
        for ident in ids:
            try:
                a,fa=read(before,ident,'before_pose');b,fb=read(after,ident,'after_pose')
                va=sum(s.volume for s in a) if a else 0;vb=sum(s.volume for s in b) if b else 0
                common=0
                for first in a or []:
                    for second in b or []:
                        budget+=1
                        if budget>8192:raise ValueError('BREP pair budget exceeded')
                        common+=common_volume(first,second)
                difference=va+vb-2*common
                if difference < -volume_tol or common>min(va,vb)+volume_tol:raise ValueError('inconsistent boolean volume')
                difference=max(0,difference)
                pose_changed=False if fa is None or fb is None else (any(abs(x-y)>linear for x,y in zip(fa[:3],fb[:3])) or any(abs(x-y)>angular for x,y in zip(fa[3:],fb[3:])))
                change='ADDED' if a is None else 'REMOVED' if b is None else 'RESHAPED' if difference>volume_tol else 'REPOSITIONED' if pose_changed else 'NO_VOLUMETRIC_CHANGE_DETECTED'
                delta_bounds=None
                if catalog.get('include_delta_bounds') and difference>volume_tol:
                    fragments=[];delta_volume=0
                    for original,cutters in ((a or [],b or []),(b or [],a or [])):
                        for solid in original:
                            remaining=solid
                            for cutter in cutters:
                                budget+=1
                                if budget>8192:raise ValueError('BREP difference budget exceeded')
                                remaining=remaining-cutter
                                pieces=list(remaining.solids())
                                if pieces and (not remaining.is_valid or any(not piece.is_valid for piece in pieces)):
                                    raise ValueError('invalid intermediate delta geometry')
                                if not pieces and remaining.faces():raise ValueError('non-solid delta remnant')
                            for piece in remaining.solids():
                                if not piece.is_valid or number(piece.volume)<=0:raise ValueError('invalid delta fragment; cannot conservatively omit material')
                                delta_volume+=number(piece.volume);fragments.append(piece.bounding_box())
                    if abs(delta_volume-difference)>volume_tol:raise ValueError('delta decomposition volume inconsistent with symmetric difference')
                    if not fragments:raise ValueError('changed volume without delta geometry')
                    delta_bounds=[[min(getattr(v.min,k) for v in fragments) for k in ('X','Y','Z')],
                                  [max(getattr(v.max,k) for v in fragments) for k in ('X','Y','Z')]]
                result['parts'].append({'id':ident,'status':'PASS','change_type':change,'shape_change':'DETECTED' if difference>volume_tol else 'NOT_DETECTED','pose_changed':pose_changed,'before_volume_mm3':va,'after_volume_mm3':vb,'symmetric_difference_mm3':difference,'delta_bounds_mm':delta_bounds,'delta_frame':'comparison_local_mm'})
            except (ValueError,OSError,KeyError,TypeError,RuntimeError,IndexError) as exc:
                result['parts'].append({'id':ident,'status':'NOT_EVALUATED','reason':str(exc)})
        for ref in result['source_artifacts']:
            if file_sha(root/ref['path'])!=ref['sha256']:raise ValueError('STEP source changed during comparison')
        result['status']='PASS' if all(p['status']=='PASS' for p in result['parts']) else 'NOT_EVALUATED'
        result['atomic_pair_checks']=budget
    except (ImportError,ValueError,OSError,KeyError,TypeError,RuntimeError,IndexError) as exc:
        result['reason']=str(exc)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--project',type=Path,required=True);p.add_argument('--config',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    try:
        config=load_json(local_path(a.project,a.config));catalog=dict(config['catalog'],project_root=str(a.project.resolve()))
        r=compare_parts(config['before'],config['after'],catalog,config['tolerance_mm'])
        write_outputs(safe_output(a.project,a.output,'geometry-comparison',[{'path':a.config},*r['source_artifacts']]),'geometry-comparison',r,'# Comparação geométrica\n\nEstado: '+r['status']+'\n\nComparação volumétrica com frames explícitos; não demonstra desempenho físico.\n')
        print(r['status']);return 0 if r['status']=='PASS' else 3
    except (ValueError,OSError,KeyError,TypeError) as exc:print('INVALID_INPUT: '+str(exc));return 2
if __name__=='__main__':raise SystemExit(main())


def solid_fragments(shape,limit=128):
    """Reject free faces/edges/vertices even when a compound also contains solids."""
    from OCP.TopExp import TopExp
    from OCP.TopTools import TopTools_IndexedMapOfShape
    from OCP.TopAbs import TopAbs_FACE,TopAbs_EDGE,TopAbs_VERTEX
    solids=list(shape.solids())
    if len(solids)>limit:raise ValueError('fragment budget exceeded')
    if solids and (not shape.is_valid or any(not s.is_valid or number(s.volume)<=0 for s in solids)):
        raise ValueError('invalid Boolean fragment')
    for kind in (TopAbs_FACE,TopAbs_EDGE,TopAbs_VERTEX):
        all_shapes=TopTools_IndexedMapOfShape();owned=TopTools_IndexedMapOfShape()
        if shape.wrapped is not None:TopExp.MapShapes_s(shape.wrapped,kind,all_shapes)
        for solid in solids:TopExp.MapShapes_s(solid.wrapped,kind,owned)
        if any(not owned.Contains(all_shapes.FindKey(i)) for i in range(1,all_shapes.Extent()+1)):
            raise ValueError('non-solid Boolean/STEP remnant')
    return solids


def region_metrics(before,after,protected_material,protected_void,editable_volumes,volume_tolerance):
    """Exact kernel Boolean volumes in a common frame; no AABB permission fallback.

    Inputs are bounded, valid nonoverlapping solid lists checked by the v2 reader.
    Every intermediate remnant is checked, including non-solid/invalid fragments.
    """
    budget=0
    def pieces(shape):return solid_fragments(shape)
    def cut(items,cutters):
        nonlocal budget
        result=[]
        for solid in items:
            current=[solid]
            for cutter in cutters:
                next_items=[]
                for item in current:
                    budget+=1
                    if budget>8192:raise ValueError('Boolean budget exceeded')
                    next_items.extend(pieces(item-cutter))
                current=next_items
            result.extend(current)
            if len(result)>128:raise ValueError('fragment budget exceeded')
        return result
    def volume(items):return sum(number(s.volume) for s in items)
    added=cut(after,before);removed=cut(before,after)
    lost=volume(cut(protected_material,after))
    initial_lost=volume(cut(protected_material,before))
    # Union through sequential subtraction avoids double-counting overlapping regions.
    void_after=volume(after)-volume(cut(after,protected_void))
    void_before=volume(before)-volume(cut(before,protected_void))
    outside=volume(cut(added+removed,editable_volumes))
    values={'added_mm3':volume(added),'removed_mm3':volume(removed),'protected_material_missing_mm3':lost,
            'baseline_protected_material_missing_mm3':initial_lost,'protected_void_occupied_mm3':void_after,
            'baseline_void_occupied_mm3':void_before,'outside_editable_mm3':outside}
    if any(v < -volume_tolerance for v in values.values()):raise ValueError('inconsistent Boolean volumes')
    return {**{k:max(0,v) for k,v in values.items()},'boolean_operations':budget}
