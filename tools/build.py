"""Static site generator for chaargold.com.
Run from the project root:  python tools/build.py
Writes the .html pages, sitemap.xml and robots.txt next to this folder's parent.
Content lives in this file (hand-written pages) and data/*.json (FAQ, Terms, Blog)."""
import json, os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = 'https://chaargold.com'
EMAIL = 'contact@chaargold.com'
PHONE = '+91 81052 70415'
PHONE_RAW = '918105270415'
INSTAGRAM = '#'   # TODO: paste Instagram profile URL
FACEBOOK = '#'    # TODO: paste Facebook page URL
VER = '2'
FORM_ENDPOINT = ''   # e.g. https://formspree.io/f/xxxxxxx  (leave empty to fall back to email)
FORM_KEY = ''        # only for Web3Forms-style services (access key)

def esc(s): return html.escape(s, quote=False)
def load(n): return json.load(open(os.path.join(ROOT, 'data', n), encoding='utf-8'))

# ------------------------------------------------------------------ icons
_I = {
 'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
 'phone': '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
 'pin': '<path d="M12 21s-7-6.2-7-11a7 7 0 1 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
 'flame': '<path d="M12 3c1 3.5 5 5.5 5 10a5 5 0 0 1-10 0c0-2 1-3 2-4 .5 1.5 1.5 2 2 2 0-3-1-5 1-8z"/>',
 'leaf': '<path d="M5 19C4 11 9 5 20 4c0 11-5 16-13 16"/><path d="M5 19c3-5 6-8 10-10"/>',
 'drop': '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>',
 'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
 'bolt': '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
 'gear': '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/>',
 'wallet': '<path d="M3 7a2 2 0 0 1 2-2h13v4"/><rect x="3" y="7" width="18" height="13" rx="2"/><circle cx="16.5" cy="13.5" r="1.2"/>',
 'chef': '<path d="M7 14a4 4 0 1 1 2-7.5 4 4 0 0 1 6 0A4 4 0 1 1 17 14v5H7z"/><path d="M7 17h10"/>',
 'factory': '<path d="M3 21V10l6 4v-4l6 4V5h4v16z"/>',
 'recycle': '<path d="M21 12a9 9 0 0 1-15.5 6.2M3 12a9 9 0 0 1 15.5-6.2"/><path d="M18.5 2v4h-4M5.5 22v-4h4"/>',
 'flask': '<path d="M9 3h6M10 3v6L4.5 19a1.5 1.5 0 0 0 1.3 2h12.4a1.5 1.5 0 0 0 1.3-2L14 9V3"/>',
 'tree': '<path d="M12 22v-6"/><path d="M12 16c-4 0-6-2-6-5 0-2 1-3 2-4 0-3 2-5 4-5s4 2 4 5c1 1 2 2 2 4 0 3-2 5-6 5z"/>',
 'target': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
 'eye': '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 'diamond': '<path d="M6 3h12l4 6-10 12L2 9z"/><path d="M2 9h20M9 3l3 6 3-6M12 21 9 9m6 0-3 12"/>',
 'bulb': '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5c1 1 1 2 1 3h6c0-1 0-2 1-3A6 6 0 0 0 12 3z"/>',
 'award': '<circle cx="12" cy="9" r="6"/><path d="m8.5 14.5-1.5 7 5-3 5 3-1.5-7"/>',
 'users': '<circle cx="9" cy="8" r="3.5"/><path d="M2 20c0-4 3-6 7-6s7 2 7 6M16 4.5a3.5 3.5 0 0 1 0 7M18 14c2.5.6 4 2.5 4 6"/>',
 'instagram': '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8" fill="currentColor"/>',
 'facebook': '<path d="M14 8h3V4h-3a4 4 0 0 0-4 4v3H7v4h3v6h4v-6h3l1-4h-4V8.5A.5.5 0 0 1 14 8z"/>',
 'whatsapp': '<path d="M3 21l1.6-4.8A9 9 0 1 1 8 19.5z"/><path d="M9 9c0 3 3 6 6 6l1.5-1.5-2-1-1 .8c-1-.4-2-1.4-2.4-2.4l.8-1-1-2z"/>',
 'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
 'download': '<path d="M12 3v12m0 0-4-4m4 4 4-4M4 20h16"/>',
 'shield': '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/>',
 'chart': '<path d="M4 20V10M10 20V4M16 20v-8M22 20H2"/>',
 'box': '<path d="M3 8l9-5 9 5v8l-9 5-9-5z"/><path d="M3 8l9 5 9-5M12 13v8"/>',
 'refresh': '<path d="M20 11a8 8 0 0 0-14-4M4 13a8 8 0 0 0 14 4"/><path d="M20 4v5h-5M4 20v-5h5"/>',
 'pot': '<path d="M4 11h16v5a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4zM9 7c0-1.5 1-1.5 1-3M14 7c0-1.5 1-1.5 1-3M2 11h20"/>',
 'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/>',
 'bug': '<ellipse cx="12" cy="14" rx="4" ry="6"/><path d="M9 5l2 3M15 5l-2 3M3 12h5M16 12h5M4 19l4-2M20 19l-4-2"/>',
 'wind': '<path d="M3 8h11a3 3 0 1 0-3-3M3 12h16a3 3 0 1 1-3 3M3 16h7"/>',
}
def icon(n, cls=''):
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" class="%s">%s</svg>' % (cls, _I[n])

# ------------------------------------------------------------------ data
PRODUCTS = [
 dict(slug='lump-charcoal', name='Lump Charcoal', img='lump-charcoal', tag='Fuel',
      short='Premium natural fuel with high fixed carbon, superior heat output and a clean burn.'),
 dict(slug='hexagonal-briquettes', name='Hexagonal Briquettes', img='hexagonal-briquettes', tag='Briquettes',
      short='The world standard for grilling and hookah — even heat, long burn, consistent ash.'),
 dict(slug='pillow-briquettes', name='Pillow Briquettes', img='pillow-briquettes', tag='Briquettes',
      short='Compact, uniform and long-burning — engineered to stack well and burn longer.'),
 dict(slug='honeycomb-briquettes', name='Honeycomb Briquettes', img='honeycomb-briquettes', tag='Briquettes',
      short='Air channels through the core for fast ignition and steady, even heat.'),
 dict(slug='biochar', name='BIOCHAARGOLD Premium Biochar', img='biochar-bag', tag='Biochar',
      short='Engineered biochar to heal soils, lock carbon for centuries and strengthen agriculture.'),
 dict(slug='pyrolysis-kilns', name='Pyrolysis Kilns & Retort Systems', img='kiln-row', tag='Equipment', fill=True,
      short='In-house engineered kilns and turnkey plants for charcoal and biochar production.'),
 dict(slug='goldflame-stoves', name='GoldFlame Charcoal Briquette Stoves', img='goldflame-logo', tag='Stoves', dark=True,
      short='Signature stoves for everyday, grilling and tandoor-style cooking on briquettes.'),
 dict(slug='wood-vinegar', name='Wood Vinegar', img='wood-vinegar', tag='By-product',
      short="Nature's liquid solution for sustainable agriculture — pyroligneous acid from our kilns."),
]
P = {p['slug']: p for p in PRODUCTS}

NAV = [('index.html', 'Home'), ('about.html', 'About Us'), ('products/index.html', 'Products'),
       ('biochaargold.html', 'BIOCHAARGOLD'), ('blog.html', 'Blog'), ('gallery.html', 'Gallery'),
       ('sustainability.html', 'Sustainability'), ('contact.html', 'Contact Us')]

PAGES = []   # (path, priority)

# ------------------------------------------------------------------ layout
def layout(path, title, desc, body, og_img='logo-chaargold', schema=''):
    base = '../' if '/' in path else ''
    cur = path
    def cls(p):
        return ' aria-current="page"' if (p == cur or (p == 'products/index.html' and cur.startswith('products/'))) else ''
    nav = []
    for p, n in NAV:
        if p == 'products/index.html':
            items = ''.join('<a href="%sproducts/%s.html">%s</a>' % (base, x['slug'], esc(x['name'])) for x in PRODUCTS)
            nav.append('<div class="dd%s"><button type="button" aria-expanded="false" aria-haspopup="true">Products %s</button><div class="dd-menu">%s<div class="sep"></div><a href="%sproducts/index.html"><b>View all products →</b></a></div></div>'
                       % (' current' if cur.startswith('products/') else '', '<svg width="10" height="10" viewBox="0 0 10 10" aria-hidden="true"><path d="M1 3l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>', items, base))
        else:
            nav.append('<a href="%s%s"%s>%s</a>' % (base, p, cls(p), n))
    nav = ''.join(nav)
    foot_products = ''.join('<li><a href="%sproducts/%s.html">%s</a></li>' % (base, x['slug'], esc(x['name'])) for x in PRODUCTS)
    form_meta = ('<meta name="form-endpoint" content="%s">' % FORM_ENDPOINT + ('<meta name="form-key" content="%s">' % FORM_KEY if FORM_KEY else '')) if FORM_ENDPOINT else ''
    full_title = title if title.startswith('ChaarGold') else title + ' | ChaarGold'
    url = DOMAIN + '/' + (path if path != 'index.html' else '')
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#bc9c23">{form_meta}
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="ChaarGold">
<meta property="og:title" content="{html.escape(full_title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{DOMAIN}/assets/img/{og_img}.webp">
<link rel="icon" href="{base}assets/img/logo-chaargold.webp" type="image/webp">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/css/style.css?v={VER}">
{schema}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap">
  <div class="tb-left"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="tel:+{PHONE_RAW}">{PHONE}</a></div>
  <div class="tb-right">Bengaluru, Karnataka · Manufacturing in Penukonda, Andhra Pradesh</div>
</div></div>
<header class="header"><div class="wrap">
  <a class="brand" href="{base}index.html" aria-label="ChaarGold home"><img src="{base}assets/img/logo-chaargold.webp" alt="ChaarGold — Crafting Carbon Perfection" width="60" height="56"></a>
  <button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
  <nav class="nav" id="nav" aria-label="Main">{nav}<span class="nav-cta"><a class="btn btn-dark" href="{base}contact.html#enquiry">Get a Quote</a></span></nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="footer"><div class="wrap">
  <div class="f-grid">
    <div class="f-brand"><img src="{base}assets/img/logo-chaargold.webp" alt="ChaarGold" width="90" height="84" loading="lazy">
      <p>Turning biomass into black gold. Charcoal briquettes, biochar, wood vinegar and turnkey pyrolysis solutions — engineered in India.</p>
      <div class="social"><a href="{INSTAGRAM}" aria-label="Instagram">{icon('instagram')}</a><a href="{FACEBOOK}" aria-label="Facebook">{icon('facebook')}</a><a href="https://wa.me/{PHONE_RAW}" aria-label="WhatsApp">{icon('whatsapp')}</a></div></div>
    <div><h4>Company</h4><ul><li><a href="{base}index.html">Home</a></li><li><a href="{base}about.html">About Us</a></li><li><a href="{base}biochaargold.html">BIOCHAARGOLD</a></li><li><a href="{base}sustainability.html">Sustainability</a></li><li><a href="{base}blog.html">Blog</a></li><li><a href="{base}gallery.html">Gallery</a></li><li><a href="{base}contact.html">Contact Us</a></li></ul></div>
    <div><h4>Products</h4><ul>{foot_products}</ul></div>
    <div><h4>Get in touch</h4><ul>
      <li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="tel:+{PHONE_RAW}">{PHONE}</a></li>
      <li>Head office: Bengaluru, Karnataka</li><li>Plant: Penukonda, Andhra Pradesh</li>
      <li><a href="{base}faq.html">FAQ</a> · <a href="{base}terms.html">Terms</a></li></ul></div>
  </div>
  <div class="f-bottom"><span>© 2026 CHAARGOLD. All rights reserved.</span><span>Crafting Carbon Perfection.</span></div>
</div></footer>
<script src="{base}assets/js/main.js?v={VER}" defer></script>
</body>
</html>'''

def write(path, title, desc, body, prio='0.7', **kw):
    out = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8', newline='\n').write(layout(path, title, desc, body, **kw))
    PAGES.append((path, prio))

# ------------------------------------------------------------------ components
def img(name, alt, base, cls='', w=None, h=None, lazy=True):
    return '<img src="%sassets/img/%s.webp" alt="%s"%s%s%s%s>' % (base, name, html.escape(alt), ' class="%s"' % cls if cls else '',
        ' width="%d"' % w if w else '', ' height="%d"' % h if h else '', ' loading="lazy" decoding="async"' if lazy else '')

def crumbs(items, base):
    out = ['<a href="%sindex.html">Home</a>' % base]
    for href, name in items:
        out.append('<a href="%s%s">%s</a>' % (base, href, name) if href else esc(name))
    return '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % '<span>/</span>'.join(out)

def checks(items, cols=False):
    return '<ul class="checks%s">%s</ul>' % (' cols' if cols else '', ''.join('<li>%s</li>' % esc(i) for i in items))

def chips(items): return '<ul class="chips">%s</ul>' % ''.join('<li>%s</li>' % esc(i) for i in items)

def table(rows, head=('Parameter', 'Typical Value'), cls=''):
    h = ''.join('<th scope="col">%s</th>' % esc(x) for x in head)
    b = ''.join('<tr><th scope="row">%s</th>%s</tr>' % (esc(r[0]), ''.join('<td>%s</td>' % esc(c) for c in r[1:])) for r in rows)
    return '<div class="table-wrap"><table class="spec %s"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (cls, h, b)

def head(eyebrow, title, lead='', center=False):
    return '<div class="section-head%s reveal"><span class="eyebrow">%s</span><h2>%s</h2>%s</div>' % (' center' if center else '', eyebrow, title, '<p class="lead">%s</p>' % lead if lead else '')

def field(label, name, typ='text', req=False, ph=''):
    return '<div class="field"><label for="{n}">{l}{r}</label><input id="{n}" name="{n}" data-label="{l}" type="{t}"{q}{p}></div>'.format(
        n=name, l=label, t=typ, r=' <i>*</i>' if req else '', q=' required' if req else '', p=' placeholder="%s"' % ph if ph else '')

def uid(prefix, name): return '%s-%s' % (prefix, name)

def quote_form(pre, selected=''):
    opts = ''.join('<label class="opt"><input type="checkbox" name="products" data-label="Products of interest" value="%s"%s> %s</label>' %
                   (html.escape(n), ' checked' if n == selected else '', esc(n)) for n in
                   ['Lump Charcoal', 'Hexagonal Briquettes', 'Pillow Briquettes', 'Honeycomb Briquettes', 'Biochar', 'Wood Vinegar', 'Charcoal Briquette Stoves', 'Pyrolysis Kilns & Retort Systems'])
    return f'''<form class="form" data-enquiry data-subject="Quote request — ChaarGold website" novalidate>
  <fieldset class="field"><legend>Products of interest <small>(select all that apply)</small></legend><div class="opts">{opts}</div></fieldset>
  <div class="row">{field('Name', pre + 'name', req=True)}{field('Company Name', pre + 'company')}</div>
  <div class="row">{field('Email Address', pre + 'email', 'email')}{field('Phone Number', pre + 'phone', 'tel', True)}</div>
  <div class="field"><label for="{pre}msg">Tell us about your requirement</label><textarea id="{pre}msg" name="message" data-label="Requirement"></textarea></div>
  <div><button class="btn btn-gold" type="submit">Submit {icon('arrow')}</button></div>
  <p class="form-msg" role="status">Thank you — your email app should have opened with your request. If it didn't, write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</form>'''

def callback_form(pre):
    return f'''<form class="form" data-enquiry data-subject="Call back request — ChaarGold website">
  <div class="row">{field('Name', pre + 'name', req=True)}{field('Contact Number', pre + 'phone', 'tel', True)}</div>
  <div><button class="btn btn-dark" type="submit">Request a Call Back</button></div>
  <p class="form-msg" role="status">Thanks — we'll call you back shortly.</p>
</form>'''

def partner_form(pre):
    return f'''<form class="form" data-enquiry data-subject="Distributor application — ChaarGold website">
  <div class="row">{field('Full Name', pre + 'name', req=True)}{field('Company Name', pre + 'company')}</div>
  <div class="row">{field('Country / State', pre + 'region')}{field('Phone Number', pre + 'phone', 'tel', True)}</div>
  {field('Email Address', pre + 'email', 'email')}
  <div class="field"><label for="{pre}msg">Tell us about your interest</label><textarea id="{pre}msg" name="message" data-label="Interest"></textarea></div>
  <div><button class="btn btn-gold" type="submit">Submit application {icon('arrow')}</button></div>
  <p class="form-msg" role="status">Thank you — we'll be in touch about the partnership.</p>
</form>'''

def enquiry_section(product='', noun='charcoal'):
    base = '../'
    return f'''<section class="section bg-cream" id="enquire">
<div class="wrap">
  {head('Work with us', 'Let’s fuel growth together', 'Get a customised quotation, speak with a specialist or join our distribution network.')}
  <div data-tabs><div class="tabs" role="tablist" aria-label="Enquiry type">
    <button role="tab" type="button" aria-selected="true" aria-controls="quote" id="t-quote">Request a Quote</button>
    <button role="tab" type="button" aria-selected="false" aria-controls="team" id="t-team">Connect with Our Team</button>
    <button role="tab" type="button" aria-selected="false" aria-controls="partner" id="t-partner">Become a Distribution Partner</button>
  </div></div>
  <div class="tabpanel" role="tabpanel" id="quote" aria-labelledby="t-quote">
    <div class="split top">
      <div><h3>Request a Quote</h3><p>Please select all products you are interested in purchasing or learning more about. Our team will review your requirements and get back to you with a customised quotation.</p>
      <p>Whether you are looking for a one-time purchase, regular supply, or customised solutions, ChaarGold is here to help. Share your requirements with us, and we’ll work with you to find the right solution.</p></div>
      <div class="form-box">{quote_form('q-', product)}</div>
    </div>
  </div>
  <div class="tabpanel" role="tabpanel" id="team" aria-labelledby="t-team" hidden>
    <div class="split top">
      <div><h3>Connect with Our Team</h3><p>Connect with our specialists to discuss your {noun} requirements and discover the CHAARGOLD difference.</p>
        <div class="grid" style="margin-top:20px">
          <div class="contact-card"><span class="ico">{icon('whatsapp')}</span><div><h3>Call / WhatsApp</h3><a href="tel:+{PHONE_RAW}">{PHONE}</a></div></div>
          <div class="contact-card"><span class="ico">{icon('mail')}</span><div><h3>Email</h3><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
        </div></div>
      <div class="form-box"><h3>Request a Call Back</h3><p>Whether you’re looking for premium charcoal briquettes, premium biochar, or setting up your own Charcoal Pyrolysis Kilns Plant, our team is ready to assist.</p>{callback_form('c-')}</div>
    </div>
  </div>
  <div class="tabpanel" role="tabpanel" id="partner" aria-labelledby="t-partner" hidden>
    <div class="split top">
      <div><span class="eyebrow">Grow with CHAARGOLD</span><h3>Become a Distribution Partner</h3>
        <p>Join our expanding network of distributors and partners delivering premium {noun} solutions to hospitality businesses, industrial users, retailers, and international markets.</p>
        <p>As a ChaarGold Distribution Partner, you will gain access to high-quality charcoal products, dependable supply chains, competitive margins, and dedicated business support designed to help you grow your market presence.</p>
        <h4>Partner benefits</h4>
        {checks(['Exclusive regional opportunities','Competitive pricing and attractive margins','Consistent product quality','Reliable bulk supply capabilities','Marketing and branding support','Export-ready products and packaging','Long-term growth partnerships','Dedicated account and technical support'])}
        <p style="margin-top:1.2rem">Partner with CHAARGOLD to deliver premium charcoal solutions backed by quality, reliability, and performance.</p></div>
      <div class="form-box"><h3>Distributor Application Form</h3>{partner_form('p-')}</div>
    </div>
  </div>
</div></section>'''

def cta_trio(cls=''):
    return f'''<div class="cta-trio"><a class="btn btn-gold" href="#quote">Request a Quote</a><a class="btn btn-line" href="#team">Connect with Our Team</a><a class="btn btn-line" href="#partner">Become a Distribution Partner</a></div>'''

def more_products(exclude):
    cards = ''.join(pcard(x, '../') for x in PRODUCTS if x['slug'] != exclude)
    return f'<section class="section"><div class="wrap">{head("Explore", "More from ChaarGold")}<div class="grid g4">{cards[:]}</div></div></section>'.replace('<div class="grid g4">', '<div class="grid g4 more">')

def pcard(p, base, products_dir=False):
    href = ('' if products_dir else base + 'products/') + p['slug'] + '.html'
    fill = ' fill' if p.get('fill') else ''
    style = ' style="background:#040404"' if p.get('dark') else ''
    return f'''<a class="pcard reveal" href="{href}"><div class="pimg{fill}"{style}>{img(p['img'], p['name'], base)}</div><div class="pbody"><span class="tag">{p['tag']}</span><h3>{esc(p['name'])}</h3><p>{esc(p['short'])}</p><span class="more">Learn more {icon('arrow')}</span></div></a>'''

def cta_band(title, text, base, extra=''):
    return f'''<section class="section tight"><div class="wrap"><div class="cta-band reveal"><span class="eyebrow">Ready to partner?</span><h2>{title}</h2><p>{text}</p>
<div class="btn-row"><a class="btn btn-gold" href="{base}contact.html#enquiry">Get a Quote</a><a class="btn btn-line" href="{base}products/index.html">View all products</a>{extra}</div></div></div></section>'''

def stats_row():
    items = [(8, '+', 'Years of Excellence'), (100, '+', 'Kilns Installed'), (3200, '+', 'Tonnes Manufactured'), (120, '+', 'Satisfied Clients')]
    return '<div class="stats">%s</div>' % ''.join('<div class="stat"><b data-count="%d" data-suffix="%s">%d%s</b><span>%s</span></div>' % (n, s, n, s, l) for n, s, l in items)

# ------------------------------------------------------------------ product pages
def product_page(slug, eyebrow, lead, intro, features, apps, extra_after='', extra_before='', brochure=None, noun='charcoal',
                 title=None, desc='', img_mode='', img_name=None, hero_extra='', spec_note=True):
    p = P[slug]; base = '../'
    title = title or p['name']
    media = img(img_name or p['img'], p['name'], base, lazy=False)
    broch = ''
    if brochure:
        broch = f'<a class="btn btn-line" href="{base}assets/brochures/{brochure}" download>{icon("download")} Brochure (PDF)</a>'
    app_html = ''
    if apps:
        if isinstance(apps[0], str): apps = [('Applications', apps)]
        app_html = ''.join('<div class="app-group"><h3>%s</h3>%s</div>' % (esc(t), chips(i)) for t, i in apps)
    feat_html = ''
    if features:
        feat_html = f'<div class="split top"><div>{head("Why it performs", "Key features")}{checks(features)}</div><div>{head("Where it’s used", "Applications")}{app_html}<p class="note">Specifications can be customized based on customer requirements and intended applications.</p></div></div>'
    elif app_html:
        feat_html = app_html
    intro_html = ''.join('<p%s>%s</p>' % (' class="lead"' if i == 0 else '', esc(t)) for i, t in enumerate(intro))
    body = f'''
<section class="page-hero"><div class="wrap">{crumbs([('products/index.html', 'Products'), (None, p['name'])], base)}
<div class="ph-grid"><div><span class="eyebrow">{eyebrow}</span><h1>{esc(title)}</h1><p class="lead">{lead}</p>
<div class="btn-row"><a class="btn btn-gold" href="#quote">Request a Quote</a>{broch}</div></div>
<div class="ph-media reveal">{media}</div></div></div></section>
{extra_before}
<section class="section"><div class="wrap"><div class="narrow" style="margin:0 auto 56px;width:min(100%,820px)">{intro_html}</div>{feat_html}</div></section>
{extra_after}
<section class="section tight"><div class="wrap"><div class="cta-band reveal"><span class="eyebrow">Next step</span><h2>Let’s discuss your requirement</h2><p>Get specifications, samples and a customised quotation for {esc(title)} from our team.</p>{cta_trio()}</div></div></section>
{enquiry_section(selected_name(slug), noun)}
{more_products(slug)}'''
    write('products/%s.html' % slug, title, desc or p['short'], body, '0.9', og_img=p['img'])

def selected_name(slug):
    return {'lump-charcoal': 'Lump Charcoal', 'hexagonal-briquettes': 'Hexagonal Briquettes', 'pillow-briquettes': 'Pillow Briquettes',
            'honeycomb-briquettes': 'Honeycomb Briquettes', 'biochar': 'Biochar', 'wood-vinegar': 'Wood Vinegar',
            'goldflame-stoves': 'Charcoal Briquette Stoves', 'pyrolysis-kilns': 'Pyrolysis Kilns & Retort Systems'}[slug]

def build_products():
    product_page('lump-charcoal', 'Lump Charcoal',
        'From restaurants to steel foundries — the widest application range of any carbon fuel.',
        ['ChaarGold’s Lump Charcoal is a premium-grade natural fuel produced through carefully controlled pyrolysis of selected biomass. Renowned for its high carbon content, superior heat output, and clean-burning characteristics, our lump charcoal is trusted by industrial users, restaurants, hospitality businesses, and international buyers seeking consistent quality and performance.',
         'Unlike conventional charcoal products, ChaarGold Lump Charcoal is manufactured using advanced carbonization processes that preserve the natural structure of the biomass while maximizing fixed carbon content. The result is a dense, durable, and high-energy fuel that ignites efficiently, burns longer, and delivers dependable heat.'],
        ['High fixed carbon content', 'Excellent calorific value', 'Longer burning duration', 'Low moisture content', 'Minimal smoke generation', 'Low ash residue', 'Consistent sizing and quality', 'Environmentally responsible production process'],
        ['Hospitality Sector', 'Food Processing Industries', 'Industrial Heating', 'Metallurgical Industries', 'Textile Industries', 'Export Markets'],
        brochure=None, desc='Premium lump charcoal from ChaarGold — high fixed carbon, long burn, low ash. Bulk supply for hospitality, industry and export.')

    product_page('hexagonal-briquettes', 'Charcoal Briquettes',
        'The world standard for grilling — perfected by ChaarGold.',
        ['The hexagonal shape is geometrically optimal for charcoal briquettes. The six sides create maximum surface contact when pieces are stacked, enabling even heat distribution. The shape also allows efficient airflow between briquettes, promoting complete combustion and reducing the risk of fire extinction in hookah and restaurant applications.',
         'ChaarGold’s hexagonal briquettes are globally recognized for their superior burn quality, exceptional longevity, and consistent ash profile. Our briquettes are produced from high-grade hardwood, coconut shell, or bamboo with natural starch binders — no chemical additives, no harmful residues.'],
        ['High calorific value for maximum heat generation', 'Extended burning time compared to conventional charcoal', 'Low ash content and minimal smoke emission', 'Uniform shape and density for consistent performance', 'Central airflow channel for improved combustion efficiency', 'Environmentally responsible fuel produced from renewable biomass', 'Easy storage, handling, and transportation'],
        ['Barbecue & Grilling', 'Food Processing Industries', 'Hospitality Sector', 'Export Markets'],
        brochure='chaargold-briquettes-brochure.pdf', title='Hexagonal Charcoal Briquettes',
        desc='Hexagonal charcoal briquettes by ChaarGold — hardwood, coconut shell or bamboo with natural binders. Even heat, long burn, low ash.')

    product_page('pillow-briquettes', 'Charcoal Briquettes',
        'Engineered for perfection — the pillow that burns longer and stacks better.',
        ['CHAARGOLD’s Pillow Charcoal Briquettes are premium compressed carbon fuel products engineered to deliver consistent heat, extended burn times, and superior combustion efficiency. Manufactured from carefully selected carbonized biomass and processed under strict quality controls, these briquettes combine performance, convenience, and sustainability in a compact pillow-shaped form.',
         'The uniform shape and density of pillow briquettes ensure reliable ignition, stable combustion, and predictable heat output, making them an ideal fuel choice for households, restaurants, hospitality establishments, and industrial users alike.',
         'Our pillow briquettes are designed to provide a cleaner, longer-lasting, and more economical alternative to traditional fuels. Their compact shape allows for easy handling, efficient storage, and optimal packing density during transportation.'],
        ['High calorific value for superior heat generation', 'Uniform size and density for consistent performance', 'Longer burn duration', 'Low moisture content', 'Minimal smoke and odor', 'Low ash residue', 'Easy ignition and steady combustion', 'Environmentally responsible production'],
        ['Barbecue & Grilling', 'Food Processing Industries', 'Hospitality Sector', 'Export Markets'],
        brochure='chaargold-briquettes-brochure.pdf', title='Pillow Charcoal Briquettes',
        desc='Pillow charcoal briquettes by ChaarGold — compact, uniform, long-burning compressed carbon fuel for BBQ, hospitality and export.')

    product_page('honeycomb-briquettes', 'Charcoal Briquettes',
        'Engineered for airflow. Built to burn longer and glow steadier. Works perfectly with our Signature Charcoal Briquette Stove — GoldFlame.',
        ['CHAARGOLD’s Honeycomb Charcoal Briquettes are premium compressed carbon fuel products, engineered to deliver consistent heat, extended burn times and efficient combustion. They are made from carefully selected carbonized biomass and processed under strict quality controls. Their signature hexagonal body with precision-formed air channels combines performance, convenience and sustainability.',
         'The honeycomb design draws air through the core of each briquette, which promotes quick ignition, even burning and stable, predictable heat output. This makes it an ideal fuel for households, restaurants, hospitality establishments and industrial users alike.',
         'Our honeycomb briquettes are designed as a cleaner, longer-lasting and more economical alternative to traditional fuels. The uniform hexagonal shape allows tight, interlocking stacking in the grill or stove, and it also makes handling, storage and transport more efficient.'],
        ['High calorific value for superior heat generation', 'Honeycomb air channels for fast ignition and efficient, even combustion', 'Uniform size and density for consistent performance', 'Longer burn duration', 'Low moisture content', 'Minimal smoke and odor', 'Low ash residue', 'Interlocking hexagonal shape for stable stacking and easy packing', 'Environmentally responsible production'],
        ['Cooking in Charcoal Briquette Stoves', 'Barbecue & Grilling', 'Tandoor', 'Food Processing Industries', 'Hospitality Sector', 'Export Markets'],
        brochure='chaargold-briquettes-brochure.pdf', title='Honeycomb Charcoal Briquettes',
        extra_after=f'''<section class="section bg-cream"><div class="wrap split"><div class="reveal"><span class="eyebrow">Perfect pairing</span><h2>Made for the GoldFlame stove</h2><p>Honeycomb briquettes light the fire in GoldFlame, ChaarGold’s signature charcoal briquette stove, and can be topped up with pillow briquettes to sustain cooking heat.</p><a class="btn btn-dark" href="goldflame-stoves.html">Discover GoldFlame {icon('arrow')}</a></div><div class="reveal imgcard">{img('gallery-honeycomb', 'Honeycomb briquette glowing in a stove', '../')}</div></div></section>''',
        desc='Honeycomb charcoal briquettes by ChaarGold — air channels for fast ignition and steady, even heat. Ideal for stoves, tandoor and BBQ.')

    # Biochar product page
    benefit = [('leaf', 'Soil Enhancement', '20–40% crop yield improvement in 2 seasons. Dramatically improves water retention and microbial activity.'),
               ('globe', 'Carbon Sequestration', 'Locks CO₂ for 100–1,000+ years. Eligible for Puro.earth, Verra, and Gold Standard carbon credits ($200–$600/t).'),
               ('drop', 'Water Filtration', 'High porosity removes heavy metals, nitrates, and organic contaminants from water systems.'),
               ('bolt', 'Industrial Uses', 'Battery additive, supercapacitors, building materials, activated carbon substitute.')]
    cards = ''.join(f'<div class="card reveal"><span class="ico">{icon(i)}</span><h3>{t}</h3><p>{d}</p></div>' for i, t, d in benefit)
    spec = table([('Product Name', 'BIO-CHAARGOLD® Biochar'), ('Appearance', 'Black Porous Granular Material'), ('Production Method', 'Controlled Pyrolysis'),
                  ('Feedstock', 'Sustainably Sourced Biomass'), ('Fixed Carbon', '65 – 85%'), ('Moisture Content', '<10%'), ('Ash Content', '<15%'), ('pH', '7.5 – 10.0'),
                  ('Bulk Density', '180 – 350 kg/m³'), ('Water Holding Capacity', 'High'), ('Porosity', 'Highly Porous Structure'), ('Particle Size', 'Customizable'),
                  ('Odour', 'Odourless'), ('Carbon Stability', 'Very High'), ('Carbon Retention Period', 'Hundreds to Thousands of Years')], cls='green')
    product_page('biochar', 'Bio-ChaarGold · Our biochar brand',
        'Transforming biomass into lasting impact — healing the Earth, sequestering carbon, and strengthening agriculture.',
        ['Bio-ChaarGold’s Biochar is a premium carbon-rich material produced through the controlled thermal conversion of biomass using advanced pyrolysis technology in a low-oxygen environment. Unlike conventional charcoal, which is primarily intended as a fuel source, our biochar is specifically engineered and tested for beneficial applications in agriculture, environmental management, carbon sequestration, and industrial systems.',
         'Developed through years of research, engineering expertise, and practical field experience, BioChaarGold Biochar is designed to enhance soil health, improve resource efficiency, and support long-term sustainability goals. Its highly porous structure creates an ideal habitat for beneficial soil microorganisms while improving water retention, nutrient availability, and soil aeration.'],
        None, None, brochure='biochaargold-brochure.pdf', noun='biochar', title='BIOCHAARGOLD Premium Biochar', img_name='biochar-bag',
        extra_before=f'<section class="section"><div class="wrap"><div class="grid g4">{cards}</div><p style="margin-top:2rem" class="center"><a class="btn btn-dark" href="../biochaargold.html">Explore more about Bio-ChaarGold… {icon("arrow")}</a></p></div></section>',
        extra_after=f'''<section class="section bg-cream brand-green"><div class="wrap"><div class="split top"><div>{head('Technical data','Typical specification')}{spec}<p class="note">Specifications can be customized based on customer requirements and intended applications.</p></div>
<div class="reveal"><figure class="figure shadow">{img('biochar-pallets', 'Bio-ChaarGold premium biochar bags stacked on pallets, ready for dispatch', '../')}<figcaption>Bio-ChaarGold premium biochar, carefully packed and prepared for dispatch to our customers, supporting healthier soils and sustainable agricultural practices.</figcaption></figure></div></div></div></section>''',
        desc='Bio-ChaarGold premium biochar — engineered for soil health, carbon sequestration and industrial uses. Specifications, applications and enquiries.')

    # Kilns
    kfeat = [('gear', 'Precision-engineered construction'), ('flame', 'Optimized thermal efficiency'), ('recycle', 'Sustainable biomass conversion'), ('chart', 'High charcoal and biochar yields'),
             ('leaf', 'Recovery of valuable by-products'), ('shield', 'Robust and durable design'), ('box', 'Scalable production capacities'), ('refresh', 'Continuous process optimization')]
    kf = ''.join(f'<div class="tile reveal"><span class="ico" style="display:block;color:var(--gold-deep);margin-bottom:.8rem">{icon(i)}</span><h3 style="margin:0;font-size:1.05rem">{t}</h3></div>' for i, t in kfeat)
    kf = kf.replace('<span class="ico" style="display:block;color:var(--gold-deep);margin-bottom:.8rem"><svg', '<span style="display:block;color:var(--gold-deep);margin-bottom:.8rem"><svg width="30" height="30"')
    three = [('factory', 'Premium Construction', 'High-grade alloy steel with refractory lining. Engineered for 10+ years of continuous operation when operated as per guidelines.'),
             ('drop', 'Condensate Collection', 'Dual-stage condensate collection for wood vinegar and smoke oil extraction, creating additional revenue from every production cycle.'),
             ('gear', 'Advanced Design', 'Advanced design ensures carbon content is locked in and biomass is effectively converted to high grade charcoal.')]
    three_h = ''.join(f'<div class="card reveal"><span class="ico">{icon(i)}</span><h3>{t}</h3><p>{d}</p></div>' for i, t, d in three)
    outputs = [('Lump Charcoal', 'Premium-quality charcoal with high fixed carbon content, long burn duration, and low ash generation.'),
               ('Charcoal Briquettes', 'Charcoal is further processed into high-quality briquettes designed to meet diverse fuel requirements across the hospitality sector, industrial applications, and other commercial uses.'),
               ('Biochar', 'Carbon-rich material engineered for agriculture, carbon sequestration, soil enhancement, and environmental applications.'),
               ('Wood Vinegar', 'A valuable pyroligneous acid used in agriculture, composting, odor management, and soil health improvement.'),
               ('Charcoal Tar', 'A recoverable pyrolysis by-product suitable for numerous applications and industrial and research applications.')]
    out_h = ''.join(f'<div class="tile reveal"><span class="n">0{i+1}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(outputs))
    appl = [('Commercial Charcoal Manufacturing', 'Designed for businesses seeking consistent production of high-quality lump charcoal and briquettes.'),
            ('Biochar Production Facilities', 'Ideal for organizations focused on regenerative agriculture, carbon sequestration, and sustainability projects.'),
            ('Carbon Credit Projects', 'Supports the production of biochar for carbon removal and climate-focused initiatives.'),
            ('Agricultural & Forestry Waste Utilization', 'Transforms biomass residues into valuable carbon products while reducing waste.'),
            ('Research & Innovation', 'Suitable for institutions, startups, and organizations developing advanced carbon and biomass solutions.')]
    app_h = ''.join(f'<div class="tile reveal"><h3>{t}</h3><p>{d}</p></div>' for t, d in appl)
    kspec = table([('Kiln Type', 'Batch'), ('Production Technology', 'Controlled Pyrolysis'), ('Feedstock Compatibility', 'Hard-Wood, Bamboo, Coconut Shell, Agricultural Residues, Forestry Biomass'),
                   ('Primary Products', 'Charcoal, Biochar'), ('Secondary Products', 'Wood Vinegar, Tar'), ('Operating Temperature', '350°C – 700°C'), ('Carbonization Efficiency', 'High Yield Optimized Design'),
                   ('Construction Material', 'Heavy-Duty Mild Steel / Custom Grades'), ('Condensation System', 'Optional Wood Vinegar & Tar Recovery'), ('Installation Type', 'Fixed / Portable'),
                   ('Operational Life', 'Long Service Life with Proper Maintenance')], ('Parameter', 'Specification'))
    cap = table([('CG-1000', '4 MT/batch', '1 – 1.5 MT/batch')], ('Model', 'Biomass Input Capacity', 'Approximate Charcoal Output'))
    turnkey = ['Project consultation and feasibility assessment', 'Kiln design and manufacturing', 'Installation and commissioning', 'Operator training', 'Production optimization', 'Technical support and after-sales service', 'Process integration for biochar and charcoal production']
    industries = ['Agriculture & Biochar Producers', 'Charcoal Manufacturers', 'Industrial Carbon Producers', 'Waste-to-Value Projects', 'Carbon Credit Developers', 'Forestry & Biomass Processing Companies', 'Research & Development Institutions']
    product_page('pyrolysis-kilns', 'Pyrolysis Kilns & Retort Systems',
        'From biomass to value, our pyrolysis kilns unlock the full potential of carbon production through innovation, efficiency, and engineering excellence.',
        ['At ChaarGold, we design and manufacture advanced pyrolysis kilns that transform biomass into high-value carbon products through efficient and controlled thermal conversion. Developed through years of engineering expertise, operational experience, and continuous innovation, our kilns are built to deliver superior performance, operational reliability, and maximum resource utilization.',
         'Whether producing charcoal, biochar, wood vinegar, smoke oil, or other value-added by-products, ChaarGold Pyrolysis Kilns provide an integrated solution for sustainable carbon manufacturing.'],
        None, None, brochure='chaargold-pyrolysis-kiln-brochure.pdf', noun='pyrolysis kiln', title='Pyrolysis Kilns & Retort Systems', img_name='kilns-hero',
        extra_before=f'''<section class="section bg-cream"><div class="wrap">{head('Key kiln features','Built to run for years')}<div class="grid g3">{three_h}</div>
<figure class="figure shadow reveal" style="margin-top:48px">{img('kiln-gantry', 'Loading the pyrolysis kiln with bamboo biomass using an overhead gantry', '../')}<figcaption><b>Loading the Pyrolysis Kiln with Bamboo Biomass.</b> Preparing bamboo biomass for controlled pyrolysis, transforming renewable biomass into valuable biochar through an efficient carbonisation process.</figcaption></figure></div></section>''',
        extra_after=f'''<section class="section"><div class="wrap">
{head('Engineered for excellence','Manufactured in-house by our engineers','Our kilns optimise the pyrolysis process through precise temperature control, efficient heat utilization, and enhanced carbon recovery — maximising product quality while minimising fuel consumption, emissions, and operational costs.')}
<div class="grid g4">{kf}</div></div></section>
<section class="section bg-ink"><div class="wrap">{head('Outputs','Products generated through our kilns')}<div class="grid g3 outputs">{out_h}</div></div></section>
<section class="section"><div class="wrap">{head('Applications','Where our kilns work')}<div class="grid g3">{app_h}</div></div></section>
<section class="section bg-cream"><div class="wrap split top"><div>{head('Turnkey solutions available','Beyond kiln manufacturing','ChaarGold offers complete turnkey pyrolysis plant solutions, including:')}{checks(turnkey)}</div>
<div><h3>Why choose CHAARGOLD pyrolysis kilns?</h3><p>Our kilns are more than equipment — they are the result of years of practical manufacturing experience and engineering innovation. Every system is designed to help clients achieve higher production efficiency, superior product quality, and long-term operational reliability.</p><p>With installations across multiple industries and applications, ChaarGold has earned a reputation for delivering dependable pyrolysis technology tailored to real-world operating conditions.</p>
<h3 style="margin-top:1.6em">Industries we serve</h3>{chips(industries)}</div></div></section>
<section class="section"><div class="wrap split top"><div>{head('Technical specifications','Built to your requirement','ChaarGold Pyrolysis Kilns are available in multiple capacities and can be customized to suit production requirements, feedstock types, and operational objectives.')}</div>
<div>{kspec}<h3 style="margin:2rem 0 1rem">Available capacity option</h3>{cap}<p class="note">Output varies depending on feedstock type, moisture content, operating conditions, and process parameters.</p></div></div></section>''',
        desc='In-house engineered pyrolysis kilns, retort systems and turnkey plants for charcoal and biochar production, with wood vinegar and tar recovery.')

    # Stoves
    pills = ''.join(f'<span class="btn btn-gold" style="cursor:default">{icon(i)}{t}</span>' for i, t in [('wallet', 'Savings on Cooking Gas'), ('flame', 'Flexible Fuel Options'), ('leaf', 'Biomass-Based Cooking')])
    why = [('wallet', 'Savings on Cooking Gas', 'GoldFlame offers an alternative to LPG cooking, with the potential to reduce fuel expenses for households and commercial kitchens. Enjoy a different approach to everyday cooking while keeping an eye on your energy costs.'),
           ('bolt', 'Alternative Energy Choices', 'GoldFlame supports the diversification of cooking fuels, helping households and businesses explore options beyond conventional fuels and build greater flexibility into their energy choices.'),
           ('leaf', 'A More Sustainable Direction', 'GoldFlame aligns with a resource-conscious approach to cooking by utilising charcoal briquettes that can be produced from responsibly sourced biomass.'),
           ('chef', 'Versatile Cooking Applications', 'From barbecue and grilling to tandoors, commercial kitchens and other compatible charcoal-burning equipment, GoldFlame offers a cooking option for a variety of settings.')]
    why_h = ''.join(f'<div class="card reveal"><span class="ico">{icon(i)}</span><h3>{t}</h3><p>{d}</p></div>' for i, t, d in why)
    ways = [('pot', '01', 'Everyday & Commercial Cooking', 'A practical option for preparing meals in small kitchens, cafés, food stalls and catering setups. GoldFlame supports a range of cooking tasks using compatible cookware, making it worth considering for businesses exploring alternatives to conventional cooking fuels.'),
            ('flame', '02', 'Grilling & Barbecue', 'From restaurants and outdoor caterers to barbecue stalls and specialist food vendors, GoldFlame can support grilling and barbecue applications with a compatible grill attachment. An additional cooking option for businesses looking to expand their menu and service offering.'),
            ('chef', '03', 'Tandoor-Style Cooking', 'With compatible tandoor-style accessories, GoldFlame can offer additional possibilities for preparing flatbreads, kebabs and other tandoor-inspired dishes. Ideal for food businesses seeking to diversify their cooking methods without automatically requiring a separate appliance for every application.')]
    ways_h = ''.join(f'<div class="tile reveal"><span class="n">{n}</span><h3>{t}</h3><p>{d}</p></div>' for _, n, t, d in ways)
    prac = [('Explore Cooking-Fuel Savings', 'Charcoal briquettes provide an alternative to LPG and other conventional fuels. Businesses can compare their local fuel costs and consumption to assess the potential for savings.'),
            ('More Versatility, More Menu Options', 'Cooking, grilling and tandoor-style preparation can serve different menu requirements, subject to stove compatibility and the appropriate accessories.'),
            ('An Alternative Energy Choice', 'GoldFlame gives kitchens and food businesses another fuel option to consider as part of a broader approach to energy resilience and responsible biomass utilisation.')]
    prac_h = ''.join(f'<li><b style="color:var(--ink)">{t}.</b> {d}</li>' for t, d in prac)
    product_page('goldflame-stoves', 'GoldFlame · Signature stoves',
        'A practical approach to affordable cooking, flexible fuel choices and a more sustainable cooking future.',
        ['GoldFlame by ChaarGold offers a practical alternative to conventional cooking fuels through charcoal briquette stoves designed for everyday cooking needs. From households and outdoor cooking to food businesses and commercial kitchens, GoldFlame brings together fuel flexibility, functionality and a forward-looking approach to cooking.'],
        None, None, noun='charcoal briquette stove', title='GoldFlame Charcoal Briquette Stoves', img_name='goldflame-logo',
        extra_before=f'''<section class="section bg-ink"><div class="wrap">{head('A cooking revolution','Fueled by smarter choices','Discover GoldFlame charcoal briquette stoves — a practical approach to affordable cooking, flexible fuel choices and a more sustainable cooking future.')}<div class="btn-row" style="margin:0">{pills}</div></div></section>
<section class="section"><div class="wrap split"><div class="reveal"><span class="eyebrow">02 — Two briquettes</span><h2>One smart combination.</h2><p class="lead">Discover how GoldFlame can combine different briquette shapes for starting and sustaining the fire.</p>
<div class="grid g2" style="margin-top:28px"><div class="card flat"><div style="aspect-ratio:1;display:grid;place-items:center;margin-bottom:12px">{img('honeycomb-briquettes', 'Honeycomb briquettes', '../')}</div><span class="eyebrow" style="margin-bottom:.4rem">Step 1 · Start</span><h3>Honeycomb Briquettes</h3><p>Honeycomb briquettes can be used to help establish the initial fire, following the stove’s recommended lighting method. Their distinctive perforated design allows air to pass through the briquette.</p></div>
<div class="card flat"><div style="aspect-ratio:1;display:grid;place-items:center;margin-bottom:12px">{img('pillow-briquettes', 'Pillow briquettes', '../')}</div><span class="eyebrow" style="margin-bottom:.4rem">Step 2 · Optional</span><h3>Pillow Briquettes</h3><p>Once the fire is established, pillow briquettes may optionally be added to help maintain the heat needed for cooking, depending on the stove design and cooking requirements.</p></div></div></div>
<div class="reveal"><div class="placeholder"><div><b>GoldFlame stove photography</b>Product pictures coming soon</div></div></div></div></section>
<section class="section bg-cream"><div class="wrap">{head('03 — Why choose GoldFlame?','Built around practical cooking')}<div class="grid g4">{why_h}</div></div></section>
<section class="section"><div class="wrap">{head('One stove. Multiple cooking possibilities.','Three ways to work','Designed for versatility, GoldFlame charcoal briquette stoves offer adaptable cooking options for small commercial kitchens, food stalls, cafés, catering operations, outdoor food businesses and home use.')}<div class="grid g3">{ways_h}</div>
<div class="split top" style="margin-top:56px"><div><h3>Built around practicality</h3><ul class="prose" style="list-style:none;padding:0;display:grid;gap:1rem">{prac_h}</ul></div>
<div class="card flat" style="background:var(--cream)"><span class="eyebrow">04 — Rethinking the future of cooking</span><p>The future of cooking is about more than the fuel we use. It is about affordability, energy resilience and responsible resource utilisation. With GoldFlame, ChaarGold aims to make charcoal briquette cooking a practical option for households, communities and businesses seeking alternative ways to meet their everyday cooking needs.</p><p><b style="color:var(--ink)">GoldFlame by ChaarGold — One stove. Multiple applications. Smarter cooking possibilities.</b></p></div></div></div></section>''',
        desc='GoldFlame by ChaarGold — signature charcoal briquette stoves for everyday cooking, grilling and tandoor-style preparation.')

    # Wood vinegar
    wv = [('tree', 'Enhances Plant Growth', 'Supports healthier plant development by stimulating root growth, improving nutrient uptake, and strengthening overall plant vigor.'),
          ('leaf', 'Improves Soil Health', 'Promotes beneficial microbial activity and contributes to a healthier, more balanced soil ecosystem.'),
          ('bug', 'Natural Pest and Disease Management', 'When appropriately diluted, wood vinegar can help deter certain pests and create less favorable conditions for some plant pathogens.'),
          ('recycle', 'Compost Enhancement', 'Accelerates composting processes and supports the decomposition of organic matter.'),
          ('wind', 'Odor Control', 'Effective in reducing odors in livestock farms, composting operations, and waste management systems.'),
          ('globe', 'Sustainable and Eco-Friendly', 'Produced from renewable biomass and supports environmentally responsible agricultural practices.')]
    wv_rows = ''.join(f'<tr><th scope="row"><span style="display:inline-flex;align-items:center;gap:.7em"><span style="color:var(--gold-deep);width:26px;height:26px;display:inline-block">{icon(i)}</span>{t}</span></th><td>{d}</td></tr>' for i, t, d in wv)
    wv_table = f'<div class="table-wrap"><table class="spec"><thead><tr><th scope="col">Benefit</th><th scope="col">How it helps</th></tr></thead><tbody>{wv_rows}</tbody></table></div>'
    wv_spec = table([('Product Name', 'ChaarGold Wood Vinegar'), ('Production Method', 'Pyrolysis Condensate'), ('Appearance', 'Brown to Dark Brown Liquid'), ('Odour', 'Characteristic Smoky Aroma'),
                     ('pH', '2.0 – 4.0'), ('Solubility', 'Fully Soluble in Water'), ('Source Material', 'Sustainable Biomass'), ('Shelf Life', '24 Months (Stored Properly)')])
    apps = [('Agricultural Applications', ['Crop cultivation', 'Plantation crops', 'Soil conditioning', 'Organic farming', 'Seed Treatment']),
            ('Horticultural Applications', ['Nurseries', 'Greenhouses', 'Landscape management', 'Home gardening']),
            ('Livestock & Poultry Applications', ['Odor Management', 'Farm Hygiene Enhancement', 'Waste Management Systems']),
            ('Composting Applications', ['Compost activation', 'Organic Waste Treatment', 'Microbial Activity Enhancement']),
            ('Environmental Applications', ['Waste Management', 'Sustainable Land Management', 'Eco-Friendly Farming Practices'])]
    apps_h = ''.join('<div class="app-group"><h3>%s</h3>%s</div>' % (t, chips(i)) for t, i in apps)
    product_page('wood-vinegar', 'Wood Vinegar · Pyroligneous acid',
        'Nature’s liquid solution for sustainable agriculture.',
        ['ChaarGold’s Wood Vinegar, also known as Pyroligneous Acid, is a natural liquid by-product obtained during the controlled pyrolysis of biomass in our advanced carbonization systems. Produced through the condensation of smoke generated during the pyrolysis process, wood vinegar contains a rich blend of naturally occurring organic compounds that have been widely recognized for their agricultural, horticultural, and environmental benefits.',
         'At ChaarGold, our wood vinegar is carefully recovered and processed from sustainably sourced biomass, ensuring a high-quality product suitable for a wide range of agricultural and industrial applications. This valuable by-product reflects our commitment to maximizing resource utilization and creating sustainable solutions from every stage of the pyrolysis process.'],
        None, None, noun='wood vinegar', title='Wood Vinegar', img_name='wood-vinegar',
        extra_before=f'''<section class="section bg-cream"><div class="wrap split"><div class="reveal"><span class="eyebrow">How it is produced</span><h2>From smoke to soil</h2><p>During pyrolysis, biomass is heated in a low-oxygen environment, producing biochar, gases, and vapors. These vapors are captured and condensed to produce wood vinegar — a nutrient-rich liquid containing organic acids, phenols, esters, alcohols, and other beneficial compounds.</p><p>Through careful collection and maturation, ChaarGold Wood Vinegar is transformed into a versatile natural product with multiple applications.</p></div>
<div class="reveal imgcard">{img('kiln-row', 'ChaarGold pyrolysis kilns', '../')}</div></div></section>
<section class="section"><div class="wrap">{head('Key benefits','Why growers choose wood vinegar')}{wv_table}</div></section>''',
        extra_after=f'''<section class="section bg-cream"><div class="wrap split top"><div>{head('Uses','Applications')}{apps_h}</div><div>{head('Technical data','Wood vinegar specification')}{wv_spec}<p class="note">Specifications can be customized based on customer requirements and intended applications.</p></div></div></section>''',
        desc='ChaarGold wood vinegar (pyroligneous acid) — a natural by-product of biomass pyrolysis for crop growth, soil health, composting and odour control.')

# ------------------------------------------------------------------ products index
def products_index():
    base = '../'
    cards = ''.join(pcard(p, base, True) for p in PRODUCTS)
    broch = [('Charcoal Briquettes', 'Explore our range of premium charcoal briquettes, available in Pillow, Hexagonal and Honeycomb shapes.', 'Our product range, applications and charcoal solutions.', 'chaargold-briquettes-brochure.pdf', 'Download Charcoal Briquettes Brochure'),
             ('Biochar Solutions', 'Discover our biochar products and their potential applications in soil improvement, agriculture and carbon management.', 'Biochar, biomass conversion and carbon solutions.', 'biochaargold-brochure.pdf', 'Download Biochar Brochure'),
             ('Pyrolysis & Retort Systems', 'Explore our pyrolysis and retort kiln solutions for biomass carbonisation and biochar production.', 'Equipment configurations, biomass processing and pyrolysis solutions.', 'chaargold-pyrolysis-kiln-brochure.pdf', 'Download Pyrolysis & Retort Systems Brochure'),
             ('CHAARGOLD — Company Profile', 'Learn more about CHAARGOLD’s capabilities in charcoal production, our products and services, equipment and turnkey carbon project solutions.', 'Integrated solutions for carbon-related projects and production facilities and the team behind it.', None, 'Request Company Profile')]
    bh = ''
    for i, (t, d, l, f, b) in enumerate(broch):
        btn = f'<a class="btn btn-dark" href="{base}assets/brochures/{f}" download>{icon("download")} {b}</a>' if f else f'<a class="btn btn-line" href="mailto:{EMAIL}?subject=Company%20Profile%20request">{icon("mail")} {b}</a>'
        bh += f'<div class="card reveal"><span class="eyebrow" style="margin-bottom:.6rem">0{i+1}</span><h3>{t}</h3><p>{d}</p><p style="margin-top:.6rem"><b style="color:var(--ink)">Learn about:</b> {l}</p><div style="margin-top:1.2rem">{btn}</div></div>'
    body = f'''<section class="page-hero"><div class="wrap">{crumbs([(None, 'Products')], base)}<span class="eyebrow">Our portfolio</span><h1>Products &amp; solutions</h1>
<p class="lead" style="max-width:760px">Biochar, lump charcoal, hexagonal, pillow and honeycomb briquettes, wood vinegar, stoves and the pyrolysis kilns that make it all possible — designed to meet global quality standards.</p></div></section>
<section class="section"><div class="wrap"><div class="grid g4">{cards}</div></div></section>
<section class="section bg-cream"><div class="wrap">{head('Brochures &amp; resources', 'Explore CHAARGOLD’s product range', 'Download our brochures to learn more about CHAARGOLD, explore our product offerings and identify solutions suited to your business requirements.')}<div class="grid g2">{bh}</div></div></section>
<section class="section tight"><div class="wrap"><div class="cta-band reveal"><span class="eyebrow">Need more information?</span><h2>Can’t find what you need?</h2><p>Our team will be happy to assist you with product details, technical enquiries, quotations and customised project requirements.</p><p><a href="mailto:{EMAIL}" style="color:#fff">{EMAIL}</a> · <a href="tel:+{PHONE_RAW}" style="color:#fff">{PHONE}</a></p><div class="btn-row"><a class="btn btn-gold" href="../contact.html">Contact CHAARGOLD</a></div></div></div></section>'''
    write('products/index.html', 'Products', 'Explore ChaarGold’s range: lump charcoal, charcoal briquettes, biochar, wood vinegar, GoldFlame stoves and pyrolysis kilns.', body, '0.9')

# ------------------------------------------------------------------ home
def home():
    b = ''
    cards = ''.join(pcard(p, '') for p in PRODUCTS)
    schema = '<script type="application/ld+json">%s</script>' % json.dumps({
        '@context': 'https://schema.org', '@type': 'Organization', 'name': 'ChaarGold', 'url': DOMAIN, 'logo': DOMAIN + '/assets/img/logo-chaargold.webp',
        'email': EMAIL, 'telephone': '+' + PHONE_RAW, 'slogan': 'Crafting Carbon Perfection',
        'address': {'@type': 'PostalAddress', 'addressLocality': 'Bengaluru', 'addressRegion': 'Karnataka', 'addressCountry': 'IN'}})
    body = f'''
<section class="hero"><div class="wrap hero-grid">
<div><span class="kicker">Engineering Excellence — With Purpose</span><h1>Turning Biomass Into <em>Black&nbsp;Gold</em></h1>
<p class="lead">We are not just a charcoal manufacturer. We are a technology company that happens to work with carbon. Every pyrolysis kiln, every briquette, every kilogram of biochar represents our commitment to precision and sustainability.</p>
<div class="btn-row"><a class="btn btn-gold" href="products/index.html">Explore products {icon('arrow')}</a><a class="btn btn-line" href="contact.html#enquiry">Get a Quote</a></div></div>
<div class="hero-media">{img('kilns-hero', 'ChaarGold in-house pyrolysis kilns inside the Penukonda plant', '', lazy=False)}<div class="hero-badge"><b>100+</b><span>pyrolysis kilns installed across India</span></div></div>
</div></section>
<section class="bg-ink" aria-label="ChaarGold in numbers"><div class="wrap">{stats_row()}</div></section>
<section class="section"><div class="wrap split">
<div class="reveal"><span class="eyebrow">In-house technology</span><h2>The gold standard of manufacturing</h2>
<p class="lead">CHAARGOLD’s in-house manufactured pyrolysis kilns are precision-engineered to deliver efficient, reliable, and high-quality charcoal and biochar production.</p>
<p>Designed using advanced pyrolysis technology, our kilns ensure optimal carbonization, enhanced fuel efficiency, reduced emissions, and superior product consistency. Built with robust materials and meticulous engineering standards, they provide a leak-proof and controlled pyrolysis environment that maximizes yield while preserving carbon quality.</p>
<p>Recognized as the gold standard in charcoal and biochar production systems, CHAARGOLD kilns are trusted by farmers, entrepreneurs, and industrial users seeking sustainable, high-performance carbon solutions. From small-scale operations to commercial production facilities, our kiln systems are engineered to deliver operational excellence, durability, and long-term value.</p>
<a class="btn btn-dark" href="products/pyrolysis-kilns.html">Pyrolysis kilns &amp; retort systems {icon('arrow')}</a></div>
<div class="reveal imgcard">{img('kiln-gantry', 'Overhead gantry loading bamboo biomass into a ChaarGold kiln', '')}</div></div></section>
<section class="section bg-cream"><div class="wrap">
{head('Our portfolio', 'Engineering sustainable carbon solutions', 'At CHAARGOLD, we believe that today’s biomass waste is tomorrow’s sustainable resource. Through advanced pyrolysis technology and innovative manufacturing processes, we convert agricultural and forestry biomass into premium carbon products that create value for farmers, industries, and the environment.')}
<div class="grid g4">{cards}</div></div></section>
<section class="section"><div class="wrap split">
<div class="reveal imgcard" style="max-width:520px;margin-inline:auto">{img('waste-to-value', 'Infographic: from waste to value — biomass to charcoal, biochar and wood vinegar', '')}</div>
<div class="reveal"><span class="eyebrow">Circular carbon</span><h2>From waste to value</h2>
<p class="lead">Our diverse portfolio includes biochar, lump charcoal, hexagonal briquettes, pillow briquettes, honeycomb briquettes, wood vinegar, smoke oil, and other carbon-rich by-products designed to meet global quality standards.</p>
<p>Whether supporting regenerative agriculture, industrial heating applications, renewable energy initiatives, or carbon sequestration projects, CHAARGOLD is committed to delivering reliable, sustainable, and performance-driven solutions.</p>
<a class="btn btn-dark" href="sustainability.html">Our sustainability commitment {icon('arrow')}</a></div></div></section>
<section class="section bg-cream brand-green"><div class="wrap split">
<div class="reveal"><img src="assets/img/logo-biochaargold.webp" alt="BIOCHAARGOLD — Accelerating Carbon Cultivation" class="hero-logo" loading="lazy" width="220" height="220"><span class="eyebrow">Our biochar brand</span><h2>Healing the Earth. Sequestering carbon.</h2><p class="lead">Bio-ChaarGold biochar is engineered and tested for agriculture, environmental management and carbon sequestration — locking carbon in stable form for centuries.</p><div class="btn-row"><a class="btn btn-dark" href="biochaargold.html">Explore BIOCHAARGOLD {icon('arrow')}</a><a class="btn btn-line" href="products/biochar.html">Premium biochar</a></div></div>
<div class="reveal imgcard">{img('biochar-bag', 'BIOCHAARGOLD premium biochar bag with spilled biochar', '')}</div></div></section>
<section class="section bg-ink"><div class="wrap">{head('Our footprint so far', 'Numbers we’re proud of', '', True)}{stats_row()}</div></section>
{cta_band('Start your ChaarGold journey today', 'Whether you need 1 FCL of briquettes or a complete pyrolysis plant installation — we have the products, the expertise, and the commitment.', '')}
'''
    write('index.html', 'ChaarGold — Turning Biomass Into Black Gold', 'ChaarGold manufactures charcoal briquettes, lump charcoal, biochar and wood vinegar, and builds turnkey pyrolysis kilns and plants. Based in Bengaluru, made in Andhra Pradesh.', body, '1.0', schema=schema)

# ------------------------------------------------------------------ about
def about():
    people = [
     ('team-prem', 'Prem Raj', 'Founder & Chief Technology Officer',
      'Prem Raj is the Founder and Chief Technology Officer of CHAARGOLD, bringing over 15 years of experience in sustainable energy, biomass conversion, and carbon solutions. An engineer, innovator, patent holder, and passionate agriculturist, he combines technical expertise with practical industry knowledge to develop advanced pyrolysis technologies and high-performance carbon products. With global exposure across diverse markets, he is also a successful hotelier and brand-builder, driven by a vision to create sustainable businesses that deliver lasting value for customers, communities, and the environment.',
      'Innovation is not just about creating new technologies; it is about transforming challenges into sustainable opportunities that create lasting value for people and the planet.'),
     ('team-namratha', 'Namratha Raj', 'Chief Executive Officer',
      'Namratha Raj serves as the Chief Executive Officer of CHAARGOLD, bringing over 9 years of experience in sustainable and renewable energy projects, complemented by a strong corporate background. Having worked extensively across the Gulf region, she brings valuable international business insight, strategic leadership, and a customer-centric approach to the organization. Passionate about nature and nurturing sustainable growth, Namratha is committed to advancing CHAARGOLD’s vision of delivering innovative carbon solutions that create positive environmental and economic impact. Her focus on operational excellence, stakeholder relationships, and sustainable development continues to drive the company’s growth and global aspirations.',
      'Growth is most meaningful when it nurtures people, protects nature, and creates lasting value.'),
     ('team-malathi', 'Malathi Raj', 'Chief Financial Officer',
      'Malathi Raj serves as the Chief Financial Officer of CHAARGOLD, bringing strong business acumen, financial discipline, and strategic oversight to the organization. With a keen focus on financial stewardship, operational efficiency, and sustainable growth, she plays a pivotal role in guiding the company’s financial strategy and long-term development. Her disciplined approach to business management, combined with a commitment to sound governance and responsible decision-making, helps ensure CHAARGOLD’s continued stability, profitability, and success.',
      'Sustainable growth is built on a foundation of discipline, integrity, and prudent financial management.'),
     ('team-deepika', 'Deepika Raj', 'Chief Marketing Officer',
      'Deepika Raj serves as the Chief Marketing Officer of CHAARGOLD, bringing a strategic perspective to brand development, market positioning, and customer engagement. With a focus on building brand value, strengthening market presence, and identifying new growth opportunities, she plays a key role in shaping the company’s marketing direction and business expansion. Her collaborative approach, combined with a commitment to clear communication, market insight, and lasting customer relationships, helps position CHAARGOLD for sustainable growth and a strong presence in the evolving biomass and sustainable solutions industry.',
      'A strong brand is built on trust, meaningful connections, and a clear vision for the future.')]
    ph = ''.join(f'<article class="person reveal">{img(i, n + ', ' + r, "")}<div><span class="role">{r}</span><h3>{n}</h3><p>{esc(bio)}</p><blockquote>“{esc(q)}” — {n}</blockquote></div></article>' for i, n, r, bio, q in people)
    vals = [('bulb', 'Innovation', 'We create smarter, better and sustainable solutions.'), ('award', 'Excellence', 'We deliver the highest standards in quality and performance.'),
            ('leaf', 'Sustainability', 'We protect nature by turning waste into value.'), ('users', 'Customer Partnership', 'We succeed when our customers succeed. Their goals drive our innovation and commitment.')]
    vh = ''.join(f'<div class="val"><b>{t}</b>{d}</div>' for _, t, d in vals)
    body = f'''<section class="page-hero"><div class="wrap">{crumbs([(None, 'About Us')], '')}<div class="ph-grid"><div><span class="eyebrow">About us</span><h1>Who we are</h1>
<p class="lead">ChaarGold is a vertically integrated manufacturing company specializing in the production and supply of charcoal briquettes, biochar, wood vinegar, smoke oil and related carbon-based products. We also offer turnkey pyrolysis plant solutions, providing end-to-end support from project planning and engineering design to equipment manufacturing, installation, commissioning, and operational training.</p></div>
<div class="ph-media photo reveal">{img('gallery-kilns', 'ChaarGold kilns at the Penukonda manufacturing facility', '', lazy=False)}</div></div></div></section>
<section class="section"><div class="wrap split top"><div class="reveal"><p>Our company was built on a simple but powerful idea: that the ancient art of charcoal making could be elevated by modern science, engineering rigor, and a deep commitment to sustainability. Today, ChaarGold stands as one of the most trusted names in carbon manufacturing, serving clients across hospitality, agriculture, textile, energy, chemical, and environmental sectors.</p>
<p>Headquartered in Bengaluru, Karnataka with an expertly engineered 5-acre manufacturing facility in Penukonda, Andhra Pradesh, we operate several production lines and a dedicated R&amp;D division — all under one roof, all to one standard of excellence.</p></div>
<div class="reveal card flat" style="background:var(--cream)"><span class="eyebrow">A family-run business</span><p>At ChaarGold, we are a family-run business built on unity, passion and a shared vision for a sustainable future. We believe in the strength of teamwork, the value of diverse perspectives, and the importance of balancing family values with professional excellence.</p><p style="margin:0">Our approach combines personal commitment with a strong sense of responsibility, driving us to build lasting partnerships, deliver dependable solutions, and grow with integrity. Together, we are committed to advancing sustainable biomass solutions through innovation, collaboration and purpose.</p></div></div></section>
<section class="bg-ink"><div class="wrap">{stats_row()}</div></section>
<section class="section bg-ink" style="padding-top:0"><div class="wrap"><div class="mvv" style="border:1px solid #bc9c2355;border-radius:20px;overflow:hidden">
<div><span class="ico">{icon('target')}</span><h3>Our Mission</h3><p>To design, manufacture and deliver premium carbon solutions through innovation, engineering excellence and responsible resource utilization — empowering our customers, supporting communities, and creating a sustainable future.</p></div>
<div><span class="ico">{icon('eye')}</span><h3>Our Vision</h3><p>To be a global leader in sustainable carbon innovation, transforming biomass into valuable resources that enrich agriculture, empower industries, and contribute to a greener, better world.</p></div>
<div><span class="ico">{icon('diamond')}</span><h3>Our Core Values</h3>{vh}</div></div></div></section>
<section class="section"><div class="wrap">{head('Our leadership', 'The team behind ChaarGold')}{ph}</div></section>
{cta_band('Let’s build better carbon solutions together', 'Talk to our team about products, projects or partnerships.', '')}'''
    write('about.html', 'About Us', 'ChaarGold is a vertically integrated, family-run carbon manufacturer with HQ in Bengaluru and a 5-acre plant in Penukonda. Meet our leadership.', body, '0.8')

# ------------------------------------------------------------------ biochaargold brand page
def biochaargold():
    kb = ['Improves soil fertility and structure', 'Enhances water retention and drought resilience', 'Increases nutrient-use efficiency', 'Supports beneficial microbial activity', 'Reduces nutrient leaching',
          'Promotes healthier root development', 'Contributes to long-term carbon sequestration', 'Supports regenerative and sustainable agriculture', 'Converts biomass waste into valuable environmental assets']
    apps = [('Agricultural Applications', ['Field crops', 'Plantation crops', 'Horticulture', 'Organic farming', 'Greenhouses']),
            ('Environmental Applications', ['Land restoration', 'Mine reclamation', 'Soil remediation', 'Carbon sequestration projects']),
            ('Landscaping Applications', ['Turf management', 'Urban greening', 'Parks and gardens']),
            ('Carbon & Waste Applications', ['Carbon credit projects', 'Compost enhancement', 'Waste management systems', 'Environmental engineering applications'])]
    ah = ''.join('<div class="app-group"><h3>%s</h3>%s</div>' % (t, chips(i)) for t, i in apps)
    benefit = [('leaf', 'Soil Enhancement', '20–40% crop yield improvement in 2 seasons. Dramatically improves water retention and microbial activity.'),
               ('globe', 'Carbon Sequestration', 'Locks CO₂ for 100–1,000+ years. Eligible for Puro.earth, Verra, and Gold Standard carbon credits ($200–$600/t).'),
               ('drop', 'Water Filtration', 'High porosity removes heavy metals, nitrates, and organic contaminants from water systems.'),
               ('bolt', 'Industrial Uses', 'Battery additive, supercapacitors, building materials, activated carbon substitute.')]
    cards = ''.join(f'<div class="card reveal"><span class="ico" style="background:var(--green-soft);color:var(--green)">{icon(i)}</span><h3>{t}</h3><p>{d}</p></div>' for i, t, d in benefit)
    body = f'''<section class="page-hero brand-green" style="background:linear-gradient(180deg,#fff 0%,var(--green-soft) 100%)"><div class="wrap">{crumbs([(None, 'BIOCHAARGOLD')], '')}<div class="ph-grid"><div>
<img src="assets/img/logo-biochaargold.webp" alt="BIOCHAARGOLD — Accelerating Carbon Cultivation" class="hero-logo" width="260" height="260">
<span class="eyebrow">Bio-ChaarGold · Our biochar brand</span><h1 style="font-size:clamp(2.2rem,4.4vw,3.6rem)">Transforming biomass into lasting impact</h1>
<p class="lead">Healing the Earth, sequestering carbon, and strengthening agriculture.</p>
<div class="btn-row"><a class="btn btn-dark" href="#join">Request a Quote</a><a class="btn btn-line" href="assets/brochures/biochaargold-brochure.pdf" download>{icon('download')} Brochure (PDF)</a></div></div>
<div class="ph-media reveal">{img('biochar-bag', 'BIOCHAARGOLD biochar bag', '', lazy=False)}</div></div></div></section>
<section class="section"><div class="wrap split top"><div class="reveal">
<p class="lead">Bio-ChaarGold’s Biochar is a premium carbon-rich material produced through the controlled thermal conversion of biomass using advanced pyrolysis technology in a low-oxygen environment. Unlike conventional charcoal, which is primarily intended as a fuel source, our biochar is specifically engineered and tested for beneficial applications in agriculture, environmental management, carbon sequestration, and industrial systems.</p>
<p>Developed through years of research, engineering expertise, and practical field experience, BioChaarGold Biochar is designed to enhance soil health, improve resource efficiency, and support long-term sustainability goals. Its highly porous structure creates an ideal habitat for beneficial soil microorganisms while improving water retention, nutrient availability, and soil aeration.</p></div>
<div class="reveal"><p>One of biochar’s most remarkable attributes is its ability to capture and store carbon in a stable form for centuries, and in many cases, millennia. Through the pyrolysis process, atmospheric carbon absorbed by plants during growth is converted into a durable carbon structure that resists decomposition. When incorporated into soil, this carbon remains locked away rather than being released back into the atmosphere, making biochar one of the most promising nature-based solutions for long-term carbon sequestration and climate change mitigation.</p>
<p>At BioChaarGold, we view biochar as more than just a product — it is a tool for regeneration. By transforming agricultural and forestry biomass into valuable carbon resources, we help create a circular economy where waste becomes wealth, soils become healthier, and carbon becomes a resource rather than a liability.</p></div></div></section>
<section class="section bg-cream"><div class="wrap">{head('At a glance', 'What biochar does', '', False)}<div class="grid g4">{cards}</div></div></section>
<section class="section"><div class="wrap split"><div class="reveal imgcard">{img('power-of-biochar', 'Infographic: The power of biochar — healthier soil, stronger plants, greater impact', '')}</div>
<div class="reveal brand-green"><span class="eyebrow">Key benefits</span><h2>Key benefits of Bio-ChaarGold biochar</h2>{checks(kb)}
<h3 style="margin-top:2rem">Creating lasting impact</h3><p>Every ton of BIO-CHAARGOLD Biochar represents a commitment to healthier soils, more productive agriculture, and a lower-carbon future. Whether applied in farming, environmental restoration, carbon credit initiatives, or industrial applications, our biochar delivers measurable value while supporting global sustainability objectives.</p></div></div></section>
<section class="section bg-cream"><div class="wrap split"><div class="reveal"><span class="eyebrow">The cycle</span><h2>The biochar cycle: from nature to a better future</h2><p class="lead">Feedstock, production, innovation, carbon credits, soil application, community and climate action — every link in the chain keeps carbon working.</p></div><div class="reveal imgcard" style="max-width:520px;margin-inline:auto">{img('biochar-cycle', 'The biochar cycle: feedstock, production, innovation, carbon credits, sustainability, soil health, soil application, community and climate action', '')}</div></div></section>
<section class="section"><div class="wrap split top"><div class="brand-green">{head('Applications', 'Where biochar works')}{ah}</div>
<div class="brand-green">{head('Specification', 'Typical values')}{table([('Product Name', 'BIO-CHAARGOLD® Biochar'), ('Appearance', 'Black Porous Granular Material'), ('Fixed Carbon', '65 – 85%'), ('Moisture Content', '<10%'), ('Ash Content', '<15%'), ('pH', '7.5 – 10.0'), ('Bulk Density', '180 – 350 kg/m³'), ('Water Holding Capacity', 'High'), ('Carbon Stability', 'Very High'), ('Carbon Retention Period', 'Hundreds to Thousands of Years')], cls='green')}<p class="note">Specifications can be customized based on customer requirements and intended applications. <a href="products/biochar.html">Full specification →</a></p></div></div></section>
<section class="section tight"><div class="wrap"><figure class="figure shadow reveal">{img('biochar-pallets', 'Bio-ChaarGold premium biochar bags stacked on pallets', '')}<figcaption>BiocharGold, our premium biochar, carefully packed and prepared for dispatch to our customers, supporting healthier soils and sustainable agricultural practices.</figcaption></figure></div></section>
<section class="section tight" id="join"><div class="wrap"><div class="cta-band reveal" style="background:var(--green)"><span class="eyebrow" style="color:var(--gold)">Join the biochar revolution</span><h2>Empower your soil, capture carbon, create lasting impact</h2><p>Empower your soil, capture carbon, and create lasting environmental impact with BIO-CHAARGOLD’s premium biochar solutions.</p>
<div class="cta-trio"><a class="btn btn-gold" href="products/biochar.html#quote">Request a Quote</a><a class="btn btn-line" href="products/biochar.html#team">Connect with Our Team</a><a class="btn btn-line" href="products/biochar.html#partner">Become a Distribution Partner</a></div></div></div></section>'''
    write('biochaargold.html', 'BIOCHAARGOLD — Premium Biochar', 'Bio-ChaarGold premium biochar: engineered for soil health, long-term carbon sequestration and industrial uses.', body, '0.9', og_img='logo-biochaargold')

# ------------------------------------------------------------------ sustainability
def sustainability():
    commit = [('globe', 'Carbon sequestration & climate action', 'Bio-ChaarGold biochar acts as a long-term carbon sink by locking atmospheric carbon into a stable form that can remain in soils for hundreds to thousands of years.',
               ['Reduce greenhouse gas emissions', 'Capture and store atmospheric carbon', 'Improve soil carbon stocks', 'Support global climate action initiatives', 'Enable carbon-negative agricultural practices']),
              ('recycle', 'Waste-to-value innovation', 'Agricultural residues are often treated as waste and burned in open fields, creating pollution and releasing carbon into the atmosphere. At ChaarGold, we view biomass as a valuable resource. We convert:',
               ['Wild Weeds', 'Coconut shells', 'Coconut husks', 'Agricultural residues', 'Wood waste', 'Forestry by-products', 'Other sustainable biomass feedstocks'])]
    reg = [('Enhanced Plant Growth', 'tree'), ('Improved Soil Structure', 'leaf'), ('Increased Water Retention', 'drop'), ('Enhanced Microbial Activity', 'flask'), ('Reduced Nutrient Leaching', 'shield'), ('Natural Weed Suppression', 'sun'), ('Improved Pest and Disease Management', 'bug'), ('Compost Enhancement', 'recycle')]
    rh = ''.join(f'<div class="tile reveal"><span style="display:block;color:var(--green);margin-bottom:.7rem"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{_I[i]}</svg></span><h3 style="margin:0;font-size:1.05rem">{t}</h3></div>' for t, i in reg)
    value = [('Farmers', 'through improved agricultural productivity', 'tree'), ('Industries', 'through sustainable carbon solutions', 'factory'), ('Communities', 'through reduced waste and emissions', 'users'), ('Businesses', 'through circular economy opportunities', 'chart'), ('Future generations', 'through responsible resource management', 'leaf')]
    vh = ''.join(f'<div class="card reveal"><span class="ico" style="background:var(--green-soft);color:var(--green)">{icon(i)}</span><h3>{t}</h3><p>{d}</p></div>' for t, d, i in value)
    cm = ''.join(f'<div class="card reveal flat"><span class="ico" style="background:var(--green-soft);color:var(--green)">{icon(i)}</span><h3>{t}</h3><p>{d}</p><div style="margin-top:1rem" class="green">{checks(l)}</div></div>' for i, t, d, l in commit)
    blog = load('blog.json')
    pyro = ['Maximize biomass utilization', 'Reduce smoke emissions', 'Recover valuable by-products', 'Improve fuel efficiency', 'Minimize environmental impact', 'Increase production consistency']
    mfg = ['Efficient resource utilization', 'Reduced waste generation', 'Biomass valorization', 'Continuous process improvement', 'Worker safety and training', 'Responsible sourcing practices']
    body = f'''<section class="page-hero brand-green" style="padding-bottom:0"><div class="wrap">{crumbs([(None, 'Sustainability')], '')}<span class="eyebrow">Sustainability at ChaarGold</span><h1 style="max-width:900px">Sustainability is not a tagline — it is the foundation of every decision we make.</h1></div>
<div class="wrap" style="margin-top:36px"><div class="banner" style="border-radius:24px 24px 0 0">{img('sustainability-banner', 'Sustainability at ChaarGold — a hand holding a seedling in soil against green hills', '', lazy=False)}</div></div></section>
<section class="section"><div class="wrap split"><div class="reveal brand-green"><span class="eyebrow">Building a circular carbon economy</span><h2>Waste becomes a resource</h2></div>
<div class="reveal"><p class="lead">At ChaarGold, sustainability is not a department — it is the foundation of everything we do. Our mission is to transform agricultural and biomass residues into high-value carbon products that create economic, environmental, and social impact.</p>
<p>Through advanced pyrolysis technology, we convert underutilized biomass into premium charcoal and briquettes, biochar, wood vinegar, and other carbon-based products while reducing waste, sequestering carbon, and supporting regenerative agriculture.</p>
<p><b style="color:var(--green)">Healing the earth, sequestering carbon, and boosting agricultural yields — one kilogram at a time.</b></p></div></div></section>
<section class="section bg-cream"><div class="wrap">{head('Our sustainability commitment', 'Climate action, from waste to wealth')}<div class="grid g2">{cm}</div>
<p style="margin-top:2rem" class="center"><b style="color:var(--ink)">Every tonne of biochar applied to soil contributes to measurable carbon removal while improving land productivity.</b></p>
<p class="center">Through a controlled pyrolysis process, this approach creates a circular economy where waste becomes a resource and environmental challenges become opportunities.</p></div></section>
<section class="section"><div class="wrap">{head('Supporting regenerative agriculture', 'Our Bio-ChaarGold products help farmers build healthier, more resilient soils')}<div class="grid g4">{rh}</div>
<p class="lead center" style="margin-top:2rem;max-width:760px;margin-inline:auto">By improving soil health naturally, biochar helps reduce dependence on synthetic inputs while supporting sustainable food production.</p></div></section>
<section class="section bg-ink"><div class="wrap split top"><div class="reveal"><span class="eyebrow">Cleaner production through pyrolysis</span><h2>Better than traditional charcoal-making</h2><p>Traditional charcoal production often results in significant emissions and resource inefficiencies. ChaarGold’s pyrolysis systems are designed to:</p>{checks(pyro)}<p style="margin-top:1.4rem">Our kiln technology continuously evolves through engineering innovation and operational improvements developed over years of practical experience.</p></div>
<div class="reveal"><span class="eyebrow">Sustainable by-product recovery</span><h2>Pyrolysis generates more than charcoal</h2><p>Our integrated systems enable the recovery and utilization of valuable co-products such as <b style="color:#fff">wood vinegar</b> — a natural liquid derived from biomass pyrolysis that can be used in agriculture, composting, soil conditioning, odor control and organic farming applications.</p><a class="btn btn-gold" href="products/wood-vinegar.html">About wood vinegar {icon('arrow')}</a>
<h3 style="margin-top:2.2rem">Sustainable manufacturing</h3><p>Our facilities are designed around responsible production principles:</p>{checks(mfg)}<p style="margin-top:1rem">We believe industrial growth and environmental stewardship can — and should — go hand in hand.</p></div></div></section>
<section class="section"><div class="wrap">{head('Creating shared value', 'Sustainability extends beyond environmental responsibility', 'Through our operations, we create value for:')}<div class="grid g3" style="grid-template-columns:repeat(auto-fit,minmax(220px,1fr))">{vh}</div></div></section>
<section class="section bg-cream"><div class="wrap split"><div class="reveal"><span class="eyebrow">Ancient wisdom, modern carbon</span><h2>Terra preta: the ancient blueprint for modern biochar</h2><p>Perhaps the most important historical discovery for modern biochar came from soil science in the Amazon basin. In the 1990s, researchers discovered <i>terra preta de Índio</i> — “Indian dark earth” — soils that were dramatically more fertile than surrounding tropical soils and had been so for over 2,000 years.</p><p>The biochar, and the extraordinary fertility it supports, has persisted for two millennia. As a biochar manufacturer in India, ChaarGold draws direct inspiration from this ancient knowledge — scaled, certified, and made available to India’s farming households.</p><a class="link-arrow" href="blog.html#art-10">Read the history of charcoal →</a></div>
<div class="reveal"><h3>Our vision for the future</h3><p>We envision a future where biomass waste is no longer discarded, where carbon is returned to the soil, and where sustainable carbon products drive environmental restoration and economic growth.</p><p>Through innovation, engineering excellence, and a commitment to responsible manufacturing, ChaarGold is working to build a cleaner, greener, and more sustainable world.</p><p class="gold" style="font:italic 600 1.5rem var(--font-display)">Crafting Carbon Perfection. Creating a Sustainable Future.</p></div></div></section>
{cta_band('Build a lower-carbon future with us', 'Talk to our team about biochar, carbon projects and sustainable fuels.', '')}'''
    write('sustainability.html', 'Sustainability', 'How ChaarGold turns biomass waste into premium carbon products, sequesters carbon with biochar and supports regenerative agriculture.', body, '0.8', og_img='sustainability-banner')

# ------------------------------------------------------------------ gallery
def gallery():
    items = [('gallery-biochar-2026', 'BiochaarGold at Biochar 2026, Hyderabad', 'As a prime sponsor of Biochar 2026, BiochaarGold proudly contributed to the conversation on India’s biochar revolution, with our Founder and Chief Technology Officer, Prem Raj (centre), sharing his insights on the future of biochar and sustainable carbon solutions in India.'),
             ('gallery-honeycomb', 'Igniting a new era of cooking', 'CHAARGOLD’s Honeycomb Charcoal Briquette burns bright, harnessing the power of innovative design to bring new possibilities to cooking. With its distinctive perforated structure and steady airflow, it represents a fresh approach to charcoal-fuelled cooking — where tradition meets innovation with CHAARGOLD.'),
             ('gallery-kilns', 'Engineering the future of carbon', 'At CHAARGOLD, our pyrolysis kilns are manufactured with a focus on robust engineering, precision fabrication and dependable performance. Each unit represents our commitment to advancing biomass carbonisation and biochar production through practical, scalable solutions for a more sustainable carbon future.'),
             ('gallery-drying', 'Precision drying for consistent quality', 'At CHAARGOLD, the drying of charcoal briquettes is an essential step in achieving consistent quality and durability. Our drying process helps reduce moisture content, preparing our Pillow, Hexagonal and Honeycomb briquettes for reliable handling, storage and dispatch.')]
    g = ''.join(f'<figure class="reveal"><button class="gimg" type="button" data-full="assets/img/{i}.webp" aria-label="Enlarge: {html.escape(t)}">{img(i, t, "")}</button><figcaption><b>{esc(t)}</b>{esc(d)}</figcaption></figure>' for i, t, d in items)
    body = f'''<section class="page-hero"><div class="wrap">{crumbs([(None, 'Gallery')], '')}<span class="eyebrow">Gallery</span><h1>Life at ChaarGold</h1><p class="lead" style="max-width:720px">From the kiln floor and drying racks to industry stages — a look at how we craft carbon.</p></div></section>
<section class="section"><div class="wrap"><div class="gal">{g}</div></div></section>
<div class="lightbox" role="dialog" aria-modal="true" aria-label="Enlarged image"><button type="button" aria-label="Close">×</button><img alt=""></div>
{cta_band('See it for yourself', 'Visit our Penukonda facility or talk to our team about your project.', '')}'''
    write('gallery.html', 'Gallery', 'Photos from ChaarGold: Biochar 2026, pyrolysis kilns, briquette drying and honeycomb briquette cooking.', body, '0.6')

# ------------------------------------------------------------------ blog
def blog():
    arts = load('blog.json'); out = ''
    for i, a in enumerate(arts, 1):
        paras = a['body']
        intro = next(t for k, t in paras if k == 'p')
        excerpt = intro if len(intro) < 260 else intro[:257].rsplit(' ', 1)[0] + '…'
        rest = ''.join('<h4>%s</h4>' % esc(t) if k == 'h' else '<p>%s</p>' % esc(t) for k, t in paras)
        out += f'''<article class="art reveal" id="art-{i}"><div class="art-head"><span class="no">Resource {i:02d}</span><h3>{esc(a['title'])}</h3><p>{esc(excerpt)}</p><button class="art-toggle" type="button" aria-expanded="false">Read full article</button></div><div class="art-body prose">{rest}</div></article>'''
    body = f'''<section class="page-hero"><div class="wrap">{crumbs([(None, 'Blog')], '')}<span class="eyebrow">Resources</span><h1>Insights from the kiln floor</h1><p class="lead" style="max-width:720px">Guides on briquettes, biochar, pyrolysis, wood vinegar and the carbon economy — written by the people who make it.</p></div></section>
<section class="section"><div class="narrow" style="width:min(100% - 40px,900px)">{out}</div></section>
{cta_band('Have a question these articles don’t answer?', 'Our specialists are happy to help with products, projects and supply.', '')}'''
    write('blog.html', 'Blog & Resources', 'ChaarGold resources: charcoal briquette buying guide, biochar 101, how pyrolysis kilns work, wood vinegar, carbon markets and more.', body, '0.7')

# ------------------------------------------------------------------ contact
def contact():
    types = ['Charcoal Briquettes', 'Biochar', 'Pyrolysis & Retort Systems', 'Turnkey Carbon Projects', 'Bulk Orders', 'Business Partnerships', 'Other']
    opts = ''.join('<option>%s</option>' % esc(t) for t in types)
    body = f'''<section class="page-hero"><div class="wrap">{crumbs([(None, 'Contact Us')], '')}<span class="eyebrow">Contact us</span><h1>Let’s build better carbon solutions together</h1>
<p class="lead" style="max-width:780px">At CHAARGOLD, we believe in creating value through quality charcoal products, innovative carbon technologies and sustainable solutions. Whether you are looking for premium charcoal briquettes, biochar, pyrolysis and retort kilns/systems, or turnkey solutions for carbon projects, our team is ready to assist.</p></div></section>
<section class="section"><div class="wrap split top">
<div class="reveal"><span class="eyebrow">Get in touch</span><h2>We’d love to hear from you</h2><p>Get in touch with us to discuss your requirements, explore our products or enquire about business collaborations. We look forward to working with you.</p>
<div class="grid" style="margin-top:24px">
<div class="contact-card"><span class="ico">{icon('mail')}</span><div><h3>Email us</h3><p>For product enquiries, quotations, bulk orders and business partnerships, reach out to our team by email.</p><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
<div class="contact-card"><span class="ico">{icon('phone')}</span><div><h3>Call us</h3><p>Have questions about our products or services? Connect with our team for information and assistance.</p><a href="tel:+{PHONE_RAW}">{PHONE}</a></div></div>
<div class="contact-card"><span class="ico">{icon('pin')}</span><div><h3>Our locations</h3><p><b style="color:var(--ink)">Head office</b><br>Bengaluru, Karnataka, India</p><p style="margin:0"><b style="color:var(--ink)">Manufacturing facility</b><br>Penukonda, Andhra Pradesh, India</p></div></div>
<div class="contact-card"><span class="ico">{icon('instagram')}</span><div><h3>Connect with us</h3><p>Follow CHAARGOLD on social media to stay updated on our products, manufacturing activities, latest developments and carbon solutions.</p><p style="margin:0"><a href="{INSTAGRAM}">Instagram</a> &nbsp; <a href="{FACEBOOK}">Facebook</a></p></div></div>
</div></div>
<div class="reveal form-box" id="enquiry"><h3>Send us an enquiry</h3><p>Have a specific requirement or project in mind? Share your details with us, and our team will get in touch to understand your needs and discuss the next steps.</p>
<form class="form" data-enquiry data-subject="Enquiry — ChaarGold website">
<div class="row">{field('Full Name', 'e-name', req=True)}{field('Company Name', 'e-company')}</div>
<div class="row">{field('Email Address', 'e-email', 'email', True)}{field('Phone Number', 'e-phone', 'tel')}</div>
<div class="row">{field('Country', 'e-country')}<div class="field"><label for="e-type">Enquiry Type</label><select id="e-type" name="type" data-label="Enquiry type">{opts}</select></div></div>
<div class="field"><label for="e-msg">Message</label><textarea id="e-msg" name="message" data-label="Message"></textarea></div>
<div><button class="btn btn-gold" type="submit">Submit Enquiry {icon('arrow')}</button></div>
<p class="form-msg" role="status">Thank you — your email app should have opened with your enquiry. If it didn't, write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></form>
<p class="note">We value your interest in CHAARGOLD and look forward to exploring how we can support your business.</p></div></div></section>'''
    write('contact.html', 'Contact Us', 'Contact ChaarGold for quotations, bulk orders, biochar, pyrolysis kilns and partnerships. Bengaluru head office; Penukonda manufacturing facility.', body, '0.8')

# ------------------------------------------------------------------ faq
def faq():
    data = load('faq.json'); groups = []; cur = None
    for s, t in data:
        if s == 'Heading1' or t.startswith('———'): continue
        if s in ('Heading3', 'Heading4'):
            if t.startswith('What is BIOCHAARGOLD') or cur is None:
                cur = {'t': 'Biochar, kilns & wood vinegar' if cur else 'About CHAARGOLD & our products', 'q': []}; groups.append(cur)
            cur['q'].append([t, []])
        elif cur and cur['q']: cur['q'][-1][1].append(t)
    gh = ''
    for g in groups:
        qs = ''.join('<details><summary>%s</summary><div class="ans">%s</div></details>' % (esc(q), ''.join('<p>%s</p>' % esc(a) for a in ans)) for q, ans in g['q'])
        gh += '<div class="faq-group faq"><h2>%s</h2>%s</div>' % (esc(g['t']), qs)
    ld = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': ' '.join(a)}} for g in groups for q, a in g['q']]}
    schema = '<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False)
    body = f'''<section class="page-hero"><div class="wrap">{crumbs([(None, 'FAQ')], '')}<span class="eyebrow">Help</span><h1>Frequently asked questions</h1><p class="lead" style="max-width:720px">Everything about our briquettes, biochar, kilns and turnkey projects. Can’t find your answer? <a href="contact.html" class="link-arrow">Ask our team</a>.</p></div></section>
<section class="section"><div class="narrow" style="width:min(100% - 40px,900px)">{gh}</div></section>
{cta_band('Still have questions?', 'Our specialists will help with product details, technical enquiries and customised project requirements.', '')}'''
    write('faq.html', 'Frequently Asked Questions', 'Answers about ChaarGold charcoal briquettes, biochar, pyrolysis kilns, wood vinegar, bulk orders and turnkey carbon projects.', body, '0.6', schema=schema)
    return groups

# ------------------------------------------------------------------ terms
def terms():
    data = load('terms.json'); out = []; inlist = False; title = ''; eff = ''
    for s, t in data:
        if s == 'ListParagraph' and not inlist: out.append('<ol>'); inlist = True
        elif s != 'ListParagraph' and inlist: out.append('</ol>'); inlist = False
        if s == 'Heading2' and not title: title = t
        elif t.startswith('Effective Date'): eff = t
        elif s == 'Heading3': out.append('<h3>%s</h3>' % esc(t))
        elif s in ('Heading4', 'Heading5'): out.append('<h4>%s</h4>' % esc(t))
        elif s == 'ListParagraph': out.append('<li>%s</li>' % esc(t))
        elif s == 'Heading2': out.append('<h2>%s</h2>' % esc(t))
        else: out.append('<p>%s</p>' % esc(t))
    if inlist: out.append('</ol>')
    body = f'''<section class="page-hero"><div class="wrap">{crumbs([(None, 'Terms')], '')}<span class="eyebrow">Legal</span><h1 style="font-size:clamp(1.8rem,3.4vw,2.8rem)">{esc(title.title().replace('&', '&'))}</h1><p class="lead">{esc(eff)}</p></div></section>
<section class="section"><div class="narrow terms prose">{''.join(out)}</div></section>'''
    write('terms.html', 'Terms & Conditions', 'Standard terms and conditions of sale, supply, installation and commissioning for CHAARGOLD and BIOCHAARGOLD.', body, '0.3')

# ------------------------------------------------------------------ site files
def site_files():
    urls = ''.join('<url><loc>%s/%s</loc><priority>%s</priority></url>' % (DOMAIN, p if p != 'index.html' else '', pr) for p, pr in PAGES)
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>' % urls)
    open(os.path.join(ROOT, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n' % DOMAIN)

if __name__ == '__main__':
    home(); about(); products_index(); build_products(); biochaargold(); sustainability(); gallery(); blog(); contact()
    g = faq(); terms(); site_files()
    print(len(PAGES), 'pages;', 'faq groups:', [(x['t'], len(x['q'])) for x in g])
