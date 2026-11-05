"""Accueils traduits (/en/, /es/, /pt/, /ar/, /it/, /de/) : l'accueil complet (recherche, bons plans, thèmes…) écrit dans la
langue de la page, pour que Google le lise dans cette langue (avant, l'accueil se traduisait seulement dans le navigateur).

- textes : attributs data-en de site/index.html (anglais) et site/i18n.js (espagnol, portugais, arabe, italien, allemand) ;
  le texte français reste dans data-fr pour que le sélecteur de langue fonctionne toujours ;
- liens : data-hrefs (version de la page cible dans la langue) ;
- la liste des trajets qui était sur ces adresses est gardée en bas de page (bloc « Guides ») ;
- app.js lit data-lang-fixed pour garder la langue de la page.
Appelé à la fin de build_pages.py, après toutes les autres pages.
"""
import html
import json
import re

E = html.escape
DOMAIN = "https://escale.live"
LANGS = ["en", "es", "pt", "ar", "it", "de"]
COL = {"es": 0, "pt": 1, "ar": 2, "it": 3, "de": 4}
LOCALE = {"fr": "fr_FR", "en": "en_GB", "es": "es_ES", "pt": "pt_PT", "ar": "ar", "it": "it_IT", "de": "de_DE"}
META = {
    "en": ("Escale: cheap flights to every destination, live prices", "Cheap flights to every destination: live prices from dozens of airlines, the cheapest day, hotels and car rental. Free, no fees added.", "Route and hotel guides"),
    "es": ("Escale: vuelos baratos a todos los destinos, precios en directo", "Vuelos baratos a todos los destinos: precios en directo de decenas de aerolíneas, el día más barato, hoteles y coches de alquiler. Gratis, sin comisiones.", "Guías de rutas y hoteles"),
    "pt": ("Escale: voos baratos para todos os destinos, preços ao vivo", "Voos baratos para todos os destinos: preços ao vivo de dezenas de companhias, o dia mais barato, hotéis e aluguer de carro. Grátis, sem taxas.", "Guias de rotas e hotéis"),
    "ar": ("Escale: رحلات طيران رخيصة إلى كل الوجهات بأسعار مباشرة", "رحلات رخيصة إلى كل الوجهات: أسعار مباشرة من عشرات شركات الطيران، أرخص يوم، فنادق وتأجير سيارات. مجانًا ودون رسوم إضافية.", "أدلة الرحلات والفنادق"),
    "it": ("Escale: voli economici per tutte le destinazioni, prezzi in diretta", "Voli economici per tutte le destinazioni: prezzi in diretta di decine di compagnie, il giorno più economico, hotel e noleggio auto. Gratis, senza costi aggiunti.", "Guide di tratte e hotel"),
    "de": ("Escale: günstige Flüge zu allen Zielen, Live-Preise", "Günstige Flüge zu allen Zielen: Live-Preise von Dutzenden Airlines, der günstigste Tag, Hotels und Mietwagen. Kostenlos, ohne Aufpreis.", "Strecken- und Hotelratgeber"),
}
MORE = {"en": "All routes and hotels", "es": "Todas las rutas y hoteles", "pt": "Todas as rotas e hotéis", "ar": "كل الرحلات والفنادق",
        "it": "Tutte le tratte e gli hotel", "de": "Alle Strecken und Hotels"}


def load_dict(site):
    """site/i18n.js -> {texte anglais: [es, pt, ar, it, de]} (objet principal + compléments ajoutés plus bas dans le fichier)."""
    js = (site / "i18n.js").read_text(encoding="utf-8")
    js = re.sub(r"(?m)^\s*//.*$", "", js)          # commentaires sur leur propre ligne
    js = re.sub(r",(\s*[}\]])", r"\1", js)          # virgules finales
    dec = json.JSONDecoder()
    i = js.index("window.ESCALE_I18N = ") + len("window.ESCALE_I18N = ")
    d, _ = dec.raw_decode(js, i)
    for m in re.finditer(r"\(function \(d, x\) \{(.*?)\}\)\(window\.ESCALE_I18N, ", js, re.S):
        extra, _ = dec.raw_decode(js, m.end())
        if "length === 3" in m.group(1):  # complète l'italien et l'allemand
            for k, v in extra.items():
                if k in d and len(d[k]) == 3:
                    d[k] = d[k] + v
        else:
            for k, v in extra.items():
                if k not in d or len(d[k]) < 5:
                    d[k] = v
    return d


def tr(d, en, lang):
    if lang == "en":
        return en
    v = d.get(en)
    return v[COL[lang]] if v and len(v) > COL[lang] and v[COL[lang]] else en


def old_sections(site, lang):
    """Sections de la liste des trajets déjà publiée à cette adresse (pour la garder en bas de l'accueil)."""
    f = site / lang / "index.html"
    if not f.exists():
        return ""
    s = f.read_text(encoding="utf-8")
    if 'data-lang-fixed=' in s:  # déjà un accueil traduit (construction relancée) : on garde ce qui était gardé
        m = re.search(r'<div class="old-routes">(.*?)</div><!-- /old-routes -->', s, re.S)
        return m.group(1) if m else ""
    m = s[s.find("<main"):s.find("</main>")]
    parts = re.findall(r"<section\b.*?</section>", m, re.S)
    return "".join(p for p in parts if 'class="faq"' not in p)


def translate(src, d, lang):
    s = src

    def text(m):
        tag, en, inner, end = m.group(1), html.unescape(m.group(3)), m.group(4), m.group(5)
        fr = html.unescape(inner)
        t = tr(d, en, lang)
        tag = tag if " data-fr=" in tag else tag[:-1] + f' data-fr="{E(fr)}">'
        return tag + E(t, quote=False) + end
    A = r'(?:[^>"]|"[^"]*")*?'  # attributs (une valeur entre guillemets peut contenir « > »)
    s = re.sub(r'(<(\w+)\b' + A + r'\sdata-en="([^"]*)"' + A + r'>)([^<]*)(</\2>)', text, s)

    def htm(m):
        tag, en, inner, end = m.group(1), html.unescape(m.group(3)), m.group(4), m.group(5)
        t = tr(d, en, lang)
        tag = tag if " data-fr-html=" in tag else tag[:-1] + f' data-fr-html="{E(inner)}">'
        return tag + t + end
    s = re.sub(r'(<(\w+)\b' + A + r'\sdata-en-html="([^"]*)"' + A + r'>)(.*?)(</\2>)', htm, s, flags=re.S)

    def ph(m):
        a = m.group(0)
        en = html.unescape(re.search(r'data-en-ph="([^"]*)"', a).group(1))
        t = tr(d, en, lang)
        old = re.search(r'\splaceholder="([^"]*)"', a)
        if old:
            a = a.replace(old.group(0), f' placeholder="{E(t)}" data-fr-ph="{old.group(1)}"', 1)
        return a
    s = re.sub(r'<(?:input|textarea)\b' + A + r'data-en-ph="[^"]*"' + A + r'>', ph, s)

    def aria(m):
        a = m.group(0)
        en = html.unescape(re.search(r'data-en-aria="([^"]*)"', a).group(1))
        t = tr(d, en, lang)
        old = re.search(r'\saria-label="([^"]*)"', a)
        if old:
            a = a.replace(old.group(0), f' aria-label="{E(t)}" data-fr-aria="{old.group(1)}"', 1)
        return a
    s = re.sub(r'<\w+\b' + A + r'data-en-aria="[^"]*"' + A + r'>', aria, s)

    def href(m):
        a = m.group(0)
        try:
            h = json.loads(html.unescape(re.search(r'data-hrefs="([^"]*)"', a).group(1)))
        except (ValueError, AttributeError):
            return a
        if h.get(lang):
            a = re.sub(r'\shref="[^"]*"', f' href="{E(h[lang])}"', a, count=1)
        return a
    s = re.sub(r'<a\b' + A + r'data-hrefs="[^"]*"' + A + r'>', href, s)
    return s


def alternates():
    out = [f'<link rel="alternate" hreflang="fr" href="{DOMAIN}/">'] + [f'<link rel="alternate" hreflang="{l}" href="{DOMAIN}/{l}/">' for l in LANGS]
    return "\n".join(out + [f'<link rel="alternate" hreflang="x-default" href="{DOMAIN}/">'])


def build(site, ctx=None):
    d = load_dict(site)
    home = site / "index.html"
    src = home.read_text(encoding="utf-8")
    # Accueil français : toutes les langues dans les balises hreflang
    src = re.sub(r'(<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n?)+', alternates() + "\n", src, count=1)
    home.write_text(src, encoding="utf-8")
    urls = []
    for lang in LANGS:
        keep = old_sections(site, lang)
        s = translate(src, d, lang)
        title, desc, guides_h = META[lang]
        s = s.replace('<html lang="fr">', f'<html lang="{lang}" dir="{"rtl" if lang == "ar" else "ltr"}" data-lang-fixed="{lang}">', 1)
        s = re.sub(r"<title>[^<]*</title>", f"<title>{E(title)}</title>", s, count=1)
        s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{E(desc)}">', s, count=1)
        s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{E(title)}">', s, count=1)
        s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{E(desc)}">', s, count=1)
        s = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{DOMAIN}/{lang}/">', s, count=1)
        s = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{DOMAIN}/{lang}/">', s, count=1)
        s = re.sub(r'<meta property="og:locale" content="[^"]*">', f'<meta property="og:locale" content="{LOCALE[lang]}">', s, count=1)
        # Bloc « Guides » : la liste des trajets et hôtels de cette langue (celle qui était publiée ici)
        if keep:
            i = s.find('<section class="block" id="guides">')
            j = s.find("</section>", i) + len("</section>") if i >= 0 else -1
            if i >= 0:
                block = (f'<section class="block" id="guides"><h2>{E(guides_h)}</h2><details class="guides-all"><summary>{E(MORE[lang])}</summary>'
                         f'<div class="old-routes">{keep}</div><!-- /old-routes --></details></section>')
                s = s[:i] + block + s[j:]
        # Traductions de l'interface chargées directement (au lieu du document.write de l'accueil français)
        if lang != "en":
            s = re.sub(r"<script>if \(!/\^\(fr\|en\)\$/\.test\(document\.documentElement\.lang\)\) document\.write\('<script src=\"(/i18n\.js[^\"]*)\" defer><\\/script>'\);</script>",
                       r'<script src="\1" defer></script>', s, count=1)
        (site / lang).mkdir(exist_ok=True)
        (site / lang / "index.html").write_text(s, encoding="utf-8")
        urls.append(f"{DOMAIN}/{lang}/")
    return urls
