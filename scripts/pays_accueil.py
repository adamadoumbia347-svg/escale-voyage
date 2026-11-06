"""Pages d'accueil par pays africain (/ci/, /sn/, /ng/…) : les vols AU DÉPART de l'Afrique (vers l'Europe, le Golfe,
l'Amérique du Nord et les autres pays africains), avec un équivalent des prix dans la monnaie locale (site/fx.js).

Escale regardait surtout de l'Europe vers l'Afrique ; ces pages servent les voyageurs qui partent d'Abidjan, Dakar, Lagos…
(étudiants, familles en visite, voyages d'affaires). Pays francophones en français, Nigeria et Ghana en anglais.
"""
import html
import urllib.parse

import build_i18n as B
import afrique_themes

E = html.escape

# code de page : (pays, drapeau, langue, aéroports de départ, monnaie, nom de la monnaie, ville principale)
PAYS = {
    "ci": ("Côte d'Ivoire", "🇨🇮", "fr", ["ABJ"], "XOF", "francs CFA", "Abidjan"),
    "sn": ("Sénégal", "🇸🇳", "fr", ["DSS"], "XOF", "francs CFA", "Dakar"),
    "ml": ("Mali", "🇲🇱", "fr", ["BKO"], "XOF", "francs CFA", "Bamako"),
    "gn": ("Guinée", "🇬🇳", "fr", ["CKY"], "GNF", "francs guinéens", "Conakry"),
    "bf": ("Burkina Faso", "🇧🇫", "fr", ["OUA"], "XOF", "francs CFA", "Ouagadougou"),
    "tg": ("Togo", "🇹🇬", "fr", ["LFW"], "XOF", "francs CFA", "Lomé"),
    "bj": ("Bénin", "🇧🇯", "fr", ["COO"], "XOF", "francs CFA", "Cotonou"),
    "cm": ("Cameroun", "🇨🇲", "fr", ["DLA"], "XAF", "francs CFA", "Douala"),
    "cd": ("RD Congo", "🇨🇩", "fr", ["FIH"], "CDF", "francs congolais", "Kinshasa"),
    "ma": ("Maroc", "🇲🇦", "fr", ["CMN", "RAK"], "MAD", "dirhams", "Casablanca"),
    "dz": ("Algérie", "🇩🇿", "fr", ["ALG"], "DZD", "dinars algériens", "Alger"),
    "tn": ("Tunisie", "🇹🇳", "fr", ["TUN"], "TND", "dinars tunisiens", "Tunis"),
    "ng": ("Nigeria", "🇳🇬", "en", ["LOS", "ABV"], "NGN", "naira", "Lagos"),
    "gh": ("Ghana", "🇬🇭", "en", ["ACC"], "GHS", "cedis", "Accra"),
}
EN_NAME = {"ng": "Nigeria", "gh": "Ghana"}
# « au départ de … » avec le bon article
DU = {"ci": "de la Côte d'Ivoire", "sn": "du Sénégal", "ml": "du Mali", "gn": "de la Guinée", "bf": "du Burkina Faso", "tg": "du Togo", "bj": "du Bénin",
      "cm": "du Cameroun", "cd": "de la RD Congo", "ma": "du Maroc", "dz": "d'Algérie", "tn": "de Tunisie"}


def de(v):
    """« de Dakar », « d'Abidjan »."""
    return ("d'" if v[:1] in "AEIOUÉÈ" else "de ") + v
EUROPE = {"France", "Belgique", "Espagne", "Portugal", "Royaume-Uni", "Irlande", "Italie", "Suisse", "Allemagne", "Pays-Bas", "Turquie"}
LOIN = {"Émirats arabes unis", "Qatar", "Arabie saoudite", "États-Unis", "Canada"}

T = {
    "fr": dict(
        title="Billets d'avion pas chers au départ {pays} | Escale", h1="Vols pas chers <span>au départ {pays}</span>",
        desc="Billets d'avion pas chers {villes} vers {dests} : prix en direct, équivalent en {cur}.",
        lead="Les prix des vols au départ {villes}, vers l'Europe, le Golfe, l'Amérique du Nord et le reste de l'Afrique. Prix comparés en euros, avec l'équivalent en {cur}.",
        eu="Vers l'Europe et la Turquie", far="Vers le Golfe et l'Amérique du Nord", afr="Vers l'Afrique",
        th=("Destination", "Aller-retour dès", ""), see="Voir", from_="dès",
        search="Rechercher un vol au départ {v}", tips_h="Nos conseils pour partir {pays}",
        tips=["Pour l'Europe (espace Schengen), le Royaume-Uni, les États-Unis et le Canada, demandez votre visa tôt : les rendez-vous sont souvent pris plus d'un mois à l'avance avant l'été et les fêtes.",
              "Comparez les vols avec escale à Casablanca, Istanbul, Addis-Abeba ou Dubaï : ils sont souvent bien moins chers que le vol direct.",
              "Regardez la franchise bagage avant de comparer deux prix : pour un long séjour, la deuxième valise change tout.",
              "Les prix sont trouvés en euros par nos partenaires ; l'équivalent en {cur} est indicatif et le prix final s'affiche sur le site de réservation."],
        visa="Visa : vérifier selon votre passeport", others="Autres pays", themes="Hajj, études, commerce", wa="Les bons plans chaque semaine sur WhatsApp"),
    "en": dict(
        title="Cheap flights from {pays}: Europe, Gulf & Africa | Escale", h1="Cheap flights <span>from {pays}</span>",
        desc="Cheap flights from {villes} to {dests}: live prices, shown with the {cur} equivalent.",
        lead="Flight prices from {villes} to Europe, the Gulf, North America and the rest of Africa. Prices are compared in euros, with the {cur} equivalent.",
        eu="To Europe and Turkey", far="To the Gulf and North America", afr="Within Africa",
        th=("Destination", "Round trip from", ""), see="See", from_="from",
        search="Search a flight from {v}", tips_h="Our tips for flying from {pays}",
        tips=["For the UK, the Schengen area, the US and Canada, apply for your visa early: appointments are often booked more than a month ahead before summer and Christmas.",
              "Compare flights with a stop in Istanbul, Addis Ababa, Casablanca or Dubai: they are often much cheaper than a direct flight.",
              "Check the baggage allowance before comparing two fares: for a long stay, the second suitcase changes everything.",
              "Our partners find prices in euros; the {cur} equivalent is a guide and the final fare is shown on the booking site."],
        visa="Visa: check for your passport", others="Other countries", themes="Hajj, study, business", wa="Weekly deals on WhatsApp"),
}


# Versions anglaise et arabe des départs du Maghreb (Search Console : beaucoup de recherches en anglais depuis la Tunisie et l'Algérie)
EXTRA = {"tn": {"en": ("en/flights-from-tunisia", "Tunisia", "Tunisian dinars"), "ar": ("ar/flights-from-tunisia", "تونس", "الدينار التونسي")},
         "dz": {"en": ("en/flights-from-algeria", "Algeria", "Algerian dinars"), "ar": ("ar/flights-from-algeria", "الجزائر", "الدينار الجزائري")},
         "ma": {"en": ("en/flights-from-morocco", "Morocco", "Moroccan dirhams"), "ar": ("ar/flights-from-morocco", "المغرب", "الدرهم المغربي")}}
T["ar"] = dict(
    title="رحلات طيران رخيصة من {pays} | Escale", h1="رحلات رخيصة <span>من {pays}</span>",
    desc="رحلات رخيصة من {villes} إلى {dests}: أسعار مباشرة مع ما يعادلها بـ{cur}.",
    lead="أسعار الرحلات من {villes} إلى أوروبا والخليج وأمريكا الشمالية وباقي أفريقيا. تُقارن الأسعار باليورو مع ما يعادلها بـ{cur}.",
    eu="إلى أوروبا وتركيا", far="إلى الخليج وأمريكا الشمالية", afr="داخل أفريقيا",
    th=("الوجهة", "ذهاب وعودة ابتداءً من", ""), see="عرض", from_="من",
    search="ابحث عن رحلة من {v}", tips_h="نصائحنا للسفر من {pays}",
    tips=["لأوروبا (منطقة شنغن) والمملكة المتحدة والولايات المتحدة وكندا، قدّم طلب التأشيرة مبكرًا: المواعيد تُحجز غالبًا قبل أكثر من شهر في الصيف والأعياد.",
          "قارن الرحلات مع توقف في إسطنبول أو الدار البيضاء أو دبي أو أديس أبابا: غالبًا ما تكون أرخص بكثير من الرحلة المباشرة.",
          "تحقق من وزن الأمتعة المسموح قبل مقارنة سعرين: في الإقامات الطويلة، الحقيبة الثانية تغيّر كل شيء.",
          "يجد شركاؤنا الأسعار باليورو؛ ما يعادلها بـ{cur} تقريبي، والسعر النهائي يظهر على موقع الحجز."],
    visa="التأشيرة: تحقق حسب جواز سفرك", others="دول أخرى", themes="الحج، الدراسة، التجارة", wa="أفضل العروض كل أسبوع على واتساب")


def build(site, ctx, route_paths):
    routes = ctx["routes"]
    urls = []
    for code, (pays, flag, lang0, origins, cur, curn0, ville0) in PAYS.items():
        rs = [r for r in routes if r[0] in origins and r in route_paths]
        if len(rs) < 4:
            continue
        variants = [(lang0, code, EN_NAME.get(code, pays), curn0)] + [(l, v[0], v[1], v[2]) for l, v in EXTRA.get(code, {}).items()]
        alt = {lang0: code, **{l: v[0] for l, v in EXTRA.get(code, {}).items()}}
        for lang, path, pname, curn in variants:
            t = T[lang]
            city = (lambda c: c) if lang == "fr" else (lambda c, _l=lang: B.city(c, _l))
            ville = city(ville0)
            vl = list(dict.fromkeys(city(r[2]) for r in rs))
            if lang == "fr":
                villes = " et ".join(de(v) for v in vl) if len(vl) > 1 else de(vl[0])
                pform, vform = DU[code], de(ville0)
            else:
                villes, pform, vform = (" و".join(vl) if lang == "ar" else " and ".join(vl)), pname, ville
            groups = [(t["eu"], [r for r in rs if r[4] in EUROPE]), (t["far"], [r for r in rs if r[4] in LOIN]),
                      (t["afr"], [r for r in rs if r[4] not in EUROPE and r[4] not in LOIN])]
            secs = ""
            for h, L in groups:
                L = [r for r in L if lang in route_paths[r]]
                if not L:
                    continue
                rows = "".join(
                    f'<tr><th scope="row"><a href="/{route_paths[r][lang]}/"><bdi>{E(city(r[2]))} → {E(city(r[3]))}</bdi></a> <span class="hub-code" dir="ltr">{r[0]}–{r[1]}</span></th>'
                    f'<td class="hub-price" data-from="{r[0]}" data-to="{r[1]}" data-label="{E(t["from_"])}"></td>'
                    f'<td><a class="price-go" href="/{route_paths[r][lang]}/">{E(t["see"])}</a></td></tr>' for r in L)
                secs += (f'<section class="hub"><h2>{E(h)}</h2><table class="hub-table"><thead><tr><th scope="col">{E(t["th"][0])}</th>'
                         f'<th scope="col">{E(t["th"][1])}</th><td></td></tr></thead><tbody>{rows}</tbody></table></section>')
            q = urllib.parse.urlencode({"type": "vols", "from": origins[0], **({"lang": lang} if lang != "fr" else {})})
            visa_href = ("/visa/" if lang == "fr" else "/en/visa/") + "?p=" + code.upper()
            tips = "".join(f"<li>{E(x.format(cur=curn))}</li>" for x in t["tips"])
            others = " · ".join(f'<a href="/{c}/">{p[1]} {E(EN_NAME.get(c, p[0]) if lang == "en" else p[0])}</a>' for c, p in PAYS.items() if c != code)
            tl = "fr" if lang == "fr" else "en"
            hero = (f'<p class="eyebrow">{flag} {E(pname)}</p><h1>{t["h1"].format(pays=E(pform))}</h1>'
                    f'<p class="hero-lead">{E(t["lead"].format(villes=villes, cur=curn))}</p>'
                    f'<div class="cta-row"><a class="btn" href="/?{E(q)}">{E(t["search"].format(v=vform))}</a><a class="btn ghost" href="{visa_href}">🛂 {E(t["visa"])}</a></div>')
            body = (secs + '<script src="/hub.js" defer></script><script src="/fx.js" defer></script>'
                    f'<section><h2>{E(t["tips_h"].format(pays=pform))}</h2><ul>{tips}</ul></section>'
                    f'<section><h2>{E(t["themes"])}</h2><ul class="links">' + "".join(f'<li><a href="/{p}/">{E(x)}</a></li>' for p, x in afrique_themes.links(tl) + [("payer-billet-avion-mobile-money", "Payer avec Orange Money, Wave ou MTN MoMo") if tl == "fr" else ("en/pay-flight-mobile-money", "Pay with Orange Money, Wave or MTN MoMo")]) + '</ul></section>'
                    f'<section class="nl-block"><h2>{E(t["wa"])}</h2>{B.wa_btn(lang)}</section>'
                    f'<section><h2>{E(t["others"])}</h2><p class="pays-links">{others}</p></section>')
            body = f'<meta name="escale-cur" content="{cur}">' + body
            dests = ", ".join(list(dict.fromkeys(city(r[3]) for r in groups[0][1] + groups[1][1] + groups[2][1]))[:5])
            urls.append(B.write(site, path, lang, t["title"].format(pays=pform), t["desc"].format(villes=villes, cur=curn, dests=dests), hero, body, "", alt, ctx))
    return urls
