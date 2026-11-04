"""One-off: optimise source images from the client's zips into assets/img (WebP) and
extract FAQ / Terms text from the docx files into data/*.json.
Usage: python -I tools/prepare_assets.py <pictures_dir> <text_dir>"""
import sys, io, os, json, zipfile
from xml.etree import ElementTree as ET
from PIL import Image, ImageChops
Image.MAX_IMAGE_PIXELS = None
pics, text = sys.argv[1], sys.argv[2]
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.join(root, 'assets', 'img')

def media(docx, name):
    return Image.open(io.BytesIO(zipfile.ZipFile(os.path.join(text, docx)).read('word/media/' + name)))

def save(im, name, w, q=82, crop_white=False):
    im = im.convert('RGBA') if name.startswith('logo') else im.convert('RGB')
    if crop_white:
        bg = Image.new('RGB', im.size, 'white')
        bbox = ImageChops.difference(im.convert('RGB'), bg).getbbox()
        if bbox:
            p = 20; im = im.crop((max(0,bbox[0]-p), max(0,bbox[1]-p), bbox[2]+p, bbox[3]+p))
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(os.path.join(out, name + '.webp'), 'WEBP', quality=q, method=6)
    print(name, im.size)

P = lambda f: Image.open(os.path.join(pics, f))
save(P('LOGOS/CHAARGOLD.png'), 'logo-chaargold', 700, 90, True)
save(P('LOGOS/LOGO BIOCHAARGOLD.png'), 'logo-biochaargold', 700, 90, True)
save(P('KILNS 2.png'), 'kilns-hero', 1800)
save(media('Products/Pyrolysis Kilns & Retort Systems.docx', 'image2.png'), 'kiln-gantry', 1400)
save(media('Products/Pyrolysis Kilns & Retort Systems.docx', 'image1.png'), 'kiln-row', 1400)
save(media('Products/Lump Charcoal.docx', 'image1.png'), 'lump-charcoal', 1000)
save(media('Products/Hexagonal Briquettes.docx', 'image1.png'), 'hexagonal-briquettes', 1000)
save(media('Products/Pillow Briquettes.docx', 'image1.png'), 'pillow-briquettes', 1000)
save(media('Products/Honeycomb Briquettes.docx', 'image2.jpeg'), 'honeycomb-briquettes', 800)
save(media('Products/BIOCHAARGOLD.docx', 'image2.png'), 'biochar-bag', 1000)
save(media('Products/BIOCHAARGOLD.docx', 'image3.png'), 'biochar-infographic', 1200)
save(media('Products/BIOCHAARGOLD.docx', 'image5.png'), 'biochar-pallets', 1400)
save(media('Products/Wood Vineger.docx', 'image1.png'), 'wood-vinegar', 1000)
save(media('Products/Charcoal Briquette Stoves.docx', 'image1.png'), 'goldflame-logo', 1400, 90)
save(media('Sustainability.docx', 'image1.png'), 'sustainability-banner', 2000)
save(media('Home.docx', 'image3.png'), 'bamboo-charcoal', 1400)
save(media('Home.docx', 'image2.png'), 'waste-to-value', 900)
save(P('ChatGPT Image Jul 10, 2026, 04_41_05 PM.png'), 'biochar-cycle', 1000)
save(P('ChatGPT Image Jul 9, 2026, 04_42_56 PM.png'), 'power-of-biochar', 1000)
save(media('Gallery.docx', 'image1.jpeg'), 'gallery-biochar-2026', 1600)
save(media('Gallery.docx', 'image2.jpeg'), 'gallery-honeycomb', 1400)
save(media('Gallery.docx', 'image3.png'), 'gallery-kilns', 1400)
save(media('Gallery.docx', 'image4.png'), 'gallery-drying', 1400)
save(media('About-Us.docx', 'image3.png'), 'team-prem', 700)
save(media('About-Us.docx', 'image4.jpeg'), 'team-namratha', 700)
save(media('About-Us.docx', 'image5.png'), 'team-malathi', 700)
save(media('About-Us.docx', 'image6.jpeg'), 'team-deepika', 700)

# ---- text
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
def paras(f):
    root_ = ET.fromstring(zipfile.ZipFile(os.path.join(text, f)).read('word/document.xml'))
    res = []
    for p in root_.iter(W + 'p'):
        st = p.find(W + 'pPr/' + W + 'pStyle')
        s = st.get(W + 'val') if st is not None else ''
        t = ''.join(x.text or '' for x in p.iter(W + 't')).strip()
        if t: res.append([s, t])
    return res
json.dump(paras('Frequently Asked Questions.docx'), open(os.path.join(root, 'data', 'faq.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(paras('terms.docx'), open(os.path.join(root, 'data', 'terms.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
