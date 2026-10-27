"""Unique English content for the routes and hotel pages that already show up in Google (Search Console, October 2026).

Same cautious wording as scripts/trajets.py: airlines and entry rules change, so the text says "usually" and links to
official travel advice. Update VERIFIED after each review.
"""
import html

E = html.escape
VERIFIED = "October 2026"
ADVICE = ('Entry rules depend on your nationality and can change: check the <a href="https://www.gov.uk/foreign-travel-advice" rel="noopener" target="_blank">UK Foreign Office advice</a> '
          'or your own government\'s travel advice before you go.')
YF = "A yellow fever vaccination certificate is required on arrival: keep it with your passport."
MAL = "Malaria prevention is recommended: talk to a doctor before you travel."
BAG_AF = ("On routes to West and Central Africa, full-service airlines often include one checked bag (sometimes two depending on the fare). "
          "The cheapest fares and some connecting itineraries only include a cabin bag: check the number of bags and their weight (often 23 kg) before comparing.")

ROUTES = {
    ("CDG", "DXB"): dict(
        intro="Paris – Dubai is popular both for a winter-sun break and as a stopover towards Asia, the Indian Ocean and East Africa. Dubai International is linked to the city centre by metro.",
        direct="Emirates and Air France fly non-stop from Paris-Charles de Gaulle, in about 6 h 30 to 7 h.",
        stops="Non-stop is the norm. Many tickets to Asia or the Indian Ocean let you stop in Dubai for a few days, sometimes at no extra cost.",
        season="November to March is warm but not extreme: it is high season. From June to September the heat is intense, but flights and hotels are cheaper.",
        bags="Emirates and Air France usually include one checked bag in economy, depending on the fare.",
        entry="Many European passport holders, including French and British citizens, can visit for a short stay without applying for a visa in advance. " + ADVICE,
        faq=[("Which airlines fly non-stop from Paris to Dubai?", "Usually Emirates and Air France, from Paris-Charles de Gaulle, in about 6 h 30 to 7 h."),
             ("When is the cheapest time to fly from Paris to Dubai?", "Summer (June to September) is cheaper but very hot. Late October, November and March, outside school holidays, are a good compromise.")],
    ),
    ("LHR", "DXB"): dict(
        intro="London – Dubai is one of the busiest long-haul routes from the UK, with many daily flights from Heathrow and Gatwick. Compare both airports.",
        direct="Emirates, British Airways and Virgin Atlantic usually fly non-stop, in about 7 hours.",
        stops="Non-stop is the norm and very competitive. Connecting flights only make sense for a much lower price.",
        season="November to March is the most pleasant (and most expensive) period. Summer is extremely hot but cheaper.",
        bags="The main airlines usually include a checked bag in economy, but some basic fares do not: compare the total price.",
        entry="British citizens can usually visit for a short stay without applying for a visa in advance. " + ADVICE,
        faq=[("How long is the flight from London to Dubai?", "About 7 hours non-stop."),
             ("Heathrow or Gatwick for Dubai?", "Both have non-stop flights. Search both airports: the price difference can be significant.")],
    ),
    ("LHR", "DSS"): dict(
        intro="London – Dakar is used by the Senegalese community in the UK and by travellers heading to the Petite-Côte beaches. There are few non-stop options, so the choice of connection matters.",
        direct="Regular non-stop flights are rare. Seasonal or charter flights (for example from Gatwick) have operated on some dates: check whether any exist for your dates.",
        stops="Most itineraries connect in Paris (Air France), Lisbon (TAP), Casablanca (Royal Air Maroc), Brussels (Brussels Airlines) or Madrid (Iberia). Compare the total travel time, not just the price.",
        season="The dry season, November to June, is the most pleasant. July-August, Christmas and Tabaski are the most expensive periods: book 3 to 4 months ahead.",
        bags=BAG_AF,
        entry="British citizens can usually visit Senegal for up to 90 days without a visa. Yellow fever vaccination is recommended. " + MAL + " " + ADVICE,
        faq=[("Is there a direct flight from London to Dakar?", "Not on a regular basis. Most trips connect in Paris, Lisbon, Casablanca, Brussels or Madrid; seasonal non-stop flights have operated on some dates."),
             ("Which connection is best from London to Dakar?", "Lisbon (TAP) and Casablanca (Royal Air Maroc) are often good value; Paris (Air France) has the most daily options.")],
    ),
    ("LHR", "ABJ"): dict(
        intro="London – Abidjan connects the UK with Côte d'Ivoire's economic capital. There is no non-stop flight, so the connection decides both price and travel time.",
        direct="There is no regular non-stop flight between London and Abidjan.",
        stops="The usual connections are Paris (Air France, then Air France or Air Côte d'Ivoire non-stop to Abidjan), Brussels (Brussels Airlines), Casablanca (Royal Air Maroc), Istanbul (Turkish Airlines) and Addis Ababa (Ethiopian Airlines).",
        season="Abidjan is hot and humid all year; the main rainy season runs from May to July. Prices peak in July-August and around Christmas.",
        bags=BAG_AF + " On a connecting trip, make sure your bag is checked through to Abidjan.",
        entry="Most visitors, including British citizens, need a visa (apply online before travelling). " + YF + " " + MAL + " " + ADVICE,
        faq=[("Is there a direct flight from London to Abidjan?", "No. Trips usually connect in Paris, Brussels, Casablanca, Istanbul or Addis Ababa."),
             ("What is the cheapest way to fly London – Abidjan?", "Casablanca (Royal Air Maroc) and Istanbul (Turkish Airlines) are often the cheapest; Paris is usually the fastest.")],
    ),
    ("LYS", "CMN"): dict(
        intro="Lyon – Casablanca links France's second city with Morocco's business capital in under 3 hours. Casablanca is also a handy hub for flights on to West Africa with Royal Air Maroc.",
        direct="Royal Air Maroc and low-cost airlines usually fly non-stop, in about 2 h 45.",
        stops="Non-stop is the norm. Lyon also has direct flights to Marrakech, Agadir and other Moroccan cities.",
        season="Mild weather most of the year. Prices rise in July-August, during French school holidays and around Eid.",
        bags="Low-cost airlines charge for checked bags; Royal Air Maroc often includes one depending on the fare. Compare the total price.",
        entry="Many European passport holders, including French and British citizens, can visit Morocco for up to 90 days without a visa. " + ADVICE,
        faq=[("How long is the flight from Lyon to Casablanca?", "About 2 h 45 non-stop."),
             ("Can I fly on to West Africa via Casablanca?", "Yes: Royal Air Maroc connects Casablanca with Dakar, Abidjan, Bamako and many other African cities.")],
    ),
    ("CDG", "AGA"): dict(
        intro="Paris – Agadir is a favourite winter-sun route, with beaches and around 300 days of sunshine a year, about 3 h 30 from Paris.",
        direct="Transavia, Royal Air Maroc and easyJet usually fly non-stop, from Orly or Charles de Gaulle.",
        stops="Non-stop is the norm. If prices are high, compare with Marrakech, about 3 hours away by road.",
        season="Sunny almost all year, ideal to escape the European winter. Prices rise during French school holidays, especially Christmas and February.",
        bags="Transavia and easyJet charge for checked bags; compare the total price with Royal Air Maroc.",
        entry="Many European passport holders, including French and British citizens, can visit Morocco for up to 90 days without a visa. " + ADVICE,
        faq=[("Which airlines fly from Paris to Agadir?", "Usually Transavia, Royal Air Maroc and easyJet, non-stop in about 3 h 30."),
             ("When is the best time to visit Agadir?", "All year round for the sun; outside French school holidays for the best prices.")],
    ),
    ("CDG", "JED"): dict(
        intro="Paris – Jeddah is the main gateway for Umrah and Hajj travellers from France. King Abdulaziz Airport is about 1 h 15 by road from Mecca, also linked by the Haramain high-speed train.",
        direct="Saudia flies non-stop from Paris-Charles de Gaulle, in about 5 h 45. Air France does not serve Jeddah.",
        stops="With a connection: Istanbul (Turkish Airlines), Cairo (EgyptAir), Dubai (Emirates), Doha (Qatar Airways) or Abu Dhabi (Etihad).",
        season="Prices soar during Ramadan (especially the last ten days) and around Hajj. Summer is extremely hot.",
        bags="Saudia usually includes checked bags. Zamzam water has special rules on the way back (5-litre containers, often outside the allowance): check with the airline.",
        entry="A visa is required. The Saudi tourist e-visa allows Umrah outside the Hajj season; Hajj requires a specific visa through an approved agency. Meningitis (ACYW) vaccination is required for pilgrims. " + ADVICE,
        faq=[("Is there a direct flight from Paris to Jeddah?", "Yes, with Saudia from Paris-Charles de Gaulle, in about 5 h 45."),
             ("Which visa do I need for Umrah?", "The Saudi tourist e-visa allows Umrah outside the Hajj period. Check the current conditions before booking.")],
    ),
    ("CDG", "DSS"): dict(
        intro="Paris – Dakar is one of the busiest routes between Europe and West Africa. Flights land at Blaise Diagne International Airport (AIBD), 45 minutes to an hour from Dakar; a regional express train (TER) also links the area to the city.",
        direct="Air France and Air Senegal fly non-stop from Paris, in about 5 h 30.",
        stops="With a connection: Casablanca (Royal Air Maroc), Lisbon (TAP), Madrid (Iberia), Brussels (Brussels Airlines) or Istanbul (Turkish Airlines), sometimes much cheaper in high season.",
        season="The dry season, November to June, is the most pleasant. July-August, Christmas, Tabaski and the Grand Magal of Touba are the most expensive periods.",
        bags=BAG_AF,
        entry="French and British citizens can usually visit Senegal for up to 90 days without a visa. Yellow fever vaccination is recommended. " + MAL + " " + ADVICE,
        faq=[("Which airlines fly non-stop from Paris to Dakar?", "Air France and Air Senegal, in about 5 h 30."),
             ("How do I get from AIBD airport to Dakar?", "By taxi, shuttle or the TER train from Diamniadio: allow 45 minutes to over an hour depending on traffic.")],
    ),
    ("CDG", "ABJ"): dict(
        intro="Paris – Abidjan is a very competitive route serving Côte d'Ivoire's economic capital. Flights land at Félix-Houphouët-Boigny Airport, about 20 minutes from the Plateau business district outside rush hour.",
        direct="Several airlines fly non-stop in about 6 h 30: Air France from Charles de Gaulle, Air Côte d'Ivoire and Corsair from Orly. Air France and Air Côte d'Ivoire codeshare since late October 2026.",
        stops="With a connection: Casablanca, Brussels, Tunis, Istanbul or Addis Ababa. Non-stop competition makes these less attractive than on other routes.",
        season="Hot and humid all year; the main rainy season runs from May to July. Prices peak in July-August and at Christmas.",
        bags=BAG_AF,
        entry="Most visitors need a visa (online application before departure). " + YF + " " + MAL + " " + ADVICE,
        faq=[("Which airlines fly non-stop from Paris to Abidjan?", "Usually Air France from Charles de Gaulle, Air Côte d'Ivoire and Corsair from Orly."),
             ("Do I need a visa for Côte d'Ivoire?", "Most visitors do: apply online before travelling. A yellow fever certificate is also required.")],
    ),
    ("CDG", "BKO"): dict(
        intro="Paris – Bamako serves one of the largest West African communities in France. Since 2023 non-stop options have been very limited, so most travellers connect.",
        direct="Air France has not served Bamako since August 2023. Corsair has operated non-stop flights from Orly with interruptions: check whether they run on your dates.",
        stops="Connections are the norm: Casablanca (Royal Air Maroc), Algiers (Air Algérie), Tunis (Tunisair), Istanbul (Turkish Airlines), Addis Ababa (Ethiopian Airlines), Dakar (Air Senegal) or Abidjan (Air Côte d'Ivoire).",
        season="November to February is the most pleasant period. March to May is very hot and the rainy season runs from June to September.",
        bags=BAG_AF + " Make sure your bag is checked through to Bamako.",
        entry="Most visitors need a visa. " + YF + " " + MAL + " Security conditions change: read your government's travel advice carefully.",
        faq=[("Are there direct flights from Paris to Bamako?", "Not with Air France since 2023. Corsair has operated non-stop flights with interruptions; most trips connect in Casablanca, Algiers, Tunis or Istanbul."),
             ("What is the best connection to Bamako?", "Casablanca, Algiers and Tunis often give the shortest trips. Compare the total travel time.")],
    ),
}

HOTELS = {
    "Bamako": dict(
        intro="Bamako spreads along both banks of the Niger. Most visitors stay in ACI 2000 or Hippodrome for business and restaurants, or near the river for a calmer setting. Modibo Keïta Airport is about 15 km south of the centre.",
        tips=["Book a room with a generator and air conditioning: power cuts can happen and the heat is intense from March to May.",
              "Serviced apartments are common and often good value for stays of a week or more.",
              "Ask the hotel to arrange an airport pick-up, especially for late-night arrivals."],
        faq=[("Which area is best to stay in Bamako?", "ACI 2000 and Hippodrome are practical for business, restaurants and nightlife; the riverside areas are calmer."),
             ("Are there serviced apartments in Bamako?", "Yes, many hotels and residences offer apartments with a kitchen, often good value for longer stays.")],
    ),
    "Douala": dict(
        intro="Douala is Cameroon's economic capital and main port. Akwa and Bonanjo are the business districts with most hotels; Bonapriso is quieter and residential. The airport is close to the centre, about 15 to 30 minutes by car depending on traffic.",
        tips=["Traffic is heavy at rush hour: choose a hotel close to your meetings.",
              "It rains a lot, especially from July to September: plan extra time for journeys.",
              "Many hotels offer airport transfers: book one in advance for a night arrival."],
        faq=[("Where to stay in Douala?", "Akwa and Bonanjo for business and convenience; Bonapriso for a quieter, residential area."),
             ("How far is Douala airport from the city centre?", "Only a few kilometres: about 15 to 30 minutes by car depending on traffic.")],
    ),
    "Kinshasa": dict(
        intro="Kinshasa is huge, and traffic can turn short distances into long journeys. Most visitors stay in Gombe, the business and diplomatic district along the river. N'djili Airport is about 25 km from Gombe: allow an hour or more.",
        tips=["Stay in Gombe if you are visiting for business: most offices and embassies are there.",
              "Book an airport transfer in advance, especially for a night arrival.",
              "Prices are high compared with the region: compare several sites and book early."],
        faq=[("Which area is best to stay in Kinshasa?", "Gombe, the business and diplomatic district, is the most practical and the most popular with visitors."),
             ("How long does it take from N'djili airport to Gombe?", "About 25 km: often an hour or more depending on traffic.")],
    ),
}


def route_html(tj, a, b, partners):
    links = " · ".join(f'<a href="{E(partners[k]["url"])}" target="_blank" rel="sponsored noopener noreferrer">{t}</a>'
                       for k, t in (("esim", "mobile data from landing (eSIM)"), ("transfer", "airport transfer booked in advance")) if k in partners)
    p = lambda t, x: f"<h3>{E(t)}</h3><p>{E(x)}</p>"
    return (f'<section class="trajet"><h2>{E(a)} – {E(b)} at a glance</h2><p>{E(tj["intro"])}</p>'
            + (f'<p class="small">On arrival in {E(b)}: {links}.</p>' if links else "")
            + p("Non-stop flights", tj["direct"]) + p("Flights with a connection", tj["stops"]) + "</section>"
            + f'<section><h2>When to go to {E(b)}</h2><p>{E(tj["season"])}</p><p><a href="/en/guides/when-to-book/">When to book to pay less</a></p></section>'
            + f'<section><h2>Baggage</h2><p>{E(tj["bags"])}</p><p><a href="/en/guides/baggage/">Our baggage guide</a></p></section>'
            + f'<section><h2>Entry requirements</h2><p>{tj["entry"]}</p>'
            + f'<p class="small">Checked in {VERIFIED}. Airlines and schedules change with the seasons: always check on the booking site.</p></section>')


def hotel_html(h, c, partners):
    links = " · ".join(f'<a href="{E(partners[k]["url"])}" target="_blank" rel="sponsored noopener noreferrer">{t}</a>'
                       for k, t in (("transfer", "book an airport transfer"), ("esim", "get mobile data with an eSIM")) if k in partners)
    return (f'<section class="trajet"><h2>Staying in {E(c)}: what to know</h2><p>{E(h["intro"])}</p>'
            + '<ul class="plain">' + "".join(f"<li>{E(t)}</li>" for t in h["tips"]) + "</ul>"
            + (f'<p class="small">Before you arrive: {links}.</p>' if links else "") + "</section>")
