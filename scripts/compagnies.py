"""Pages compagnies (/compagnie/air-france/, /en/airline/air-france/…) : pour chaque compagnie qui relie l'Europe et l'Afrique,
où elle est basée, ce qu'elle dessert surtout, les liens officiels (site, bagages), nos conseils, et le bloc « ce que les voyageurs
ont payé » rempli par le serveur (src/paye.ts, déclarations anonymes sur les pages trajets). Aucun prix ni franchise écrit ici :
ces chiffres changent trop souvent ; les liens officiels font foi. Liste des compagnies : scripts/pratique_afrique.AIRLINES."""
import html

import build_i18n as B
from pratique_afrique import AIRLINES

E = html.escape
# Compléments par compagnie : (type, hubs/villes clés, conseil). Faits généraux et stables ; les horaires, lignes et tarifs se vérifient sur le site officiel.
INFO = {
    "Air Côte d'Ivoire": ("Compagnie nationale ivoirienne", "Hub à Abidjan ; vols régionaux vers l'Afrique de l'Ouest et centrale, et ligne vers Paris.", "Pratique pour enchaîner un vol international vers Abidjan et une correspondance régionale avec une seule compagnie."),
    "ASKY Airlines": ("Compagnie régionale ouest-africaine", "Hub à Lomé ; dessert une trentaine de villes d'Afrique de l'Ouest et centrale, en partenariat avec Ethiopian Airlines.", "Depuis l'Europe, on l'emprunte surtout en correspondance à Lomé ou en combinaison avec Ethiopian."),
    "Air Sénégal": ("Compagnie nationale sénégalaise", "Hub à Dakar ; vols vers l'Europe (Paris, Milan, Bruxelles…) et l'Afrique de l'Ouest.", "Comparez le direct Dakar avec les vols via Casablanca : la différence de prix varie beaucoup selon la saison."),
    "Air Peace": ("Première compagnie privée du Nigeria", "Base à Lagos ; réseau intérieur nigérian, Afrique de l'Ouest et ligne vers Londres.", "Pour Lagos ou Abuja depuis le Royaume-Uni, à comparer avec British Airways et les compagnies du Golfe."),
    "RwandAir": ("Compagnie nationale rwandaise", "Hub à Kigali ; Afrique de l'Est, centrale et australe, Europe (Paris, Bruxelles, Londres).", "Kigali est une correspondance pratique vers l'Afrique de l'Est et centrale."),
    "Kenya Airways": ("Compagnie nationale kényane", "Hub à Nairobi ; Afrique de l'Est, australe et de l'Ouest, Europe (Paris, Londres, Amsterdam).", "Souvent compétitive vers Nairobi et au-delà en correspondance."),
    "Ethiopian Airlines": ("Plus grande compagnie d'Afrique", "Hub à Addis-Abeba ; dessert la quasi-totalité des capitales africaines et de nombreuses villes d'Europe.", "Pour une ville africaine mal desservie en direct, la correspondance à Addis-Abeba est souvent la solution la moins chère."),
    "Royal Air Maroc": ("Compagnie nationale marocaine", "Hub à Casablanca ; Maroc, Afrique de l'Ouest et centrale, Europe entière.", "Casablanca est le grand carrefour entre l'Europe et l'Afrique de l'Ouest : comparez toujours le prix via Casablanca."),
    "Air Algérie": ("Compagnie nationale algérienne", "Hub à Alger ; nombreuses villes de France et d'Europe, Afrique de l'Ouest en correspondance.", "Pour Alger, Oran ou Constantine, comparez avec Transavia, ASL Airlines et Vueling selon la ville de départ."),
    "Tunisair": ("Compagnie nationale tunisienne", "Hub à Tunis ; Tunisie, Europe, quelques villes d'Afrique de l'Ouest.", "Les compagnies à bas prix sont souvent moins chères sur Paris – Tunis hors saison ; en été, comparez."),
    "EgyptAir": ("Compagnie nationale égyptienne", "Hub au Caire ; Égypte, Afrique, Moyen-Orient, Europe.", "Correspondance au Caire pratique vers l'Afrique de l'Est et l'Afrique australe."),
    "Air France": ("Compagnie nationale française", "Hub à Paris-Charles-de-Gaulle ; vols directs vers une vingtaine de villes d'Afrique de l'Ouest, centrale et du Maghreb.", "Les directs Paris – Afrique sont confortables mais rarement les moins chers : comparez avec les vols via Casablanca, Istanbul ou Addis-Abeba."),
    "Brussels Airlines": ("Compagnie belge (groupe Lufthansa)", "Hub à Bruxelles ; Afrique de l'Ouest, centrale et de l'Est (Kinshasa, Dakar, Abidjan, Douala…).", "Pour le nord de la France, partir de Bruxelles est souvent intéressant vers l'Afrique centrale."),
    "Corsair": ("Compagnie française long-courrier", "Base à Paris-Orly ; Abidjan, Bamako, Cotonou, Douala, Antilles, Réunion, Maurice.", "Propose le paiement en plusieurs fois et des tarifs intéressants hors saison depuis Orly."),
    "Turkish Airlines": ("Compagnie nationale turque", "Hub à Istanbul ; l'un des plus grands réseaux africains au monde, depuis toute l'Europe.", "Via Istanbul, souvent parmi les moins chers vers l'Afrique de l'Ouest et de l'Est, avec une franchise bagages généreuse selon le tarif."),
    "Emirates": ("Compagnie de Dubaï", "Hub à Dubaï ; grandes villes d'Afrique de l'Ouest, de l'Est et australe.", "Correspondance longue mais réseau étendu ; à comparer pour l'Afrique de l'Est et australe."),
    "Qatar Airways": ("Compagnie du Qatar", "Hub à Doha ; Afrique de l'Est, australe, de l'Ouest et Maghreb.", "Même logique qu'Emirates : parfois très compétitive sur l'Afrique de l'Est."),
    "TAP Air Portugal": ("Compagnie nationale portugaise", "Hub à Lisbonne ; Afrique lusophone (Luanda, Maputo, Bissau, Praia, São Tomé) et Afrique de l'Ouest.", "Incontournable vers les pays lusophones ; depuis Paris ou Milan, la correspondance à Lisbonne est courte."),
    "Iberia": ("Compagnie nationale espagnole", "Hub à Madrid ; Maroc, Sénégal, Afrique de l'Ouest.", "Via Madrid, parfois intéressante vers Dakar depuis le sud de la France."),
    "ITA Airways": ("Compagnie nationale italienne", "Hub à Rome ; Afrique du Nord, Dakar, Accra et autres villes selon la saison.", "Pour la diaspora en Italie, comparez avec les vols via Casablanca ou Istanbul depuis Milan et Rome."),
    "Transavia": ("Compagnie à bas prix (groupe Air France-KLM)", "Bases à Paris-Orly et Amsterdam ; Maroc, Algérie, Tunisie, Dakar.", "Bagages en soute payants : comparez le prix total avec valise, pas le prix d'appel."),
}
EN = {
    "Compagnie nationale ivoirienne": "Ivory Coast's national airline", "Compagnie régionale ouest-africaine": "West African regional airline", "Compagnie nationale sénégalaise": "Senegal's national airline",
    "Première compagnie privée du Nigeria": "Nigeria's largest private airline", "Compagnie nationale rwandaise": "Rwanda's national airline", "Compagnie nationale kényane": "Kenya's national airline",
    "Plus grande compagnie d'Afrique": "Africa's largest airline", "Compagnie nationale marocaine": "Morocco's national airline", "Compagnie nationale algérienne": "Algeria's national airline",
    "Compagnie nationale tunisienne": "Tunisia's national airline", "Compagnie nationale égyptienne": "Egypt's national airline", "Compagnie nationale française": "France's national airline",
    "Compagnie belge (groupe Lufthansa)": "Belgian airline (Lufthansa Group)", "Compagnie française long-courrier": "French long-haul airline", "Compagnie nationale turque": "Turkey's national airline",
    "Compagnie de Dubaï": "Dubai-based airline", "Compagnie du Qatar": "Qatar's national airline", "Compagnie nationale portugaise": "Portugal's national airline", "Compagnie nationale espagnole": "Spain's national airline",
    "Compagnie nationale italienne": "Italy's national airline", "Compagnie à bas prix (groupe Air France-KLM)": "Low-cost airline (Air France-KLM Group)",
}
T = {
    "fr": dict(dir="compagnie", idx="compagnies-aeriennes-afrique", eyebrow="Compagnie aérienne", h1="{n} : <span>vols vers l'Afrique</span>", title="{n} : vols Europe – Afrique, bagages, prix payés par les voyageurs | Escale",
               desc="{n} ({t}) : ce qu'elle dessert entre l'Europe et l'Afrique, où trouver les règles officielles de bagages, nos conseils et les prix réellement payés par les voyageurs d'Escale.",
               lead="{t}. {r}", based="Basée à", serves="Dessert surtout", site="Site officiel", bag="Règles bagages (site officiel)", tip="Notre conseil", paid_h="Ce que les voyageurs ont payé avec {n}",
               paid_wait="Les voyageurs d'Escale déclarent le prix payé sur les pages de trajets. Dès qu'il y aura assez de déclarations citant {n}, les chiffres s'afficheront ici.",
               compare="Comparer les prix de tous les trajets", other="Les autres compagnies", idx_h1="Les compagnies qui relient <span>l'Europe et l'Afrique</span>", idx_title="Compagnies aériennes Europe – Afrique : qui dessert quoi | Escale",
               idx_desc="Air France, Royal Air Maroc, Ethiopian, Turkish, Air Côte d'Ivoire, Air Sénégal, Brussels Airlines, Corsair… : ce que chaque compagnie dessert entre l'Europe et l'Afrique, les liens officiels et les prix payés par les voyageurs.",
               idx_lead="Pour chaque compagnie : où elle est basée, ce qu'elle dessert, où lire ses règles de bagages, et ce que les voyageurs ont réellement payé.",
               note="Escale ne vend pas de billets et n'est lié à aucune compagnie. Les lignes, horaires et franchises changent : le site officiel fait foi. Les prix « payés par les voyageurs » sont déclarés par des visiteurs, non vérifiés, à titre indicatif."),
    "en": dict(dir="en/airline", idx="en/airlines-europe-africa", eyebrow="Airline", h1="{n}: <span>flights to Africa</span>", title="{n}: Europe – Africa flights, baggage, fares travellers paid | Escale",
               desc="{n} ({t}): what it flies between Europe and Africa, where to find the official baggage rules, our tips and the fares Escale travellers actually paid.",
               lead="{t}. {r}", based="Based in", serves="Mainly flies to", site="Official website", bag="Baggage rules (official site)", tip="Our tip", paid_h="What travellers paid with {n}",
               paid_wait="Escale travellers report the fare they paid on route pages. As soon as there are enough reports naming {n}, the figures will appear here.",
               compare="Compare fares on all routes", other="Other airlines", idx_h1="Airlines linking <span>Europe and Africa</span>", idx_title="Europe – Africa airlines: who flies where | Escale",
               idx_desc="Air France, Royal Air Maroc, Ethiopian, Turkish, Air Côte d'Ivoire, Air Senegal, Brussels Airlines, Corsair…: what each airline flies between Europe and Africa, official links and fares travellers paid.",
               idx_lead="For each airline: where it is based, what it flies, where to read its baggage rules, and what travellers really paid.",
               note="Escale does not sell tickets and is not affiliated with any airline. Routes, schedules and allowances change: the official site prevails. 'Fares travellers paid' are reported by visitors, unverified, for guidance only."),
}
CITY_EN = {"Abidjan": "Abidjan", "Lomé": "Lomé", "Dakar": "Dakar", "Lagos": "Lagos", "Kigali": "Kigali", "Nairobi": "Nairobi", "Addis-Abeba": "Addis Ababa", "Casablanca": "Casablanca", "Alger": "Algiers", "Tunis": "Tunis",
           "Le Caire": "Cairo", "Paris": "Paris", "Bruxelles": "Brussels", "Istanbul": "Istanbul", "Dubaï": "Dubai", "Doha": "Doha", "Lisbonne": "Lisbon", "Madrid": "Madrid", "Rome": "Rome", "Paris / Amsterdam": "Paris / Amsterdam"}


def slug(n):
    return B.slugify(n)


def build(site, ctx):
    urls = []
    for lang, t in T.items():
        items = []
        for name, base, serves, url in AIRLINES:
            typ, hubs, tip = INFO.get(name, ("", "", ""))
            s = slug(name)
            path = f"{t['dir']}/{s}"
            paths = {"fr": f"compagnie/{s}", "en": f"en/airline/{s}"}
            typ_l = EN.get(typ, typ) if lang == "en" else typ
            hubs_l = hubs if lang == "fr" else ""
            base_l = CITY_EN.get(base, base) if lang == "en" else base
            others = "".join(f'<li><a href="/{t["dir"]}/{slug(n2)}/">{E(n2)}</a></li>' for n2, *_ in AIRLINES if n2 != name)
            hero = (f'<p class="eyebrow">{E(t["eyebrow"])}</p><h1>{t["h1"].format(n=E(name))}</h1>'
                    f'<p class="hero-lead">{E(t["lead"].format(t=typ_l, r=(hubs_l or serves[1 if lang == "en" else 0])))}</p>'
                    f'<div class="cta-row"><a class="btn" href="/{"" if lang == "fr" else "?lang=en"}">{E(t["compare"])}</a><a class="btn ghost" href="{E(url)}" target="_blank" rel="noopener nofollow">{E(t["site"])} ↗</a></div>')
            body = ('<style>.kv{display:grid;gap:10px;margin:0}.kv div{display:grid;gap:2px;padding:10px 14px;border:1px solid var(--line);border-radius:12px;background:var(--surface,#fff)}.kv dt{font-size:.8rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}.kv dd{margin:0;font-weight:600}</style>'
                    f'<section><dl class="kv"><div><dt>{E(t["based"])}</dt><dd>{E(base_l)}</dd></div><div><dt>{E(t["serves"])}</dt><dd>{E(serves[1 if lang == "en" else 0])}</dd></div>'
                    f'<div><dt>{E(t["bag"])}</dt><dd><a href="{E(url)}" target="_blank" rel="noopener nofollow">{E(url.replace("https://", "").rstrip("/"))} ↗</a></dd></div></dl></section>'
                    + (f'<section><h2>{E(t["tip"])}</h2><p>{E(tip)}</p></section>' if tip and lang == "fr" else "")
                    + f'<section><h2>{E(t["paid_h"].format(n=name))}</h2><div id="cie-paye" data-cie="{E(name)}" data-lang="{lang}"><p class="small">{E(t["paid_wait"].format(n=name))}</p></div></section>'
                    f'<section><h2>{E(t["other"])}</h2><ul class="route-links">{others}</ul></section>'
                    f'<p class="small">{E(t["note"])}</p>')
            urls.append(B.write(site, path, lang, t["title"].format(n=name), t["desc"].format(n=name, t=typ_l), hero, body, "", paths, ctx))
            items.append(f'<li><a href="/{path}/"><strong>{E(name)}</strong></a> · {E(typ_l)} · {E(serves[1 if lang == "en" else 0])}</li>')
        hero = f'<p class="eyebrow">{E(t["eyebrow"])}s</p><h1>{t["idx_h1"]}</h1><p class="hero-lead">{E(t["idx_lead"])}</p>'
        body = f'<section><ul class="pf-list">{"".join(items)}</ul></section><p class="small">{E(t["note"])}</p>'
        urls.append(B.write(site, t["idx"], lang, t["idx_title"], t["idx_desc"], hero, body, "", {"fr": T["fr"]["idx"], "en": T["en"]["idx"]}, ctx))
    return urls
