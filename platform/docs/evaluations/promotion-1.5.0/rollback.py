#!/usr/bin/env python3
"""Restore only the two links changed by the recorded activation."""
from pathlib import Path
import json,os,uuid
snapshot=json.loads(Path(__file__).with_name('activation-snapshot.json').read_text())
for name,expected in snapshot['next'].items():
 link=Path(name)
 if not link.is_symlink() or os.readlink(link)!=expected:
  raise SystemExit('Refusing rollback: active link changed since activation: '+name)
for name,target in snapshot['previous'].items():
 link=Path(name);temporary=link.with_name(link.name+'.rollback-'+uuid.uuid4().hex)
 try:
  temporary.symlink_to(target);os.replace(temporary,link)
 finally:
  if temporary.is_symlink():temporary.unlink()
print('Prior CLI and skill links restored; Docker images and projects preserved.')
