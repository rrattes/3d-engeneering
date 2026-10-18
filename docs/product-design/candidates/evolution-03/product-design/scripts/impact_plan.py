#!/usr/bin/env python3
"""Plan file reuse by declared dependencies; never execute tasks or grant engineering acceptance."""
import argparse
import json
import os
import re
import tempfile
from pathlib import Path
from pd_common import canonical_sha,file_sha,load_json,local_path,safe_output,write_outputs

KINDS={'cad','engineering_check','render','review','report'}


def ordered(config,root):
    if not isinstance(config,dict):raise ValueError('workflow object required')
    if config.get('schema')!='product-design-workflow-v1':raise ValueError('unsupported workflow schema')
    rows=config.get('tasks')
    if not isinstance(rows,list) or not 1<=len(rows)<=128:raise ValueError('bounded task list required')
    tasks={};outputs=set()
    for row in rows:
        if not isinstance(row,dict):raise ValueError('task object required')
        ident=row.get('id')
        if not isinstance(ident,str) or not re.fullmatch(r'[a-z][a-z0-9_-]{0,63}',ident) or ident in tasks:raise ValueError('unique simple task IDs required')
        if row.get('kind') not in KINDS:raise ValueError('unsupported task kind')
        if not isinstance(row.get('depends_on'),list) or not isinstance(row.get('inputs'),list) or not isinstance(row.get('outputs'),list) or not row['outputs']:raise ValueError('explicit dependencies, inputs and nonempty outputs required')
        if not isinstance(row.get('parameters'),dict) or not isinstance(row.get('environment'),dict) or not row['environment']:raise ValueError('explicit parameters and tool/environment identities required')
        for path in row['inputs']:local_path(root,path)
        for path in row['outputs']:
            target=local_path(root,path)
            if target in outputs:raise ValueError('outputs must have one producer')
            outputs.add(target)
        if len(set(row['depends_on']))!=len(row['depends_on']):raise ValueError('duplicate dependency')
        tasks[ident]=row
    # Every consumed produced file needs its producer as an explicit graph dependency.
    producers={local_path(root,p):ident for ident,row in tasks.items() for p in row['outputs']}
    for ident,row in tasks.items():
        for path in row['inputs']:
            producer=producers.get(local_path(root,path))
            if producer is not None and producer not in row['depends_on']:raise ValueError('produced input missing graph dependency')
    order=[];visiting=set();done=set()
    def visit(ident):
        if ident not in tasks:raise ValueError('unknown dependency')
        if ident in visiting:raise ValueError('dependency cycle')
        if ident in done:return
        visiting.add(ident)
        for dep in tasks[ident]['depends_on']:visit(dep)
        visiting.remove(ident);done.add(ident);order.append(ident)
    for ident in tasks:visit(ident)
    return tasks,order


def snapshot(root,paths,required):
    result={}
    for name in paths:
        try:result[name]=file_sha(local_path(root,name))
        except (ValueError,OSError):
            if required:raise
            result[name]=None
    return result


def plan_work(config,state,root):
    root=Path(root).resolve();tasks,order=ordered(config,root);planned={}
    if not isinstance(state,dict):raise ValueError('cache state object required')
    if state.get('schema') not in (None,'product-design-cache-v1'):raise ValueError('unsupported cache state')
    records=state.get('tasks',{})
    if not isinstance(records,dict) or any(not isinstance(record,dict) for record in records.values()):
        raise ValueError('cache tasks must map IDs to record objects')
    for ident in order:
        task=tasks[ident];parents=[planned[d] for d in task['depends_on']]
        try:
            if task.get('dependencies_complete') is not True:raise ValueError('dependencies are not declared complete; no safe reuse plan')
            if any(p['state']=='BLOCKED' for p in parents):raise ValueError('dependency blocked')
            inputs=snapshot(root,task['inputs'],True);outputs=snapshot(root,task['outputs'],False)
            key=canonical_sha({'task':task,'inputs':inputs,'parents':{p['id']:{'fingerprint':p['fingerprint'],'outputs':p.get('outputs')} for p in parents},'planner_sha256':file_sha(Path(__file__))})
            old=state.get('tasks',{}).get(ident,{})
            reuse=old.get('fingerprint')==key and old.get('outputs')==outputs and all(outputs.values()) and all(p['state']=='REUSE' for p in parents)
            planned[ident]={'id':ident,'kind':task['kind'],'state':'REUSE' if reuse else 'RUN','fingerprint':key,'inputs':inputs,'outputs':outputs,
                            'reason':'declared inputs/dependencies/environment and output hashes unchanged' if reuse else 'missing/stale execution record, dependency, input, environment or output'}
        except (ValueError,OSError,KeyError,TypeError) as exc:
            planned[ident]={'id':ident,'kind':task['kind'],'state':'BLOCKED','reason':str(exc)}
    return {'schema':'product-design-work-plan-v1','tasks':list(planned.values()),'engineering_acceptance':'NOT_EVALUATED',
            'limits':['Reuse applies only to declared file dependencies and environment identities; undeclared state is not tracked.',
                      'No task is executed by this script. A cached image is not a visual review or user decision.']}


def record_task(config,state,root,ident):
    plan=plan_work(config,state,root);rows={r['id']:r for r in plan['tasks']};tasks,_=ordered(config,root)
    if ident not in rows:raise ValueError('unknown task')
    row=rows[ident]
    if row['state']=='BLOCKED' or any(rows[d]['state']!='REUSE' for d in tasks[ident]['depends_on']):raise ValueError('dependencies must have current completed records')
    if not all(row['outputs'].values()):raise ValueError('record only after outputs have actually been produced')
    result={'schema':'product-design-cache-v1','tasks':dict(state.get('tasks',{}))}
    result['tasks'][ident]={'fingerprint':row['fingerprint'],'outputs':row['outputs'],'record_type':'caller-declared completed execution; integrity only'}
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['plan','record']);p.add_argument('--project',type=Path,required=True)
    p.add_argument('--config',required=True);p.add_argument('--state',required=True);p.add_argument('--output');p.add_argument('--task');a=p.parse_args()
    try:
        config_path=local_path(a.project,a.config);config=load_json(config_path);state_path=local_path(a.project,a.state)
        state=load_json(state_path) if state_path.exists() else {}
        if a.action=='plan':
            if not a.output:raise ValueError('--output required')
            result=plan_work(config,state,a.project)
            directory=safe_output(a.project,a.output,'work-plan',[{'path':a.config},{'path':a.state},*[{'path':x} for t in config['tasks'] for x in t['inputs']+t['outputs']]])
            lines=['# Plano de reaproveitamento','']+[r['id']+': '+r['state']+' — '+r['reason'] for r in result['tasks']]
            write_outputs(directory,'work-plan',result,'\n'.join(lines)+'\n')
            print(json.dumps({'counts':{state:sum(t['state']==state for t in result['tasks']) for state in ('RUN','REUSE','BLOCKED')},'report':str((directory/'work-plan.json').relative_to(a.project.resolve()))}))
            return 3 if any(t['state']=='BLOCKED' for t in result['tasks']) else 0
        if not a.task:raise ValueError('--task required after actual external task completion')
        if not state_path.is_relative_to(a.project.resolve()/'reports'):raise ValueError('cache state must stay under reports')
        protected={config_path,*[local_path(a.project,x) for t in config['tasks'] for x in t['inputs']+t['outputs']]}
        if state_path in protected:raise ValueError('state cannot overwrite inputs or produced evidence')
        before=file_sha(state_path) if state_path.exists() else None
        result=record_task(config,state,a.project,a.task);state_path.parent.mkdir(parents=True,exist_ok=True)
        with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=state_path.parent,prefix='.cache-',delete=False) as stream:
            temp=Path(stream.name);json.dump(result,stream,ensure_ascii=False,indent=2,allow_nan=False);stream.write('\n')
        try:
            if (file_sha(state_path) if state_path.exists() else None)!=before:raise ValueError('state changed concurrently; retry after reviewing current state')
            temp.replace(state_path)
        finally:temp.unlink(missing_ok=True)
        print('RECORDED_INTEGRITY_ONLY');return 0
    except (ValueError,OSError,KeyError,TypeError,IndexError) as exc:print('INVALID_INPUT: '+str(exc));return 2
if __name__=='__main__':raise SystemExit(main())
