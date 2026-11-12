"""Versions anglaise et italienne des pages de scripts/diaspora_plus.py (argent, colis, vol à plusieurs étapes, aéroports de départ).
Mêmes règles : aucun prix, aucune durée précise, aucun horaire ; liens officiels ; pas de lien d'affiliation sur argent et colis.
Traduit le 12 novembre 2026."""
import html

import build_i18n as B
import diaspora_plus as D

E = html.escape
EXT, ul, faq_html = D.EXT, D.ul, D.faq_html
CHECKED = {"en": "November 2026", "it": "novembre 2026"}

# Pages liées qui existent dans chaque langue (sinon la version anglaise)
LK = {
    "en": dict(home="/en/", bag="/en/baggage-allowance-africa-airlines/", bagguide="/en/guides/baggage/", visa="/en/visa/", check="/en/pre-flight-check/", momo="/en/pay-flight-mobile-money/",
               money="/en/guides/money-abroad/", guides="/en/guides/", arr="/en/arriving-at-{}-airport/"),
    "it": dict(home="/it/", bag="/en/baggage-allowance-africa-airlines/", bagguide="/en/guides/baggage/", visa="/en/visa/", check="/it/controllo-prima-del-volo/", momo="/en/pay-flight-mobile-money/",
               money="/en/guides/money-abroad/", guides="/en/guides/", arr="/en/arriving-at-{}-airport/"),
}
P = D.PATHS


def plus(l):
    t = {"en": ("Read next", "Sending money home: how to compare", "Sending a parcel or extra bags home", "Multi-city flights", "Getting to your departure airport", "Baggage: each airline's allowance", "All guides"),
         "it": ("Per approfondire", "Inviare soldi a casa: come confrontare", "Spedire un pacco o valigie in più", "Voli multi-tratta", "Raggiungere l'aeroporto di partenza", "Bagagli: la franchigia di ogni compagnia (in inglese)", "Tutte le guide (in inglese)")}[l]
    k = LK[l]
    return (f'<section><h2>{t[0]}</h2><ul><li><a href="/{P["argent"][l]}/">{t[1]}</a></li><li><a href="/{P["colis"][l]}/">{t[2]}</a></li>'
            f'<li><a href="/{P["etapes"][l]}/">{t[3]}</a></li><li><a href="/{P["hub"][l]}/">{t[4]}</a></li>'
            f'<li><a href="{k["bag"]}">{t[5]}</a></li><li><a href="{k["guides"]}">{t[6]}</a></li></ul></section>')


FAQ_H = {"en": "Frequently asked questions", "it": "Domande frequenti"}

# ---------------------------------------------------------------- argent
ARGENT = {
    "en": dict(
        title="Sending money home: how to compare services | Escale",
        desc="Wise, Remitly, WorldRemit, Sendwave, Taptap Send, Western Union: how to compare the amount actually received, the free public comparison sites and the exchange-rate traps.",
        eyebrow="Guide · checked in ", h1='Sending money <span>back home</span>',
        lead="Wise, Remitly, WorldRemit, Sendwave, Taptap Send, Western Union, MoneyGram… Rates change every day. Here is how to compare in two minutes and stop losing money in the exchange rate.",
        brief_h="In short", brief=[
            "Do not compare the advertised fees: compare <strong>the amount the person receives</strong> for the same amount sent.",
            "The cost is often hidden in the <strong>exchange rate</strong>, even when the service says “zero fees”.",
            "The way the money is received changes the price: <strong>mobile money</strong>, bank account or cash pick-up.",
            "Use a <strong>free public comparison site</strong> before every large transfer."],
        steps_h="The method in 4 steps", steps=[
            "Decide how much to send and how the person wants to receive it (mobile money, account, cash).",
            "Open two or three services and enter exactly the same amount and the same country.",
            "For each one, note the <strong>amount received in the local currency</strong> and the delivery time shown.",
            "Pick the one that delivers the most within a delay that suits you. Compare again next time: the ranking changes."],
        cmp_h="Public comparison sites", cmp_p="These sites compare transfer services without selling anything:", cmp=[
            EXT("https://remittanceprices.worldbank.org/", "Remittance Prices Worldwide") + ": the World Bank database, country by country.",
            EXT("https://www.envoidargent.fr/", "envoidargent.fr") + ": comparison site backed by the French development agency, for transfers from France (in French).",
            EXT("https://www.mandasoldiacasa.it/", "mandasoldiacasa.it") + ": Italian comparison site for transfers from Italy."],
        svc_h="The best-known services", svc_p="Links to the official sites, in no particular order: Escale earns no commission on these services.", svc=[
            EXT("https://wise.com/", "Wise") + ": transfer to a bank account, and mobile money in some countries.",
            EXT("https://www.remitly.com/", "Remitly") + ": bank account, mobile money or cash pick-up depending on the country.",
            EXT("https://www.worldremit.com/", "WorldRemit") + ": mobile money, bank account, cash, airtime top-up.",
            EXT("https://www.sendwave.com/", "Sendwave") + ": mobile app, mostly to mobile money.",
            EXT("https://www.taptapsend.com/", "Taptap Send") + ": mobile app, mostly to mobile money.",
            EXT("https://www.westernunion.com/", "Western Union") + " and " + EXT("https://www.moneygram.com/", "MoneyGram") + ": agent networks for cash pick-up, plus online transfers."],
        svc_note="Not every service covers every country or every mobile money operator: check on their site before opening an account.",
        traps_h="Traps to avoid", traps=[
            "Sending several small amounts: fixed fees can add up. Check whether a single transfer costs less.",
            "Paying by credit card: some services or banks add fees. A bank transfer or debit card often costs less.",
            "Getting one digit wrong in the recipient's number: a transfer to the wrong number is very hard to recover. Read it twice.",
            "Forgetting the limits: each service caps amounts and may ask for ID or proof of funds."],
        ticket_h="What about the plane ticket?",
        ticket='A relative back home can sometimes pay for the ticket directly: see <a href="{momo}">paying for a flight with Orange Money, Wave or MTN MoMo</a>. For money during the trip: <a href="{money}">money abroad</a>.',
        small="Escale does not sell money transfers and shows no rates here, because they change every day. The official sites are the reference.",
        faq=[
            ("Which service is cheapest for sending money to Africa?", "There is no fixed answer: it depends on the country, the amount, how the money is received and the day. The right habit is to compare, for the same amount sent, what the person will actually receive. The public comparison sites listed on this page do that calculation for free."),
            ("Why look at the exchange rate and not only the fees?", "Because part of the cost is often hidden in the exchange rate. A service can advertise “zero fees” and apply a worse rate. Only the amount received, in the local currency, lets you compare."),
            ("Mobile money, bank account or cash pick-up?", "Mobile money (Orange Money, Wave, MTN MoMo…) is handy when the recipient has no bank account and lives far from an agent. A bank transfer suits large amounts. Cash pick-up is still useful in an emergency, but needs ID and a trip to the agent."),
            ("How do I avoid scams?", "Only send money to people you know. Be wary of invented emergencies, promised winnings and requests to keep the transfer secret. Always go through the service's official site or app, never through a link received by message.")]),
    "it": dict(
        title="Inviare soldi a casa: come confrontare i servizi | Escale",
        desc="Wise, Remitly, WorldRemit, Sendwave, Taptap Send, Western Union: come confrontare la somma davvero ricevuta, i comparatori pubblici gratuiti e le trappole del tasso di cambio.",
        eyebrow="Guida · verificata a ", h1='Inviare soldi <span>a casa</span>',
        lead="Wise, Remitly, WorldRemit, Sendwave, Taptap Send, Western Union, MoneyGram… Le tariffe cambiano ogni giorno. Ecco come confrontare in due minuti e non perdere soldi nel tasso di cambio.",
        brief_h="In breve", brief=[
            "Non confrontare le commissioni dichiarate: confronta <strong>la somma che la persona riceve</strong> a parità di importo inviato.",
            "Il costo si nasconde spesso nel <strong>tasso di cambio</strong>, anche quando il servizio dice «zero commissioni».",
            "Il modo di ricezione cambia il prezzo: <strong>mobile money</strong>, conto bancario o ritiro in contanti.",
            "Usa un <strong>comparatore pubblico e gratuito</strong> prima di ogni invio importante."],
        steps_h="Il metodo in 4 passi", steps=[
            "Decidi quanto inviare e come la persona vuole ricevere i soldi (mobile money, conto, contanti).",
            "Apri due o tre servizi e inserisci esattamente lo stesso importo e lo stesso paese.",
            "Per ciascuno annota la <strong>somma ricevuta nella valuta del paese</strong> e i tempi indicati.",
            "Scegli quello che fa arrivare di più in un tempo che ti va bene. Rifai il confronto la volta dopo: la classifica cambia."],
        cmp_h="I comparatori pubblici", cmp_p="Questi siti confrontano i servizi di trasferimento senza vendere nulla:", cmp=[
            EXT("https://www.mandasoldiacasa.it/", "mandasoldiacasa.it") + ": il comparatore italiano per gli invii di denaro dall'Italia.",
            EXT("https://remittanceprices.worldbank.org/", "Remittance Prices Worldwide") + ": la banca dati della Banca Mondiale, paese per paese (in inglese).",
            EXT("https://www.envoidargent.fr/", "envoidargent.fr") + ": comparatore sostenuto dall'agenzia francese per lo sviluppo, per gli invii dalla Francia (in francese)."],
        svc_h="I servizi più conosciuti", svc_p="Link ai siti ufficiali, senza classifica: Escale non riceve alcuna commissione da questi servizi.", svc=[
            EXT("https://wise.com/", "Wise") + ": bonifico su conto bancario, e mobile money in alcuni paesi.",
            EXT("https://www.remitly.com/", "Remitly") + ": conto bancario, mobile money o ritiro in contanti a seconda del paese.",
            EXT("https://www.worldremit.com/", "WorldRemit") + ": mobile money, conto bancario, contanti, ricarica telefonica.",
            EXT("https://www.sendwave.com/", "Sendwave") + ": app per telefono, soprattutto verso il mobile money.",
            EXT("https://www.taptapsend.com/", "Taptap Send") + ": app per telefono, soprattutto verso il mobile money.",
            EXT("https://www.westernunion.com/", "Western Union") + " e " + EXT("https://www.moneygram.com/", "MoneyGram") + ": reti di agenzie per il ritiro in contanti, e invio online."],
        svc_note="Non tutti i servizi coprono tutti i paesi né tutti gli operatori di mobile money: verifica sul loro sito prima di aprire un conto.",
        traps_h="Le trappole da evitare", traps=[
            "Inviare in tante piccole volte: le commissioni fisse possono sommarsi. Guarda se un solo invio costa meno.",
            "Pagare con carta di credito: alcuni servizi o banche aggiungono costi. Il bonifico o la carta di debito costano spesso meno.",
            "Sbagliare una cifra nel numero del destinatario: un invio al numero sbagliato è molto difficile da recuperare. Rileggi due volte.",
            "Dimenticare i limiti: ogni servizio ha un tetto agli importi e può chiedere un documento o un giustificativo."],
        ticket_h="E per il biglietto aereo?",
        ticket='A volte un familiare al paese può pagare lui il biglietto: vedi <a href="{momo}">pagare il volo con Orange Money, Wave o MTN MoMo</a> (in inglese). Per i soldi durante il viaggio: <a href="{money}">soldi in viaggio</a> (in inglese).',
        small="Escale non vende trasferimenti di denaro e qui non mostra tariffe, perché cambiano ogni giorno. Fanno fede i siti ufficiali.",
        faq=[
            ("Qual è il servizio più economico per inviare soldi in Africa?", "Non c'è una risposta fissa: dipende dal paese, dall'importo, dal modo di ricezione e dal giorno. La buona abitudine è confrontare, a parità di importo inviato, quanto riceverà davvero la persona. I comparatori pubblici citati in questa pagina fanno questo calcolo gratis."),
            ("Perché guardare il tasso di cambio e non solo le commissioni?", "Perché una parte del costo è spesso nascosta nel tasso di cambio. Un servizio può dichiarare «zero commissioni» e applicare un tasso peggiore. Solo la somma ricevuta, nella valuta del paese, permette di confrontare."),
            ("Mobile money, conto bancario o ritiro in contanti?", "Il mobile money (Orange Money, Wave, MTN MoMo…) è comodo quando il destinatario non ha un conto e vive lontano da un'agenzia. Il bonifico su conto va bene per importi grandi. Il ritiro in contanti resta utile in emergenza, ma richiede un documento e uno spostamento."),
            ("Come evitare le truffe?", "Invia soldi solo a persone che conosci. Diffida delle emergenze inventate, delle vincite promesse e di chi chiede di tenere segreto l'invio. Passa sempre dal sito o dall'app ufficiale del servizio, mai da un link ricevuto per messaggio.")]),
}


def argent(site, ctx, l):
    t, k = ARGENT[l], LK[l]
    hero = f'<p class="eyebrow">{t["eyebrow"]}{CHECKED[l]}</p><h1>{t["h1"]}</h1><p class="hero-lead">{E(t["lead"])}</p>'
    body = (f'<section><h2>{t["brief_h"]}</h2>{ul(t["brief"])}</section>'
            f'<section><h2>{t["steps_h"]}</h2><ol>' + "".join(f"<li>{x}</li>" for x in t["steps"]) + '</ol></section>'
            f'<section><h2>{t["cmp_h"]}</h2><p>{t["cmp_p"]}</p>{ul(t["cmp"])}</section>'
            f'<section><h2>{t["svc_h"]}</h2><p>{t["svc_p"]}</p>{ul(t["svc"])}<p class="small">{t["svc_note"]}</p></section>'
            f'<section><h2>{t["traps_h"]}</h2>{ul(t["traps"])}</section>'
            f'<section><h2>{t["ticket_h"]}</h2><p>{t["ticket"].format(**k)}</p></section>'
            f'<section class="faq"><h2>{FAQ_H[l]}</h2>{faq_html(t["faq"])}</section>' + plus(l) + f'<p class="small">{t["small"]}</p>' + B.faq_ld(t["faq"]))
    return B.write(site, P["argent"][l], l, t["title"], t["desc"], hero, body, "", P["argent"], ctx)


# ---------------------------------------------------------------- colis
COLIS = {
    "en": dict(
        title="Sending a parcel or extra bags home: what to choose | Escale",
        desc="Extra baggage, postal parcel, air freight or shared sea container to Africa: which option for which weight and urgency, customs, what not to send and what to ask the freight agent.",
        eyebrow="Guide · checked in ", h1='Sending a parcel <span>or extra bags home</span>',
        lead="Extra checked bag, postal parcel, air freight, shared sea container: which option to choose depending on weight, urgency and budget, and the rules to know before you send.",
        brief_h="In short", brief=[
            "<strong>You are travelling</strong> and it is one or two suitcases: extra baggage, bought online before departure.",
            "<strong>Small urgent parcel</strong> (documents, permitted medicines, a phone): the post office or an express courier.",
            "<strong>A few boxes</strong>: air freight, priced per kilo, in a few days.",
            "<strong>Large, non-urgent volume</strong> (furniture, appliances, barrels): a shared sea container, in several weeks."],
        sec=[
            ("1. The extra bag on the plane", [
                "Buy the extra bag <strong>online before departure</strong>: it is usually cheaper than at the airport desk.",
                "Compare the fare <strong>with bags included</strong> rather than the bare fare: a dearer airline can end up cheaper once the suitcases are counted.",
                "Weigh everything at home: an extra kilo is expensive at check-in.",
                'Each airline\'s allowance and rules: <a href="{bag}">baggage by airline</a> and the guide <a href="{bagguide}">how not to pay more</a>.']),
            ("2. Postal or express parcel", [
                "For a small parcel, your country's postal service (" + EXT("https://www.royalmail.com/", "Royal Mail") + " in the UK, " + EXT("https://www.laposte.fr/", "La Poste") + " in France, " + EXT("https://www.poste.it/", "Poste Italiane") + " in Italy, " + EXT("https://www.bpost.be/", "bpost") + " in Belgium) or an express courier.",
                "Get the quote online with the real weight and dimensions: the price also depends on volume.",
                "Fill in the <strong>customs declaration</strong> carefully (contents, value) and keep the tracking number.",
                "Ask whether delivery is to the door or to the post office: in many cities the recipient has to collect the parcel."]),
            ("3. Air freight", [
                "Freight agents specialised by country collect boxes in Europe and hand them over on arrival, often at their own office.",
                "The price is calculated <strong>per kilo or by volume</strong>: always ask for a written quote, with what is included (packing, customs, delivery).",
                "Check that the agent has an address, a company number and a receipt listing the contents."]),
            ("4. Shared sea container", [
                "For barrels, many boxes, furniture and appliances: you pay for a share of a container.",
                "Allow <strong>several weeks</strong>, plus customs clearance on arrival.",
                "Make a <strong>detailed, photographed inventory</strong>: it is used by customs and in case of loss or damage."]),
            ("What you should not send", [
                "Loose lithium batteries, aerosols, flammable products and perfume in quantity are restricted or banned on aircraft.",
                "Cash, valuable jewellery and original identity documents do not travel in an ordinary parcel.",
                "Medicines, food, plants and animal products have rules specific to each country.",
                "On arrival, it is the destination country's customs that decides: check its rules or ask the freight agent before sending."])],
        small="Escale does not ship parcels and shows no rates here: always ask for a written quote. Customs rules change: the official sites are the reference.",
        faq=[
            ("Extra suitcase or parcel: which is cheaper?", "For one or two suitcases, extra baggage bought online before departure is often the simplest, since you travel with it. Beyond that, or if you are not travelling, ask for a freight quote: the price is per kilo or by volume and depends on the country."),
            ("How long does sea freight take?", "Several weeks, plus customs clearance on arrival. Sea freight suits bulky, non-urgent belongings. Ask the agent for a door-to-door time, not just the crossing time."),
            ("Will there be customs duties on arrival?", "Often yes: each country has its own rules for new goods, electronics, vehicles or commercial quantities. Ask the destination country's customs or the freight agent before sending, so you do not discover the charges at collection."),
            ("Can I give a parcel to a traveller?", "It is common practice, but risky for both sides: the traveller is responsible for everything they carry before customs and the airline. Only hand over or accept open parcels whose contents are known and allowed.")]),
    "it": dict(
        title="Spedire un pacco o valigie in più a casa: cosa scegliere | Escale",
        desc="Bagaglio extra, pacco postale, spedizione aerea o container condiviso verso l'Africa: quale soluzione secondo peso e urgenza, la dogana, cosa non spedire e cosa chiedere allo spedizioniere.",
        eyebrow="Guida · verificata a ", h1='Spedire un pacco <span>o valigie in più a casa</span>',
        lead="Bagaglio extra, pacco postale, spedizione aerea, container condiviso via mare: quale soluzione scegliere secondo il peso, l'urgenza e il budget, e le regole da conoscere prima di spedire.",
        brief_h="In breve", brief=[
            "<strong>Viaggi tu</strong> e si tratta di una o due valigie: il bagaglio extra, comprato online prima della partenza.",
            "<strong>Piccolo pacco urgente</strong> (documenti, medicinali consentiti, un telefono): le poste o un corriere espresso.",
            "<strong>Qualche scatolone</strong>: la spedizione aerea, a peso, in pochi giorni.",
            "<strong>Grande volume non urgente</strong> (mobili, elettrodomestici, fusti): il container condiviso via mare, in più settimane."],
        sec=[
            ("1. La valigia in più in aereo", [
                "Compra il bagaglio extra <strong>online prima della partenza</strong>: di solito costa meno che al banco in aeroporto.",
                "Confronta il biglietto <strong>con i bagagli inclusi</strong> e non il solo biglietto: una compagnia più cara può costare meno una volta contate le valigie.",
                "Pesa tutto a casa: il chilo in più si paga caro al check-in.",
                'La franchigia e le regole di ogni compagnia: <a href="{bag}">bagagli per compagnia</a> e la guida <a href="{bagguide}">non pagare di più</a> (in inglese).']),
            ("2. Il pacco postale o espresso", [
                "Per un pacco piccolo, le poste del tuo paese (" + EXT("https://www.poste.it/", "Poste Italiane") + " in Italia, " + EXT("https://www.laposte.fr/", "La Poste") + " in Francia, " + EXT("https://www.bpost.be/", "bpost") + " in Belgio) o un corriere espresso.",
                "Fai il preventivo online con peso e dimensioni reali: il prezzo dipende anche dal volume.",
                "Compila con cura la <strong>dichiarazione doganale</strong> (contenuto, valore) e conserva il numero di tracciamento.",
                "Chiedi se la consegna è a domicilio o all'ufficio postale: in molte città il destinatario deve andare a ritirare il pacco."]),
            ("3. La spedizione aerea", [
                "Spedizionieri specializzati per paese ritirano gli scatoloni in Europa e li consegnano all'arrivo, spesso nella loro agenzia.",
                "Il prezzo si calcola <strong>a peso o a volume</strong>: chiedi sempre un preventivo scritto, con ciò che è incluso (imballaggio, dogana, consegna).",
                "Verifica che lo spedizioniere abbia un indirizzo, una partita IVA e una ricevuta con il dettaglio del contenuto."]),
            ("4. Il container condiviso via mare", [
                "Per fusti, tanti scatoloni, mobili ed elettrodomestici: paghi una parte di un container condiviso.",
                "Metti in conto <strong>più settimane</strong>, oltre allo sdoganamento all'arrivo.",
                "Fai un <strong>inventario dettagliato con foto</strong>: serve alla dogana e in caso di perdita o danni."]),
            ("Cosa non si spedisce", [
                "Batterie al litio sfuse, bombolette spray, prodotti infiammabili e profumi in quantità sono limitati o vietati in aereo.",
                "Contanti, gioielli di valore e documenti d'identità originali non viaggiano in un pacco normale.",
                "Medicinali, cibo, piante e prodotti animali hanno regole proprie in ogni paese.",
                "Per le spedizioni fuori dall'Unione europea vedi l'" + EXT("https://www.adm.gov.it/", "Agenzia delle Dogane e dei Monopoli") + ". All'arrivo decide la dogana del paese di destinazione."])],
        small="Escale non trasporta pacchi e qui non mostra tariffe: chiedi sempre un preventivo scritto. Le regole doganali cambiano: fanno fede i siti ufficiali.",
        faq=[
            ("Valigia in più o pacco: cosa costa meno?", "Per una o due valigie, il bagaglio extra comprato online prima della partenza è spesso la soluzione più semplice, perché viaggia con te. Oltre, o se non viaggi, chiedi un preventivo di spedizione: il prezzo è a peso o a volume e dipende dal paese."),
            ("Quanto ci mette una spedizione via mare?", "Più settimane, a cui si aggiunge lo sdoganamento all'arrivo. Il trasporto via mare va bene per cose ingombranti e non urgenti. Chiedi allo spedizioniere un tempo porta a porta, non solo la durata della traversata."),
            ("Si pagano dazi all'arrivo?", "Spesso sì: ogni paese ha le sue regole per merci nuove, elettronica, veicoli o quantità commerciali. Informati presso la dogana del paese di arrivo o lo spedizioniere prima di spedire, per non scoprire i costi al ritiro."),
            ("Posso affidare un pacco a un viaggiatore?", "È una pratica diffusa, ma rischiosa per entrambi: il viaggiatore è responsabile di tutto ciò che trasporta davanti alla dogana e alla compagnia. Affida e accetta solo pacchi aperti, con contenuto noto e consentito.")]),
}


def colis(site, ctx, l):
    t, k = COLIS[l], LK[l]
    hero = f'<p class="eyebrow">{t["eyebrow"]}{CHECKED[l]}</p><h1>{t["h1"]}</h1><p class="hero-lead">{E(t["lead"])}</p>'
    body = (f'<section><h2>{t["brief_h"]}</h2>{ul(t["brief"])}</section>'
            + "".join(f'<section><h2>{E(h)}</h2>{ul([x.format(**k) if "{bag" in x else x for x in items])}</section>' for h, items in t["sec"])
            + f'<section class="faq"><h2>{FAQ_H[l]}</h2>{faq_html(t["faq"])}</section>' + plus(l) + f'<p class="small">{t["small"]}</p>' + B.faq_ld(t["faq"]))
    return B.write(site, P["colis"][l], l, t["title"], t["desc"], hero, body, "", P["colis"], ctx)


# ---------------------------------------------------------------- vol à plusieurs étapes
ETAPES = {
    "en": dict(
        title="Multi-city flights: plan a trip with several stops | Escale",
        desc="Free tool for a trip in 2 to 4 legs (for example London, Lagos, Accra, London): one search per leg, the lowest price spotted that month and the precautions for separate tickets.",
        eyebrow="Free tool", h1='Multi-city <span>flights</span>',
        lead="London → Lagos → Accra → London? Enter your legs: Escale prepares one search per leg, with the lowest price spotted that month when it is known.",
        legs_h="Your legs", leg="Leg {i}: from", to="To", date="Date", ph="City or airport", add="+ Add a leg", pax="Travellers", go="Prepare my searches",
        how_h="How it works", how=[
            "Each leg is a <strong>one-way flight</strong>: you compare and book the tickets one by one.",
            "The arrival of one leg becomes the departure of the next, to save time.",
            "The price shown is the lowest <strong>recently spotted for that month</strong>, per person: it is confirmed when you open the search."],
        know_h="Before you book", know=[
            "<strong>Separate tickets = unprotected connection.</strong> If one flight is late, the next one does not wait and is not refunded. Leave a wide margin, ideally a night.",
            "You have to <strong>collect and re-check your bags</strong> at each leg.",
            'Each country has its own entry rules: check with the <a href="{visa}">visa tool</a>.',
            'Always compare with a plain return: two returns from the same city are sometimes cheaper. <a href="{home}">Compare a return flight</a>.'],
        faq=[
            ("Why one search per leg?", "Because separate tickets are often the cheapest way to visit two countries in one trip, and each leg can then be compared like a one-way flight. The tool prepares those searches for you, with the right dates."),
            ("What is the risk with separate tickets?", "The flights are not linked. If the first is late and you miss the next, the second airline owes you nothing. Leave a wide margin between two legs, ideally a night, and collect your bags at each leg."),
            ("Do I need a visa for each country?", "Yes, every country you enter applies its own rules, even for a short stop. Check before booking with Escale's visa tool and on the official sites."),
            ("What about a single ticket with a long stopover?", "Some airlines let you stay one or more days in their hub on a single ticket. That is safer than two separate tickets. Look at the offers of the airline linking your two cities.")]),
    "it": dict(
        title="Voli multi-tratta: organizzare un viaggio a più tappe | Escale",
        desc="Strumento gratuito per un viaggio in 2-4 tappe (per esempio Milano, Abidjan, Dakar, Milano): una ricerca per tappa, il prezzo più basso rilevato quel mese e le precauzioni dei biglietti separati.",
        eyebrow="Strumento gratuito", h1='Voli <span>multi-tratta</span>',
        lead="Milano → Abidjan → Dakar → Milano? Inserisci le tue tappe: Escale prepara una ricerca per tappa, con il prezzo più basso rilevato quel mese quando è noto.",
        legs_h="Le tue tappe", leg="Tappa {i}: partenza", to="Arrivo", date="Data", ph="Città o aeroporto", add="+ Aggiungi una tappa", pax="Viaggiatori", go="Prepara le mie ricerche",
        how_h="Come funziona", how=[
            "Ogni tappa è un <strong>volo di sola andata</strong>: confronti e prenoti i biglietti uno per uno.",
            "L'arrivo di una tappa diventa la partenza della successiva, per risparmiare tempo.",
            "Il prezzo mostrato è il più basso <strong>rilevato di recente per quel mese</strong>, a persona: si conferma aprendo la ricerca."],
        know_h="Da sapere prima di prenotare", know=[
            "<strong>Biglietti separati = coincidenza non protetta.</strong> Se un volo è in ritardo, il successivo non aspetta e non viene rimborsato. Tieni un margine ampio, meglio una notte.",
            "Devi <strong>ritirare e imbarcare di nuovo i bagagli</strong> a ogni tappa.",
            'Ogni paese ha le sue regole d\'ingresso: verifica con lo <a href="{visa}">strumento visti</a> (in inglese).',
            'Confronta sempre con un semplice andata e ritorno: a volte due andata e ritorno dalla stessa città costano meno. <a href="{home}">Confronta un andata e ritorno</a>.'],
        faq=[
            ("Perché una ricerca per tappa?", "Perché i biglietti separati sono spesso il modo più economico di visitare due paesi nello stesso viaggio, e ogni tappa si confronta allora come una sola andata. Lo strumento prepara queste ricerche per te, con le date giuste."),
            ("Qual è il rischio dei biglietti separati?", "I voli non sono collegati tra loro. Se il primo è in ritardo e perdi il successivo, la seconda compagnia non ti deve nulla. Tieni un margine ampio tra due tappe, meglio una notte, e ritira i bagagli a ogni tappa."),
            ("Serve un visto per ogni paese?", "Sì, ogni paese in cui entri applica le sue regole, anche per una tappa breve. Verifica prima di prenotare con lo strumento visti di Escale e sui siti ufficiali."),
            ("E un biglietto unico con uno scalo lungo?", "Alcune compagnie permettono di fermarsi uno o più giorni nella loro città di scalo con un solo biglietto. È più sicuro di due biglietti separati. Guarda le offerte della compagnia che collega le tue due città.")]),
}


def etapes(site, ctx, l):
    t, k = ETAPES[l], LK[l]
    hero = f'<p class="eyebrow">{t["eyebrow"]}</p><h1>{t["h1"]}</h1><p class="hero-lead">{E(t["lead"])}</p>'
    row = lambda i: (f'<div class="et-row" data-i="{i}"><div class="tool-grid"><label><span>{t["leg"].format(i=i)}</span><input class="et-from" placeholder="{t["ph"]}" autocomplete="off"></label>'
                     f'<label><span>{t["to"]}</span><input class="et-to" placeholder="{t["ph"]}" autocomplete="off"></label>'
                     f'<label><span>{t["date"]}</span><input class="et-date" type="date"></label></div></div>')
    body = (f'<section><h2>{t["legs_h"]}</h2><form id="et-form" class="tool-form" novalidate>' + row(1) + row(2) +
            f'<div id="et-more"></div><p class="et-actions"><button type="button" class="btn ghost" id="et-add">{t["add"]}</button> '
            f'<label class="et-pax"><span>{t["pax"]}</span> <select id="et-pax"><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option><option>6</option></select></label></p>'
            f'<p><button type="submit" class="btn">{t["go"]}</button></p><p id="et-msg" class="small" role="status"></p></form>'
            '<div id="et-out" aria-live="polite"></div></section>'
            f'<section><h2>{t["how_h"]}</h2>{ul(t["how"])}</section>'
            f'<section><h2>{t["know_h"]}</h2>{ul([x.format(**k) if "{" in x else x for x in t["know"]])}</section>'
            f'<section class="faq"><h2>{FAQ_H[l]}</h2>{faq_html(t["faq"])}</section>' + plus(l) + B.faq_ld(t["faq"]) +
            '<script src="/ac-mini.js" defer></script><script src="/etapes.js" defer></script>')
    return B.write(site, P["etapes"][l], l, t["title"], t["desc"], hero, body, "", P["etapes"], ctx)


# ---------------------------------------------------------------- aéroports de départ
# slug -> (nom, ville, [transports], remarque) par langue ; code et site officiel repris de D.AERO
AERO = {
    "en": {
        "paris-cdg": ("Paris Charles de Gaulle", "Paris", [
            "<strong>RER B</strong> suburban train from Gare du Nord, Châtelet-Les Halles, Saint-Michel or Denfert-Rochereau. Two stations: “Aéroport Charles de Gaulle 1” for terminals 1 and 3, “Aéroport Charles de Gaulle 2 TGV” for terminal 2.",
            "<strong>Roissybus</strong> from the Opéra district.",
            "<strong>High-speed trains (TGV)</strong>: the terminal 2 station has direct trains from many French cities and from Brussels, without going through Paris.",
            "<strong>CDGVAL</strong>: the free automatic shuttle links the terminals, the stations and the car parks."],
            "Check your terminal on the ticket: the airport is very spread out and terminal 2 has several halls."),
        "paris-orly": ("Paris Orly", "Paris", [
            "<strong>Metro line 14</strong> to “Aéroport d'Orly” station, from Châtelet, Gare de Lyon or Saint-Lazare.",
            "<strong>Tram T7</strong> from Villejuif-Louis Aragon (metro line 7).",
            "<strong>Orlyval</strong> shuttle train from Antony station (RER B)."],
            "Orly has four sectors (Orly 1, 2, 3 and 4) linked on foot: check yours on the ticket."),
        "lyon": ("Lyon Saint-Exupéry", "Lyon", [
            "<strong>Rhônexpress</strong>: the express tram from Lyon Part-Dieu station.",
            "<strong>High-speed trains (TGV)</strong>: Lyon-Saint-Exupéry TGV station is next to the terminals.",
            "<strong>Coaches</strong> link the airport to several cities in the region (Grenoble, Chambéry, Annecy…)."], ""),
        "marseille": ("Marseille Provence", "Marseille", [
            "<strong>Shuttle coach</strong> from Marseille Saint-Charles station.",
            "<strong>Train</strong> to “Vitrolles Aéroport Marseille Provence” station, then a shuttle bus to the terminals.",
            "Coaches also link the airport to Aix-en-Provence."],
            "The airport has two terminals, one of them for low-cost airlines: check yours."),
        "bruxelles": ("Brussels Zaventem", "Brussels", [
            "<strong>Train</strong>: “Brussels Airport-Zaventem” station is under the terminal. Direct trains from Brussels-Midi, Brussels-Central and Brussels-North, and from several Belgian cities (Antwerp, Ghent, Leuven, Liège…).",
            "<strong>Buses</strong> from Brussels and nearby towns, on level 0 of the terminal."],
            "Do not confuse it with Brussels South Charleroi (CRL), a different airport about an hour's drive from Brussels."),
        "londres-heathrow": ("London Heathrow", "London", [
            "<strong>Elizabeth line</strong> from central London (Paddington, Bond Street, Liverpool Street…).",
            "<strong>Piccadilly line</strong> (Underground): the cheapest, and slower.",
            "<strong>Heathrow Express</strong>: non-stop train from Paddington station.",
            "<strong>Coaches</strong> from many UK cities to the central bus station."],
            "Heathrow has four terminals in use (2, 3, 4 and 5), with different stations: check yours before boarding the train."),
        "milan-malpensa": ("Milan Malpensa", "Milan", [
            "<strong>Malpensa Express</strong>: train from Milano Centrale, Milano Porta Garibaldi and Milano Cadorna, to terminals 1 and 2.",
            "<strong>Coaches</strong> from Milano Centrale station, and from other cities in northern Italy."],
            "Milan has three airports: Malpensa (MXP), Linate (LIN) and Bergamo-Orio al Serio (BGY). Check the code on your ticket."),
        "rome-fiumicino": ("Rome Fiumicino", "Rome", [
            "<strong>Leonardo Express</strong>: non-stop train from Roma Termini station.",
            "<strong>Regional train FL1</strong> from Roma Tiburtina, Roma Ostiense and Roma Trastevere (it does not call at Termini).",
            "<strong>Coaches</strong> from Termini and other points in the city."],
            "Do not confuse it with Rome Ciampino (CIA), Rome's other airport."),
        "geneve": ("Geneva", "Geneva", [
            "<strong>Train</strong>: “Genève-Aéroport” station is connected to the terminal. Every train from Genève-Cornavin gets there in a few minutes, and direct trains arrive from Lausanne, Bern or Zurich.",
            "<strong>Buses</strong> of the Geneva public transport network from the city centre."],
            "The airport also has a French sector, reachable from France without going through Swiss customs."),
        "madrid": ("Madrid Barajas", "Madrid", [
            "<strong>Metro line 8</strong> from Nuevos Ministerios: one station for terminals 1-2-3, another for terminal 4.",
            "<strong>Suburban trains (Cercanías)</strong> lines C1 and C10 to terminal 4, from Atocha and Chamartín.",
            "<strong>Exprés Aeropuerto bus</strong> from Atocha and Cibeles, day and night."],
            "Terminal 4 is far from the other three: a free shuttle links them, so allow time."),
        "barcelone": ("Barcelona El Prat", "Barcelona", [
            "<strong>Aerobús</strong> from Plaça de Catalunya, to terminal 1 or terminal 2.",
            "<strong>Metro line L9 Sud</strong> to both terminals.",
            "<strong>R2 Nord train</strong> from Barcelona Sants and Passeig de Gràcia to terminal 2."],
            "The two terminals are far apart: a free shuttle links them."),
        "francfort": ("Frankfurt", "Frankfurt", [
            "<strong>S-Bahn S8 and S9</strong> from the main station (Hauptbahnhof) to the airport regional station, at terminal 1.",
            "<strong>Long-distance trains (ICE)</strong>: “Frankfurt Flughafen Fernbahnhof” station has direct trains from many German cities."],
            "Do not confuse it with Frankfurt-Hahn (HHN), an airport very far from the city."),
        "lisbonne": ("Lisbon", "Lisbon", [
            "<strong>Metro red line (Vermelha)</strong> to “Aeroporto” station, at terminal 1.",
            "<strong>City buses</strong> from the centre."],
            "Terminal 2, used by low-cost airlines for departures, is reached by a free shuttle from terminal 1."),
        "montreal": ("Montréal-Trudeau", "Montreal", [
            "<strong>Bus 747</strong> run by the STM from downtown (Berri-UQAM station, with a stop at Lionel-Groulx), day and night.",
            "<strong>Taxi</strong> at a fixed fare between the airport and downtown."], ""),
    },
    "it": {
        "paris-cdg": ("Parigi Charles de Gaulle", "Parigi", [
            "<strong>RER B</strong> (treno suburbano) da Gare du Nord, Châtelet-Les Halles, Saint-Michel o Denfert-Rochereau. Due stazioni: «Aéroport Charles de Gaulle 1» per i terminal 1 e 3, «Aéroport Charles de Gaulle 2 TGV» per il terminal 2.",
            "<strong>Roissybus</strong> dal quartiere dell'Opéra.",
            "<strong>Treni ad alta velocità (TGV)</strong>: la stazione del terminal 2 ha treni diretti da molte città francesi e da Bruxelles, senza passare per Parigi.",
            "<strong>CDGVAL</strong>: la navetta automatica gratuita collega i terminal, le stazioni e i parcheggi."],
            "Controlla il terminal sul biglietto: l'aeroporto è molto esteso e il terminal 2 ha più hall."),
        "paris-orly": ("Parigi Orly", "Parigi", [
            "<strong>Metro linea 14</strong> fino alla stazione «Aéroport d'Orly», da Châtelet, Gare de Lyon o Saint-Lazare.",
            "<strong>Tram T7</strong> da Villejuif-Louis Aragon (metro linea 7).",
            "<strong>Orlyval</strong> dalla stazione di Antony (RER B)."],
            "Orly ha quattro settori (Orly 1, 2, 3 e 4) collegati a piedi: controlla il tuo sul biglietto."),
        "lyon": ("Lione Saint-Exupéry", "Lione", [
            "<strong>Rhônexpress</strong>: il tram espresso dalla stazione di Lyon Part-Dieu.",
            "<strong>Treni ad alta velocità (TGV)</strong>: la stazione Lyon-Saint-Exupéry TGV è accanto ai terminal.",
            "<strong>Pullman</strong> collegano l'aeroporto a diverse città della regione (Grenoble, Chambéry, Annecy…)."], ""),
        "marseille": ("Marsiglia Provenza", "Marsiglia", [
            "<strong>Navetta in pullman</strong> dalla stazione Marseille Saint-Charles.",
            "<strong>Treno</strong> fino alla stazione «Vitrolles Aéroport Marseille Provence», poi navetta in bus fino ai terminal.",
            "Altri pullman collegano l'aeroporto ad Aix-en-Provence."],
            "L'aeroporto ha due terminal, uno dei quali per le compagnie low cost: controlla il tuo."),
        "bruxelles": ("Bruxelles Zaventem", "Bruxelles", [
            "<strong>Treno</strong>: la stazione «Brussels Airport-Zaventem» è sotto il terminal. Treni diretti da Bruxelles-Midi, Bruxelles-Central e Bruxelles-Nord, e da diverse città belghe (Anversa, Gand, Lovanio, Liegi…).",
            "<strong>Autobus</strong> da Bruxelles e dai comuni vicini, al livello 0 del terminal."],
            "Da non confondere con Bruxelles Sud Charleroi (CRL), un altro aeroporto a circa un'ora di strada da Bruxelles."),
        "londres-heathrow": ("Londra Heathrow", "Londra", [
            "<strong>Elizabeth line</strong> dal centro di Londra (Paddington, Bond Street, Liverpool Street…).",
            "<strong>Metropolitana Piccadilly line</strong>: la più economica, più lenta.",
            "<strong>Heathrow Express</strong>: treno senza fermate dalla stazione di Paddington.",
            "<strong>Pullman</strong> da molte città del Regno Unito fino all'autostazione centrale."],
            "Heathrow ha quattro terminal in servizio (2, 3, 4 e 5), con stazioni diverse: controlla il tuo prima di salire sul treno."),
        "milan-malpensa": ("Milano Malpensa", "Milano", [
            "<strong>Malpensa Express</strong>: treno da Milano Centrale, Milano Porta Garibaldi e Milano Cadorna, fino ai terminal 1 e 2.",
            "<strong>Pullman</strong> dalla stazione di Milano Centrale, e da altre città del nord Italia."],
            "Milano ha tre aeroporti: Malpensa (MXP), Linate (LIN) e Bergamo-Orio al Serio (BGY). Controlla il codice sul biglietto."),
        "rome-fiumicino": ("Roma Fiumicino", "Roma", [
            "<strong>Leonardo Express</strong>: treno senza fermate dalla stazione di Roma Termini.",
            "<strong>Treno regionale FL1</strong> da Roma Tiburtina, Roma Ostiense e Roma Trastevere (non passa da Termini).",
            "<strong>Pullman</strong> da Termini e da altri punti della città."],
            "Da non confondere con Roma Ciampino (CIA), l'altro aeroporto di Roma."),
        "geneve": ("Ginevra", "Ginevra", [
            "<strong>Treno</strong>: la stazione «Genève-Aéroport» è collegata al terminal. Tutti i treni da Genève-Cornavin ci arrivano in pochi minuti, e ci sono treni diretti da Losanna, Berna o Zurigo.",
            "<strong>Autobus</strong> dei trasporti pubblici ginevrini dal centro città."],
            "L'aeroporto ha anche un settore francese, raggiungibile dalla Francia senza passare la dogana svizzera."),
        "madrid": ("Madrid Barajas", "Madrid", [
            "<strong>Metro linea 8</strong> da Nuevos Ministerios: una stazione per i terminal 1-2-3, un'altra per il terminal 4.",
            "<strong>Treni suburbani (Cercanías)</strong> linee C1 e C10 fino al terminal 4, da Atocha e Chamartín.",
            "<strong>Bus Exprés Aeropuerto</strong> da Atocha e Cibeles, giorno e notte."],
            "Il terminal 4 è lontano dagli altri tre: una navetta gratuita li collega, metti in conto del tempo."),
        "barcelone": ("Barcellona El Prat", "Barcellona", [
            "<strong>Aerobús</strong> da Plaça de Catalunya, verso il terminal 1 o il terminal 2.",
            "<strong>Metro linea L9 Sud</strong> fino ai due terminal.",
            "<strong>Treno R2 Nord</strong> da Barcelona Sants e Passeig de Gràcia fino al terminal 2."],
            "I due terminal sono lontani tra loro: una navetta gratuita li collega."),
        "francfort": ("Francoforte", "Francoforte", [
            "<strong>S-Bahn S8 e S9</strong> dalla stazione centrale (Hauptbahnhof) fino alla stazione regionale dell'aeroporto, al terminal 1.",
            "<strong>Treni a lunga percorrenza (ICE)</strong>: la stazione «Frankfurt Flughafen Fernbahnhof» ha treni diretti da molte città tedesche."],
            "Da non confondere con Francoforte-Hahn (HHN), un aeroporto molto lontano dalla città."),
        "lisbonne": ("Lisbona", "Lisbona", [
            "<strong>Metro linea rossa (Vermelha)</strong> fino alla stazione «Aeroporto», al terminal 1.",
            "<strong>Autobus</strong> urbani dal centro."],
            "Il terminal 2, usato dalle compagnie low cost per le partenze, si raggiunge con una navetta gratuita dal terminal 1."),
        "montreal": ("Montréal-Trudeau", "Montréal", [
            "<strong>Bus 747</strong> della STM dal centro (stazione Berri-UQAM, con fermata a Lionel-Groulx), giorno e notte.",
            "<strong>Taxi</strong> a tariffa fissa tra l'aeroporto e il centro."], ""),
    },
}
AT = {
    "en": dict(
        title="Getting to {n} airport ({c}): train, metro, bus | Escale",
        desc="How to get to {n} airport ({c}) before a flight: the trains, metro lines and buses that serve it, parking, what to check the day before, with the link to the official site.",
        eyebrow="Departure airport · checked in ", h1='Getting to <span>{n} airport ({c})</span>',
        lead="Train, metro, bus, car: how to reach {n} before your flight, and what to check the day before.",
        pt_h="By public transport", off="Timetables, fares and engineering works: {a}.", offl="the airport's official site",
        car_h="By car", car=[
            "<strong>Official car parks</strong> can be booked online on the airport's site: it is usually cheaper than turning up without a booking.",
            "To drop someone off, follow the “drop-off” signs: stopping there is limited to a few minutes.",
            "Allow a margin for traffic at rush hour and for the shuttle between the car park and the terminal."],
        eve_h="The day before", eve=[
            "Check the <strong>terminal</strong> and the check-in deadline on your ticket.",
            "See whether there is a strike or engineering work on your line, and have a plan B.",
            'Weigh your bags: <a href="{bag}">each airline\'s allowance</a>.',
            'Go through the <a href="{check}">pre-flight check</a>: passport, visa, documents.'],
        cmp_h="Compare flights from {v}", cmp_b="See flights from {v}", others="Other departure airports",
        small="This is general guidance. Lines, stops and terminals can change: the airport's official site is the reference.",
        faq=lambda n: [
            (f"How long before the flight should I arrive at {n}?", "For a long-haul flight to Africa, airlines often recommend arriving about three hours before departure. Your airline's check-in deadline is shown on the ticket: that is the one that counts."),
            ("Train or car?", "The train or metro avoids traffic jams and the cost of parking for a long stay. The car is still practical for a family with many suitcases or for a very early flight: in that case, book the official car park online in advance."),
            ("Where do I find timetables and fares?", "On the airport's official site and on the transport operator's site. Escale shows neither timetables nor fares, because they change: check the day before departure, especially if there is a strike or engineering work.")],
        hub_title="Getting to your departure airport: train, metro, bus | Escale",
        hub_desc="How to get to the airport before a flight: Paris CDG and Orly, Lyon, Marseille, Brussels, London Heathrow, Milan Malpensa, Rome Fiumicino, Geneva, Madrid, Barcelona, Frankfurt, Lisbon, Montreal.",
        hub_eyebrow="Guides · checked in ", hub_h1='Getting to your <span>departure airport</span>',
        hub_lead="Train, metro, bus or car: how to get to the airport before a flight to Africa, from the main European cities and Montreal.",
        hub_pick="Choose your airport", hub_tips_h="Good habits", hub_tips=[
            "Check the <strong>airport code</strong> on the ticket: several cities have two or three airports (Paris, Milan, Rome, London, Brussels).",
            "For a long-haul flight, airlines often recommend arriving about <strong>three hours before</strong>: the check-in deadline is on the ticket.",
            "The day before, check whether there is a strike or engineering work on your line.",
            'On arrival in Africa: <a href="/en/arriving-at-abidjan-airport/">Abidjan</a>, <a href="/en/arriving-at-accra-airport/">Accra</a>, <a href="/en/arriving-at-lagos-airport/">Lagos</a>, <a href="/en/arriving-at-dakar-airport/">Dakar</a> and the other cities in the <a href="{guides}">guides</a>.'],
        hub_n="the airport"),
    "it": dict(
        title="Come arrivare all'aeroporto di {n} ({c}): treno, metro, bus | Escale",
        desc="Come raggiungere l'aeroporto di {n} ({c}) prima di un volo: i treni, le metro e i bus che lo servono, il parcheggio, cosa controllare il giorno prima, con il link al sito ufficiale.",
        eyebrow="Aeroporto di partenza · verificato a ", h1='Arrivare all\'aeroporto di <span>{n} ({c})</span>',
        lead="Treno, metro, bus, auto: come raggiungere {n} prima del volo, e cosa controllare il giorno prima.",
        pt_h="Con i mezzi pubblici", off="Orari, tariffe e lavori: {a}.", offl="sito ufficiale dell'aeroporto",
        car_h="In auto", car=[
            "I <strong>parcheggi ufficiali</strong> si prenotano online sul sito dell'aeroporto: di solito costa meno che arrivare senza prenotazione.",
            "Per accompagnare qualcuno, segui i cartelli della sosta breve: la fermata è limitata a pochi minuti.",
            "Metti in conto un margine per il traffico nelle ore di punta e per la navetta tra parcheggio e terminal."],
        eve_h="Il giorno prima", eve=[
            "Controlla il <strong>terminal</strong> e l'orario limite del check-in sul biglietto.",
            "Guarda se c'è uno sciopero o dei lavori sulla tua linea, e prepara un piano B.",
            'Pesa le valigie: <a href="{bag}">franchigia di ogni compagnia</a> (in inglese).',
            'Ripassa il <a href="{check}">controllo prima del volo</a>: passaporto, visto, documenti.'],
        cmp_h="Confronta i voli da {v}", cmp_b="Vedi i voli da {v}", others="Altri aeroporti di partenza",
        small="Sono indicazioni generali. Linee, fermate e terminal possono cambiare: fa fede il sito ufficiale dell'aeroporto.",
        faq=lambda n: [
            (f"Quanto tempo prima del volo bisogna arrivare a {n}?", "Per un volo a lungo raggio verso l'Africa, le compagnie consigliano spesso di arrivare circa tre ore prima della partenza. L'orario limite del check-in della tua compagnia è indicato sul biglietto: è quello che conta."),
            ("Treno o auto?", "Il treno o la metro evitano il traffico e il costo del parcheggio per un soggiorno lungo. L'auto resta comoda in famiglia con tante valigie o per un volo molto presto: in questo caso prenota in anticipo online il parcheggio ufficiale."),
            ("Dove trovo orari e tariffe?", "Sul sito ufficiale dell'aeroporto e su quello dell'azienda di trasporto. Escale non mostra né orari né tariffe, perché cambiano: verifica il giorno prima della partenza, soprattutto in caso di sciopero o lavori.")],
        hub_title="Raggiungere l'aeroporto di partenza: treno, metro, bus | Escale",
        hub_desc="Come arrivare in aeroporto prima di un volo: Milano Malpensa, Roma Fiumicino, Parigi CDG e Orly, Lione, Marsiglia, Bruxelles, Londra Heathrow, Ginevra, Madrid, Barcellona, Francoforte, Lisbona, Montréal.",
        hub_eyebrow="Guide · verificate a ", hub_h1='Raggiungere l\'<span>aeroporto di partenza</span>',
        hub_lead="Treno, metro, bus o auto: come arrivare in aeroporto prima di un volo per l'Africa, dalle grandi città d'Europa e da Montréal.",
        hub_pick="Scegli il tuo aeroporto", hub_tips_h="Le buone abitudini", hub_tips=[
            "Controlla il <strong>codice dell'aeroporto</strong> sul biglietto: diverse città ne hanno due o tre (Milano, Roma, Parigi, Londra, Bruxelles).",
            "Per un volo a lungo raggio, le compagnie consigliano spesso di arrivare circa <strong>tre ore prima</strong>: l'orario limite del check-in è sul biglietto.",
            "Il giorno prima guarda se c'è uno sciopero o dei lavori sulla tua linea.",
            'All\'arrivo in Africa (in inglese): <a href="/en/arriving-at-abidjan-airport/">Abidjan</a>, <a href="/en/arriving-at-dakar-airport/">Dakar</a>, <a href="/en/arriving-at-lagos-airport/">Lagos</a>, <a href="/en/arriving-at-casablanca-airport/">Casablanca</a> e le altre città nelle <a href="{guides}">guide</a>.'],
        hub_n="l'aeroporto"),
}


def aeroports(site, ctx, l):
    t, k, urls = AT[l], LK[l], []
    order = D.AERO if l == "en" else sorted(D.AERO, key=lambda a: a[0] not in ("milan-malpensa", "rome-fiumicino"))
    for a in D.AERO:
        slug, code, off = a[0], a[3], a[4]
        nom, ville, lignes, note = AERO[l][slug]
        autres = "".join(f'<li><a href="/{D.A_PATHS(x[0])[l]}/">{E(AERO[l][x[0]][0])} ({x[3]})</a></li>' for x in order if x[0] != slug)
        faq = t["faq"](nom)
        hero = (f'<p class="eyebrow">{t["eyebrow"]}{CHECKED[l]}</p><h1>{t["h1"].format(n=E(nom), c=code)}</h1><p class="hero-lead">{E(t["lead"].format(n=nom))}</p>')
        body = (f'<section><h2>{t["pt_h"]}</h2>{ul(lignes)}' + (f"<p>{note}</p>" if note else "") + f'<p>{t["off"].format(a=EXT(off, t["offl"]))}</p></section>'
                f'<section><h2>{t["car_h"]}</h2>{ul(t["car"])}</section>'
                f'<section><h2>{t["eve_h"]}</h2>{ul([x.format(**k) if "{" in x else x for x in t["eve"]])}</section>'
                f'<section><h2>{E(t["cmp_h"].format(v=ville))}</h2><p><a class="btn" href="{k["home"]}?type=vols&amp;from={code}">{E(t["cmp_b"].format(v=ville))}</a></p></section>'
                f'<section class="faq"><h2>{FAQ_H[l]}</h2>{faq_html(faq)}</section>'
                f'<section><h2>{t["others"]}</h2><ul class="links">{autres}</ul></section>' + plus(l) + f'<p class="small">{t["small"]}</p>' + B.faq_ld(faq))
        urls.append(B.write(site, D.A_PATHS(slug)[l], l, t["title"].format(n=nom, c=code), t["desc"].format(n=nom, c=code), hero, body, "", D.A_PATHS(slug), ctx))
    liste = "".join(f'<li><a href="/{D.A_PATHS(a[0])[l]}/">{E(AERO[l][a[0]][0])} ({a[3]})</a></li>' for a in order)
    faq = t["faq"](t["hub_n"])
    hero = f'<p class="eyebrow">{t["hub_eyebrow"]}{CHECKED[l]}</p><h1>{t["hub_h1"]}</h1><p class="hero-lead">{E(t["hub_lead"])}</p>'
    body = (f'<section><h2>{t["hub_pick"]}</h2><ul class="links">{liste}</ul></section>'
            f'<section><h2>{t["hub_tips_h"]}</h2>{ul([x.format(**k) if "{guides" in x else x for x in t["hub_tips"]])}</section>'
            f'<section class="faq"><h2>{FAQ_H[l]}</h2>{faq_html(faq)}</section>' + plus(l) + B.faq_ld(faq))
    urls.append(B.write(site, P["hub"][l], l, t["hub_title"], t["hub_desc"], hero, body, "", P["hub"], ctx))
    return urls


def build(site, ctx):
    urls = []
    for l in ("en", "it"):
        urls += [argent(site, ctx, l), colis(site, ctx, l), etapes(site, ctx, l)] + aeroports(site, ctx, l)
    return urls
