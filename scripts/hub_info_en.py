"""« Travel essentials » on the English "flights to …" pages (scripts/hubs.py): visa by nationality, currency, best time to go,
airport to city, and useful partner services. These pages get impressions from the UK, Ireland and North America (Search Console).

Entry rules are summarised cautiously and always point to official advice: they depend on nationality and change.
Checked: October 2026. Review once a year (update CHECKED).
"""
import html

E = html.escape
CHECKED = "October 2026"
NAT = ("UK", "US", "Canada", "EU")
ESIM = "https://airalo.tpm.lv/FrG2grmd"
TRANSFER = "https://kiwitaxi.tpm.lv/hWfXu1nw"

# French city name (as in the routes) → info. visa: one short answer per nationality (UK, US, Canada, EU).
INFO = {
    "Tunis": dict(country="Tunisia", gov="tunisia",
                  visa=["No visa needed for a tourist stay", "No visa needed for a tourist stay", "No visa needed for a tourist stay", "No visa needed for a tourist stay"],
                  money="Tunisian dinar (TND). It cannot be taken out of the country: change only what you need and keep your exchange receipts.",
                  best="April to June and September to October: warm and sunny without the peak-summer heat and prices.",
                  airport="Tunis-Carthage Airport is about 8 km from the city centre: allow 15 to 25 minutes by taxi.",
                  extra="Combine Tunis with Sidi Bou Said, Carthage and the beaches of Hammamet."),
    "Alger": dict(country="Algeria", gov="algeria",
                  visa=["Visa required, apply before you travel", "Visa required, apply before you travel", "Visa required, apply before you travel", "Visa required, apply before you travel"],
                  money="Algerian dinar (DZD). Bring euros or pounds in cash to exchange: cards are not accepted everywhere.",
                  best="March to May and September to November: mild temperatures, ideal for the city and the coast.",
                  airport="Houari-Boumediene Airport is about 20 km east of the centre: taxi or the airport train.",
                  extra="Apply for the visa at the Algerian consulate several weeks before departure, and book a changeable fare until it is issued."),
    "Abidjan": dict(country="Côte d'Ivoire", gov="",
                    visa=["Visa required (e-visa online)", "Visa required (e-visa online)", "Visa required (e-visa online)", "Visa required (e-visa online)"],
                    money="West African CFA franc (XOF), pegged to the euro. Cash is still widely used.",
                    best="December to March, the main dry season. May to July is the rainy season.",
                    airport="Félix-Houphouët-Boigny Airport is in Port-Bouët, south of the city: 30 minutes to over an hour to the Plateau or Cocody depending on traffic.",
                    extra="A yellow fever vaccination certificate is required on arrival."),
    "Casablanca": dict(country="Morocco", gov="morocco",
                       visa=["No visa needed (up to 90 days)", "No visa needed (up to 90 days)", "No visa needed (up to 90 days)", "No visa needed (up to 90 days)"],
                       money="Moroccan dirham (MAD). It cannot be taken out of the country: change money on arrival or use ATMs.",
                       best="March to May and September to November. Summer is hot inland but pleasant on the coast.",
                       airport="Mohammed V Airport is about 30 km from the city: a direct train runs to the city centre, or take a taxi.",
                       extra="Compare Casablanca with Rabat, Marrakech, Tangier or Fez: another airport may be cheaper and closer to where you are going."),
    "Marrakech": dict(country="Morocco", gov="morocco",
                      visa=["No visa needed (up to 90 days)", "No visa needed (up to 90 days)", "No visa needed (up to 90 days)", "No visa needed (up to 90 days)"],
                      money="Moroccan dirham (MAD). It cannot be taken out of the country: change money on arrival or use ATMs.",
                      best="March to May and October to November. July and August are very hot (often above 40 °C).",
                      airport="Marrakech-Menara Airport is only about 6 km from the medina: 15 to 20 minutes by taxi (agree the fare before you leave).",
                      extra="Many low-cost airlines fly to Marrakech: check the baggage allowance before comparing prices."),
    "Dakar": dict(country="Senegal", gov="senegal",
                  visa=["No visa needed (up to 90 days)", "No visa needed (up to 90 days)", "No visa needed (up to 90 days)", "No visa needed (up to 90 days)"],
                  money="West African CFA franc (XOF), pegged to the euro.",
                  best="November to May, the dry season. July to October is the rainy season, hot and humid.",
                  airport="Blaise-Diagne Airport (AIBD) is in Diass, about 45 km from Dakar: allow an hour by taxi or the express bus.",
                  extra="A yellow fever certificate may be required depending on where you travel from."),
    "Lagos": dict(country="Nigeria", gov="nigeria",
                  visa=["Visa required, apply before you travel", "Visa required, apply before you travel", "Visa required, apply before you travel", "Visa required, apply before you travel"],
                  money="Nigerian naira (NGN). Card payments are common in Lagos, but carry some cash.",
                  best="November to February, the dry season (with the Harmattan haze in December–January).",
                  airport="Murtala Muhammed Airport is in Ikeja: the drive to Victoria Island can take one to two hours in traffic.",
                  extra="A yellow fever vaccination certificate is required on arrival."),
    "Accra": dict(country="Ghana", gov="ghana",
                  visa=["Visa required, apply before you travel", "Visa required, apply before you travel", "Visa required, apply before you travel", "Visa required, apply before you travel"],
                  money="Ghanaian cedi (GHS). Mobile money and cards are widely used in Accra.",
                  best="November to March, the dry season. December is very busy and more expensive.",
                  airport="Kotoka Airport is about 10 km from central Accra: 20 to 45 minutes by taxi or ride-hailing.",
                  extra="A yellow fever vaccination certificate is required on arrival."),
    "Le Caire": dict(country="Egypt", gov="egypt",
                     visa=["Visa required: e-visa or on arrival", "Visa required: e-visa or on arrival", "Visa required: e-visa or on arrival", "Visa required: e-visa or on arrival"],
                     money="Egyptian pound (EGP). Keep small notes for tips and taxis.",
                     best="October to April. Summer is very hot.",
                     airport="Cairo International Airport is about 20 km north-east of downtown: 40 minutes to over an hour by taxi or ride-hailing.",
                     extra="The pyramids of Giza are on the opposite side of the city from the airport: plan an extra hour."),
    "Bamako": dict(country="Mali", gov="mali",
                   visa=["Visa required, apply before you travel", "Visa required, apply before you travel", "Visa required, apply before you travel", "Visa required, apply before you travel"],
                   money="West African CFA franc (XOF), pegged to the euro.",
                   best="November to February, the cool dry season.",
                   airport="Modibo-Keïta Airport is about 15 km south of the city centre.",
                   extra="Several governments advise against travel to parts of Mali: read the official advice before you book. A yellow fever certificate is required."),
}


def html_block(ct, b, hotel_href):
    d = INFO.get(ct)
    if not d:
        return "", []
    gov = f"https://www.gov.uk/foreign-travel-advice/{d['gov']}" if d["gov"] else "https://www.gov.uk/foreign-travel-advice"
    rows = "".join(f"<tr><th scope=\"row\">{E(n)} passport</th><td>{E(v)}</td></tr>" for n, v in zip(NAT, d["visa"]))
    links = [f'<li><a href="{ESIM}" target="_blank" rel="sponsored noopener">Mobile data on arrival (eSIM) · Airalo</a></li>',
             f'<li><a href="{TRANSFER}" target="_blank" rel="sponsored noopener">Airport transfer booked in advance · Kiwitaxi</a></li>']
    if hotel_href:
        links.insert(0, f'<li><a href="{hotel_href}">Cheap hotels in {E(b)}: live prices</a></li>')
    block = (f'<section class="essentials"><h2>Travel essentials for {E(b)}</h2>'
             f'<h3>Do I need a visa for {E(d["country"])}?</h3><table class="fete-table"><tbody>{rows}</tbody></table>'
             f'<p class="small">Short tourist stays. Rules depend on your nationality and change: always check the '
             f'<a href="{gov}" target="_blank" rel="noopener">UK Foreign Office advice</a>, the '
             f'<a href="https://travel.state.gov/" target="_blank" rel="noopener">US State Department</a>, '
             f'<a href="https://travel.gc.ca/travelling/advisories" target="_blank" rel="noopener">Travel.gc.ca</a> '
             f'or your own government before you book. Summary checked in {CHECKED}.</p>'
             f'<ul><li><strong>Money:</strong> {E(d["money"])}</li><li><strong>Best time to go:</strong> {E(d["best"])}</li>'
             f'<li><strong>From the airport:</strong> {E(d["airport"])}</li><li><strong>Good to know:</strong> {E(d["extra"])}</li></ul>'
             f'<h3>Before you go</h3><ul class="links">{"".join(links)}</ul></section>')
    faq = [(f"Do I need a visa for {d['country']}?", f"UK: {d['visa'][0]}. US: {d['visa'][1]}. Canada: {d['visa'][2]}. EU: {d['visa'][3]}. Rules change: check your government's official travel advice before you book."),
           (f"When is the best time to visit {b}?", d["best"])]
    return block, faq
