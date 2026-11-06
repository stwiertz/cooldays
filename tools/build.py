"""Génère les pages HTML du site (FR à la racine, NL dans nl/, DE dans de/).

Usage, depuis la racine du projet :  python tools/build.py
Nécessite Pillow (pip install pillow), uniquement pour lire la taille des images.
Les textes sont dans tools/i18n.py. Attention : écrase les fichiers .html générés.
"""
import os, sys, json, html
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i18n import T, PHOTO_ALTS

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ["fr", "nl", "de"]
LI = {"fr": 0, "nl": 1, "de": 2}
PAGES = ["index.html", "gite-1.html", "gite-2.html", "photos.html", "tarifs.html", "seminaire.html", "environs.html", "contact.html"]

_dims = {}
def dims(rel):
    if rel not in _dims:
        with Image.open(os.path.join(ROOT, rel)) as im:
            _dims[rel] = im.size
    return _dims[rel]

esc = lambda s: html.escape(s, quote=True)

class Page:
    def __init__(self, lang, name):
        self.lang, self.name, self.t = lang, name, T[lang]
        self.up = "" if lang == "fr" else "../"

    def a(self, rel):  # chemin vers une ressource
        return self.up + rel

    def url(self, lang, name):
        return self.up + ("" if lang == "fr" else lang + "/") + name

    def img(self, rel, alt, cls="", lazy=True, extra=""):
        w, h = dims(rel)
        s = f'<img src="{self.a(rel)}" alt="{esc(alt)}" width="{w}" height="{h}"'
        if cls: s += f' class="{cls}"'
        if lazy: s += ' loading="lazy" decoding="async"'
        if extra: s += " " + extra
        return s + ">"

def svg(d, size=20, sw=2.2, stroke="currentColor", style=""):
    st = f' style="{style}"' if style else ""
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{stroke}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"{st}>{d}</svg>')

I_CAL = '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>'
I_PHONE = '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>'
I_MAIL = '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>'
I_ARROW = '<path d="M5 12h14M13 5l7 7-7 7"/>'
I_CHECK = '<path d="M20 6 9 17l-5-5"/>'
I_MENU = '<path d="M3 6h18M3 12h18M3 18h18"/>'
I_PIN = '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>'
ARROW = svg(I_ARROW, 18, 2.4)

def check_list(items):
    li = "".join(f'<li>{svg(I_CHECK, 20, 3, "#A2B52F")}<span>{t}</span></li>' for t in items)
    return f'<ul class="checks">{li}</ul>'

TEL_FIXE = ("+3287785307", "087 78 53 07")
TEL_MN = ("+32495706985", "0495 70 69 85")
TEL_CH = ("+32474726595", "0474 72 65 95")
EMAIL = "info@cooldays.be"
STREET, CITY = "Rue de Beusdael 81", "4851 Sippenaeken"
ADDRESS = f"{STREET}, {CITY}"
MAPS = "https://www.google.com/maps/dir/?api=1&destination=Rue+de+Beusdael+81%2C+4851+Sippenaeken%2C+Belgique"

NAV = [("gites", "index.html#gites", "var(--pink)"), ("sem", "seminaire.html", "var(--violet)"),
       ("tarifs", "tarifs.html", "var(--orange)"), ("env", "environs.html", "var(--plum)"),
       ("photos", "photos.html", "var(--cyan)"), ("contact", "contact.html", "var(--grey)")]

G1 = ["communes1", "communes3", "communes2", "communes8", "communes6", "communes7", "img_6856", "img_6867",
      "chambres2", "chambres3", "chambres0", "chambres1", "chambres9", "chambres13", "chambres4", "chambres7",
      "chambres6", "chambres16", "chambres8", "communes10", "communes12", "communes11", "communes13",
      "communes14", "communes15", "environs9", "environs6", "environs10"]
G2 = ["mg_4724", "mg_4742", "mg_4763", "mg_4717", "img_5378", "img_5370", "img_5377", "img_5496b",
      "img_5415", "img_5413", "img_5416", "img_5417", "img_5403", "img_5397", "img_5400", "img_6879",
      "img_5429", "img_5439", "img_5430", "img_5441", "img_5469", "img_5445", "img_5449", "img_5451",
      "img_5482", "img_5461", "img_5468", "img_5487"]

def gallery(p, folder, names):
    out = []
    for n in names:
        rel = f"assets/img/{folder}/{n}.jpg"
        out.append(f'<a href="{p.a(rel)}">{p.img(rel, PHOTO_ALTS[n][LI[p.lang]])}</a>')
    return '<div class="gallery">' + "".join(out) + "</div>"

def euro(lang, v):
    if lang == "fr":
        return f"{v:,}".replace(",", " ") + " €"
    s = f"{v:,}".replace(",", ".")
    return f"€ {s}" if lang == "nl" else f"{s} €"

# ---------- Gabarit ----------
def head(p, title, desc, extra=""):
    alt = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{p.url(l, p.name)}">' for l in LANGS)
    return f"""<!DOCTYPE html>
<html lang="{p.lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<!-- Version de test : à retirer à la mise en ligne définitive -->
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#5C5850">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{p.a('assets/img/exterieur.jpg')}">
<meta property="og:locale" content="{p.t['locale']}">
{alt}
<link rel="icon" type="image/png" href="{p.a('assets/img/logo.png')}">
<link rel="preload" href="{p.a('assets/fonts/baloo2-latin.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{p.a('assets/fonts/nunito-sans-latin.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{p.a('assets/css/style.css')}">
<script>document.documentElement.classList.add("js")</script>
<script src="{p.a('assets/js/main.js')}" defer></script>
{extra}</head>
"""

def lang_switch(p, cls):
    links = "".join(
        f'<a href="{p.url(l, p.name)}" hreflang="{l}" lang="{l}"' + (' aria-current="true"' if l == p.lang else "") + f">{l.upper()}</a>"
        for l in LANGS)
    return f'<nav class="lang {cls}" aria-label="{p.t["lang_label"]}">{links}</nav>'

def header(p, active, home=False):
    t = p.t
    nav = "\n".join(
        f'<a href="{href}" style="--c:{c}"' + (' aria-current="page"' if key == active else "") + f">{label}</a>"
        for (key, href, c), label in zip(NAV, t["nav"]))
    return f"""<body{' class="is-home"' if home else ''}>
<a class="skip-link" href="#contenu">{t['skip']}</a>
<header class="site-header">
<div class="wrap">
<a class="header-logo" href="index.html" aria-label="{t['home_label']}">{p.img("assets/img/logo.png", "Cool Days", lazy=False)}</a>
<nav class="main-nav" id="menu" aria-label="{t['nav_label']}">
{nav}
{lang_switch(p, "lang--menu")}
</nav>
<div class="header-actions">
{lang_switch(p, "lang--header")}
<a class="header-call" href="tel:{TEL_MN[0]}" aria-label="{t['call_label']} {TEL_MN[1]}">{svg(I_PHONE, 22, 2)}</a>
<button type="button" class="menu-toggle" aria-expanded="false" aria-controls="menu">{svg(I_MENU, 20, 2.4)}{t['menu']}</button>
<a class="btn btn--lime" href="contact.html">{t['cta']}</a>
</div>
</div>
</header>
<main id="contenu">
"""

def contact_strip(p):
    t = p.t
    return f"""<section class="contact-strip" aria-labelledby="question">
<div class="wrap">
<div class="text">
<h2 id="question">{t['question']}</h2>
<p class="muted">{ADDRESS} · <a href="{MAPS}" style="font-weight:700">{t['itinerary']}</a></p>
</div>
<div class="actions">
<a class="btn btn--lime btn--lg" href="tel:{TEL_FIXE[0]}">{svg(I_PHONE, 20, 2)}{TEL_FIXE[1]}</a>
<a class="btn btn--lg" href="tel:{TEL_MN[0]}">GSM {TEL_MN[1]}</a>
<a class="btn btn--lg" href="mailto:{EMAIL}">{svg(I_MAIL, 20, 2)}{EMAIL}</a>
</div>
</div>
</section>
"""

def footer(p):
    t = p.t
    fl = t["footer_links"]
    return f"""</main>
<img class="footer-hill" src="{p.a('assets/img/colline.png')}" alt="" width="1262" height="240" loading="lazy">
<footer class="site-footer">
<div class="wrap">
<div class="footer-top">
<strong>Cool Days · Sippenaeken</strong>
<a href="environs.html#liens">{fl[0]}</a>
<a href="photos.html">{fl[1]}</a>
<a href="tarifs.html">{fl[2]}</a>
<a href="contact.html">{fl[3]}</a>
</div>
<div class="footer-bottom">
<address>
{t['owners']} · {ADDRESS}<br>
<a href="tel:{TEL_FIXE[0]}">{TEL_FIXE[1]}</a> · <a href="tel:{TEL_MN[0]}">{TEL_MN[1]}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a>
</address>
{lang_switch(p, "lang--footer")}
<div class="labels">
<a href="http://www.accueilchampetre.be/fr/wiertz#890-gite-a-la-ferme-cool-days">{p.img("assets/img/label-accueil-champetre.png", "Accueil Champêtre en Wallonie")}</a>
<a href="http://www.walloniedestinationqualite.be/fr/accueil.html?IDC=747">{p.img("assets/img/label-wallonie-qualite.png", "Wallonie Destination Qualité")}</a>
</div>
</div>
</div>
</footer>
<nav class="quick-actions" aria-label="{t['quick_label']}">
<a class="btn" href="tel:{TEL_MN[0]}">{svg(I_PHONE, 20, 2)}{t['call']}</a>
<a class="btn btn--lime" href="contact.html">{t['cta']}</a>
</nav>
</body>
</html>
"""

def page_hero(p, tag_cls, tag, title, intro):
    cloud = p.a("assets/img/nuage.png")
    return f"""<section class="page-hero">
<img class="cloud cloud--a" src="{cloud}" alt="" width="47" height="39">
<img class="cloud cloud--b" src="{cloud}" alt="" width="47" height="39">
<div class="wrap">
<span class="tag {tag_cls}">{tag}</span>
<h1>{title}</h1>
<p>{intro}</p>
</div>
</section>
"""

def write(p, content):
    d = ROOT if p.lang == "fr" else os.path.join(ROOT, p.lang)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, p.name), "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

# ================= ACCUEIL =================
def build_index(lang):
    p = Page(lang, "index.html"); t = p.t; nav = t["nav"]
    jsonld = {
        "@context": "https://schema.org", "@type": "LodgingBusiness", "name": "Cool Days",
        "description": t["home_desc"],
        "address": {"@type": "PostalAddress", "streetAddress": STREET, "postalCode": "4851",
                    "addressLocality": "Sippenaeken", "addressCountry": "BE"},
        "telephone": "+32 87 78 53 07", "email": EMAIL,
    }
    s = head(p, t["home_title"], t["home_desc"], f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>\n')
    s += header(p, "", home=True)
    cloud = p.a("assets/img/nuage.png")
    stats = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in t["stats"])
    chips = "".join(f'<span class="chip">{c}</span>' for c in t["garden_items"])
    teaser = "".join(f'<a class="link-card" href="environs.html#{slug}"><strong>{n}</strong><span>{d}</span></a>' for slug, n, d in t["env_teaser"])
    hp = list(zip(["gite-2/img_5378", "gite-1/communes10", "gite-2/img_5469", "gite-1/environs9"], t["home_photo_alts"]))
    photos = "".join(f'<a href="{p.a("assets/img/" + r + ".jpg")}">{p.img("assets/img/" + r + ".jpg", alt)}</a>' for r, alt in hp)

    def card(n, rel, alt, points):
        return f"""<article class="card">
{p.img(rel, alt)}
<div class="card-body">
<h3>{t['gite'].format(n=n)} <small>· {t['people'].format(n=22 if n == 1 else 20)}</small></h3>
{check_list(points)}
<div class="card-actions">
<a class="btn" href="gite-{n}.html">{t['discover'].format(n=n)} {ARROW}</a>
<a href="photos.html#photos-gite-{n}">{t['photos_link']}</a>
</div>
</div>
</article>"""

    s += f"""<section class="hero">
<img class="cloud cloud--a" src="{cloud}" alt="" width="47" height="39">
<img class="cloud cloud--b" src="{cloud}" alt="" width="47" height="39">
<div class="wrap">
<a class="hero-logo" href="index.html" aria-label="{t['home_label']}">{p.img("assets/img/logo.png", "Cool Days", lazy=False)}</a>
<div class="hero-text">
<span class="kicker">{t['kicker']}</span>
<h1>{t['h1']}</h1>
<p>{t['hero_p']}</p>
<div class="btn-row">
<a class="btn btn--lime btn--lg" href="contact.html">{svg(I_CAL)}{t['cta']}</a>
<a class="btn btn--ghost btn--lg" href="tarifs.html">{t['see_prices']}</a>
</div>
</div>
{p.img("assets/img/exterieur.jpg", t['hero_alt'], "hero-img", lazy=False, extra='fetchpriority="high"')}
</div>
</section>

<section class="stats" aria-label="{t['stats_label']}">
<dl class="wrap">{stats}</dl>
</section>

<section id="gites" class="wrap section" aria-labelledby="gites-titre">
<div class="section-head">
<span class="tag tag--gites">{nav[0]}</span>
<h2 id="gites-titre">{t['gites_h2']}</h2>
</div>
<div class="grid-2">
{card(1, "assets/img/gite-1/communes1.jpg", t['g1_card_alt'], t['g1_points'])}
{card(2, "assets/img/gite-2/img_5415.jpg", t['g2_card_alt'], t['g2_points'])}
</div>
<div class="chips"><strong>{t['garden']}</strong>{chips}</div>
</section>

<section class="wrap section section--tight-top grid-cards" aria-label="{t['prices_sem_label']}">
<div class="card">
<div class="card-band card-band--tarifs">{nav[2]}</div>
<div class="card-body">
<p class="card-big">{t['prices_big']}</p>
<p class="muted">{t['prices_small']}</p>
<div class="card-actions"><a class="btn" href="tarifs.html">{t['prices_btn']}</a></div>
</div>
</div>
<div class="card">
<div class="card-band card-band--sem">{nav[1]}</div>
<div class="card-body">
<p class="card-big">{t['sem_big']}</p>
<p class="muted">{t['sem_small']}</p>
<div class="card-actions"><a class="btn" href="seminaire.html">{t['sem_btn']}</a></div>
</div>
</div>
</section>

<section class="section--pink" aria-labelledby="photos-titre">
<div class="wrap section">
<div class="section-head section-head--row">
<div>
<span class="tag tag--photos">{nav[4]}</span>
<h2 id="photos-titre">{t['tour_h2']}</h2>
</div>
<a class="btn" href="photos.html">{t['see_all_photos']}</a>
</div>
<div class="gallery">{photos}</div>
</div>
</section>

<section class="wrap section" aria-labelledby="env-titre">
<div class="section-head">
<span class="tag tag--env">{nav[3]}</span>
<h2 id="env-titre">{t['env_h2']}</h2>
</div>
<div class="links-grid">{teaser}</div>
</section>
"""
    s += contact_strip(p) + footer(p)
    write(p, s)

# ================= GÎTES =================
def build_gite(lang, n):
    p = Page(lang, f"gite-{n}.html"); t = p.t
    people = 22 if n == 1 else 20
    k = f"g{n}_"
    hero_img = "assets/img/exterieur-2.jpg" if n == 1 else "assets/img/gite-2/mg_4724.jpg"
    floors = ""
    for title, items, note in t[k + "floors"]:
        lis = "".join(f"<li>{i}</li>" for i in items)
        nh = f'<p class="note">{note}</p>' if note else ""
        floors += f'<div class="floor"><h3>{title}</h3><ul>{lis}</ul>{nh}</div>'
    s = head(p, t["gite_title"].format(n=n, p=people), t["gite_desc"].format(n=n, p=people))
    s += header(p, "gites")
    s += page_hero(p, "tag--gites", t["nav"][0], f"{t['gite'].format(n=n)} · {t['people'].format(n=people)}", t[k + "intro"])
    s += f"""<section class="wrap section" aria-labelledby="essentiel">
<div class="grid-2" style="align-items:start">
{p.img(hero_img, t[k + 'img_alt'], extra='style="width:100%;border-radius:22px;aspect-ratio:709/472;object-fit:cover"')}
<div class="callout">
<h2 id="essentiel" style="font-size:30px">{t['essentials']}</h2>
{check_list(t[k + 'extras'])}
<div class="btn-row" style="padding-top:8px">
<a class="btn btn--lime" href="contact.html">{svg(I_CAL)}{t['cta']}</a>
<a class="btn" href="tarifs.html">{t['nav'][2]}</a>
</div>
</div>
</div>
<h2>{t['floor_by_floor']}</h2>
<div class="floors">{floors}</div>
</section>

<section class="section--pink" aria-labelledby="photos-g">
<div class="wrap section">
<div class="section-head section-head--row">
<div><span class="tag tag--photos">{t['nav'][4]}</span><h2 id="photos-g">{t['in_pictures'].format(n=n)}</h2></div>
<a class="btn" href="gite-{3 - n}.html">{t['see_other'].format(n=3 - n)} {ARROW}</a>
</div>
{gallery(p, f"gite-{n}", G1 if n == 1 else G2)}
</div>
</section>
"""
    s += contact_strip(p) + footer(p)
    write(p, s)

# ================= PHOTOS =================
def build_photos(lang):
    p = Page(lang, "photos.html"); t = p.t
    s = head(p, t["photos_title"], t["photos_desc"]) + header(p, "photos")
    s += page_hero(p, "tag--photos", t["nav"][4], t["tour_h2"], t["photos_intro"])
    for n, names in ((1, G1), (2, G2)):
        people = 22 if n == 1 else 20
        inner = f"""<div class="section-head section-head--row">
<div><h2 id="pg{n}">{t['gite'].format(n=n)} · {t['people'].format(n=people)}</h2></div>
<a class="btn" href="gite-{n}.html">{t['discover'].format(n=n)} {ARROW}</a>
</div>
{gallery(p, f"gite-{n}", names)}"""
        if n == 1:
            s += f'<section id="photos-gite-1" class="wrap section" aria-labelledby="pg1">\n{inner}\n</section>\n'
        else:
            s += f'<section id="photos-gite-2" class="section--pink" aria-labelledby="pg2">\n<div class="wrap section">\n{inner}\n</div>\n</section>\n'
    s += '<div style="height:48px"></div>\n' + contact_strip(p) + footer(p)
    write(p, s)

# ================= TARIFS =================
SEASONS = [("s-basse", [1161, 1050, 1050, 1050]), ("s-moyA", [1474, 1323, 1323, 1323]),
           ("s-moyB", [1747, 1464, 1464, 1464]), ("s-haute", [1828, 1555, 1555, 1555]),
           ("s-noel", [2201, None, None, None]), ("s-nouvel", [2605, None, None, None]),
           ("s-speciaux", [1979, 1676, 1676, 1676])]

def build_tarifs(lang):
    p = Page(lang, "tarifs.html"); t = p.t
    def table(caption, factor):
        head_ = "".join(f'<th scope="col">{c}</th>' for c in t["cols"])
        rows = ""
        for (cls, vals), label in zip(SEASONS, t["seasons"]):
            tds = ""
            for c, v in zip(t["cols"], vals):
                if v is None:
                    tds += f'<td class="na" data-label="{c}"><span aria-label="{t["not_offered"]}">–</span></td>'
                else:
                    tds += f'<td data-label="{c}">{euro(lang, v * factor)}</td>'
            rows += f'<tr><th scope="row"><span class="season {cls}">{label}</span></th>{tds}</tr>'
        return f"""<div class="table-box"><table class="price-table">
<caption>{caption}</caption>
<thead><tr><th scope="col">{t['season_col']}</th>{head_}</tr></thead>
<tbody>{rows}</tbody>
</table></div>"""
    legend = "".join(f'<li><span class="season {cls}" style="font-weight:600">{label}</span></li>' for (cls, _), label in zip(SEASONS, t["seasons"]))
    fees = "".join(f"<li><strong>{a}</strong><span>{b}</span></li>" for a, b in t["fees"])
    cal = "assets/img/calendrier-saisons.jpg"
    s = head(p, t["prices_title"], t["prices_desc"]) + header(p, "tarifs")
    s += page_hero(p, "tag--tarifs", t["nav"][2], t["prices_h1"], t["prices_intro"])
    s += f"""<section class="wrap section" aria-label="{t['prices_tables_label']}">
{table(t['table_one'], 1)}
{table(t['table_two'], 2)}
</section>

<section class="wrap section section--tight-top" aria-labelledby="frais">
<div class="section-head">
<h2 id="frais">{t['fees_h2']}</h2>
<p class="lead">{t['fees_intro']}</p>
</div>
<ul class="fees">{fees}</ul>
</section>

<section class="section--pink" aria-labelledby="calendrier">
<div class="wrap section calendar">
<div class="section-head">
<span class="tag tag--tarifs">{t['cal_tag']}</span>
<h2 id="calendrier">{t['cal_h2']}</h2>
<p class="lead">{t['cal_intro']}</p>
</div>
<ul class="legend">{legend}</ul>
<div class="gallery" style="grid-template-columns:minmax(0,640px)"><a href="{p.a(cal)}">{p.img(cal, t['cal_alt'], extra='style="aspect-ratio:auto;object-fit:contain"')}</a></div>
</div>
</section>
<div style="height:48px"></div>
"""
    s += contact_strip(p) + footer(p)
    write(p, s)

# ================= SÉMINAIRE =================
def build_seminaire(lang):
    p = Page(lang, "seminaire.html"); t = p.t
    ph = list(zip(["communes14", "communes11", "communes12", "communes1"], t["sem_photo_alts"]))
    photos = "".join(f'<a href="{p.a("assets/img/gite-1/" + n + ".jpg")}">{p.img("assets/img/gite-1/" + n + ".jpg", alt)}</a>' for n, alt in ph)
    s = head(p, t["sem_title"], t["sem_desc"]) + header(p, "sem")
    s += page_hero(p, "tag--sem", t["nav"][1], t["sem_h1"], t["sem_intro"])
    s += f"""<section class="wrap section" aria-labelledby="salle">
<div class="grid-2" style="align-items:start">
{p.img("assets/img/gite-1/communes15.jpg", PHOTO_ALTS["communes15"][LI[lang]], extra='style="width:100%;border-radius:22px;aspect-ratio:513/360;object-fit:cover"')}
<div class="callout">
<h2 id="salle" style="font-size:30px">{t['sem_room']}</h2>
<p>{t['sem_room_p']}</p>
{check_list(t['sem_points'])}
<div class="btn-row" style="padding-top:8px">
<a class="btn btn--lime" href="contact.html">{svg(I_MAIL)}{t['contact_us']}</a>
</div>
</div>
</div>
<div class="gallery">{photos}</div>
</section>
"""
    s += contact_strip(p) + footer(p)
    write(p, s)

# ================= ENVIRONS =================
ENV_META = [("sippenaeken", None), ("le-soigneur", "www.lesoigneur.be"), ("trois-bornes", "www.trois-frontieres.be"),
            ("val-dieu", "www.val-dieu.net"), ("ligne-38", "www.paysdeherve.be"), ("golf-gemmenich", "www.mergelhof.com"),
            ("teuven", "www.greenvalley.be"), ("hombourg", "www.grain-dorge.com"), ("moresnet", "www.moresnet-chapelle.com"),
            ("aubel", "www.aubel.be"), ("gulpen", "www.mosaqua.nl"), ("plombieres", "www.paysdesterrils.eu"),
            ("natagora", "www.carabo.be"), ("gileppe", "www.gileppe.com"), ("blegny", "www.blegnymine.be")]
LINK_URLS = ["www.paysdeherve.be", "www.natagora.be", "www.botrange.be", "www.trois-frontieres.be", "www.plombieres.be"]

def build_environs(lang):
    p = Page(lang, "environs.html"); t = p.t
    cards = ""
    for (slug, url), (name, desc) in zip(ENV_META, t["env"]):
        if url:
            cards += f'<a class="link-card" id="{slug}" href="https://{url}" rel="noopener"><strong>{name}</strong><span>{desc}</span><span class="url">{url}</span></a>'
        else:
            cards += f'<div class="link-card" id="{slug}"><strong>{name}</strong><span>{desc}</span></div>'
    links = "".join(f'<a class="link-card" href="https://{u}" rel="noopener"><strong>{n}</strong><span class="url">{u}</span></a>' for n, u in zip(t["links"], LINK_URLS))
    s = head(p, t["env_title"], t["env_desc"]) + header(p, "env")
    s += page_hero(p, "tag--env", t["nav"][3], t["env_h2"], t["env_intro"])
    s += f"""<section class="wrap section" aria-label="{t['env_list_label']}">
<div class="links-grid">{cards}</div>
</section>
<section id="liens" class="section--pink" aria-labelledby="liens-titre">
<div class="wrap section">
<div class="section-head"><h2 id="liens-titre">{t['links_h2']}</h2></div>
<div class="links-grid">{links}</div>
<p class="muted">{t['furniture']} <a href="https://www.marcelisluc.be" rel="noopener">www.marcelisluc.be</a></p>
</div>
</section>
<div style="height:48px"></div>
"""
    s += contact_strip(p) + footer(p)
    write(p, s)

# ================= CONTACT =================
def build_contact(lang):
    p = Page(lang, "contact.html"); t = p.t
    opts = "".join(f"<option>{o}</option>" for o in t["f_options"])
    s = head(p, t["contact_title"], t["contact_desc"]) + header(p, "contact")
    s += page_hero(p, "tag--contact", t["nav"][5], t["question"], t["contact_intro"])
    s += f"""<section class="wrap section" aria-label="{t['contact_label']}">
<div class="contact-layout">
<form id="contact-form" class="form" action="mailto:{EMAIL}" method="post" enctype="text/plain" data-to="{EMAIL}">
<h2 class="field--full" style="font-size:30px">{t['form_h2']}</h2>
<div class="field"><label for="nom">{t['f_name']}</label><input id="nom" name="nom" autocomplete="name" required></div>
<div class="field"><label for="email">{t['f_email']}</label><input id="email" name="email" type="email" autocomplete="email" required></div>
<div class="field"><label for="telephone">{t['f_phone']} <span class="hint">{t['optional']}</span></label><input id="telephone" name="telephone" type="tel" autocomplete="tel"></div>
<div class="field"><label for="formule">{t['f_want']}</label><select id="formule" name="formule">{opts}</select></div>
<div class="field"><label for="arrivee">{t['f_arrival']}</label><input id="arrivee" name="arrivee" type="date"></div>
<div class="field"><label for="depart">{t['f_departure']}</label><input id="depart" name="depart" type="date"></div>
<div class="field"><label for="personnes">{t['f_people']}</label><input id="personnes" name="personnes" type="number" min="1" max="60" inputmode="numeric"></div>
<div class="field field--full"><label for="message">{t['f_message']}</label><textarea id="message" name="message" required></textarea></div>
<p class="form-note">{t['f_note']}</p>
<div class="form-actions">
<button class="btn btn--lime btn--lg" type="submit">{svg(I_MAIL)}{t['f_send']}</button>
<p class="form-status" role="status"></p>
</div>
</form>
<aside class="contact-card" aria-labelledby="coord">
<h2 id="coord" style="font-size:30px">{t['owners']}</h2>
<address>{STREET}<br>{CITY}<br><a href="{MAPS}" style="font-weight:700">{svg(I_PIN, 18, 2, style="vertical-align:-3px")} {t['itinerary']}</a></address>
<a class="btn btn--lime btn--lg" href="tel:{TEL_FIXE[0]}">{svg(I_PHONE, 20, 2)}{t['tel']} {TEL_FIXE[1]}</a>
<a class="btn btn--lg" href="tel:{TEL_MN[0]}">{svg(I_PHONE, 20, 2)}Marie-Noëlle {TEL_MN[1]}</a>
<a class="btn btn--lg" href="tel:{TEL_CH[0]}">{svg(I_PHONE, 20, 2)}Christian {TEL_CH[1]}</a>
<a class="btn btn--lg" href="mailto:{EMAIL}">{svg(I_MAIL, 20, 2)}{EMAIL}</a>
</aside>
</div>
</section>
"""
    s += footer(p)
    write(p, s)

for lang in LANGS:
    build_index(lang); build_gite(lang, 1); build_gite(lang, 2); build_photos(lang)
    build_tarifs(lang); build_seminaire(lang); build_environs(lang); build_contact(lang)
    print("ok", lang)
