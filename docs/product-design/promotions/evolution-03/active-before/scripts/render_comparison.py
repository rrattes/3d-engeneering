#!/usr/bin/env python3
"""Matched STEP views using the existing CAD3D renderer; no aesthetic PASS is inferred."""
import argparse
import itertools
import math
import re
import sys
from pathlib import Path
from pd_common import artifact,canonical_sha,file_sha,load_json,local_path,number,safe_output,write_outputs


def vector(value):
    if not isinstance(value,list) or len(value)!=3:raise ValueError('XYZ triple required')
    return tuple(number(x) for x in value)


def unit(v):
    norm=math.sqrt(sum(x*x for x in v))
    if norm<1e-12:raise ValueError('zero camera vector')
    return tuple(x/norm for x in v)


def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b):return sum(x*y for x,y in zip(a,b))


def camera_for_bounds(all_bounds,direction,up,aspect):
    """Fit projected bounding-box corners with equal space reserved for titles/footers."""
    normal=unit(vector(direction));right=unit(cross(vector(up),normal));vertical=unit(cross(normal,right))
    low=[min(b[0][i] for b in all_bounds) for i in range(3)];high=[max(b[1][i] for b in all_bounds) for i in range(3)]
    center=tuple((a+b)/2 for a,b in zip(low,high))
    points=[tuple(p[i]-center[i] for i in range(3)) for b in all_bounds for p in itertools.product(*zip(b[0],b[1]))]
    x=max(abs(dot(p,right)) for p in points);y=max(abs(dot(p,vertical)) for p in points)
    scale=max(y/.78,x/aspect,1)*1.13
    distance=max(math.dist(low,high)*3,100)
    return {'position':[center[i]+normal[i]*distance for i in range(3)],'target':center,'up':vertical,
            'parallel_scale_mm':scale,'fit':'projected union bounds; 22 percent vertical annotation reserve; 13 percent margin'}


def render_comparison(config,root,directory):
    root=Path(root).resolve();directory=Path(directory).resolve()
    if not directory.is_relative_to(root/'reports'):raise ValueError('render outputs must stay within project reports')
    if not isinstance(config,dict):raise ValueError('comparison object required')
    if config.get('schema')!='product-design-visual-comparison-v1' or config.get('units')!='mm':raise ValueError('explicit visual schema and mm units required')
    cases=config.get('cases');views=config.get('views')
    if not isinstance(cases,list) or not 2<=len(cases)<=12 or not isinstance(views,list) or not 1<=len(views)<=4:raise ValueError('2..12 cases and 1..4 views required')
    for rows in (cases,views):
        if any(not isinstance(r,dict) for r in rows):raise ValueError('case/view objects required')
        ids=[r.get('id') for r in rows]
        if any(not isinstance(i,str) or not re.fullmatch(r'[a-z][a-z0-9_-]{0,40}',i) for i in ids) or len(set(ids))!=len(ids):raise ValueError('unique simple case/view IDs required')
    import pyvista as pv
    from build123d import import_step,Pos,Rot
    if '/opt/cad3d' not in sys.path:sys.path.insert(0,'/opt/cad3d')
    from cad3d_visualization import _tessellate
    loaded=[];references=[];boxes=[];count=0
    for case in cases:
        parts=case.get('parts')
        if not isinstance(parts,list) or not parts:raise ValueError('case parts required')
        models=[]
        for part in parts:
            if not isinstance(part,dict):raise ValueError('part object required')
            count+=1
            if count>64:raise ValueError('comparison limited to 64 part instances')
            ref=part['source'];artifact(root,ref);references.append(ref)
            pose=part.get('pose')
            if not isinstance(pose,list) or len(pose)!=6:raise ValueError('explicit six-number display pose required')
            pose=[number(x) for x in pose]
            shape=import_step(str(local_path(root,ref['path'])))
            if not shape.is_valid or not shape.solids():raise ValueError('invalid/empty STEP')
            shape=Pos(*pose[:3])*Rot(*pose[3:])*shape
            b=shape.bounding_box();boxes.append([[b.min.X,b.min.Y,b.min.Z],[b.max.X,b.max.Y,b.max.Z]])
            models.append((_tessellate(shape),part.get('color','#bfc3c7')))
        loaded.append(models)
    protected={local_path(root,ref['path']) for ref in references}
    columns=min(3,len(cases));rows=math.ceil(len(cases)/columns)
    pixels=(columns*800,rows*680);aspect=800/680
    cameras={};images=[]
    directory.mkdir(parents=True,exist_ok=True)
    lighting={'ambient':.3,'diffuse':.7,'specular':.12,'feature_angle_deg':25,'background':'#eef0f1','palette_mode':'per-part declared colors, common defaults'}
    for view in views:
        camera=camera_for_bounds(boxes,view['direction'],view['up'],aspect);cameras[view['id']]=camera
        path=directory/('comparison-'+view['id']+'.png')
        if path.resolve() in protected:raise ValueError('image would overwrite a source')
        plot=pv.Plotter(shape=(rows,columns),off_screen=True,window_size=pixels,border=False)
        try:
            plot.enable_anti_aliasing('ssaa')
            for index,case in enumerate(cases):
                plot.subplot(index//columns,index%columns);plot.set_background(lighting['background'])
                for mesh,color in loaded[index]:
                    plot.add_mesh(mesh,color=color,smooth_shading=True,split_sharp_edges=True,feature_angle=25,
                                  ambient=lighting['ambient'],diffuse=lighting['diffuse'],specular=lighting['specular'])
                plot.camera_position=[camera['position'],camera['target'],camera['up']]
                plot.enable_parallel_projection();plot.camera.parallel_scale=camera['parallel_scale_mm']
                plot.add_text(case.get('label',case['id']),position='upper_left',font_size=17,color='#27343f')
                plot.add_text('STEP CAD | same camera and scale | finish simulated',position='lower_left',font_size=10,color='#4d5963')
            plot.screenshot(str(path))
        finally:plot.close()
        images.append({'path':str(path.relative_to(root)),'sha256':file_sha(path)})
    for ref in references:artifact(root,ref)
    return {'schema':'product-design-visual-output-v1','status':'PASS','scope':'render generation and geometric framing only',
            'config_sha256':canonical_sha(config),'sources':references,'cameras':cameras,'lighting':lighting,'window_pixels':pixels,
            'images':images,'actual_visual_review':'NOT_EVALUATED','user_acceptance':'PENDING','physical_finish':'NOT_EVALUATED',
            'limits':['Display poses/exploded views are not assembly motion analysis.','Imported STEP units are declared by the source workflow, not inferred from image scale.']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--project',type=Path,required=True);p.add_argument('--config',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    try:
        config=load_json(local_path(a.project,a.config))
        if not isinstance(config,dict):raise ValueError('comparison object required')
        directory=safe_output(a.project,a.output,'visual-comparison',[config,{'path':a.config}])
        # Also protect the config itself against an image naming collision.
        for view in config.get('views',[]):
            if not isinstance(view,dict):raise ValueError('view object required')
            if (directory/('comparison-'+str(view.get('id'))+'.png')).resolve()==local_path(a.project,a.config):raise ValueError('image cannot overwrite config')
        result=render_comparison(config,a.project,directory)
        write_outputs(directory,'visual-comparison',result,'# Comparação visual\n\nGeração: PASS. Revisão visual: NOT_EVALUATED até abrir as imagens.\n')
        print('PASS_RENDER_ONLY');return 0
    except ImportError as exc:print('NOT_EVALUATED: existing CAD/render backend unavailable: '+str(exc));return 3
    except (ValueError,OSError,KeyError,TypeError,RuntimeError) as exc:print('INVALID_INPUT: '+str(exc));return 2
if __name__=='__main__':raise SystemExit(main())
