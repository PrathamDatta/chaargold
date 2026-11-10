"""One-off (round 2): import the client's NEW PICS and cut a flame-only logo icon.
Usage: python -I tools/prepare_new_assets.py <NEW PICS dir> <CHAARGOLD logo png>"""
import os, sys
from PIL import Image, ImageChops
Image.MAX_IMAGE_PIXELS = None
pics, logo = sys.argv[1], sys.argv[2]
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'img')

def save(src, name, w, q=82, alpha=False):
    # some macOS screenshot names contain a narrow no-break space, so match on the exact name or its prefix
    path = os.path.join(pics, src)
    if not os.path.exists(path):
        stem = src.rsplit(' ', 1)[0]
        path = os.path.join(pics, next(f for f in os.listdir(pics) if f.startswith(stem)))
    im = Image.open(path).convert('RGBA' if alpha else 'RGB')
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(os.path.join(out, name + '.webp'), 'WEBP', quality=q, method=6)
    print(name, im.size)

save('WhatsApp Image 2026-11-04 at 11.01.54.jpeg', 'hero-coals', 1400)
save('Industrial Plant with Yellow Ducts.png', 'plant-yellow-ducts', 900)
save('GOLDFLAME_text_flameA_for_light_bg_transparent.png', 'goldflame-light', 1200, 92, alpha=True)
save('Premium Wood Vinegar Bottle.png', 'wood-vinegar-bottle', 700)
save('Chaargold Carbon Products Infographic.png', 'carbon-products', 1400)
save('Biomass Options Infographic.png', 'biomass-options', 1500)
save('Chaargold’s 5-Step Charcoal Journey.png', 'five-step-journey', 1500)
save('GoldFlame Briquette Charcoal Stove.png', 'goldflame-stove', 1100)
save('Chaargold Wood Vinegar Product Display.png', 'wood-vinegar-display', 1400)
save('Viscous Black Liquid Pouring into Drum.png', 'gallery-coal-tar', 1100)
save('Screenshot 2026-11-09 at 11.15.33 PM.png', 'gallery-coconut-loading', 1400)
save('Charcoal Kiln Workshop and Basket.png', 'gallery-coconut-unloading', 1100)
save('Charcoal-Filled Wire Cage in Industrial Yard.png', 'gallery-charcoal-unloading', 1100)
save('Open Box of Charcoal Briquettes.png', 'gallery-packed', 1400)
save('Charcoal Briquettes Drying in a Polytunnel.png', 'gallery-pillow-drying', 1100)
save('Screenshot 2026-11-09 at 11.47.27 PM.png', 'gallery-lump', 1100)
save('Bamboo Yard Under Clear Skies.png', 'gallery-bamboo', 1400)

# Flame-only logo icon: drop the wordmark below the flame and make white transparent
im = Image.open(logo).convert('RGB')
bg = Image.new('RGB', im.size, 'white')
mask = ImageChops.difference(im, bg).convert('L').point(lambda v: 255 if v > 24 else 0)
rows = [mask.crop((0, y, im.width, y + 1)).getbbox() is not None for y in range(im.height)]
# first block of non-empty rows = flame (wordmark follows after a blank gap)
y0 = next(i for i, r in enumerate(rows) if r); y = y0
while y < im.height and (rows[y] or any(rows[y:y + 25])): y += 1
flame = im.crop((0, y0, im.width, y))
flame = flame.crop(ImageChops.difference(flame, Image.new('RGB', flame.size, 'white')).getbbox())
a = flame.point(lambda v: v)  # keep colour
alpha = Image.eval(ImageChops.invert(flame.convert('L')), lambda v: min(255, int(v * 2.2)))
rgba = flame.convert('RGBA'); rgba.putalpha(alpha)
pad = 12; canvas = Image.new('RGBA', (rgba.width + 2 * pad, rgba.height + 2 * pad), (0, 0, 0, 0)); canvas.paste(rgba, (pad, pad))
canvas.thumbnail((360, 360), Image.LANCZOS)
canvas.save(os.path.join(out, 'logo-icon.webp'), 'WEBP', quality=92, method=6)
print('logo-icon', canvas.size)
