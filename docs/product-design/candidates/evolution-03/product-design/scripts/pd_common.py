"""Bounded local evidence and deterministic JSON utilities; no external services."""
import hashlib
import json
import math
import tempfile
from pathlib import Path

MAX_BYTES=64*1024*1024

def canonical_sha(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def number(value):
    if isinstance(value,bool) or not isinstance(value,(int,float)):
        raise ValueError('expected finite number, not boolean')
    try:
        finite=math.isfinite(value)
    except OverflowError:
        finite=False
    if not finite:
        raise ValueError('expected finite number, not boolean')
    return float(value)

def local_path(root, name):
    if not isinstance(name,str) or not name or Path(name).is_absolute() or '..' in Path(name).parts:
        raise ValueError('reference must be a confined relative path')
    root=Path(root).resolve();path=(root/name).resolve()
    if not path.is_relative_to(root):raise ValueError('reference escapes project')
    return path

def file_sha(path):
    path=Path(path)
    if not path.is_file() or path.stat().st_size>MAX_BYTES:raise ValueError('missing or oversized evidence')
    h=hashlib.sha256()
    with path.open('rb') as f:
        size=0
        for block in iter(lambda:f.read(1024*1024),b''):
            size+=len(block)
            if size>MAX_BYTES:raise ValueError('oversized evidence')
            h.update(block)
    return h.hexdigest()

def _object(pairs):
    value={}
    for key,item in pairs:
        if key in value:raise ValueError('duplicate JSON key')
        value[key]=item
    return value

def load_json(path):
    file_sha(path)
    return json.loads(Path(path).read_text(encoding='utf-8'),object_pairs_hook=_object,
                      parse_constant=lambda value:(_ for _ in ()).throw(ValueError('nonfinite JSON number')))

def artifact(root, ref, parse=False):
    if not isinstance(ref,dict):raise ValueError('missing evidence reference')
    path=local_path(root,ref.get('path'));sha=ref.get('sha256')
    if not isinstance(sha,str) or len(sha)!=64 or file_sha(path)!=sha:raise ValueError('evidence hash mismatch')
    value=load_json(path) if parse else None
    pointer=ref.get('pointer','')
    if pointer:
        if not parse or not isinstance(pointer,str) or not pointer.startswith('/'):raise ValueError('invalid JSON pointer')
        for token in pointer[1:].split('/'):
            token=token.replace('~1','/').replace('~0','~')
            if isinstance(value,list):
                if not token.isdigit():raise ValueError('invalid list pointer')
                value=value[int(token)]
            else:value=value[token]
    return value

def write_outputs(directory, stem, payload, markdown):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    for suffix,content in [('json',json.dumps(payload,ensure_ascii=False,indent=2,allow_nan=False)+'\n'),('md',markdown)]:
        path=directory/(stem+'.'+suffix)
        with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=directory,prefix='.report-',delete=False) as stream:
            temp=Path(stream.name);stream.write(content)
        try:temp.replace(path)
        finally:temp.unlink(missing_ok=True)


def safe_output(root, name, stem, inputs):
    """Constrain reports and reject writes over pinned source/evidence files."""
    root=Path(root).resolve();directory=local_path(root,name)
    if not directory.is_relative_to(root/'reports'):
        raise ValueError('outputs must stay under the project reports directory')
    protected=set()
    def visit(value):
        if isinstance(value,dict):
            if isinstance(value.get('path'),str):protected.add(local_path(root,value['path']))
            for item in value.values():visit(item)
        elif isinstance(value,list):
            for item in value:visit(item)
    visit(inputs)
    for suffix in ('json','md'):
        if (directory/(stem+'.'+suffix)).resolve() in protected:
            raise ValueError('output would overwrite input/evidence')
    return directory
