"""Build-time Markdown projection for the optional Guides reference template."""
from __future__ import annotations

import os
import re
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
# Editorial publication order; prose stays in its existing Markdown source.
GUIDES = [
    ('VirtualDJ Reference', 'Start here'),
    ('Evidence Standards', 'Start here'),
    ('VDJScript Grammar', 'Scripting'),
    ('Skin SDK', 'Skins'),
    ('Skin Waveforms', 'Skins'),
    ('Pad Page XML', 'Pads and controllers'),
    ('Mapper XML', 'Pads and controllers'),
    ('Effects Usage', 'Effects'),
]


# A legacy fragment in Skin SDK predates the current heading spelling.
# Resolve it in the projection without rewriting the authored source.
ANCHOR_ALIASES = {
    ("virtualdj-reference", "visual-type----full-type-reference"): "visual-type--full-type-reference",
}


def slug(text):
    return re.sub(r'[^\w\- ]', '', text.lower()).replace(' ', '-')


def route(doc_id, anchor=''):
    return '#docs/' + quote(doc_id) + ('/' + quote(anchor) if anchor else '')


def guide_records(out):
    try:
        from markdown_it import MarkdownIt
    except ImportError:
        raise SystemExit('Guides need markdown-it-py; run `just install`.')
    md = MarkdownIt('commonmark', {'html': False}).enable('table').enable('strikethrough')
    paths = {ROOT / 'docs' / (title + '.md'): slug(title) for title, _ in GUIDES}
    records = []
    for title, category in GUIDES:
        source = ROOT / 'docs' / (title + '.md')
        doc_id = paths[source]
        tokens = md.parse(source.read_text())
        headings, seen = [], set()
        for i, token in enumerate(tokens):
            if token.type != 'heading_open':
                continue
            inline = tokens[i + 1]
            text = ''.join(t.content for t in inline.children or [] if t.type in ('text', 'code_inline'))
            base, anchor, n = slug(text), slug(text), 0
            while anchor in seen:
                n += 1
                anchor = f'{base}-{n}'
            seen.add(anchor)
            token.attrSet('id', anchor)
            headings.append({'title': text, 'id': anchor, 'level': int(token.tag[1:]),
                             'line': token.map[0] + 1})
        def rewrite(url):
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc:
                return url
            target = (source.parent / unquote(parsed.path)).resolve() if parsed.path else source
            if target in paths:
                anchor = unquote(parsed.fragment)
                anchor = ANCHOR_ALIASES.get((paths[target], anchor), anchor)
                return route(paths[target], anchor)
            return quote(os.path.relpath(target, out.resolve().parent)) + (
                '#' + quote(unquote(parsed.fragment)) if parsed.fragment else '')
        # Raw HTML is escaped. Keep explicit Markdown anchor aliases as safe spans.
        for token in tokens:
            for child in token.children or []:
                if child.type == 'link_open':
                    child.attrSet('href', rewrite(child.attrGet('href')))
                elif child.type == 'image':
                    child.attrSet('src', rewrite(child.attrGet('src')))
                elif child.type == 'text':
                    match = re.fullmatch(r'<a id="([\w-]+)"></a>', child.content)
                    if match:
                        child.type = 'html_inline'
                        child.content = '<span id="' + match[1] + '"></span>'
        # Search each heading's own content, keeping the precise destination.
        lines = source.read_text().splitlines()
        for i, h in enumerate(headings):
            end = headings[i + 1]['line'] - 1 if i + 1 < len(headings) else len(lines)
            h['text'] = '\n'.join(lines[h['line']:end])
        records.append({'name': title, 'id': doc_id, 'section': category,
                        'description': next((t.content for t in tokens if t.type == 'inline' and t.level == 1 and t.content != title), ''),
                        'kind': 'Guide', 'status': 'unverified', 'statusLabel': 'Provenance is recorded within the guide',
                        'source': str(source.relative_to(ROOT)),
                        'sourceUrl': quote(os.path.relpath(source, out.resolve().parent)),
                        'html': md.renderer.render(tokens, md.options, {}), 'headings': headings})
    return records


def connect_skin_docs(skins, guides):
    by_path = {g['source']: g for g in guides}
    for skin in skins:
        for doc in skin['docs']:
            guide = by_path.get(doc['doc'])
            if guide:
                heading = next((h for h in guide['headings'] if h['line'] == doc['line']), None)
                doc['url'] = route(guide['id'], heading['id'] if heading else '')
