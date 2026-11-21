#!/usr/bin/env python3
"""Static reference validation for OSTF 5.0.0 examples.

Checks local JSON syntax, version-specific JSON Schema constraints,
whole-file byte SHA, and OSTFP manifest/file inventory. NOT a DAW/plug-in,
security audit, independent parser, semantic completeness certification or
runtime test. jsonschema>=4 is an optional dependency for developers.
"""
from __future__ import annotations
import hashlib
import json
import sys
import zipfile
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:
    raise SystemExit('Install jsonschema: python -m pip install jsonschema') from exc

import ostfp

ROOT=Path(__file__).resolve().parents[1]
SCHEMAS=ROOT/'schema'
LEGACY=ROOT/'adopted-4.3'/'schema'


def strict_json(raw:bytes, source:str):
    def duplicate_guard(pairs):
        result={}
        for k,v in pairs:
            if k in result:
                raise ValueError(f'{source}: duplicate JSON key {k!r}')
            result[k]=v
        return result
    def bad_number(x):
        raise ValueError(f'{source}: non-finite JSON numeric constant {x!r}')
    if raw.startswith(b'\xef\xbb\xbf'):
        raise ValueError(f'{source}: UTF-8 BOM is forbidden')
    return json.loads(raw.decode('utf-8'),object_pairs_hook=duplicate_guard,parse_constant=bad_number)


def load_schemas():
    table={
        'score:5.0.0': SCHEMAS/'ostf-5.0.0.schema.json',
        'score:4.3.0': LEGACY/'ostf-4.3.0.schema.json',
        'production:0.3.0': SCHEMAS/'ostf-production-session-0.3.schema.json',
        'production:0.2.0': LEGACY/'ostf-production-session-0.2.schema.json',
        'distributed:0.3': SCHEMAS/'ostf-distributed-session-0.3.schema.json',
        'distributed:0.2': LEGACY/'ostf-distributed-session-0.2.schema.json',
        'manifest:1.0.0': SCHEMAS/'ostf-package-manifest-1.0.schema.json',
        'plugin:1.0.0': SCHEMAS/'ostf-plugin-context-1.0.schema.json',
    }
    validators={}
    for name,path in table.items():
        schema=strict_json(path.read_bytes(),str(path))
        Draft202012Validator.check_schema(schema)
        validators[name]=Draft202012Validator(schema)
    return validators


def check(validators,key,payload,source):
    errs=sorted(validators[key].iter_errors(payload),key=lambda e:list(map(str,e.absolute_path)))
    if errs:
        err=errs[0]
        where='/'.join(map(str,err.absolute_path))
        raise ValueError(f'{source}: {key}: {where}: {err.message}')


def validate_package(path:Path,validators):
    ostfp.validate(path)
    with zipfile.ZipFile(path) as z:
        m=strict_json(z.read('manifest.json'),str(path)+'/manifest.json')
        check(validators,'manifest:1.0.0',m,str(path))
        score_b=z.read(m['score']['path'])
        score=strict_json(score_b,str(path)+'/score')
        check(validators,'score:'+m['score']['version'],score,str(path))
        if hashlib.sha256(score_b).hexdigest()!=m['score']['sha256']:
            raise ValueError(f'{path}: Score SHA mismatch')
        if score.get('format')!='OSTF' or score.get('version')!=m['score']['version']:
            raise ValueError(f'{path}: manifest Score version mismatch')
        for d in m['documents']:
            raw=z.read(d['path'])
            if hashlib.sha256(raw).hexdigest()!=d['sha256']:
                raise ValueError(f'{path}: document SHA mismatch: {d["id"]}')
            obj=strict_json(raw,str(path)+'/'+d['path'])
            key='production:'+d['version'] if d['role']=='productionSession' else 'distributed:'+d['version']
            check(validators,key,obj,str(path)+'/'+d['path'])
        for asset in m['assets']:
            b=z.read(asset['path'])
            if len(b)!=asset['sizeBytes'] or hashlib.sha256(b).hexdigest()!=asset['sha256']:
                raise ValueError(f'{path}: asset byte length or SHA mismatch: {asset["id"]}')


def main():
    val=load_schemas()
    count={'score':0,'production':0,'distributed':0,'plugin':0,'ostfp':0}
    for folder,key,ext in [
        ('score','score:5.0.0','.ostf'),
        ('production','production:0.3.0','.json'),
        ('distributed','distributed:0.3','.json'),
        ('plugin','plugin:1.0.0','.json')
    ]:
        for f in sorted((ROOT/'examples'/folder).glob('*'+ext)):
            parsed=strict_json(f.read_bytes(),str(f))
            check(val,key,parsed,str(f))
            count[folder]+=1
    for f in sorted((ROOT/'examples/ostfp').glob('*.ostfp')):
        validate_package(f,val)
        count['ostfp']+=1
    # Exactly 25 standalone Scores and 11 real project examples in this edition.
    if (count['score'],count['ostfp'])!=(25,11):
        raise ValueError('unexpected release example count: '+repr(count))
    print('Static structure, inner bytes and source pins verified:',count)
    print('No runtime/interoperability/security certification performed.')

if __name__=='__main__':
    try:main()
    except (OSError,ValueError,TypeError,KeyError,zipfile.BadZipFile,ostfp.PackageError) as e:
        print('ERROR:',e,file=sys.stderr)
        raise SystemExit(1)
