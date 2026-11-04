"""Page « Fais venir un proche / Paye pour moi » : internationale (n'importe quel départ et arrivée), 6 langues.

Le proche choisit un vol réel et l'envoie sur WhatsApp à la personne qui paie ; celle-ci ouvre le lien, voit le même vol
et le prix actuel, puis réserve chez le partenaire (site/proche.js). Escale ne touche jamais à l'argent.
Check-list vérifiée en novembre 2026 (sources concordantes, liens officiels) : visa Schengen 90 € adulte / 45 € (6-12 ans)
depuis juin 2024, assurance Schengen d'au moins 30 000 €, France : attestation d'accueil (cerfa 10798, timbre fiscal 30 €),
Italie : dichiarazione di ospitalità, Belgique : engagement de prise en charge (annexe 3bis).
"""
import html
import json

import build_i18n as B

E = html.escape

FROMS = ["ABJ", "DSS", "DLA", "LOS", "CMN", "ALG", "FIH", "ACC", "MNL", "BOM", "MEX", "BOG", "GRU", "LIM", "IST", "CAI"]
TOS = ["PAR", "LON", "MIL", "ROM", "MAD", "BCN", "BRU", "FRA", "LIS", "NYC", "YMQ", "GVA"]
OFF = [("France-Visas", "https://france-visas.gouv.fr/"), ("Service-Public.fr : attestation d'accueil", "https://www.service-public.fr/particuliers/vosdroits/F2191"),
       ("Visti per l'Italia", "https://vistoperitalia.esteri.it/"), ("Office des étrangers (Belgique)", "https://dofi.ibz.be/"),
       ("Schengen (Commission européenne)", "https://home-affairs.ec.europa.eu/policies/schengen-borders-and-visa/visa-policy_en"),
       ("UK Standard Visitor visa (GOV.UK)", "https://www.gov.uk/standard-visitor"), ("U.S. Visitor Visa (travel.state.gov)", "https://travel.state.gov/content/travel/en/us-visas/tourism-visit/visitor.html"),
       ("Visit Canada (canada.ca)", "https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada.html")]


def chk(passport, visa, visa_a, invit, insur, cost, ticket):
    return [("🛂", *passport), ("📄", visa[0], visa[1].replace("{a}", f'<a id="pr-visa" href="VISA">{E(visa_a)}</a>')), ("🏠", *invit), ("🛡️", *insur), ("💶", *cost), ("🎫", *ticket)]


T = {
    "fr": dict(path="faire-venir-un-proche", visa="/visa/", title="Faire venir un proche : il choisit son billet, vous payez en 1 clic | Escale",
               desc="Un parent ou un ami vient vous voir, où que vous soyez ? Il choisit le vol le moins cher depuis chez lui et vous l'envoie sur WhatsApp : vous payez en un clic. Visa, invitation, assurance : la check-list.",
               h1="Fais venir <span>un proche</span>", lead="Ton proche choisit le vol le moins cher depuis chez lui, partout dans le monde, et te l'envoie sur WhatsApp. Tu ouvres le lien et tu paies en un clic.",
               how_h="Comment ça marche", how=["Ton proche (ou toi) choisit la ville de départ, la ville d'arrivée et le mois.", "Escale affiche les 3 vols aller-retour les moins chers, avec les vrais prix.",
                    "Il appuie sur « Envoyer pour paiement » : un message WhatsApp part avec le lien du vol.", "Tu ouvres le lien : même vol, mêmes dates, prix mis à jour. Tu réserves et tu paies chez le partenaire."],
               chk_h="Check-list pour faire venir un proche", chk=chk(
                   ("Le passeport", "Valable pendant tout le séjour, et souvent 3 à 6 mois de plus selon le pays : vérifiez avant de réserver."),
                   ("Le visa", "Il dépend du passeport et du pays d'arrivée. {a}, puis confirmez sur le site officiel du pays."), "Vérifiez avec l'outil visa d'Escale",
                   ("L'invitation", "Beaucoup de pays demandent une preuve d'hébergement ou une lettre d'invitation. Exemples : en France, attestation d'accueil en mairie (cerfa n°10798, timbre fiscal de 30 €) ; en Italie, « dichiarazione di ospitalità » ; en Belgique, engagement de prise en charge (annexe 3bis) à la commune."),
                   ("L'assurance", "Obligatoire pour le visa Schengen (au moins 30 000 € de frais médicaux et le rapatriement). Vivement conseillée partout ailleurs, surtout aux États-Unis et au Canada."),
                   ("Le prix du visa", "Espace Schengen : 90 € par adulte, 45 € de 6 à 12 ans, plus les frais du centre de visa. Ailleurs : voir le site officiel du pays."),
                   ("Le billet", "Au nom exact du passeport. Un aller-retour est souvent demandé pour le visa : gardez la confirmation pour le dossier.")),
               off_h="Sites officiels", checked="Informations vérifiées en novembre 2026 : les règles et les montants changent. Vérifiez toujours auprès du consulat et des autorités du pays d'arrivée.",
               t=dict(q_from="D'où part ton proche ?", q_to="Où arrive-t-il ?", q_month="Quel mois ?", ph="Autre ville ou aéroport…", loading="Recherche des vols les moins chers…",
                      none="Pas encore de prix trouvé pour ce trajet ce mois-ci. Essaie un autre mois ou un aéroport proche.", best_h="Les 3 vols les moins chers : {a} → {b}",
                      cheapest="Le moins cher", rt="aller-retour", direct="direct", stop1="1 escale", stops="{n} escales", send="Envoyer pour paiement", self="Réserver moi-même",
                      note="Prix aller-retour trouvés récemment, pour ces dates précises. Ils se confirment sur le site de réservation.",
                      wa="Bonjour ! J'ai choisi ce billet sur Escale : {a} → {b}, aller le {d}, retour le {r}, vu à {p}. Tu peux le réserver et le payer ici : {u}",
                      pay_eyebrow="Ton proche a choisi ce vol", seen="Prix vu par ton proche : {p}", checking="Vérification du prix actuel…", now="Prix actuel : {p}",
                      now_none="Prix actuel indisponible pour l'instant : il s'affichera sur le site de réservation.", book="Réserver et payer ce vol",
                      book_note="Tu réserves sur le site de la compagnie ou de l'agence, au nom du passager (exactement comme sur son passeport). Escale ne touche jamais à l'argent.", visa_link="Faut-il un visa ?")),
    "en": dict(path="en/bring-family", visa="/en/visa/", title="Bring a relative or friend: they pick the flight, you pay in 1 click | Escale",
               desc="A relative or friend is coming to visit, wherever you live? They pick the cheapest flight from home and send it to you on WhatsApp: you pay in one click. Visa, invitation, insurance: the checklist.",
               h1="Bring <span>a loved one</span>", lead="Your relative picks the cheapest flight from home, anywhere in the world, and sends it to you on WhatsApp. You open the link and pay in one click.",
               how_h="How it works", how=["Your relative (or you) picks the departure city, arrival city and month.", "Escale shows the 3 cheapest round trips, with real prices.",
                    "They tap 'Send for payment': a WhatsApp message goes out with the flight link.", "You open the link: same flight, same dates, updated price. You book and pay on the partner's site."],
               chk_h="Checklist to bring a loved one", chk=chk(
                   ("Passport", "Valid for the whole stay, and often 3 to 6 months longer depending on the country: check before booking."),
                   ("Visa", "It depends on the passport and the destination country. {a}, then confirm on the country's official website."), "Check with Escale's visa tool",
                   ("Invitation", "Many countries ask for proof of accommodation or an invitation letter. Examples: France, 'attestation d'accueil' from the town hall (cerfa 10798, €30 tax stamp); Italy, 'dichiarazione di ospitalità'; Belgium, sponsorship form (annex 3bis) at the commune."),
                   ("Insurance", "Required for a Schengen visa (at least €30,000 of medical costs and repatriation). Strongly advised everywhere else, especially in the USA and Canada."),
                   ("Visa fee", "Schengen area: €90 per adult, €45 for ages 6 to 12, plus visa centre fees. Elsewhere: see the country's official website."),
                   ("Ticket", "In the exact passport name. A round trip is often expected for the visa: keep the confirmation for the file.")),
               off_h="Official websites", checked="Information checked in November 2026: rules and fees change. Always check with the consulate and the destination country's authorities.",
               t=dict(q_from="Where is your loved one flying from?", q_to="Where are they flying to?", q_month="Which month?", ph="Other city or airport…", loading="Finding the cheapest flights…",
                      none="No price found yet for this route this month. Try another month or a nearby airport.", best_h="The 3 cheapest flights: {a} → {b}",
                      cheapest="Cheapest", rt="round trip", direct="direct", stop1="1 stop", stops="{n} stops", send="Send for payment", self="Book it myself",
                      note="Round-trip prices recently found, for these exact dates. They are confirmed on the booking site.",
                      wa="Hi! I picked this ticket on Escale: {a} → {b}, out on {d}, back on {r}, seen at {p}. You can book and pay for it here: {u}",
                      pay_eyebrow="Your loved one picked this flight", seen="Price they saw: {p}", checking="Checking the current price…", now="Current price: {p}",
                      now_none="Current price not available right now: it will show on the booking site.", book="Book and pay for this flight",
                      book_note="You book on the airline's or agency's site, in the passenger's name (exactly as on their passport). Escale never handles any money.", visa_link="Need a visa?")),
    "es": dict(path="es/traer-a-un-familiar", visa="/en/visa/", title="Traer a un familiar: elige su billete y tú pagas en 1 clic | Escale",
               desc="¿Un familiar o amigo viene a verte, vivas donde vivas? Elige el vuelo más barato desde su ciudad y te lo envía por WhatsApp: pagas en un clic. Visado, invitación, seguro: la lista.",
               h1="Trae a <span>un ser querido</span>", lead="Tu familiar elige el vuelo más barato desde su ciudad, en cualquier parte del mundo, y te lo envía por WhatsApp. Abres el enlace y pagas en un clic.",
               how_h="Cómo funciona", how=["Tu familiar (o tú) elige la ciudad de salida, la de llegada y el mes.", "Escale muestra los 3 vuelos de ida y vuelta más baratos, con precios reales.",
                    "Pulsa «Enviar para pagar»: sale un mensaje de WhatsApp con el enlace del vuelo.", "Abres el enlace: mismo vuelo, mismas fechas, precio actualizado. Reservas y pagas en la web del socio."],
               chk_h="Lista para traer a un ser querido", chk=chk(
                   ("El pasaporte", "Válido durante toda la estancia, y a menudo de 3 a 6 meses más según el país: compruébalo antes de reservar."),
                   ("El visado", "Depende del pasaporte y del país de llegada. {a} y confírmalo en la web oficial del país."), "Compruébalo con la herramienta de visados de Escale",
                   ("La invitación", "Muchos países piden una prueba de alojamiento o una carta de invitación. Ejemplos: Francia, «attestation d'accueil» en el ayuntamiento (cerfa 10798, timbre fiscal de 30 €); Italia, «dichiarazione di ospitalità»; Bélgica, compromiso de toma a cargo (anexo 3bis)."),
                   ("El seguro", "Obligatorio para el visado Schengen (al menos 30 000 € de gastos médicos y repatriación). Muy recomendable en todas partes, sobre todo en Estados Unidos y Canadá."),
                   ("Precio del visado", "Espacio Schengen: 90 € por adulto, 45 € de 6 a 12 años, más las tasas del centro de visados. En otros países: ver la web oficial."),
                   ("El billete", "Con el nombre exacto del pasaporte. Para el visado se suele pedir ida y vuelta: guarda la confirmación.")),
               off_h="Webs oficiales", checked="Información comprobada en noviembre de 2026: las normas y los importes cambian. Consulta siempre al consulado y a las autoridades del país de llegada.",
               t=dict(q_from="¿Desde dónde sale tu familiar?", q_to="¿Adónde llega?", q_month="¿Qué mes?", ph="Otra ciudad o aeropuerto…", loading="Buscando los vuelos más baratos…",
                      none="Aún no hay precios para esta ruta este mes. Prueba otro mes o un aeropuerto cercano.", best_h="Los 3 vuelos más baratos: {a} → {b}",
                      cheapest="El más barato", rt="ida y vuelta", direct="directo", stop1="1 escala", stops="{n} escalas", send="Enviar para pagar", self="Reservar yo mismo",
                      note="Precios de ida y vuelta encontrados recientemente, para estas fechas. Se confirman en la web de reserva.",
                      wa="¡Hola! He elegido este billete en Escale: {a} → {b}, ida el {d}, vuelta el {r}, visto a {p}. Puedes reservarlo y pagarlo aquí: {u}",
                      pay_eyebrow="Tu familiar eligió este vuelo", seen="Precio que vio: {p}", checking="Comprobando el precio actual…", now="Precio actual: {p}",
                      now_none="Precio actual no disponible por ahora: se mostrará en la web de reserva.", book="Reservar y pagar este vuelo",
                      book_note="Reservas en la web de la aerolínea o agencia, a nombre del pasajero (igual que en su pasaporte). Escale nunca toca el dinero.", visa_link="¿Hace falta visado?")),
    "pt": dict(path="pt/trazer-um-familiar", visa="/en/visa/", title="Trazer um familiar: ele escolhe o bilhete e você paga em 1 clique | Escale",
               desc="Um familiar ou amigo vem visitá-lo, onde quer que viva? Escolhe o voo mais barato a partir da sua cidade e envia-o por WhatsApp: paga num clique. Visto, convite, seguro: a lista.",
               h1="Traga <span>quem você ama</span>", lead="O seu familiar escolhe o voo mais barato a partir da sua cidade, em qualquer parte do mundo, e envia-o por WhatsApp. Abre a ligação e paga num clique.",
               how_h="Como funciona", how=["O seu familiar (ou você) escolhe a cidade de partida, a de chegada e o mês.", "A Escale mostra os 3 voos de ida e volta mais baratos, com preços reais.",
                    "Toca em «Enviar para pagamento»: sai uma mensagem de WhatsApp com a ligação do voo.", "Abre a ligação: mesmo voo, mesmas datas, preço atualizado. Reserva e paga no site do parceiro."],
               chk_h="Lista para trazer quem você ama", chk=chk(
                   ("O passaporte", "Válido durante toda a estadia, e muitas vezes 3 a 6 meses mais, conforme o país: verifique antes de reservar."),
                   ("O visto", "Depende do passaporte e do país de chegada. {a} e confirme no site oficial do país."), "Verifique com a ferramenta de vistos da Escale",
                   ("O convite", "Muitos países pedem prova de alojamento ou carta-convite. Exemplos: França, «attestation d'accueil» na câmara municipal (cerfa 10798, selo fiscal de 30 €); Itália, «dichiarazione di ospitalità»; Bélgica, termo de responsabilidade (anexo 3bis)."),
                   ("O seguro", "Obrigatório para o visto Schengen (pelo menos 30 000 € de despesas médicas e repatriamento). Muito recomendado em todo o lado, sobretudo nos EUA e no Canadá."),
                   ("Preço do visto", "Espaço Schengen: 90 € por adulto, 45 € dos 6 aos 12 anos, mais as taxas do centro de vistos. Noutros países: ver o site oficial."),
                   ("O bilhete", "Com o nome exato do passaporte. Para o visto pede-se muitas vezes ida e volta: guarde a confirmação.")),
               off_h="Sites oficiais", checked="Informação verificada em novembro de 2026: as regras e os valores mudam. Confirme sempre junto do consulado e das autoridades do país de chegada.",
               t=dict(q_from="De onde parte o seu familiar?", q_to="Para onde vai?", q_month="Que mês?", ph="Outra cidade ou aeroporto…", loading="A procurar os voos mais baratos…",
                      none="Ainda não há preços para este percurso este mês. Experimente outro mês ou um aeroporto próximo.", best_h="Os 3 voos mais baratos: {a} → {b}",
                      cheapest="O mais barato", rt="ida e volta", direct="direto", stop1="1 escala", stops="{n} escalas", send="Enviar para pagamento", self="Reservar eu mesmo",
                      note="Preços de ida e volta encontrados recentemente, para estas datas. Confirmam-se no site de reserva.",
                      wa="Olá! Escolhi este bilhete na Escale: {a} → {b}, ida a {d}, volta a {r}, visto a {p}. Podes reservá-lo e pagá-lo aqui: {u}",
                      pay_eyebrow="O seu familiar escolheu este voo", seen="Preço que viu: {p}", checking="A verificar o preço atual…", now="Preço atual: {p}",
                      now_none="Preço atual indisponível de momento: aparecerá no site de reserva.", book="Reservar e pagar este voo",
                      book_note="Reserva no site da companhia ou da agência, em nome do passageiro (exatamente como no passaporte). A Escale nunca toca no dinheiro.", visa_link="Precisa de visto?")),
    "it": dict(path="it/far-venire-un-familiare", visa="/en/visa/", title="Far venire un familiare: sceglie il volo, tu paghi in 1 clic | Escale",
               desc="Un familiare o un amico viene a trovarti, ovunque tu viva? Sceglie il volo più economico dalla sua città e te lo manda su WhatsApp: paghi in un clic. Visto, invito, assicurazione: la checklist.",
               h1="Fai venire <span>una persona cara</span>", lead="Il tuo familiare sceglie il volo più economico dalla sua città, ovunque nel mondo, e te lo manda su WhatsApp. Apri il link e paghi in un clic.",
               how_h="Come funziona", how=["Il tuo familiare (o tu) sceglie la città di partenza, quella di arrivo e il mese.", "Escale mostra i 3 voli andata e ritorno più economici, con prezzi reali.",
                    "Tocca «Invia per il pagamento»: parte un messaggio WhatsApp con il link del volo.", "Apri il link: stesso volo, stesse date, prezzo aggiornato. Prenoti e paghi sul sito del partner."],
               chk_h="Checklist per far venire una persona cara", chk=chk(
                   ("Il passaporto", "Valido per tutto il soggiorno, e spesso 3-6 mesi in più a seconda del paese: verificalo prima di prenotare."),
                   ("Il visto", "Dipende dal passaporto e dal paese di arrivo. {a}, poi conferma sul sito ufficiale del paese."), "Verifica con lo strumento visti di Escale",
                   ("L'invito", "Molti paesi chiedono una prova di alloggio o una lettera d'invito. Esempi: Italia, «dichiarazione di ospitalità» o invito secondo il modello del consolato; Francia, «attestation d'accueil» in comune (cerfa 10798, marca da 30 €); Belgio, impegno di presa in carico (allegato 3bis)."),
                   ("L'assicurazione", "Obbligatoria per il visto Schengen (almeno 30.000 € di spese mediche e rimpatrio). Fortemente consigliata ovunque, soprattutto negli Stati Uniti e in Canada."),
                   ("Costo del visto", "Area Schengen: 90 € per adulto, 45 € dai 6 ai 12 anni, più le spese del centro visti. Altrove: vedi il sito ufficiale del paese."),
                   ("Il biglietto", "Al nome esatto del passaporto. Per il visto spesso serve andata e ritorno: conserva la conferma.")),
               off_h="Siti ufficiali", checked="Informazioni verificate a novembre 2026: regole e importi cambiano. Verifica sempre con il consolato e le autorità del paese di arrivo.",
               t=dict(q_from="Da dove parte il tuo familiare?", q_to="Dove arriva?", q_month="Quale mese?", ph="Altra città o aeroporto…", loading="Ricerca dei voli più economici…",
                      none="Nessun prezzo ancora per questa tratta questo mese. Prova un altro mese o un aeroporto vicino.", best_h="I 3 voli più economici: {a} → {b}",
                      cheapest="Il più economico", rt="andata e ritorno", direct="diretto", stop1="1 scalo", stops="{n} scali", send="Invia per il pagamento", self="Prenoto io",
                      note="Prezzi andata e ritorno trovati di recente, per queste date. Si confermano sul sito di prenotazione.",
                      wa="Ciao! Ho scelto questo biglietto su Escale: {a} → {b}, andata il {d}, ritorno il {r}, visto a {p}. Puoi prenotarlo e pagarlo qui: {u}",
                      pay_eyebrow="Il tuo familiare ha scelto questo volo", seen="Prezzo che ha visto: {p}", checking="Verifica del prezzo attuale…", now="Prezzo attuale: {p}",
                      now_none="Prezzo attuale non disponibile per ora: comparirà sul sito di prenotazione.", book="Prenota e paga questo volo",
                      book_note="Prenoti sul sito della compagnia o dell'agenzia, a nome del passeggero (esattamente come sul passaporto). Escale non tocca mai il denaro.", visa_link="Serve il visto?")),
    "de": dict(path="de/familie-einladen", visa="/en/visa/", title="Familie einladen: Sie wählt den Flug, du zahlst mit 1 Klick | Escale",
               desc="Ein Verwandter oder Freund kommt zu Besuch, wo auch immer du lebst? Er wählt den günstigsten Flug ab seiner Stadt und schickt ihn dir per WhatsApp: du zahlst mit einem Klick. Visum, Einladung, Versicherung: die Checkliste.",
               h1="Lade <span>deine Liebsten</span> ein", lead="Dein Verwandter wählt den günstigsten Flug ab seiner Stadt, überall auf der Welt, und schickt ihn dir per WhatsApp. Du öffnest den Link und zahlst mit einem Klick.",
               how_h="So funktioniert es", how=["Dein Verwandter (oder du) wählt Abflugstadt, Zielstadt und Monat.", "Escale zeigt die 3 günstigsten Hin- und Rückflüge mit echten Preisen.",
                    "Er tippt auf „Zum Bezahlen senden“: Eine WhatsApp-Nachricht mit dem Flug-Link wird verschickt.", "Du öffnest den Link: gleicher Flug, gleiche Daten, aktueller Preis. Du buchst und zahlst beim Partner."],
               chk_h="Checkliste für den Besuch", chk=chk(
                   ("Reisepass", "Für den ganzen Aufenthalt gültig, je nach Land oft 3 bis 6 Monate länger: vor der Buchung prüfen."),
                   ("Visum", "Hängt vom Pass und vom Zielland ab. {a} und auf der offiziellen Seite des Landes bestätigen."), "Mit dem Visum-Tool von Escale prüfen",
                   ("Einladung", "Viele Länder verlangen einen Unterkunftsnachweis oder ein Einladungsschreiben. Beispiele: Deutschland, Verpflichtungserklärung bei der Ausländerbehörde; Frankreich, „attestation d'accueil“ im Rathaus (cerfa 10798, 30 € Steuermarke); Italien, „dichiarazione di ospitalità“."),
                   ("Versicherung", "Pflicht für ein Schengen-Visum (mindestens 30.000 € für Arztkosten und Rücktransport). Überall sonst dringend empfohlen, besonders in den USA und Kanada."),
                   ("Visumgebühr", "Schengen-Raum: 90 € pro Erwachsenem, 45 € von 6 bis 12 Jahren, plus Gebühren des Visazentrums. Anderswo: siehe offizielle Seite des Landes."),
                   ("Ticket", "Auf den genauen Namen im Pass. Für das Visum wird oft ein Hin- und Rückflug verlangt: Bestätigung aufbewahren.")),
               off_h="Offizielle Seiten", checked="Informationen geprüft im November 2026: Regeln und Gebühren ändern sich. Immer beim Konsulat und den Behörden des Ziellandes nachfragen.",
               t=dict(q_from="Von wo fliegt dein Besuch ab?", q_to="Wohin fliegt er?", q_month="Welcher Monat?", ph="Andere Stadt oder anderer Flughafen…", loading="Suche nach den günstigsten Flügen…",
                      none="Noch kein Preis für diese Strecke in diesem Monat. Versuche einen anderen Monat oder einen nahen Flughafen.", best_h="Die 3 günstigsten Flüge: {a} → {b}",
                      cheapest="Am günstigsten", rt="hin und zurück", direct="direkt", stop1="1 Stopp", stops="{n} Stopps", send="Zum Bezahlen senden", self="Selbst buchen",
                      note="Kürzlich gefundene Preise für Hin- und Rückflug zu diesen Daten. Sie werden auf der Buchungsseite bestätigt.",
                      wa="Hallo! Ich habe dieses Ticket auf Escale gewählt: {a} → {b}, Hinflug am {d}, Rückflug am {r}, gesehen für {p}. Du kannst es hier buchen und bezahlen: {u}",
                      pay_eyebrow="Dein Besuch hat diesen Flug gewählt", seen="Gesehener Preis: {p}", checking="Aktueller Preis wird geprüft…", now="Aktueller Preis: {p}",
                      now_none="Aktueller Preis gerade nicht verfügbar: Er erscheint auf der Buchungsseite.", book="Diesen Flug buchen und bezahlen",
                      book_note="Du buchst auf der Seite der Airline oder Agentur, auf den Namen des Passagiers (genau wie im Pass). Escale berührt nie Geld.", visa_link="Brauche ich ein Visum?")),
}


def build(site, ctx):
    paths = {l: T[l]["path"] for l in T}
    urls = []
    for lang, t in T.items():
        q = "" if lang == "fr" else f"?lang={lang}"
        how = "".join(f"<li>{E(x)}</li>" for x in t["how"])
        chkh = "".join(f'<li class="pv-item"><span class="pv-ic" aria-hidden="true">{ic}</span><div><h3>{E(h)}</h3><p>{d.replace("VISA", t["visa"])}</p></div></li>'
                       for ic, h, d in t["chk"])
        body = (f'<section class="pr-choose-only"><h2>{E(t["how_h"])}</h2><ol class="pr-how">{how}</ol></section>'
                f'<div id="pr-app" class="pr-app" data-t="{E(json.dumps(t["t"], ensure_ascii=False))}" data-from="{E(json.dumps(FROMS))}" data-to="{E(json.dumps(TOS))}">'
                f'<noscript><p><a class="btn" href="/{q}">Escale</a></p></noscript></div>'
                f'<section id="price-alert" class="price-alert" data-from="ABJ" data-to="PAR" hidden></section>'
                f'<section><h2>{E(t["chk_h"])}</h2><ol class="pv-list pr-chk">{chkh}</ol></section>'
                f'<section><h2>{E(t["off_h"])}</h2><ul>' + "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{E(n)}</a></li>' for n, u in OFF) +
                f'</ul><p class="small">{E(t["checked"])}</p></section>'
                '<script src="/fetes.js" defer></script><script src="/proche.js" defer></script><script src="/alerts.js" defer></script>')
        hero = f'<p class="eyebrow">💝 Escale</p><h1>{t["h1"]}</h1><p class="hero-lead">{E(t["lead"])}</p>'
        ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "WebApplication", "name": t["title"].split(" | ")[0],
                                                                   "description": t["desc"], "inLanguage": lang, "applicationCategory": "TravelApplication", "operatingSystem": "Web",
                                                                   "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}}, ensure_ascii=False) + "</script>"
        urls.append(B.write(site, t["path"], lang, t["title"], t["desc"], hero, body, ld, paths, ctx))
    return urls
