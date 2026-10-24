"""Regenerate every byte and check source/approval/archive/card provenance."""
import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit,unquote
from tools.strategy_catalog.verify import Links
from .core import load_records
from .build import prepare_outputs


def compare_outputs(directory,outputs):
    directory=Path(directory)
    files={str(p.relative_to(directory)) for p in directory.rglob('*') if p.is_file()}
    if files!=set(outputs):raise ValueError('Missing or unexpected delivery files')
    for name,data in outputs.items():
        if (directory/name).read_bytes()!=data:raise ValueError('Output differs from reviewed source: '+name)
    return True


def verify(root):
    root=Path(root).resolve();records,approvals=load_records(root)
    outputs,summary=prepare_outputs(root,records,approvals);out=root/'analysis/top300/optimized'
    compare_outputs(out,outputs);links=0
    for name,payload in outputs.items():
        if not name.endswith('.html'):continue
        parser=Links();parser.feed(payload.decode())
        for href in parser.links:
            url=urlsplit(href)
            if not url.scheme and url.path:
                target=(out/name).parent/unquote(url.path);target=target.resolve()
                if root not in target.parents or not target.is_file():raise ValueError('Invalid local link: '+href)
                links+=1
    return dict(status='PASS',records=len(records),actions=summary['actions'],files=len(outputs),links=links,native_compile=False,backtest=False)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2]);args=parser.parse_args()
    print(json.dumps(verify(args.root),ensure_ascii=False,indent=2))


if __name__=='__main__':main()
