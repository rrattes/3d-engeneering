#!/usr/bin/env python3
"""Optional exterior features in the existing build123d backend, not a second CAD engine."""
import argparse
from pathlib import Path
from pd_common import load_json,local_path,number,safe_output,write_outputs,file_sha


def positive(value):
    value=number(value)
    if value<=0:raise ValueError('positive dimension required')
    return value


def profile(spec):
    if not isinstance(spec,dict):raise ValueError('profile specification object required')
    from build123d import Pos,Polygon,RectangleRounded
    width=positive(spec['width']);depth=positive(spec['depth']);z=number(spec.get('z',0))
    x=number(spec.get('x',0));y=number(spec.get('y',0))
    if spec['kind']=='rounded':
        radius=positive(spec['radius'])
        if 2*radius>=min(width,depth):raise ValueError('radius must fit the section')
        shape=RectangleRounded(width,depth,radius)
    elif spec['kind']=='faceted':
        c=positive(spec['clip']);a=width/2;b=depth/2
        if c>=min(a,b):raise ValueError('facet cut too large')
        shape=Polygon((-a+c,-b),(a-c,-b),(a,-b+c),(a,b-c),(a-c,b),(-a+c,b),(-a,b-c),(-a,-b+c),align=None)
    else:raise ValueError('supported profiles: rounded, faceted')
    return Pos(x,y,z)*shape


def make_feature(spec):
    if not isinstance(spec,dict):raise ValueError('feature specification object required')
    from build123d import extrude,loft,Box,Pos,Rot,Align
    kind=spec['kind']
    if kind=='loft':
        sections=spec['sections']
        if not isinstance(sections,list) or not 2<=len(sections)<=16:raise ValueError('2..16 sections required')
        levels=[number(s['z']) for s in sections]
        if any(a>=b for a,b in zip(levels,levels[1:])):raise ValueError('strictly increasing Z sections required')
        if not isinstance(spec.get('ruled'),bool):raise ValueError('explicit ruled/smooth selection required')
        shape=loft([profile(s) for s in sections],ruled=spec['ruled'])
    elif kind=='frame':
        outer=spec['outer'];inner=spec['inner'];height=positive(spec['height'])
        # Concentric rounded profiles with the same datum avoid hidden disconnected rings.
        if outer['kind']!='rounded' or inner['kind']!='rounded':raise ValueError('rounded concentric frame required')
        for axis in ('x','y','z'):
            if number(outer.get(axis,0))!=number(inner.get(axis,0)):raise ValueError('frame datums must coincide')
        a=profile(outer);b=profile(inner)
        if positive(inner['width'])>=positive(outer['width']) or positive(inner['depth'])>=positive(outer['depth']):raise ValueError('inner profile must be smaller')
        outside=b-a
        if sum(face.area for face in outside.faces())>1e-6:raise ValueError('inner frame extends beyond outer contour')
        shape=extrude(a-b,amount=height)
    elif kind=='relief':
        length=positive(spec['length']);width=positive(spec['width']);height=positive(spec['height'])
        shape=Pos(number(spec.get('x',0)),number(spec.get('y',0)),number(spec.get('z',0)))*Rot(0,0,number(spec['angle_deg']))*Box(length,width,height,align=(Align.CENTER,Align.CENTER,Align.MIN))
    else:raise ValueError('supported features: loft, frame, relief')
    if not shape.is_valid or len(shape.solids())!=1 or number(shape.volume)<=0:raise ValueError('recipe did not produce one valid solid')
    return shape


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--project',type=Path,required=True);p.add_argument('--spec',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    try:
        spec=load_json(local_path(a.project,a.spec));directory=safe_output(a.project,a.output,'style-feature',[{'path':a.spec}])
        from build123d import export_step
        shape=make_feature(spec);directory.mkdir(parents=True,exist_ok=True);path=directory/'style-feature.step'
        if path.resolve()==local_path(a.project,a.spec):raise ValueError('output cannot overwrite spec')
        export_step(shape,str(path));result={'status':'PASS','scope':'feature CAD only','feature':spec['kind'],'volume_mm3':shape.volume,'step':{'path':str(path.relative_to(a.project.resolve())),'sha256':file_sha(path)},'physical_validation':'NOT_EVALUATED'}
        write_outputs(directory,'style-feature',result,'# Recurso paramétrico\n\nUm recurso CAD, não um produto validado.\n');print('PASS');return 0
    except ImportError as exc:print('NOT_EVALUATED: backend unavailable: '+str(exc));return 3
    except (ValueError,OSError,KeyError,TypeError,RuntimeError) as exc:print('INVALID_INPUT: '+str(exc));return 2
if __name__=='__main__':raise SystemExit(main())
