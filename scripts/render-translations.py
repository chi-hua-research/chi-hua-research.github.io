#!/usr/bin/env python3
"""Render isolated locale sites and retain all original English URLs."""
import html
import os
from pathlib import Path
import shutil
import subprocess

root = Path(__file__).resolve().parents[1]
quarto = os.environ.get('QUARTO_PATH') or shutil.which('quarto')
if not quarto:
    raise SystemExit('Quarto must be available on PATH.')
for lang in ('en', 'zh'):
    subprocess.run([quarto, 'render', str(root / lang)], cwd=root / lang, check=True)
for lang in ('en', 'zh'):
    shutil.copy(root / 'styles.css', root / '_site' / lang / 'styles.css')
    shutil.copytree(root / 'assets', root / '_site' / lang / 'assets', dirs_exist_ok=True)
# Existing bookmarked article, listing, and about URLs continue to resolve.
for source in (root / 'en').rglob('*.qmd'):
    relative = source.relative_to(root / 'en').with_suffix('.html')
    if str(relative) == 'index.html':
        continue
    target = '/en/' + relative.as_posix()
    dest = root / '_site' / relative
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url={html.escape(target)}"><link rel="canonical" href="https://chi-hua-research.github.io{html.escape(target)}"><title>Page moved</title></head><body><a href="{html.escape(target)}">Continue to the English edition</a></body></html>')
print('Rendered both locales and preserved original English page URLs.')
