"""One-off: import the 12 Nov 2026 update (application photos, new infographic, brochures).
Usage: python -I tools/prepare_update_assets.py <extracted-folder> <beauty.png>"""
import os, shutil, sys
from PIL import Image

src, beauty = sys.argv[1], sys.argv[2]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, 'assets', 'img')

def save(path, name, width=1400, q=82):
    im = Image.open(path).convert('RGB')
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(os.path.join(IMG, name + '.webp'), 'WEBP', quality=q, method=6)

photos = {
    'Biochar Feeding a Young Seedling.png': 'app-agriculture',
    'pasted-image.png': 'app-poultry',
    'pasted-image-2.png': 'app-hospitality',
    'pasted-image-3.png': 'app-industrial',
    'pasted-image-4.png': 'app-textile',
    'pasted-image-5.png': 'app-food',
    'pasted-image-6.png': 'app-ceramics',
    'pasted-image-7.png': 'app-metallurgy',
    'pasted-image-8.png': 'app-water',
}
for f, n in photos.items():
    save(os.path.join(src, f), n)
save(beauty, 'app-beauty')
save(os.path.join(src, 'Chaargold Charcoal Products Infographic.png'), 'carbon-products', width=1536, q=88)

b = os.path.join(src, 'BROCHURES')
dst = os.path.join(ROOT, 'assets', 'brochures')
for f, n in [('BiochaarGold Brochure 2.pdf', 'biochaargold-brochure.pdf'),
             ('CHAARGOLD_Briquettes_Brochure_v3.pdf', 'chaargold-briquettes-brochure.pdf'),
             ('ChaarGold_Pyrolysis_Kiln_Brochure_v4.pdf', 'chaargold-pyrolysis-kiln-brochure.pdf')]:
    shutil.copyfile(os.path.join(b, f), os.path.join(dst, n))
print('done')
