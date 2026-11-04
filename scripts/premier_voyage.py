"""Pages « Premier voyage à… » (Zanzibar, Bali, Japon), fr et en.

Règles vérifiées en novembre 2026 (sources : immigration de Tanzanie, gouvernement de Zanzibar, immigration indonésienne,
province de Bali, Visit Japan Web ; montants confirmés par plusieurs guides de voyage). Elles changent : chaque page le dit
et renvoie vers les sites officiels. Le prix n'est jamais écrit : site/tendances.js le charge en direct depuis l'aéroport
du visiteur, avec l'alerte prix (alerts.js).
"""
import html
import json

import build_i18n as B

E = html.escape


def hero_src(site, img):
    """Grande photo (-1280) si elle existe, sinon la photo normale."""
    big = img.replace(".webp", "-1280.webp")
    return big if (site / big.lstrip("/")).exists() else img

# clé, codes d'aéroport, photo d'en-tête (site/img/villes), photos de la galerie (site/img/premier), textes
DESTS = [
    ("zanzibar", "ZNZ", "zanzibar", ["zanzibar"], {
        "fr": dict(path="premier-voyage-zanzibar", name="Zanzibar", flag="🇹🇿",
                   title="Premier voyage à Zanzibar : visa, assurance obligatoire, argent, saison | Escale",
                   desc="Premier voyage à Zanzibar : e-visa de Tanzanie, assurance obligatoire de Zanzibar (44 $), fièvre jaune, argent, tenue, meilleure saison et prix du billet en direct.",
                   lead="9 choses à savoir avant de partir, et le prix du billet en direct depuis votre aéroport.",
                   items=[("🛂", "Le passeport", "Valable au moins 6 mois après le retour, avec une page vierge."),
                          ("📄", "L'e-visa de Tanzanie", "À demander en ligne avant de partir, uniquement sur le site officiel de l'immigration tanzanienne (souvent 50 $)."),
                          ("🛡️", "L'assurance obligatoire de Zanzibar", "Depuis octobre 2024, Zanzibar exige son assurance d'arrivée (44 $ par adulte), même si vous avez déjà une assurance voyage."),
                          ("💉", "La fièvre jaune", "Certificat demandé si vous venez d'un pays à risque ou y faites escale. Parlez aussi du paludisme à votre médecin."),
                          ("💵", "L'argent", "Monnaie : le shilling tanzanien. Les dollars récents sont acceptés presque partout."),
                          ("👗", "La tenue", "Île majoritairement musulmane : épaules et genoux couverts en ville, maillot seulement à la plage."),
                          ("🗣️", "Trois mots de swahili", "Jambo (bonjour), Asante (merci), Karibu (bienvenue). On parle aussi anglais."),
                          ("☀️", "La bonne saison", "Juin à octobre et décembre à février. Grandes pluies vers avril-mai."),
                          ("🔌", "Prises et eau", "Prises de type G (anglaises) : prenez un adaptateur. Buvez de l'eau en bouteille.")],
                   links=[("Demande d'e-visa (immigration de Tanzanie)", "https://visa.immigration.go.tz/")]),
        "en": dict(path="en/first-trip-zanzibar", name="Zanzibar", flag="🇹🇿",
                   title="First trip to Zanzibar: visa, mandatory insurance, money, season | Escale",
                   desc="First trip to Zanzibar: Tanzania e-visa, Zanzibar's mandatory insurance ($44), yellow fever, money, dress code, best season and live flight prices.",
                   lead="9 things to know before you go, and the live flight price from your airport.",
                   items=[("🛂", "Passport", "Valid for at least 6 months after your return, with a blank page."),
                          ("📄", "Tanzania e-visa", "Apply online before you go, only on the official Tanzanian immigration website (often $50)."),
                          ("🛡️", "Zanzibar's mandatory insurance", "Since October 2024 Zanzibar requires its own arrival insurance ($44 per adult), even if you already have travel insurance."),
                          ("💉", "Yellow fever", "A certificate is required if you come from, or transit through, a risk country. Ask your doctor about malaria too."),
                          ("💵", "Money", "Currency: the Tanzanian shilling. Recent US dollars are accepted almost everywhere."),
                          ("👗", "Dress code", "A mainly Muslim island: shoulders and knees covered in town, swimwear on the beach only."),
                          ("🗣️", "Three Swahili words", "Jambo (hello), Asante (thank you), Karibu (welcome). English is widely spoken."),
                          ("☀️", "Best season", "June to October and December to February. Long rains around April-May."),
                          ("🔌", "Plugs and water", "Type G (UK) plugs: bring an adapter. Drink bottled water.")],
                   links=[("e-Visa application (Tanzania immigration)", "https://visa.immigration.go.tz/")]),
    }),
    ("bali", "DPS", "bali", ["kelingking", "tanahlot", "riziere", "uluwatu"], {
        "fr": dict(path="premier-voyage-bali", name="Bali", flag="🇮🇩",
                   title="Premier voyage à Bali : visa à l'arrivée, taxe de Bali, carte d'arrivée, saison | Escale",
                   desc="Premier voyage à Bali : visa à l'arrivée (e-VOA), taxe touristique de Bali, carte d'arrivée All Indonesia, temples, argent, saison et prix du billet en direct.",
                   lead="9 choses à savoir avant de partir, et le prix du billet en direct depuis votre aéroport.",
                   items=[("🛂", "Le passeport", "Valable au moins 6 mois après votre arrivée, avec des pages libres."),
                          ("📄", "Le visa à l'arrivée", "Environ 500 000 roupies pour 30 jours. Demandez-le en ligne sur le site officiel (e-VOA) ou à l'aéroport."),
                          ("🎟️", "La taxe de Bali", "150 000 roupies par personne et par séjour, à payer sur le site officiel « Love Bali »."),
                          ("📱", "La carte d'arrivée", "Formulaire « All Indonesia » gratuit, à remplir en ligne quelques jours avant le vol."),
                          ("🛕", "Les temples", "Sarong obligatoire (souvent prêté à l'entrée), épaules et genoux couverts."),
                          ("🐒", "Attention aux singes", "Ils adorent les lunettes et les téléphones : rangez tout avant d'entrer dans la forêt."),
                          ("💵", "L'argent", "Monnaie : la roupie. Changez dans un bureau officiel et comptez vos billets au guichet."),
                          ("☀️", "La bonne saison", "Saison sèche d'avril à octobre. Pluies tropicales de novembre à mars, souvent courtes."),
                          ("🔌", "Prises et eau", "Prises comme en France, pas besoin d'adaptateur. Buvez de l'eau en bouteille.")],
                   links=[("Visa à l'arrivée en ligne (immigration indonésienne)", "https://evisa.imigrasi.go.id/"),
                          ("Taxe de Bali « Love Bali » (province de Bali)", "https://lovebali.baliprov.go.id/")]),
        "en": dict(path="en/first-trip-bali", name="Bali", flag="🇮🇩",
                   title="First trip to Bali: visa on arrival, Bali tourist levy, arrival card, season | Escale",
                   desc="First trip to Bali: visa on arrival (e-VOA), Bali tourist levy, All Indonesia arrival card, temples, money, best season and live flight prices.",
                   lead="9 things to know before you go, and the live flight price from your airport.",
                   items=[("🛂", "Passport", "Valid for at least 6 months after arrival, with free pages."),
                          ("📄", "Visa on arrival", "About 500,000 rupiah for 30 days. Apply online on the official site (e-VOA) or at the airport."),
                          ("🎟️", "Bali tourist levy", "150,000 rupiah per person per trip, paid on the official 'Love Bali' website."),
                          ("📱", "Arrival card", "Free 'All Indonesia' form, to fill in online a few days before your flight."),
                          ("🛕", "Temples", "Sarong required (often lent at the entrance), shoulders and knees covered."),
                          ("🐒", "Watch the monkeys", "They love sunglasses and phones: put everything away before entering the forest."),
                          ("💵", "Money", "Currency: the rupiah. Change money at official exchange offices and count your notes at the counter."),
                          ("☀️", "Best season", "Dry season April to October. Tropical rain November to March, usually short."),
                          ("🔌", "Plugs and water", "European plugs (type C/F): no adapter needed from mainland Europe. Drink bottled water.")],
                   links=[("Visa on arrival online (Indonesian immigration)", "https://evisa.imigrasi.go.id/"),
                          ("Bali tourist levy 'Love Bali' (Bali province)", "https://lovebali.baliprov.go.id/")]),
    }),
    ("japon", "TYO", "tokyo", ["fuji", "fushimi", "kinkakuji", "shibuya"], {
        "fr": dict(path="premier-voyage-japon", name="Japon", flag="🇯🇵",
                   title="Premier voyage au Japon : visa, Visit Japan Web, argent, prises, saison | Escale",
                   desc="Premier voyage au Japon : pas de visa jusqu'à 90 jours pour un passeport français, Visit Japan Web, prises, espèces, pourboire, saison et prix du billet en direct.",
                   lead="7 choses à savoir avant de partir, et le prix du billet en direct depuis votre aéroport.",
                   items=[("🛂", "Pas de visa", "Jusqu'à 90 jours pour un séjour touristique avec un passeport français. Passeport valide pendant tout le séjour."),
                          ("📱", "Visit Japan Web", "Enregistrement gratuit en ligne avant le vol : un QR code pour passer plus vite l'immigration et la douane."),
                          ("🔌", "Les prises", "Prises plates et 100 V : prenez un adaptateur."),
                          ("💴", "Le liquide", "Le yen en espèces reste utile. Les distributeurs des konbini acceptent souvent les cartes étrangères."),
                          ("🙇", "Pas de pourboire", "Au Japon, on ne laisse pas de pourboire. Et on parle doucement dans le train."),
                          ("👟", "Les chaussures", "On les enlève dans les maisons, les ryokans et certains temples."),
                          ("🌸", "La bonne saison", "Printemps (cerisiers fin mars - début avril) et automne pour les couleurs.")],
                   links=[("Visit Japan Web (gouvernement japonais)", "https://www.vjw.digital.go.jp/")]),
        "en": dict(path="en/first-trip-japan", name="Japan", flag="🇯🇵",
                   title="First trip to Japan: visa, Visit Japan Web, money, plugs, season | Escale",
                   desc="First trip to Japan: entry rules, Visit Japan Web, plugs, cash, no tipping, best season and live flight prices from your airport.",
                   lead="7 things to know before you go, and the live flight price from your airport.",
                   items=[("🛂", "Visa", "Many passports (EU, UK, US…) need no visa for up to 90 days of tourism: check for yours. Passport valid for your whole stay."),
                          ("📱", "Visit Japan Web", "Free online registration before your flight: a QR code for faster immigration and customs."),
                          ("🔌", "Plugs", "Flat-pin plugs and 100 V: bring an adapter."),
                          ("💴", "Cash", "Yen in cash is still useful. Convenience-store ATMs often accept foreign cards."),
                          ("🙇", "No tipping", "In Japan you don't tip. And keep your voice down on trains."),
                          ("👟", "Shoes", "Take them off in homes, ryokans and some temples."),
                          ("🌸", "Best season", "Spring (cherry blossoms late March - early April) and autumn for the colours.")],
                   links=[("Visit Japan Web (Japanese government)", "https://www.vjw.digital.go.jp/")]),
    }),
]

UI = {
    "fr": dict(h1="Premier voyage {pre} <span>{name}</span> ?", pre={"zanzibar": "à", "bali": "à", "japon": "au"}, eyebrow="Premier voyage",
               know="À savoir avant de partir", price_h="Et le billet ?", price_p="Meilleur aller-retour des deux prochains mois, en direct depuis votre aéroport.",
               off="Sites officiels", checked="Règles vérifiées en novembre 2026 : elles peuvent changer. Vérifiez toujours sur les sites officiels avant de partir.",
               photo="Photo", other="Autres premiers voyages", bell="Alerte prix", alert_for="Alerte pour :", from_l="dès", loading="Prix en cours…", none="Comparer les prix",
               flight="Vols aller-retour", from_txt="Départ de", act_h="Activités et excursions", act_p="Excursions, visites guidées et transferts à réserver avant de partir.", act_b="Voir les activités sur Klook"),
    "en": dict(h1="First trip to <span>{name}</span>?", pre={}, eyebrow="First trip",
               know="Good to know before you go", price_h="And the flight?", price_p="Best round trip over the next two months, live from your airport.",
               off="Official websites", checked="Rules checked in November 2026: they can change. Always check the official websites before you travel.",
               photo="Photo", other="Other first trips", bell="Price alert", alert_for="Alert for:", from_l="from", loading="Loading price…", none="Compare prices",
               flight="Round-trip flights", from_txt="Leaving from", act_h="Tours and activities", act_p="Day trips, guided tours and transfers to book before you go.", act_b="See activities on Klook"),
}


def build(site, ctx):
    photos = json.loads((site / "data" / "premier-photos.json").read_text(encoding="utf-8"))
    villes = {p["code"]: p for p in json.loads((site / "data" / "photos.json").read_text(encoding="utf-8"))}
    urls = []
    for key, code, hero_img, gallery, texts in DESTS:
        paths = {l: texts[l]["path"] for l in texts}
        for lang, t in texts.items():
            u = UI[lang]
            h1 = u["h1"].format(pre=u["pre"].get(key, ""), name=E(t["name"]))
            cards = "".join(f'<li class="pv-item"><span class="pv-ic" aria-hidden="true">{ic}</span><div><h3>{E(h)}</h3><p>{E(d)}</p></div></li>' for ic, h, d in t["items"])
            gal = ""
            if len(gallery) > 1:
                gal = '<ul class="pv-gal">' + "".join(
                    f'<li><img src="/img/premier/{g}.webp" alt="" width="480" height="640" loading="lazy" decoding="async"><small>{E(u["photo"])} : <a href="{E(photos[g]["page"])}" target="_blank" rel="noopener">{E(photos[g]["author"][:40])}</a>, {E(photos[g]["license"])}</small></li>'
                    for g in gallery) + "</ul>"
            v = next((p for p in villes.values() if p["img"].endswith(f"/{hero_img}.webp")), None)
            fq = "" if lang == "fr" else "&amp;lang=en"
            price = (f'<ul class="tr-grid pv-price"><li class="tr-card" data-to="{code}"><a class="tr-link" href="/?type=vols&amp;to={code}{fq}">'
                     f'<img src="/img/premier/{gallery[0]}.webp" alt="{E(t["name"])}" width="480" height="640" loading="lazy" decoding="async">'
                     f'<span class="tr-info"><strong>{E(t["flag"])} {E(t["name"])}</strong><small>{E(u["flight"])}</small><span class="tr-price" aria-live="polite"></span></span></a>'
                     f'<button type="button" class="tr-bell alert-cta" hidden data-name="{E(t["name"])}">🔔 {E(u["bell"])}</button></li></ul>')
            others = [d for d in DESTS if d[0] != key]
            other = "".join(f'<li><a href="/{d[4][lang]["path"]}/">{E(d[4][lang]["flag"])} {E(d[4][lang]["name"])}</a></li>' for d in others)
            body = (f'<section><h2>{E(u["know"])}</h2><ol class="pv-list">{cards}</ol></section>{gal}'
                    f'<section class="pv-price-sec"><h2>{E(u["price_h"])}</h2><p class="small">{E(u["price_p"])} <span class="tr-from" hidden>· {E(u["from_txt"])} <strong class="tr-from-city"></strong></span></p>{price}</section>'
                    f'<section class="pv-act"><h2>🎟️ {E(u["act_h"])}</h2><p>{E(u["act_p"])}</p><p><a class="btn ghost" href="https://klook.tpm.lv/MHEoG42I" target="_blank" rel="sponsored noopener noreferrer">{E(u["act_b"])} ↗</a></p></section>'
                    f'<section id="price-alert" class="price-alert" data-from="PAR" data-to="{code}" data-for="{E(u["alert_for"])}" hidden></section>'
                    f'<section><h2>{E(u["off"])}</h2><ul>' + "".join(f'<li><a href="{x}" target="_blank" rel="noopener">{E(n)}</a></li>' for n, x in t["links"]) +
                    f'</ul><p class="small">{E(u["checked"])}</p></section>'
                    f'<section><h2>{E(u["other"])}</h2><ul class="pv-other">{other}</ul></section>'
                    f'<div id="tr-cfg" hidden data-from="{E(u["from_l"])}" data-loading="{E(u["loading"])}" data-none="{E(u["none"])}"></div>'
                    '<script src="/fetes.js" defer></script><script src="/tendances.js" defer></script><script src="/alerts.js" defer></script>')
            img = (f'<img class="pv-hero" src="{hero_src(site, v["img"])}" alt="{E(t["name"])}" width="1280" height="960" fetchpriority="high">'
                   f'<p class="pv-cred small">{E(u["photo"])} : {E(v["author"][:50])}, {E(v["license"])}</p>') if v else ""
            hero = f'<p class="eyebrow">{E(t["flag"])} {E(u["eyebrow"])}</p><h1>{h1}</h1><p class="hero-lead">{E(t["lead"])}</p>{img}'
            ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": t["title"].split(" | ")[0],
                                                                       "description": t["desc"], "inLanguage": lang, "dateModified": "2026-11-04",
                                                                       "author": {"@type": "Organization", "name": "Escale"}}, ensure_ascii=False) + "</script>"
            urls.append(B.write(site, t["path"], lang, t["title"], t["desc"], hero, body, ld, paths, ctx))
    return urls
