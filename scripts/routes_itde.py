"""Versions italienne et allemande des 34 grands trajets (Paris, Bruxelles, Marseille, Lyon, Genève → Afrique, Maghreb, Outre-mer…).

Les visiteurs italiens et allemands qui arrivent sur « Vol Paris → Dakar » ont la page dans leur langue (site/langue.js les y mène
tout seul). Mêmes informations que la page française : durée, aéroport, saisons chères, conseil, prix en direct.
Chaque entrée : (it, de). Branché dans build_i18n.build().
"""

LANGS = ["it", "de"]
COLX = {"it": 0, "de": 1}

UI = {
    "it": dict(
        hotel_slug="hotel-economici",
        title_route="Voli economici {a} {b}: confronta i prezzi",
        desc_route="Voli economici {a} – {b} ({fa} → {ta}): prezzi in diretta di decine di compagnie, i giorni più economici e un avviso prezzo gratuito.",
        h1_route="Voli economici {a} <span>→</span> {b}", cta="Confronta i prezzi ora", back="Ritorno {b} → {a}",
        duration="Durata del volo", arrival="Arrivo", peak="Periodi più cari",
        dur_direct="Circa {d} con volo diretto", dur_var="Variabile: la maggior parte dei viaggi ha almeno uno scalo",
        dur_long_direct="Circa {d} con volo diretto", dur_long_var="Dipende: la maggior parte dei viaggi ha almeno uno scalo",
        prices_h="Prezzi trovati di recente",
        prices_p="Prezzi andata e ritorno più bassi trovati dai viaggiatori negli ultimi giorni, per mese di partenza. La tariffa esatta disponibile appare sui siti di prenotazione.",
        tip_h="Il nostro consiglio per questa tratta", cheap_h="Come pagare meno",
        steps=["<strong>Attiva le date flessibili.</strong> Spostare la partenza di un giorno o due cambia spesso il prezzo più della scelta del sito.",
               "<strong>Confronta i prezzi in diretta.</strong> La ricerca di Escale confronta in tempo reale decine di compagnie e agenzie, ordinate per prezzo.",
               "<strong>Controlla il bagaglio.</strong> Aggiungi il prezzo della valigia prima di confrontare due tariffe.",
               "<strong>Crea un avviso prezzo gratuito</strong> su questa pagina se parti fra qualche mese: ricevi un'e-mail quando il prezzo scende."],
        launch="Cerca {a} → {b}", direct_h="Accesso diretto ai comparatori",
        sky="Prezzi e date su Aviasales", hotels_in="Hotel a {b}", cars_in="Noleggio auto a {b}",
        faq_h="Domande frequenti", other_routes="Altre tratte",
        faq=[("Quanto dura un volo {a} – {b}?", "{dur_long}. Con uno scalo, il viaggio totale dura spesso alcune ore in più a seconda della coincidenza."),
             ("Quando prenotare un volo economico {a} – {b}?", "Di solito due o tre mesi prima della partenza. I prezzi salgono molto durante {peak}: per questi periodi prenota prima."),
             ("Quale aeroporto a {b}?", "I voli arrivano a {airport} ({ta})."),
             ("Il bagaglio è incluso?", "Non sempre. Le tariffe più basse a volte includono solo una borsa piccola. Controlla la franchigia del bagaglio in stiva prima di pagare.")],
        est="Circa {d} senza scalo (stima in base alla distanza di {km} km)",
    ),
    "de": dict(
        hotel_slug="guenstige-hotels",
        title_route="Günstige Flüge {a} {b}: Preise vergleichen",
        desc_route="Günstige Flüge {a} – {b} ({fa} → {ta}): Live-Preise von Dutzenden Airlines, die günstigsten Tage und ein kostenloser Preisalarm.",
        h1_route="Günstige Flüge {a} <span>→</span> {b}", cta="Jetzt Preise vergleichen", back="Rückflug {b} → {a}",
        duration="Flugdauer", arrival="Ankunft", peak="Teuerste Zeiten",
        dur_direct="Etwa {d} im Direktflug", dur_var="Unterschiedlich: Die meisten Verbindungen haben mindestens einen Zwischenstopp",
        dur_long_direct="Etwa {d} im Direktflug", dur_long_var="Das ist unterschiedlich: Die meisten Verbindungen haben mindestens einen Zwischenstopp",
        prices_h="Kürzlich gefundene Preise",
        prices_p="Niedrigste Preise für Hin- und Rückflug, die Reisende in den letzten Tagen gefunden haben, nach Abflugmonat. Der genaue verfügbare Tarif erscheint auf den Buchungsseiten.",
        tip_h="Unser Tipp für diese Strecke", cheap_h="So zahlst du weniger",
        steps=["<strong>Flexible Daten einschalten.</strong> Ein oder zwei Tage früher oder später ändern den Preis oft mehr als die Wahl der Website.",
               "<strong>Live-Preise vergleichen.</strong> Die Suche von Escale vergleicht in Echtzeit Dutzende Airlines und Reisebüros, nach Preis sortiert.",
               "<strong>Gepäck prüfen.</strong> Rechne den Preis für den Koffer ein, bevor du zwei Tarife vergleichst.",
               "<strong>Kostenlosen Preisalarm erstellen</strong> auf dieser Seite, wenn du erst in einigen Monaten fliegst: Du bekommst eine E-Mail, wenn der Preis sinkt."],
        launch="Suche {a} → {b}", direct_h="Direkt zu den Vergleichsseiten",
        sky="Preise und Daten auf Aviasales", hotels_in="Hotels in {b}", cars_in="Mietwagen in {b}",
        faq_h="Häufige Fragen", other_routes="Weitere Strecken",
        faq=[("Wie lange dauert ein Flug {a} – {b}?", "{dur_long}. Mit Zwischenstopp dauert die Reise je nach Anschluss oft einige Stunden länger."),
             ("Wann sollte ich einen günstigen Flug {a} – {b} buchen?", "Meist zwei bis drei Monate vor Abflug. In folgenden Zeiten steigen die Preise stark: {peak}. Buche dafür früher."),
             ("Welcher Flughafen in {b}?", "Die Flüge landen in {airport} ({ta})."),
             ("Ist Gepäck inklusive?", "Nicht immer. Die günstigsten Tarife enthalten manchmal nur ein kleines Handgepäck. Prüfe die Freigepäckmenge vor dem Bezahlen.")],
        est="Etwa {d} nonstop (Schätzung nach der Entfernung von {km} km)",
    ),
}

CITIES = {
    "Paris": ("Parigi", "Paris"), "Bruxelles": ("Bruxelles", "Brüssel"), "Marseille": ("Marsiglia", "Marseille"), "Lyon": ("Lione", "Lyon"),
    "Genève": ("Ginevra", "Genf"), "Bamako": ("Bamako", "Bamako"), "Dakar": ("Dakar", "Dakar"), "Abidjan": ("Abidjan", "Abidjan"),
    "Conakry": ("Conakry", "Conakry"), "Douala": ("Douala", "Douala"), "Lomé": ("Lomé", "Lomé"), "Cotonou": ("Cotonou", "Cotonou"),
    "Ouagadougou": ("Ouagadougou", "Ouagadougou"), "Kinshasa": ("Kinshasa", "Kinshasa"), "Casablanca": ("Casablanca", "Casablanca"),
    "Alger": ("Algeri", "Algier"), "Tunis": ("Tunisi", "Tunis"), "Montréal": ("Montréal", "Montreal"), "Dubaï": ("Dubai", "Dubai"),
    "Libreville": ("Libreville", "Libreville"), "Yaoundé": ("Yaoundé", "Yaoundé"), "Nouakchott": ("Nouakchott", "Nouakchott"),
    "Niamey": ("Niamey", "Niamey"), "Marrakech": ("Marrakech", "Marrakesch"), "Istanbul": ("Istanbul", "Istanbul"),
    "Djeddah": ("Gedda", "Dschidda"), "Pointe-à-Pitre": ("Pointe-à-Pitre", "Pointe-à-Pitre"), "La Réunion": ("Riunione", "Réunion"),
}

COUNTRIES = {
    "Algérie": ("Algeria", "Algerien"), "Arabie saoudite": ("Arabia Saudita", "Saudi-Arabien"), "Burkina Faso": ("Burkina Faso", "Burkina Faso"),
    "Bénin": ("Benin", "Benin"), "Cameroun": ("Camerun", "Kamerun"), "Canada": ("Canada", "Kanada"), "Côte d'Ivoire": ("Costa d'Avorio", "Elfenbeinküste"),
    "Gabon": ("Gabon", "Gabun"), "Guadeloupe": ("Guadalupa", "Guadeloupe"), "Guinée": ("Guinea", "Guinea"), "La Réunion": ("Riunione", "Réunion"),
    "Mali": ("Mali", "Mali"), "Maroc": ("Marocco", "Marokko"), "Mauritanie": ("Mauritania", "Mauretanien"), "Niger": ("Niger", "Niger"),
    "RD Congo": ("RD del Congo", "DR Kongo"), "Sénégal": ("Senegal", "Senegal"), "Togo": ("Togo", "Togo"), "Tunisie": ("Tunisia", "Tunesien"),
    "Turquie": ("Turchia", "Türkei"), "Émirats arabes unis": ("Emirati Arabi Uniti", "Vereinigte Arabische Emirate"),
}

PEAKS = {
    "de novembre à mars, quand il fait moins chaud": ("da novembre a marzo, quando fa meno caldo", "November bis März, wenn es weniger heiß ist"),
    "juillet-août et décembre-janvier": ("luglio-agosto e dicembre-gennaio", "Juli–August und Dezember–Januar"),
    "juillet-août et l'Aïd": ("luglio-agosto e l'Eid", "Juli–August und das Opferfest/Zuckerfest (Eid)"),
    "juillet-août et les fêtes de fin d'année": ("luglio-agosto e le feste di fine anno", "Juli–August und die Feiertage zum Jahresende"),
    "juillet-août et les vacances de printemps": ("luglio-agosto e le vacanze di primavera", "Juli–August und die Frühlingsferien"),
    "juillet-août, Noël et le carnaval": ("luglio-agosto, Natale e il carnevale", "Juli–August, Weihnachten und Karneval"),
    "juillet-août, l'Aïd et les vacances scolaires": ("luglio-agosto, l'Eid e le vacanze scolastiche", "Juli–August, Eid und die Schulferien"),
    "juillet-août, les fêtes de fin d'année et la Tabaski": ("luglio-agosto, le feste di fine anno e la Tabaski", "Juli–August, die Feiertage zum Jahresende und Tabaski"),
    "juillet-août, les fêtes de fin d'année, la Tabaski et le Magal de Touba": ("luglio-agosto, le feste di fine anno, la Tabaski e il Magal di Touba",
                                                                             "Juli–August, die Feiertage zum Jahresende, Tabaski und der Magal von Touba"),
    "juillet-août, les vacances scolaires et l'Aïd": ("luglio-agosto, le vacanze scolastiche e l'Eid", "Juli–August, die Schulferien und Eid"),
    "le Ramadan, le Hajj et les vacances scolaires": ("il Ramadan, l'Hajj e le vacanze scolastiche", "Ramadan, Hadsch und die Schulferien"),
    "les vacances scolaires, Noël et Pâques": ("le vacanze scolastiche, Natale e Pasqua", "die Schulferien, Weihnachten und Ostern"),
}

NOTES = {
    "CDG-BKO": ("I voli diretti da Parigi sono rari o sospesi in alcuni periodi: la maggior parte dei viaggi fa scalo a Casablanca, Algeri, Tunisi, Istanbul o Addis Abeba. Confronta la durata totale, non solo il prezzo.",
                "Direktflüge ab Paris sind selten oder zeitweise ausgesetzt: Die meisten Verbindungen führen über Casablanca, Algier, Tunis, Istanbul oder Addis Abeba. Vergleiche die gesamte Reisezeit, nicht nur den Preis."),
    "CDG-DSS": ("Ci sono voli anche da Orly: seleziona entrambi gli aeroporti di Parigi nei comparatori per avere più scelta.",
                "Es gibt auch Flüge ab Orly: Wähle in den Vergleichsseiten beide Pariser Flughäfen, um mehr Auswahl zu haben."),
    "CDG-ABJ": ("Diverse compagnie volano su questa tratta da Roissy e Orly: la concorrenza fa spesso scendere i prezzi in bassa stagione.",
                "Mehrere Airlines fliegen die Strecke ab Roissy und Orly: Die Konkurrenz drückt die Preise in der Nebensaison oft nach unten."),
    "CDG-CKY": ("I voli con scalo a Casablanca, Dakar o Bruxelles sono a volte molto più economici del volo diretto.",
                "Flüge mit Zwischenstopp in Casablanca, Dakar oder Brüssel sind manchmal deutlich günstiger als der Direktflug."),
    "CDG-DLA": ("Valuta anche Yaoundé-Nsimalen (NSI) se la tua destinazione finale è nel centro del paese.",
                "Ziehe auch Yaoundé-Nsimalen (NSI) in Betracht, wenn dein Ziel in der Landesmitte liegt."),
    "CDG-LFW": ("Confronta con un volo per Cotonou (COO) o Accra (ACC) e poi la strada: a volte costa meno.",
                "Vergleiche mit einem Flug nach Cotonou (COO) oder Accra (ACC) und dann weiter über Land: Das ist manchmal günstiger."),
    "CDG-COO": ("Confronta con Lomé (LFW): le due città sono vicine e i prezzi cambiano molto.",
                "Vergleiche mit Lomé (LFW): Die beiden Städte liegen nah beieinander und die Preise schwanken stark."),
    "CDG-OUA": ("Le offerte di voli diretti cambiano con la situazione: sono frequenti i viaggi con scalo ad Abidjan, Casablanca, Algeri o Istanbul.",
                "Das Angebot an Direktflügen ändert sich je nach Lage: Verbindungen über Abidjan, Casablanca, Algier oder Istanbul sind häufig."),
    "BRU-FIH": ("Da Parigi, confronta con una partenza da Bruxelles: spesso conviene, anche con il biglietto del treno.",
                "Ab Paris lohnt der Vergleich mit einem Abflug ab Brüssel: Oft günstiger, selbst mit dem Zugticket."),
    "ORY-CMN": ("Le compagnie low cost volano anche su Marrakech, Rabat e Tangeri: guarda la città più vicina alla tua destinazione.",
                "Billigairlines fliegen auch nach Marrakesch, Rabat und Tanger: Schau dir die Stadt an, die deinem Ziel am nächsten liegt."),
    "CDG-ALG": ("Confronta con Lione, Marsiglia o Bordeaux se puoi partire da un'altra città: d'estate i prezzi cambiano molto da un aeroporto all'altro.",
                "Vergleiche mit Lyon, Marseille oder Bordeaux, wenn du von einer anderen Stadt abfliegen kannst: Im Sommer unterscheiden sich die Preise stark."),
    "CDG-TUN": ("Valuta anche Djerba (DJE) e Monastir (MIR), spesso servite da voli più economici d'estate.",
                "Ziehe auch Djerba (DJE) und Monastir (MIR) in Betracht: Im Sommer oft mit günstigeren Flügen erreichbar."),
    "CDG-YUL": ("La maggior parte dei viaggiatori ha bisogno di un'autorizzazione di viaggio elettronica (eTA): controlla prima di prenotare.",
                "Die meisten Reisenden brauchen eine elektronische Reisegenehmigung (eTA): Prüfe das vor der Buchung."),
    "CDG-DXB": ("Dubai è anche uno scalo comodo verso l'Asia e l'Africa orientale: una sosta di qualche giorno a volte non costa di più.",
                "Dubai ist auch ein praktischer Zwischenstopp Richtung Asien und Ostafrika: Ein paar Tage Aufenthalt kosten manchmal nichts extra."),
    "CDG-FIH": ("Confronta con una partenza da Bruxelles, storicamente molto ben collegata a Kinshasa: la differenza di prezzo può coprire il treno Parigi–Bruxelles.",
                "Vergleiche mit einem Abflug ab Brüssel, traditionell sehr gut mit Kinshasa verbunden: Der Preisunterschied kann den Zug Paris–Brüssel bezahlen."),
    "CDG-LBV": ("Poche compagnie volano diretto su questa tratta: prenota presto per l'estate e guarda anche gli scali a Casablanca, Addis Abeba o Douala.",
                "Nur wenige Airlines fliegen direkt: Buche für den Sommer früh und schau auch nach Verbindungen über Casablanca, Addis Abeba oder Douala."),
    "CDG-NSI": ("Confronta con Douala (DLA): a seconda delle date, atterrare a Douala e proseguire in auto o con un volo interno può costare meno.",
                "Vergleiche mit Douala (DLA): Je nach Datum kann es günstiger sein, in Douala zu landen und mit dem Auto oder einem Inlandsflug weiterzureisen."),
    "CDG-NKC": ("Sono frequenti i viaggi con scalo a Casablanca, Tunisi o Dakar: confronta il tempo di coincidenza.",
                "Verbindungen mit Zwischenstopp in Casablanca, Tunis oder Dakar sind häufig: Vergleiche die Umsteigezeit."),
    "CDG-NIM": ("Le offerte di volo cambiano con la situazione: usa i comparatori per vedere quali coincidenze sono disponibili (Casablanca, Algeri, Istanbul, Addis Abeba…).",
                "Das Flugangebot ändert sich je nach Lage: Nutze die Vergleichsseiten, um verfügbare Verbindungen zu sehen (Casablanca, Algier, Istanbul, Addis Abeba…)."),
    "CDG-RAK": ("Molti voli low cost partono da Orly e Beauvais: controlla tutti e tre gli aeroporti di Parigi.",
                "Viele Billigflüge starten ab Orly und Beauvais: Prüfe alle drei Pariser Flughäfen."),
    "CDG-IST": ("Valuta anche l'aeroporto Sabiha Gökçen (SAW), sul lato asiatico, spesso servito da compagnie più economiche.",
                "Ziehe auch den Flughafen Sabiha Gökçen (SAW) auf der asiatischen Seite in Betracht: oft von günstigeren Airlines angeflogen."),
    "CDG-JED": ("Per l'Umrah prenota il prima possibile prima del Ramadan: i prezzi salgono molto. Medina (MED) è un aeroporto di arrivo alternativo.",
                "Für die Umrah so früh wie möglich vor dem Ramadan buchen: Die Preise steigen stark. Medina (MED) ist ein alternativer Ankunftsflughafen."),
    "CDG-PTP": ("I voli partono da Roissy e Orly: confronta entrambi, le differenze di prezzo sono frequenti.",
                "Die Flüge starten ab Roissy und Orly: Vergleiche beide, Preisunterschiede sind häufig."),
    "CDG-RUN": ("Confronta anche l'arrivo a Saint-Pierre Pierrefonds (ZSE) se vai nel sud dell'isola.",
                "Vergleiche auch die Ankunft in Saint-Pierre Pierrefonds (ZSE), wenn du in den Süden der Insel willst."),
    "MRS-ALG": ("D'estate i prezzi salgono molto in fretta: prenota in primavera e confronta con una partenza da Lione o Montpellier.",
                "Im Sommer steigen die Preise sehr schnell: Buche im Frühling und vergleiche mit einem Abflug ab Lyon oder Montpellier."),
    "MRS-TUN": ("Confronta con Djerba (DJE) e Monastir (MIR) a seconda della tua destinazione finale.",
                "Vergleiche je nach Ziel mit Djerba (DJE) und Monastir (MIR)."),
    "MRS-DSS": ("Confronta un volo da Marsiglia con scalo con un treno per Parigi seguito da un volo diretto: il secondo a volte costa meno.",
                "Vergleiche einen Flug ab Marseille mit Zwischenstopp mit einer Zugfahrt nach Paris und einem Direktflug: Letzteres ist manchmal günstiger."),
    "LYS-CMN": ("Guarda anche i voli Lione–Marrakech e Lione–Oujda a seconda della tua destinazione finale.",
                "Schau je nach Ziel auch nach Flügen Lyon–Marrakesch und Lyon–Oujda."),
    "LYS-DSS": ("Confronta con una partenza da Ginevra, a meno di 2 ore da Lione: a volte ci sono più opzioni.",
                "Vergleiche mit einem Abflug ab Genf, weniger als 2 Stunden von Lyon: Manchmal gibt es mehr Auswahl."),
    "BRU-DSS": ("Dal nord della Francia, confronta con Parigi: la differenza di prezzo copre spesso il treno.",
                "Aus Nordfrankreich lohnt der Vergleich mit Paris: Der Preisunterschied deckt oft die Zugfahrt."),
    "BRU-ABJ": ("Confronta con una partenza da Parigi: lì la concorrenza è più forte e le offerte più frequenti.",
                "Vergleiche mit einem Abflug ab Paris: Dort ist die Konkurrenz größer und Angebote sind häufiger."),
    "BRU-DLA": ("Confronta la durata totale del viaggio: alcuni voli fanno uno scalo tecnico in Africa occidentale o centrale.",
                "Vergleiche die gesamte Reisezeit: Manche Flüge machen einen technischen Zwischenstopp in West- oder Zentralafrika."),
    "GVA-CMN": ("Se vivi nella Francia vicina, confronta con Lione: entrambi gli aeroporti sono a meno di 2 ore.",
                "Wenn du im nahen Frankreich wohnst, vergleiche mit Lyon: Beide Flughäfen sind weniger als 2 Stunden entfernt."),
    "GVA-DSS": ("I voli fanno spesso scalo a Parigi, Bruxelles, Lisbona o Casablanca: confronta il tempo di attesa.",
                "Die Flüge führen oft über Paris, Brüssel, Lissabon oder Casablanca: Vergleiche die Umsteigezeit."),
}

TOP = {k for k in NOTES}


def city(name, lang):
    v = CITIES.get(name)
    return v[COLX[lang]] if v else name


def tr(table, key, lang):
    v = table.get(key)
    return v[COLX[lang]] if v else key
