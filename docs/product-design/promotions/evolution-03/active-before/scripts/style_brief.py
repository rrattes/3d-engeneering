#!/usr/bin/env python3
"""Read only the selected style vocabulary and source cards; no CAD or web fetch."""
import argparse
from pathlib import Path
from pd_common import load_json,write_outputs,local_path,safe_output


def make_brief(style,variant=None,custom=None):
    assets=Path(__file__).resolve().parents[1]/'assets'
    if style=='custom':
        if not isinstance(custom,dict) or not custom.get('form') or not custom.get('criteria'):
            raise ValueError('custom direction requires form and observable criteria')
        return {'style':'custom','direction':custom,'references':[],'engineering':'Preserve the engineering contract; optional final stage.'}
    vocabulary=load_json(assets/'style_vocabulary.json')['styles']
    if style not in vocabulary:raise ValueError('unknown style; use custom for another direction')
    selected=vocabulary[style]
    if variant is not None and variant not in selected['variants']:raise ValueError('unknown substyle')
    variants={variant:selected['variants'][variant]} if variant else selected['variants']
    ids={ref for item in variants.values() for ref in item['references']}
    cards=load_json(assets/'reference_cards.json')['cards']
    return {'style':style,'signature':selected['signature'],'avoid':selected['avoid'],'variants':variants,
            'review_question':selected['check'],'references':[c for c in cards if c['id'] in ids],
            'engineering':'Preserve protected interfaces; differences must be implemented and rechecked.'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--style',required=True);p.add_argument('--variant');p.add_argument('--custom',type=Path)
    p.add_argument('--project',type=Path);p.add_argument('--output');a=p.parse_args()
    try:
        custom=load_json(a.custom) if a.custom else None
        result=make_brief(a.style,a.variant,custom)
        if a.output:
            if a.project is None:raise ValueError('--project required with --output')
            directory=safe_output(a.project,a.output,'style-brief',[{'path':str(a.custom.resolve().relative_to(a.project.resolve()))}] if a.custom else [])
            lines=['# Direção de estilo: '+result['style'],'']
            lines+=['- '+x for x in result.get('signature',[])]
            for name,item in result.get('variants',{}).items():lines+=['','## '+name,'',item['form'],'',item['cmf']]
            lines+=['','Referências requerem inspeção das imagens antes de avaliar aparência.','']
            write_outputs(directory,'style-brief',result,'\n'.join(lines))
        import json
        print(json.dumps(result,ensure_ascii=False,indent=2));return 0
    except (ValueError,OSError,KeyError,TypeError) as exc:print('INVALID_INPUT: '+str(exc));return 2
if __name__=='__main__':raise SystemExit(main())
