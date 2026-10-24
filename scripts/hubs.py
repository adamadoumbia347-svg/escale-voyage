"""Pages « destination » : tous les vols vers une ville (Dakar, Casablanca…), depuis chaque ville de départ, en 5 langues.

Elles répondent aux recherches du type « vol Dakar pas cher », « flights to Dakar », « vuelos a Marrakech »,
et relient entre elles toutes les pages trajets d'une même destination.
"""
import collections
import html
import re

from build_i18n import ALL, TR, duration, faq_ld, slugify, tr, write

E = html.escape
MIN_ORIGINS = 3

H = {
    "fr": dict(path="vols-pour-{s}", title="Vols pas chers pour {b} : comparer depuis {n} villes",
               desc="Vols pas chers pour {b} ({code}) au départ de {some} et d’autres villes : durée du vol, prix repérés récemment et meilleure période pour réserver.",
               h1="Vols pas chers pour <span>{b}</span>",
               lead="Comparez les vols vers {b} depuis {n} villes d’Europe et d’Amérique du Nord : durée, prix repérés récemment et conseils pour payer moins cher.",
               th=("Départ de", "Durée du vol", "Prix repéré"), see="Voir le trajet", direct="vol direct", est="estimation", stops="avec escale",
               airport="Aéroport d’arrivée", shortest="Vol le plus court", peak="Prix les plus hauts", short_v="depuis {a}, environ {d}",
               table_h="Les vols pour {b}, ville par ville", table_p="Prix aller-retour les plus bas repérés récemment par des voyageurs. Le tarif exact s’affiche sur les sites de réservation.",
               more_h="Préparer le voyage", hotels="Hôtels pas chers à {b}", cars="Louer une voiture à {b}", search="Rechercher un vol pour {b}",
               faq_h="Questions fréquentes",
               faq=[("Depuis quelles villes partent les vols pour {b} ?", "Escale compare les vols pour {b} au départ de {all}."),
                    ("Quel est le vol le plus court pour {b} ?", "Depuis {a}, comptez environ {d} de vol ({kind})."),
                    ("Quand réserver un vol pour {b} pas cher ?", "En général deux à trois mois avant le départ. Réservez plus tôt pour {peak} : les prix montent fortement."),
                    ("Quel aéroport à {b} ?", "Les vols arrivent à {airport} (code {code}).")],
               from_="dès"),
    "en": dict(path="en/flights-to-{s}", title="Cheap flights to {b}: compare from {n} cities",
               desc="Cheap flights to {b} ({code}) from {some} and more: flight time, recent prices and the best time to book.",
               h1="Cheap flights to <span>{b}</span>",
               lead="Compare flights to {b} from {n} cities in Europe and North America: flight time, recent prices and tips to pay less.",
               th=("From", "Flight time", "Price found"), see="See route", direct="direct", est="estimate", stops="with a stop",
               airport="Arrival airport", shortest="Shortest flight", peak="Most expensive periods", short_v="from {a}, about {d}",
               table_h="Flights to {b}, city by city", table_p="Lowest round-trip prices recently found by travellers. The exact fare is shown on the booking sites.",
               more_h="Plan your trip", hotels="Cheap hotels in {b}", cars="Car rental in {b}", search="Search a flight to {b}",
               faq_h="Frequently asked questions",
               faq=[("Which cities have flights to {b}?", "Escale compares flights to {b} from {all}."),
                    ("What is the shortest flight to {b}?", "From {a}, allow about {d} of flying ({kind})."),
                    ("When should I book a cheap flight to {b}?", "Usually two to three months before departure. Book earlier for {peak}: prices rise sharply."),
                    ("Which airport in {b}?", "Flights arrive at {airport} (code {code}).")],
               from_="from"),
    "es": dict(path="es/vuelos-a-{s}", title="Vuelos baratos a {b}: compara desde {n} ciudades",
               desc="Vuelos baratos a {b} ({code}) desde {some} y otras ciudades: duración del vuelo, precios recientes y el mejor momento para reservar.",
               h1="Vuelos baratos a <span>{b}</span>",
               lead="Compara los vuelos a {b} desde {n} ciudades de Europa y Norteamérica: duración, precios recientes y consejos para pagar menos.",
               th=("Salida desde", "Duración", "Precio encontrado"), see="Ver la ruta", direct="vuelo directo", est="estimación", stops="con escala",
               airport="Aeropuerto de llegada", shortest="Vuelo más corto", peak="Precios más altos", short_v="desde {a}, unas {d}",
               table_h="Vuelos a {b}, ciudad por ciudad", table_p="Precios de ida y vuelta más bajos encontrados recientemente por viajeros. La tarifa exacta aparece en los sitios de reserva.",
               more_h="Preparar el viaje", hotels="Hoteles baratos en {b}", cars="Alquiler de coches en {b}", search="Buscar un vuelo a {b}",
               faq_h="Preguntas frecuentes",
               faq=[("¿Desde qué ciudades salen vuelos a {b}?", "Escale compara los vuelos a {b} desde {all}."),
                    ("¿Cuál es el vuelo más corto a {b}?", "Desde {a}, cuenta unas {d} de vuelo ({kind})."),
                    ("¿Cuándo reservar un vuelo barato a {b}?", "En general dos o tres meses antes de la salida. Reserva antes para {peak}: los precios suben mucho."),
                    ("¿Qué aeropuerto hay en {b}?", "Los vuelos llegan a {airport} (código {code}).")],
               from_="desde"),
    "pt": dict(path="pt/voos-para-{s}", title="Voos baratos para {b}: compare a partir de {n} cidades",
               desc="Voos baratos para {b} ({code}) a partir de {some} e outras cidades: duração do voo, preços recentes e a melhor altura para reservar.",
               h1="Voos baratos para <span>{b}</span>",
               lead="Compare os voos para {b} a partir de {n} cidades da Europa e da América do Norte: duração, preços recentes e dicas para pagar menos.",
               th=("Partida de", "Duração", "Preço encontrado"), see="Ver a rota", direct="voo direto", est="estimativa", stops="com escala",
               airport="Aeroporto de chegada", shortest="Voo mais curto", peak="Preços mais altos", short_v="a partir de {a}, cerca de {d}",
               table_h="Voos para {b}, cidade a cidade", table_p="Preços de ida e volta mais baixos encontrados recentemente por viajantes. A tarifa exata aparece nos sites de reserva.",
               more_h="Preparar a viagem", hotels="Hotéis baratos em {b}", cars="Aluguer de carros em {b}", search="Pesquisar um voo para {b}",
               faq_h="Perguntas frequentes",
               faq=[("De que cidades partem voos para {b}?", "A Escale compara os voos para {b} a partir de {all}."),
                    ("Qual é o voo mais curto para {b}?", "A partir de {a}, conte cerca de {d} de voo ({kind})."),
                    ("Quando reservar um voo barato para {b}?", "Em geral dois a três meses antes da partida. Reserve mais cedo para {peak}: os preços sobem muito."),
                    ("Que aeroporto em {b}?", "Os voos chegam a {airport} (código {code}).")],
               from_="desde"),
    "ar": dict(path="ar/flights-to-{s}", title="رحلات رخيصة إلى {b}: قارن من {n} مدينة",
               desc="رحلات رخيصة إلى {b} ({code}) من {some} ومدن أخرى: مدة الرحلة والأسعار الأخيرة وأفضل وقت للحجز.",
               h1="رحلات رخيصة إلى <span>{b}</span>",
               lead="قارن الرحلات إلى {b} من {n} مدينة في أوروبا وأمريكا الشمالية: المدة والأسعار الأخيرة ونصائح لدفع أقل.",
               th=("المغادرة من", "مدة الرحلة", "السعر"), see="اعرض الرحلة", direct="رحلة مباشرة", est="تقدير", stops="مع توقف",
               airport="مطار الوصول", shortest="أقصر رحلة", peak="أغلى الفترات", short_v="من {a}، حوالي {d}",
               table_h="الرحلات إلى {b} حسب المدينة", table_p="أدنى أسعار الذهاب والعودة التي وجدها المسافرون مؤخرًا. يظهر السعر الدقيق على مواقع الحجز.",
               more_h="التحضير للرحلة", hotels="فنادق رخيصة في {b}", cars="تأجير سيارة في {b}", search="ابحث عن رحلة إلى {b}",
               faq_h="أسئلة شائعة",
               faq=[("من أي مدن توجد رحلات إلى {b}؟", "يقارن Escale الرحلات إلى {b} من {all}."),
                    ("ما أقصر رحلة إلى {b}؟", "من {a}، احسب حوالي {d} من الطيران ({kind})."),
                    ("متى أحجز رحلة رخيصة إلى {b}؟", "عادةً قبل شهرين إلى ثلاثة أشهر من السفر. احجز مبكرًا لفترة {peak}: ترتفع الأسعار كثيرًا."),
                    ("ما مطار {b}؟", "تصل الرحلات إلى {airport} (الرمز {code}).")],
               from_="من"),
}
SEP = {"fr": ", ", "en": ", ", "es": ", ", "pt": ", ", "ar": "، "}


def loc(table, key, lang):
    return key if lang == "fr" else tr(table, key, lang)


def minutes(d):
    m = re.match(r"~?(\d+) h(?: (\d+))?", d or "")
    return int(m.group(1)) * 60 + int(m.group(2) or 0) if m else None


def hub_paths(routes):
    """{ville d'arrivée (nom français) : {langue : chemin}} pour les destinations desservies depuis au moins 3 villes."""
    count = collections.Counter(r[3] for r in routes)
    return {ct: {l: H[l]["path"].format(s=slugify(ct if l == "fr" else loc(TR.CITIES, ct, "en" if l == "ar" else l))) for l in ALL}
            for ct, n in count.items() if n >= MIN_ORIGINS}


def build_hubs(site, ctx, route_paths, hotel_paths):
    routes, airports = ctx["routes"], ctx["airports"]
    paths = hub_paths(routes)
    urls = []
    for ct, hp in paths.items():
        rs = [r for r in routes if r[3] == ct]
        code = collections.Counter(r[1] for r in rs).most_common(1)[0][0]
        country = rs[0][4]
        peak_fr = collections.Counter(r[7] for r in rs).most_common(1)[0][0]
        ap = airports.get(code)
        timed = sorted((r for r in rs if minutes(r[6]) is not None), key=lambda r: minutes(r[6]))
        rs.sort(key=lambda r: (minutes(r[6]) or 10 ** 6, r[2]))
        hotel = next((h for h in ctx["hotels"] if h[0] == ct), None)
        for lang in ALL:
            h = H[lang]
            b = loc(TR.CITIES, ct, lang)
            cities = [loc(TR.CITIES, r[2], lang) for r in rs]
            some = SEP[lang].join(cities[:4])
            peak = loc(TR.PEAKS, peak_fr, lang)
            airport = (ap[2] if ap else code) if lang != "fr" else rs[0][5]
            q = "" if lang == "fr" else "&lang=" + lang
            rows = []
            for r in rs:
                a = loc(TR.CITIES, r[2], lang)
                dur = r[6]
                if not dur:
                    dtxt = h["stops"]
                else:
                    dtxt = duration(dur.lstrip("~"), lang) + " (" + (h["est"] if dur.startswith("~") else h["direct"]) + ")"
                rows.append(f'<tr><th scope="row"><a href="/{route_paths[r][lang]}/"><bdi>{E(a)}</bdi></a> <span class="hub-code" dir="ltr">{r[0]}</span></th>'
                            f'<td>{E(dtxt)}</td><td class="hub-price" data-from="{r[0]}" data-to="{r[1]}" data-label="{E(h["from_"])}"></td>'
                            f'<td><a class="price-go" href="/{route_paths[r][lang]}/">{E(h["see"])}</a></td></tr>')
            facts = [(h["airport"], f"{airport} ({code})"), (h["peak"], peak[0].upper() + peak[1:])]
            kind = ""
            if timed:
                t0 = timed[0]
                d0 = duration(t0[6].lstrip("~"), lang)
                kind = h["est"] if t0[6].startswith("~") else h["direct"]
                facts.insert(1, (h["shortest"], h["short_v"].format(a=loc(TR.CITIES, t0[2], lang), d=d0)))
            f = dict(b=b, all=SEP[lang].join(cities), airport=airport, code=code, peak=peak,
                     a=loc(TR.CITIES, timed[0][2], lang) if timed else "", d=duration(timed[0][6].lstrip("~"), lang) if timed else "", kind=kind)
            faq = [(qq.format(**f), aa.format(**f)) for i, (qq, aa) in enumerate(h["faq"]) if i != 1 or timed]
            more = [f'<li><a href="/?type=vols&amp;to={code}{E(q)}">{E(h["search"].format(b=b))}</a></li>']
            if hotel:
                more.append(f'<li><a href="/{hotel_paths[hotel[0]][lang]}/">{E(h["hotels"].format(b=b))}</a></li>')
            more.append(f'<li><a href="/?type=voitures&amp;pick={code}{E(q)}">{E(h["cars"].format(b=b))}</a></li>')
            hero = (f'<p class="eyebrow">{E(loc(TR.COUNTRIES, country, lang))}</p><h1>{h["h1"].format(b=E(b))}</h1>'
                    f'<p class="hero-lead">{E(h["lead"].format(b=b, n=len(rs)))}</p>')
            body = (f'<dl class="facts">' + "".join(f"<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>" for k, v in facts) + "</dl>"
                    f'<section class="hub"><h2>{E(h["table_h"].format(b=b))}</h2><p class="small">{E(h["table_p"])}</p>'
                    f'<table class="hub-table"><thead><tr><th scope="col">{E(h["th"][0])}</th><th scope="col">{E(h["th"][1])}</th>'
                    f'<th scope="col">{E(h["th"][2])}</th><td></td></tr></thead><tbody>{"".join(rows)}</tbody></table></section>'
                    f'<script src="/hub.js" defer></script>'
                    f'<section><h2>{E(h["more_h"])}</h2><ul class="links">{"".join(more)}</ul></section>'
                    f'<section class="faq"><h2>{E(h["faq_h"])}</h2>' + "".join(f"<details><summary>{E(qq)}</summary><p>{E(aa)}</p></details>" for qq, aa in faq) + "</section>")
            title = h["title"].format(b=b, n=len(rs))
            desc = h["desc"].format(b=b, code=code, some=some)
            urls.append(write(site, hp[lang], lang, title + " | Escale", desc, hero, body, faq_ld(faq), hp, ctx))
    return urls, paths
