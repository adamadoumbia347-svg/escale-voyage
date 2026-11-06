"""eSIM, location de voiture, hôtels d'aéroport : italien et allemand (mêmes conseils prudents que fr/en)."""
# code pays -> (slug it, nom it, slug de, nom de, préposition it « in/nel/… + nom »)
PAYS = {"ci": ("costa-d-avorio", "Costa d'Avorio", "elfenbeinkueste", "Elfenbeinküste", "in Costa d'Avorio"),
        "sn": ("senegal", "Senegal", "senegal", "Senegal", "in Senegal"), "cm": ("camerun", "Camerun", "kamerun", "Kamerun", "in Camerun"),
        "ml": ("mali", "Mali", "mali", "Mali", "in Mali"), "bj": ("benin", "Benin", "benin", "Benin", "in Benin"), "tg": ("togo", "Togo", "togo", "Togo", "in Togo"),
        "bf": ("burkina-faso", "Burkina Faso", "burkina-faso", "Burkina Faso", "in Burkina Faso"), "gn": ("guinea", "Guinea", "guinea", "Guinea", "in Guinea"),
        "ga": ("gabon", "Gabon", "gabun", "Gabun", "in Gabon"), "cd": ("rd-congo", "RD del Congo", "dr-kongo", "DR Kongo", "nella RD del Congo"),
        "ng": ("nigeria", "Nigeria", "nigeria", "Nigeria", "in Nigeria"), "gh": ("ghana", "Ghana", "ghana", "Ghana", "in Ghana"),
        "ma": ("marocco", "Marocco", "marokko", "Marokko", "in Marocco"), "dz": ("algeria", "Algeria", "algerien", "Algerien", "in Algeria"),
        "tn": ("tunisia", "Tunisia", "tunesien", "Tunesien", "in Tunisia"), "eg": ("egitto", "Egitto", "aegypten", "Ägypten", "in Egitto"),
        "ke": ("kenya", "Kenya", "kenia", "Kenia", "in Kenya")}
# slug fr de la ville -> (nom it, nom de)
VILLES = {"abidjan": ("Abidjan", "Abidjan"), "dakar": ("Dakar", "Dakar"), "casablanca": ("Casablanca", "Casablanca"), "marrakech": ("Marrakech", "Marrakesch"),
          "agadir": ("Agadir", "Agadir"), "tunis": ("Tunisi", "Tunis"), "djerba": ("Djerba", "Djerba"), "alger": ("Algeri", "Algier"), "douala": ("Douala", "Douala"),
          "accra": ("Accra", "Accra"), "lome": ("Lomé", "Lomé"), "bamako": ("Bamako", "Bamako"), "conakry": ("Conakry", "Conakry"), "kinshasa": ("Kinshasa", "Kinshasa"),
          "lagos": ("Lagos", "Lagos")}
VOWEL = ("A", "E", "I", "O", "U")


def a_it(name):
    """« a Dakar », « ad Abidjan »."""
    return ("ad " if name.startswith(VOWEL) else "a ") + name


T = {
    "it": dict(
        esim_secs=[("eSIM o SIM locale?", [
            "<strong>L'eSIM</strong> si compra online prima di partire e si installa in pochi minuti con un QR code: internet funziona appena atterri, senza cercare venditori in aeroporto. Tieni la tua SIM abituale per chiamate e SMS.",
            "<strong>La SIM locale</strong> si compra sul posto (aeroporto, negozi degli operatori). Ti dà un numero locale, utile per chiamare sul posto e per il mobile money. Di solito serve il passaporto per registrarla.",
            "Molti viaggiatori combinano le due: l'eSIM per arrivare connessi, poi una SIM locale per un soggiorno lungo."]),
            ("Prima di comprare un'eSIM", [
                "Verifica che il telefono supporti l'eSIM (impostazioni → rete mobile → «aggiungi eSIM») e che non sia bloccato dal tuo operatore.",
                "Verifica che il paese sia coperto e guarda durata e volume di dati del piano {a}.",
                "Installa l'eSIM prima di partire, con il Wi-Fi, e attivala solo all'arrivo.",
                "Disattiva il roaming della tua SIM abituale per evitare costi."]),
            ("Da sapere", [
                "WhatsApp, chiamate e messaggi passano da internet: un'eSIM «solo dati» spesso basta per restare in contatto con la famiglia.",
                "Fuori dalle grandi città la copertura può essere più debole: scarica le mappe offline prima di partire."])],
        esim_cta="Vedi le eSIM per {n}", esim_note="Link partner: Escale può ricevere una commissione, senza costi per te. Piani e prezzi da verificare su Airalo.",
        esim_title="eSIM {n}: internet appena arrivi | Escale",
        esim_desc="Essere connessi appena atterri {a}: eSIM o SIM locale, telefono compatibile, installazione e consigli.", esim_h1="Internet appena arrivi {a}",
        car_secs=[("Prima di prenotare", [
            "<strong>Patente:</strong> la patente internazionale è spesso richiesta, oltre a quella nazionale. Informati presso il noleggiatore e l'ambasciata, e porta entrambe.",
            "<strong>Età e carta:</strong> la maggior parte dei noleggiatori chiede un'età minima e una carta di credito intestata al conducente per la cauzione.",
            "<strong>Assicurazione e franchigia:</strong> guarda l'importo della franchigia (quello che paghi in caso di danni) e cosa è coperto.",
            "<strong>Carburante:</strong> scegli la formula «pieno/pieno»: restituisci l'auto con il serbatoio pieno, senza costi nascosti."]),
            ("Sul posto", [
                "Si guida a destra. Fotografa l'auto (carrozzeria, gomme, contachilometri) al ritiro e alla riconsegna.",
                "Tieni con te il contratto di noleggio, la patente e il passaporto: i controlli stradali sono frequenti.",
                "In città il traffico può essere molto intenso: prevedi margine per l'aeroporto.",
                "Un'<strong>auto con autista</strong> è spesso una buona alternativa per un primo viaggio: chiedi al noleggiatore."]),
            ("Aeroporto o centro città?", [
                "Ritirare l'auto in aeroporto è più comodo all'arrivo, ma a volte un po' più caro che in città. Confronta le due opzioni nelle offerte."])],
        car_cta="Vedi le auto {a}", car_note="Link partner: Escale può ricevere una commissione, senza costi per te. Condizioni (patente, età, cauzione) da verificare con il noleggiatore.",
        car_title="Noleggio auto {a}: patente, assicurazione e offerte | Escale",
        car_desc="Noleggiare un'auto {a}: patente internazionale, franchigia, carburante, aeroporto o centro città, e le offerte in diretta.",
        car_eyebrow="Noleggio auto", car_h1="Noleggia un'auto <span>{a}</span>",
        night_h="Arrivare di notte: le buone abitudini",
        night_dss="L'aeroporto Blaise Diagne è lontano dal centro di Dakar (circa un'ora di strada a seconda del traffico): dormire vicino all'aeroporto evita la strada in piena notte.",
        night_tips=["Prenota il transfer o il taxi <strong>prima</strong> di partire, o fatti aspettare da una persona di fiducia.",
                    "Evita i «taxi» che ti avvicinano nella hall: usa i taxi ufficiali o il transfer prenotato.",
                    "Tieni un po' di contanti locali e il telefono carico (un'eSIM aiuta a essere connessi all'arrivo).",
                    "Manda a un familiare l'indirizzo dell'hotel e l'orario di arrivo."],
        night_map="{n} (aeroporto)", night_hotels="Vedi gli hotel vicino all'aeroporto", night_taxi="Prenota un transfer",
        night_guide="Guida completa (in inglese): arrivare all'aeroporto di {n}", night_note="Link partner: Escale può ricevere una commissione, senza costi per te.",
        night_title="Hotel vicino all'aeroporto di {n}: arrivare di notte tranquilli | Escale",
        night_desc="Volo che arriva di notte {a}? Gli hotel vicino all'aeroporto, il transfer da prenotare e le buone abitudini per arrivare tranquilli.",
        night_eyebrow="Arrivo di notte", night_h1="Dormire vicino all'aeroporto <span>di {n}</span>",
        fam=dict(esim=dict(base="it/esim", ttl="eSIM per l'Africa: internet all'arrivo, paese per paese | Escale", h1="Un'eSIM <span>per l'Africa</span>",
                           lead="Internet appena atterri, senza cercare venditori in aeroporto: scegli il tuo paese.", desc="eSIM o SIM locale? I consigli per essere connessi all'arrivo in Costa d'Avorio, Senegal, Camerun, Marocco e altri 13 paesi."),
                 car=dict(base="it/noleggio-auto", ttl="Noleggio auto in Africa: Abidjan, Dakar, Casablanca, Marrakech… | Escale", h1="Noleggia un'auto <span>a casa</span>",
                          lead="Patente, assicurazione, carburante, aeroporto o centro: consigli e offerte, città per città.", desc="Noleggiare un'auto ad Abidjan, Dakar, Casablanca, Marrakech, Tunisi, Algeri, Douala, Accra o Lomé: patente, franchigia, carburante e offerte in diretta."),
                 night=dict(base="it/hotel-aeroporto", ttl="Arrivo di notte: hotel vicino agli aeroporti in Africa | Escale", h1="Arrivo di notte: <span>dormire vicino all'aeroporto</span>",
                            lead="Molti voli arrivano tardi. Gli hotel vicino all'aeroporto e le buone abitudini, aeroporto per aeroporto.", desc="Volo che arriva di notte ad Abidjan, Dakar, Lagos, Douala, Kinshasa? Gli hotel vicino all'aeroporto, il transfer da prenotare e le buone abitudini.")),
    ),
    "de": dict(
        esim_secs=[("eSIM oder lokale SIM-Karte?", [
            "<strong>Die eSIM</strong> kaufst du vor der Reise online und installierst sie in wenigen Minuten per QR-Code: Das Internet funktioniert direkt nach der Landung, ohne Verkäufer am Flughafen zu suchen. Deine gewohnte SIM behältst du für Anrufe und SMS.",
            "<strong>Die lokale SIM-Karte</strong> kaufst du vor Ort (Flughafen, Läden der Anbieter). Du bekommst eine lokale Nummer, praktisch für Anrufe vor Ort und Mobile Money. Zur Registrierung brauchst du meist deinen Pass.",
            "Viele Reisende kombinieren beides: die eSIM, um verbunden anzukommen, dann eine lokale SIM für einen längeren Aufenthalt."]),
            ("Bevor du eine eSIM kaufst", [
                "Prüfe, ob dein Handy eSIM unterstützt (Einstellungen → Mobilfunk → „eSIM hinzufügen“) und nicht an deinen Anbieter gebunden ist.",
                "Prüfe, ob das Land abgedeckt ist, und sieh dir Laufzeit und Datenvolumen des Tarifs {a} an.",
                "Installiere die eSIM vor der Abreise im WLAN und aktiviere sie erst bei der Ankunft.",
                "Schalte das Roaming deiner gewohnten SIM aus, um Kosten zu vermeiden."]),
            ("Gut zu wissen", [
                "WhatsApp, Anrufe und Nachrichten laufen übers Internet: Eine reine Daten-eSIM reicht oft, um mit der Familie in Kontakt zu bleiben.",
                "Außerhalb großer Städte kann der Empfang schwächer sein: Lade vor der Reise Offline-Karten herunter."])],
        esim_cta="eSIMs für {n} ansehen", esim_note="Partnerlink: Escale erhält eventuell eine Provision, ohne Mehrkosten für dich. Tarife und Preise bei Airalo prüfen.",
        esim_title="eSIM {n}: Internet direkt nach der Ankunft | Escale",
        esim_desc="Direkt nach der Landung {a} online sein: eSIM oder lokale SIM, kompatibles Handy, Einrichtung und Tipps.", esim_h1="Internet direkt nach der Ankunft {a}",
        car_secs=[("Vor der Buchung", [
            "<strong>Führerschein:</strong> Der internationale Führerschein wird oft verlangt, zusätzlich zum nationalen. Erkundige dich beim Vermieter und bei der Botschaft und nimm beide mit.",
            "<strong>Alter und Karte:</strong> Die meisten Vermieter verlangen ein Mindestalter und eine Kreditkarte auf den Namen des Fahrers für die Kaution.",
            "<strong>Versicherung und Selbstbeteiligung:</strong> Achte auf die Höhe der Selbstbeteiligung (was du bei einem Schaden zahlst) und was abgedeckt ist.",
            "<strong>Tank:</strong> Wähle „voll/voll“: Du gibst das Auto vollgetankt zurück, ohne versteckte Kosten."]),
            ("Vor Ort", [
                "Es herrscht Rechtsverkehr. Fotografiere das Auto (Karosserie, Reifen, Kilometerstand) bei Abholung und Rückgabe.",
                "Hab Mietvertrag, Führerschein und Pass dabei: Straßenkontrollen sind häufig.",
                "In der Stadt kann der Verkehr sehr dicht sein: Plane für den Weg zum Flughafen Puffer ein.",
                "Ein <strong>Auto mit Fahrer</strong> ist für eine erste Reise oft eine gute Alternative: Frag den Vermieter."]),
            ("Flughafen oder Stadtzentrum?", [
                "Die Abholung am Flughafen ist bei der Ankunft praktischer, aber manchmal etwas teurer als in der Stadt. Vergleiche beides in den Angeboten."])],
        car_cta="Mietwagen in {n} ansehen", car_note="Partnerlink: Escale erhält eventuell eine Provision, ohne Mehrkosten für dich. Bedingungen (Führerschein, Alter, Kaution) beim Vermieter prüfen.",
        car_title="Mietwagen in {n}: Führerschein, Versicherung, Angebote | Escale",
        car_desc="Ein Auto in {n} mieten: internationaler Führerschein, Selbstbeteiligung, Tank, Flughafen oder Stadtzentrum, und Live-Angebote.",
        car_eyebrow="Mietwagen", car_h1="Mietwagen <span>in {n}</span>",
        night_h="Nachts ankommen: die richtigen Gewohnheiten",
        night_dss="Der Flughafen Blaise Diagne liegt weit vom Zentrum Dakars (je nach Verkehr etwa eine Stunde Fahrt): Eine Nacht am Flughafen erspart dir die Fahrt mitten in der Nacht.",
        night_tips=["Buche deinen Transfer oder dein Taxi <strong>vor</strong> der Reise, oder lass dich von einer Vertrauensperson abholen.",
                    "Meide „Taxis“, die dich in der Ankunftshalle ansprechen: Nimm offizielle Taxis oder deinen gebuchten Transfer.",
                    "Hab etwas Bargeld in Landeswährung und ein geladenes Handy dabei (eine eSIM hilft, bei Ankunft online zu sein).",
                    "Schick einer Vertrauensperson die Adresse deines Hotels und deine Ankunftszeit."],
        night_map="{n} (Flughafen)", night_hotels="Hotels am Flughafen ansehen", night_taxi="Transfer buchen",
        night_guide="Ausführlicher Ratgeber (auf Englisch): Ankunft am Flughafen {n}", night_note="Partnerlinks: Escale erhält eventuell eine Provision, ohne Mehrkosten für dich.",
        night_title="Hotel am Flughafen {n}: entspannt nachts ankommen | Escale",
        night_desc="Dein Flug landet nachts in {n}? Hotels nahe dem Flughafen, der Transfer zum Buchen und die richtigen Gewohnheiten für eine entspannte Ankunft.",
        night_eyebrow="Ankunft in der Nacht", night_h1="Schlafen am <span>Flughafen {n}</span>",
        fam=dict(esim=dict(base="de/esim", ttl="eSIM für Afrika: Internet bei Ankunft, Land für Land | Escale", h1="Eine eSIM <span>für Afrika</span>",
                           lead="Internet direkt nach der Landung, ohne Verkäufer am Flughafen zu suchen: Wähle dein Land.", desc="eSIM oder lokale SIM? Tipps, um bei Ankunft in Nigeria, Ghana, Kenia, Elfenbeinküste, Senegal, Marokko und mehr online zu sein."),
                 car=dict(base="de/mietwagen", ttl="Mietwagen in Afrika: Abidjan, Dakar, Casablanca, Accra… | Escale", h1="Mietwagen <span>in der Heimat</span>",
                          lead="Führerschein, Versicherung, Tank, Flughafen oder Stadt: Tipps und Live-Angebote, Stadt für Stadt.", desc="Ein Auto in Accra, Lagos, Abidjan, Dakar, Casablanca, Marrakesch oder Tunis mieten: Führerschein, Selbstbeteiligung, Tank und Live-Angebote."),
                 night=dict(base="de/flughafenhotels", ttl="Nachts ankommen: Hotels an Afrikas Flughäfen | Escale", h1="Nachts ankommen: <span>am Flughafen schlafen</span>",
                            lead="Viele Flüge landen spät. Hotels nahe dem Flughafen und die richtigen Gewohnheiten, Flughafen für Flughafen.", desc="Du landest nachts in Lagos, Accra, Abidjan, Dakar, Douala? Hotels am Flughafen, der Transfer zum Buchen und die richtigen Gewohnheiten.")),
    ),
}
