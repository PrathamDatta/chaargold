"""One-off: pull the 10 RESOURCE articles out of 'Lump Charcoal.docx' into data/blog.json.
Usage: python -I tools/extract_blog.py <text_dir>"""
import sys, os, json, zipfile, re
from xml.etree import ElementTree as ET
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
x = ET.fromstring(zipfile.ZipFile(os.path.join(sys.argv[1], 'Products/Lump Charcoal.docx')).read('word/document.xml'))
arts, cur = [], None
for p in x.iter(W + 'p'):
    st = p.find(W + 'pPr/' + W + 'pStyle'); s = st.get(W + 'val') if st is not None else ''
    t = ''.join(e.text or '' for e in p.iter(W + 't')).strip()
    if not t: continue
    if s == 'Heading1' and t.startswith('RESOURCE '):
        cur = {'no': t, 'title': '', 'body': []}; arts.append(cur); continue
    if cur is None: continue
    if s == 'Heading2' and not cur['title']: cur['title'] = t; continue
    if s == 'Heading2' and cur['title'] and cur['body']:   # next product section begins
        cur = None; continue
    cur['body'].append(['h' if s.startswith('Heading') else 'p', t.replace('contcat@', 'contact@')])
json.dump(arts, open(os.path.join(root, 'data', 'blog.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for a in arts: print(a['no'], a['title'][:70], len(a['body']))
