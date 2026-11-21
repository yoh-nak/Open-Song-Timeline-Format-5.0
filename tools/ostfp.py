#!/usr/bin/env python3
"""OSTFP 1.0 prototype static package verifier / packer / unpacker.
Not a DAW, plugin, audio playback, or security-certified implementation.
Stream binary payloads; keep bounded Score/session/manifest JSON in memory.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import pathlib
import re
import shutil
import stat
import sys
import tempfile
import unicodedata
import zipfile

MIME=b'application/vnd.ostf-project+zip'
MAX_ENTRIES=10000
MAX_TOTAL_BYTES=20*1024**3
MAX_RATIO=1000
MAX_MANIFEST_BYTES=8*1024**2
MAX_JSON_BYTES=64*1024**2
CHUNK=1024*1024
REQUIRED={'packageFormat','packageVersion','projectId','title','score','documents','assets','bindings'}

class PackageError(Exception):pass

def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()

def parse_json(data:bytes,label:str):
    def no_duplicates(pairs):
        d={}
        for k,v in pairs:
            if k in d:raise PackageError(f'{label}: duplicate JSON key {k!r}')
            d[k]=v
        return d
    def bad_constant(v):raise PackageError(f'{label}: forbidden JSON value {v}')
    if data.startswith(b'\xef\xbb\xbf'):
        raise PackageError(f'{label}: BOM not supported by this prototype')
    try:
        return json.loads(data.decode('utf-8'),object_pairs_hook=no_duplicates,parse_constant=bad_constant)
    except (UnicodeError,ValueError) as e:
        raise PackageError(f'{label}: malformed JSON/UTF-8: {e}') from e

def check_path(path):
    if not isinstance(path,str) or not path or len(path)>1024:raise PackageError(f'bad path {path!r}')
    if unicodedata.normalize('NFC',path)!=path:raise PackageError(f'non-NFC path {path}')
    if path.startswith('/') or '\\' in path or ':' in path or '\x00' in path:
        raise PackageError(f'unsafe path {path}')
    if any(x in ('.','..','') for x in path.split('/')):raise PackageError(f'unsafe path segments {path}')
    if any(ord(c)<32 or ord(c)==127 for c in path):raise PackageError(f'control char in path {path}')
    if path in ('mimetype','manifest.json'):raise PackageError('reserved member path')
    return path

def descriptor_paths(manifest):
    if not isinstance(manifest,dict) or not REQUIRED<=set(manifest):
        raise PackageError('manifest missing required fields')
    if manifest['packageFormat']!='OSTFP' or manifest['packageVersion']!='1.0.0':
        raise PackageError('unsupported package identity')
    sc=manifest['score']
    if not isinstance(sc,dict) or not {'path','format','version','sha256'}<=set(sc):
        raise PackageError('score descriptor incomplete')
    if sc['format']!='OSTF' or sc['version'] not in ('4.3.0','5.0.0'):
        raise PackageError('unsupported Score version')
    descriptors=[('score',sc)]
    for typ in ('documents','assets'):
        if not isinstance(manifest[typ],list):raise PackageError(f'{typ} must be array')
        for x in manifest[typ]:
            if not isinstance(x,dict):raise PackageError(f'nonobject {typ}')
            descriptors.append((typ,x))
    paths={};seen_fold=set();seen_id=set()
    for typ,d in descriptors:
        p=check_path(d.get('path'))
        if p in paths or p.casefold() in seen_fold:raise PackageError(f'duplicate / folded path {p}')
        paths[p]=(typ,d);seen_fold.add(p.casefold())
        if not isinstance(d.get('sha256'),str) or not re.fullmatch(r'[0-9a-f]{64}',d['sha256']):
            raise PackageError(f'invalid digest {p}')
        if typ!='score':
            key=(typ,d.get('id'))
            if not isinstance(d.get('id'),str) or not d['id'] or key in seen_id:
                raise PackageError(f'missing or duplicate ID {key}')
            seen_id.add(key)
        if typ=='assets':
            sz=d.get('sizeBytes')
            if type(sz) is not int or sz<0:raise PackageError(f'invalid sizeBytes {p}')
            if not d.get('purpose') or not d.get('mediaType'):raise PackageError(f'incomplete Asset {p}')
    if not isinstance(manifest['bindings'],list):raise PackageError('nonarray bindings')
    asset_ids={a['id'] for a in manifest['assets']}
    doc_paths={d['path'] for d in manifest['documents']}
    for b in manifest['bindings']:
        if not isinstance(b,dict) or not b.get('resourceId') or b.get('assetId') not in asset_ids:
            raise PackageError('unresolved asset binding')
        if b.get('documentPath') not in doc_paths|{sc['path']}:
            raise PackageError('binding path is not Score or declared document')
    return paths

def stream_meta(fobj):
    h=hashlib.sha256();size=0
    while True:
        chunk=fobj.read(CHUNK)
        if not chunk:break
        size+=len(chunk);h.update(chunk)
        if size>MAX_TOTAL_BYTES:raise PackageError('member exceeds prototype max total uncompressed bytes')
    return h.hexdigest(),size

def check_identity_and_bindings(manifest,raw_json):
    sc=manifest['score'];score=parse_json(raw_json[sc['path']],sc['path'])
    if not isinstance(score,dict) or score.get('format')!='OSTF' or score.get('version')!=sc['version']:
        raise PackageError('Score format/version disagrees with manifest')
    docs={}
    for d in manifest['documents']:
        obj=parse_json(raw_json[d['path']],d['path'])
        if not isinstance(obj,dict):raise PackageError(f'nonobject JSON document {d["path"]}')
        docs[d['path']]=obj
        role=d['role']
        if role=='productionSession':
            if d['family']!='OSTF-Production-Session' or obj.get('profile')!=d['family'] or obj.get('profileVersion')!=d['version']:
                raise PackageError('Production role/family/version mismatch')
            pin=obj.get('score') or {}
            if pin.get('sha256')!=sc['sha256'] or pin.get('formatVersion')!=sc['version']:
                raise PackageError('Production Score digest/version pin mismatch')
            doc=score.get('document') or {}
            for k in ('documentId','revisionId'):
                if k in pin and pin[k]!=doc.get('id' if k=='documentId' else 'revisionId'):
                    raise PackageError(f'Production {k} disagrees with Score')
            if (d['version'],sc['version']) not in (('0.2.0','4.3.0'),('0.3.0','5.0.0')):
                raise PackageError('Production Profile version incompatible with Score')
        elif role=='distributedSession':
            if obj.get('profile')!=d['family']:
                raise PackageError('Distributed descriptor family != payload profile')
            if d['version']=='0.3':
                if d['family']!='OSTF-Distributed-Session-0.3' or sc['version']!='5.0.0':
                    raise PackageError('Distributed 0.3 requires Score 5')
                if obj.get('scoreSha256')!=sc['sha256']:
                    raise PackageError('Distributed 0.3 scoreSha256 mismatch')
                doc=score.get('document') or {}
                if obj.get('documentId')!=doc.get('id') or obj.get('revisionId')!=doc.get('revisionId'):
                    raise PackageError('Distributed 0.3 document/revision pin mismatch')
                plans=score.get('performancePlans',[])
                if len([pl for pl in plans if isinstance(pl,dict) and pl.get('id')==obj.get('performancePlanId')])!=1:
                    raise PackageError('Distributed 0.3 performancePlanId missing/nonunique')
            elif d['version']=='0.2':
                if d['family']!='OSTF-Distributed-Session-0.2' or sc['version']!='4.3.0':
                    raise PackageError('Distributed 0.2 requires Score 4.3')
                # Legacy 0.2 identity fields are checked only where available in this draft utility.
                if obj.get('scoreSha256') is not None and obj.get('scoreSha256')!=sc['sha256']:
                    raise PackageError('Distributed 0.2 scoreSha256 disagrees with Score')
                doc=score.get('document') or {}
                if obj.get('documentId') is not None and obj['documentId']!=doc.get('id'):
                    raise PackageError('Distributed 0.2 documentId mismatch')
                if obj.get('revisionId') is not None and obj['revisionId']!=doc.get('revisionId'):
                    raise PackageError('Distributed 0.2 revisionId mismatch')
                if obj.get('performancePlanId') is not None:
                    plans=score.get('performancePlans',[])
                    if len([p for p in plans if isinstance(p,dict) and p.get('id')==obj['performancePlanId']])!=1:
                        raise PackageError('Distributed 0.2 referenced Plan missing/nonunique')
            else:raise PackageError('unsupported Distributed Session version')
    # Manifest assets resolve byte identity, not plug-in availability/authorization.
    assets={a['id']:a for a in manifest['assets']}
    d_index={d['path']:d for d in manifest['documents']}
    seen=set()
    for b in manifest['bindings']:
        path,kind,resource_id=b['documentPath'],b['resourceKind'],b['resourceId']
        key=path,kind,resource_id
        if key in seen:raise PackageError(f'duplicate binding {key}')
        seen.add(key)
        if kind=='coreResource':
            if path!=sc['path']:raise PackageError('coreResource path is not the Score')
            refs=score.get('resources',[])
        elif kind=='productionAsset':
            if path not in d_index or d_index[path].get('role')!='productionSession':
                raise PackageError('productionAsset binding must name a Production Session')
            refs=docs[path].get('assets',[])
        else:raise PackageError('invalid resourceKind')
        if not isinstance(refs,list):raise PackageError('referenced resource list is not array')
        matches=[r for r in refs if isinstance(r,dict) and r.get('id')==resource_id]
        if len(matches)!=1:raise PackageError(f'missing or nonunique resource {resource_id}')
        actual=matches[0];packed=assets[b['assetId']]
        if actual.get('sha256') is not None and actual['sha256']!=packed['sha256']:
            raise PackageError('binding SHA disagreement')
        if kind=='productionAsset' and actual.get('purpose')!=packed['purpose']:
            raise PackageError('Production asset purpose mismatch')
        if actual.get('mediaType') and actual['mediaType']!=packed['mediaType']:
            raise PackageError('binding mediaType mismatch')

def check_payloads(manifest,metadata,raw_json):
    desc=descriptor_paths(manifest)
    if set(metadata)!=set(desc):
        raise PackageError(f'payload manifest mismatch: missing={sorted(set(desc)-set(metadata))}; unexpected={sorted(set(metadata)-set(desc))}')
    for path,(typ,d) in desc.items():
        gotsha,gotsz=metadata[path]
        if gotsha!=d['sha256']:raise PackageError(f'SHA mismatch {path}')
        if typ=='assets' and gotsz!=d['sizeBytes']:
            raise PackageError(f'asset length mismatch {path}')
    check_identity_and_bindings(manifest,raw_json)
    return len(desc)

def validate(path:pathlib.Path):
    path=pathlib.Path(path)
    if path.is_dir():
        if path.is_symlink():raise PackageError('project root symlink forbidden')
        if (path/'mimetype').is_symlink() or (path/'manifest.json').is_symlink():
            raise PackageError('manifest/mimetype symlink forbidden')
        if not (path/'mimetype').is_file() or (path/'mimetype').read_bytes()!=MIME:
            raise PackageError('bad project mimetype')
        if not (path/'manifest.json').is_file() or (path/'manifest.json').stat().st_size>MAX_MANIFEST_BYTES:
            raise PackageError('missing or oversized manifest')
        manifest=parse_json((path/'manifest.json').read_bytes(),'manifest.json')
        desc=descriptor_paths(manifest)
        members=[]
        for root,dirs,files in os.walk(path,followlinks=False):
            for nm in dirs+files:
                full=pathlib.Path(root)/nm
                if full.is_symlink():raise PackageError(f'symlink forbidden {full}')
            for nm in files:
                full=pathlib.Path(root)/nm
                rel=full.relative_to(path).as_posix()
                if rel in ('mimetype','manifest.json'):continue
                check_path(rel);members.append(rel)
                if len(members)>MAX_ENTRIES:raise PackageError('too many files')
        if len(set(p.casefold() for p in members))!=len(members):raise PackageError('casefold collision')
        if set(members)!=set(desc):raise PackageError('unlisted or missing package members')
        meta={};raw={};total=0
        for name,(kind,_) in desc.items():
            full=path/name;size=full.stat().st_size;total+=size
            if total>MAX_TOTAL_BYTES:raise PackageError('total uncompressed limit exceeded')
            if kind in ('score','documents') and size>MAX_JSON_BYTES:raise PackageError('oversized Score / Profile JSON')
            with full.open('rb') as fh:h,n=stream_meta(fh)
            meta[name]=(h,n)
            if kind in ('score','documents'):raw[name]=full.read_bytes()
        return check_payloads(manifest,meta,raw)
    if not zipfile.is_zipfile(path):raise PackageError('not a ZIP archive')
    with zipfile.ZipFile(path) as z:
        infos=z.infolist()
        if not (2<=len(infos)<=MAX_ENTRIES+2):raise PackageError('invalid member count')
        if infos[0].filename!='mimetype' or infos[0].compress_type!=zipfile.ZIP_STORED or infos[0].file_size!=len(MIME):
            raise PackageError('first ZIP member must be stored exact mimetype')
        if infos[1].filename!='manifest.json' or infos[1].file_size>MAX_MANIFEST_BYTES:
            raise PackageError('second ZIP member must be bounded manifest')
        if z.read(infos[0])!=MIME:raise PackageError('invalid mimetype bytes')
        seen=set();total=0
        for i,info in enumerate(infos):
            p=info.filename
            if i>=2:check_path(p)
            if info.is_dir():raise PackageError('directory entry not supported by this prototype')
            if p.casefold() in seen:raise PackageError('duplicate or casefolded ZIP member')
            seen.add(p.casefold())
            mode=info.external_attr>>16
            if stat.S_IFMT(mode)==stat.S_IFLNK:raise PackageError('symlink entry forbidden')
            if info.flag_bits & 1:raise PackageError('encrypted ZIP member forbidden')
            if info.compress_type not in (zipfile.ZIP_STORED,zipfile.ZIP_DEFLATED):
                raise PackageError('unsupported ZIP compression')
            total+=info.file_size
            if total>MAX_TOTAL_BYTES:raise PackageError('uncompressed bytes exceed prototype limit')
            if info.file_size>65536 and info.file_size/max(1,info.compress_size)>MAX_RATIO:
                raise PackageError('potential ZIP bomb ratio')
        manifest=parse_json(z.read(infos[1]),'manifest.json')
        desc=descriptor_paths(manifest)
        actual={info.filename for info in infos[2:]}
        if actual!=set(desc):raise PackageError('unlisted/missing payload member')
        meta={};raw={}
        for info in infos[2:]:
            typ,_=desc[info.filename]
            if typ in ('score','documents') and info.file_size>MAX_JSON_BYTES:
                raise PackageError('oversized JSON score/profile')
            with z.open(info,'r') as fh:
                if typ in ('score','documents'):
                    data=fh.read(MAX_JSON_BYTES+1)
                    if len(data)>MAX_JSON_BYTES:raise PackageError('oversized JSON payload')
                    h,n=sha(data),len(data);raw[info.filename]=data
                else:
                    h,n=stream_meta(fh)
            if n!=info.file_size:raise PackageError(f'ZIP uncompressed count mismatch {info.filename}')
            meta[info.filename]=(h,n)
        return check_payloads(manifest,meta,raw)

def pack(src:pathlib.Path,dst:pathlib.Path):
    src,dst=pathlib.Path(src),pathlib.Path(dst)
    if dst.exists():raise PackageError('destination exists')
    validate(src)
    member_names=sorted([p.relative_to(src).as_posix() for p in src.rglob('*') if p.is_file() and p.relative_to(src).as_posix() not in ('mimetype','manifest.json')])
    dst.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix='.ostfp-pack-',suffix='.tmp',dir=dst.parent)
    os.close(fd)
    try:
        with zipfile.ZipFile(tmp,'w',allowZip64=True) as z:
            z.write(src/'mimetype','mimetype',compress_type=zipfile.ZIP_STORED)
            z.write(src/'manifest.json','manifest.json',compress_type=zipfile.ZIP_DEFLATED)
            for nm in member_names:z.write(src/nm,nm,compress_type=zipfile.ZIP_DEFLATED)
        validate(pathlib.Path(tmp))
        if dst.exists():raise PackageError('destination appeared during pack')
        os.replace(tmp,dst)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)

def unpack(src:pathlib.Path,dst:pathlib.Path):
    src,dst=pathlib.Path(src),pathlib.Path(dst)
    validate(src)
    if dst.exists():raise PackageError('destination exists')
    dst.parent.mkdir(parents=True,exist_ok=True)
    tmp=pathlib.Path(tempfile.mkdtemp(prefix='.ostfp-unpack-',dir=dst.parent))
    try:
        with zipfile.ZipFile(src) as z:
            for i in z.infolist():
                p=tmp/i.filename
                p.parent.mkdir(parents=True,exist_ok=True)
                with z.open(i) as fi,p.open('xb') as fo:shutil.copyfileobj(fi,fo,CHUNK)
        validate(tmp)
        if dst.exists():raise PackageError('destination appeared during unpack')
        os.replace(tmp,dst)
    finally:
        if tmp.exists():shutil.rmtree(tmp)

def main():
    p=argparse.ArgumentParser(description='OSTF 5.0.0 reference static OSTFP utility; NOT an interoperability certification')
    sub=p.add_subparsers(dest='command',required=True)
    a=sub.add_parser('validate');a.add_argument('source',type=pathlib.Path)
    a=sub.add_parser('pack');a.add_argument('source',type=pathlib.Path);a.add_argument('output',type=pathlib.Path)
    a=sub.add_parser('unpack');a.add_argument('source',type=pathlib.Path);a.add_argument('output',type=pathlib.Path)
    a=p.parse_args()
    try:
        if a.command=='validate':print('Static payload contract accepted:',validate(a.source),'members')
        elif a.command=='pack':pack(a.source,a.output);print('Wrote',a.output)
        elif a.command=='unpack':unpack(a.source,a.output);print('Expanded',a.output)
    except (PackageError,OSError,zipfile.BadZipFile,KeyError,TypeError,ValueError) as exc:
        print('ERROR:',str(exc),file=sys.stderr);raise SystemExit(1)
if __name__=='__main__':main()
