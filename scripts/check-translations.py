#!/usr/bin/env python3
"""Guard paired content; --record attests that both editions were reviewed."""
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'translations.json'


def snapshots():
    pages = {lang: {str(p.relative_to(ROOT / lang)): p for p in (ROOT / lang).rglob('*.qmd')} for lang in ('en', 'zh')}
    if not pages['en'] or pages['en'].keys() != pages['zh'].keys():
        raise ValueError('Missing paired pages: ' + str(sorted(pages['en'].keys() ^ pages['zh'].keys())))
    result = {}
    for name in sorted(pages['en']):
        texts = {lang: pages[lang][name].read_text() for lang in pages}
        # Display equations, labels, and numerical code must agree exactly.
        for pattern, label in [(r'\$\$.*?\$\$', 'display equations'), (r'(?<!\$)\$(?!\$)([^\n$]+)(?<!\$)\$(?!\$)', 'inline equations'), (r'```.*?```', 'code'), (r'^(?:date: .*|.*\{#(?:eq|prp|thm|lem)-[^}]+\}.*)$', 'dates and theorem labels')]:
            if re.findall(pattern, texts['en'], re.S if label != 'dates and theorem labels' else re.M) != re.findall(pattern, texts['zh'], re.S if label != 'dates and theorem labels' else re.M):
                raise ValueError(f'{name}: mismatched {label}')
        result[name] = {lang: hashlib.sha256(texts[lang].encode()).hexdigest() for lang in pages}
    return result


def main():
    current = snapshots()
    previous = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    if sys.argv[1:] == ['--record']:
        for name, hashes in current.items():
            if name in previous:
                changed = [lang for lang in hashes if hashes[lang] != previous[name][lang]]
                if len(changed) == 1:
                    raise ValueError(f'{name}: only {changed[0]} changed; update and review its translation before recording')
        MANIFEST.write_text(json.dumps(current, indent=2, ensure_ascii=False) + '\n')
        print(f'Recorded {len(current)} reviewed translation pairs.')
    elif sys.argv[1:]:
        raise ValueError('Usage: python3 scripts/check-translations.py [--record]')
    elif current != previous:
        changed = sorted(k for k in current.keys() | previous.keys() if current.get(k) != previous.get(k))
        raise ValueError('Unreviewed translation changes: ' + ', '.join(changed) + '. Update both editions, review, then run with --record.')
    else:
        print(f'PASS: {len(current)} translation pairs, reviewed hashes, equations, code, dates, and labels.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError) as error:
        sys.exit(str(error))
