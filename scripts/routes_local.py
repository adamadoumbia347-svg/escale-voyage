"""Contenu propre à quelques trajets en espagnol et en portugais (pages qui ont des impressions dans Google, novembre 2026),
et bloc « Depuis Londres » ajouté aux pages anglaises au départ de Londres.
Règles d'entrée résumées prudemment (vérifiées en novembre 2026) : chaque page renvoie vers la vérification officielle.
"""
import html

E = html.escape

L = {
    "es": dict(glance="{a} – {b} en resumen", direct="Vuelos directos", stops="Vuelos con escala", when="Cuándo ir a {b}", bags="Equipaje",
               entry="Requisitos de entrada", checked="Información revisada en noviembre de 2026. Las compañías y los horarios cambian según la temporada: compruébalo siempre en el sitio de reserva."),
    "pt": dict(glance="{a} – {b} em resumo", direct="Voos diretos", stops="Voos com escala", when="Quando ir a {b}", bags="Bagagem",
               entry="Requisitos de entrada", checked="Informação verificada em novembro de 2026. As companhias e os horários mudam conforme a época: confirme sempre no site de reserva."),
}

ROUTES = {
    ("MAD", "RAK", "es"): dict(
        intro="Madrid – Marrakech es una de las rutas más baratas para ir a Marruecos desde España: vuelo corto, varias compañías y muchas ofertas fuera de temporada alta.",
        direct="Hay vuelos directos de unas 2 horas, sobre todo con compañías de bajo coste, además de compañías tradicionales según la temporada. Compara el precio con la maleta incluida.",
        stops="Si no hay plazas directas a buen precio, mira las escalas en Casablanca (Royal Air Maroc) o la llegada a otro aeropuerto como Agadir o Fez, a pocas horas por carretera o en tren.",
        season="La primavera (marzo-mayo) y el otoño (septiembre-noviembre) son las épocas más agradables. En verano hace mucho calor; Semana Santa, puentes y vacaciones de Navidad suben los precios.",
        bags="Las tarifas más baratas suelen incluir solo un bolso pequeño bajo el asiento. Si llevas maleta, añade su precio antes de comparar dos vuelos.",
        entry="Los ciudadanos españoles y de la UE pueden entrar en Marruecos sin visado para estancias turísticas de hasta 90 días, con el pasaporte en vigor. Otros pasaportes: compruébalo antes de viajar.",
        faq=[("¿Cuánto dura el vuelo Madrid – Marrakech?", "Unas 2 horas en vuelo directo."),
             ("¿Cuándo es más barato volar de Madrid a Marrakech?", "Fuera de Semana Santa, puentes, verano y Navidad. Los martes y miércoles suelen ser más baratos; reserva con uno o dos meses de antelación."),
             ("¿Necesito visado para ir a Marruecos desde España?", "No para ciudadanos españoles y de la UE en estancias turísticas de hasta 90 días. Lleva el pasaporte (no basta el DNI).")]),
    ("LIS", "LAD", "pt"): dict(
        intro="Lisboa – Luanda é uma das ligações mais procuradas entre Portugal e Angola, por famílias, estudantes e viagens de negócios. Há voos diretos, mas os preços sobem muito nas épocas festivas.",
        direct="A TAP e a TAAG operam voos diretos, com cerca de 8 horas de duração. Compare as duas companhias e as tarifas com bagagem incluída.",
        stops="Com escala, os voos passam muitas vezes por Madrid, Paris, Istambul, Adis Abeba ou Dubai: podem ser mais baratos, mas a viagem é bem mais longa.",
        season="A época seca vai de maio a setembro (o cacimbo), mais fresca. Natal, fim de ano e as férias de verão em Portugal são os períodos mais caros: reserve com 3 a 4 meses de antecedência.",
        bags="Nas rotas para África a bagagem pesa no preço final: verifique quantas malas estão incluídas, sobretudo para estadias longas.",
        entry="Desde 2023, Angola isenta de visto muitos passaportes, incluindo o português, para turismo de curta duração. O certificado de vacinação contra a febre amarela é exigido. Confirme as regras em vigor antes de viajar.",
        faq=[("Há voos diretos de Lisboa para Luanda?", "Sim, a TAP e a TAAG voam diretamente, em cerca de 8 horas."),
             ("Preciso de visto para ir a Angola com passaporte português?", "Desde 2023 os portugueses estão isentos de visto para turismo de curta duração. Confirme sempre antes de viajar, e leve o certificado da febre amarela."),
             ("Quando é mais barato voar de Lisboa para Luanda?", "Fora do Natal, fim de ano e verão. Ative as datas flexíveis e crie um alerta de preço.")]),
    ("LIS", "MPM", "pt"): dict(
        intro="Lisboa – Maputo liga Portugal à capital de Moçambique. Há voo direto, e as escalas em Joanesburgo, Adis Abeba ou no Golfo são alternativas frequentes.",
        direct="A TAP opera voos diretos, com cerca de 10 horas e meia. Os lugares esgotam cedo no Natal e no verão.",
        stops="As ligações com escala passam muitas vezes por Joanesburgo, Adis Abeba, Doha ou Dubai. Compare a duração total, não só o preço.",
        season="De maio a outubro é a época seca e mais fresca, a melhor para visitar. O Natal e o verão europeu são os períodos mais caros.",
        bags="Verifique a franquia de bagagem antes de comparar: para estadias longas, a segunda mala muda tudo.",
        entry="Moçambique isentou de visto vários passaportes para turismo de curta duração desde 2023. As regras e as formalidades online mudam: confirme no site oficial antes de viajar.",
        faq=[("Há voo direto de Lisboa para Maputo?", "Sim, a TAP voa diretamente, em cerca de 10 horas e meia."),
             ("Qual é a melhor época para ir a Maputo?", "De maio a outubro, a época seca e mais fresca.")]),
    ("LIS", "RAI", "pt"): dict(
        intro="Lisboa – Praia é a ligação mais direta entre Portugal e a ilha de Santiago, em Cabo Verde. Voo curto e várias opções por semana.",
        direct="Há voos diretos de cerca de 4 horas, nomeadamente da TAP e da Cabo Verde Airlines.",
        stops="Se Praia estiver cara, compare com a chegada ao Sal ou à Boa Vista e um voo interno, ou ao contrário.",
        season="O clima é ameno quase todo o ano; a época das chuvas, curta, vai sobretudo de agosto a outubro. Natal, Páscoa e verão sobem os preços.",
        bags="As tarifas mais baratas podem não incluir mala no porão: verifique antes de pagar.",
        entry="Os cidadãos da União Europeia estão isentos de visto para estadias curtas, mas têm de fazer o registo prévio online e pagar a taxa de segurança aeroportuária antes da viagem. Confirme no site oficial.",
        faq=[("Quanto tempo dura o voo Lisboa – Praia?", "Cerca de 4 horas em voo direto."),
             ("Preciso de visto para Cabo Verde com passaporte português?", "Não para estadias curtas, mas o registo prévio online e a taxa de segurança aeroportuária são obrigatórios.")]),
}


def route_html(r, a, b, lang):
    t = L[lang]
    p = lambda h, x: f"<h3>{E(h)}</h3><p>{E(x)}</p>"
    return (f'<section class="trajet"><h2>{E(t["glance"].format(a=a, b=b))}</h2><p>{E(r["intro"])}</p>'
            + p(t["direct"], r["direct"]) + p(t["stops"], r["stops"]) + "</section>"
            + f'<section><h2>{E(t["when"].format(b=b))}</h2><p>{E(r["season"])}</p></section>'
            + f'<section><h2>{E(t["bags"])}</h2><p>{E(r["bags"])}</p></section>'
            + f'<section><h2>{E(t["entry"])}</h2><p>{E(r["entry"])}</p><p class="small">{E(t["checked"])}</p></section>')


# ---------- Bloc « Depuis Londres » (pages anglaises au départ de Londres) ----------
def london_html(b):
    return (f'<section class="trajet"><h2>Flying from London to {E(b)}: practical tips</h2>'
            f'<h3>Which London airport?</h3><p>Most flights to {E(b)} leave from Heathrow (LHR) or Gatwick (LGW); some connecting itineraries start from Stansted or Luton. '
            'Search “London (all airports)” to compare them in one go, and count the cost and time of getting to each airport.</p>'
            '<h3>Connections in Europe</h3><p>Many trips connect in Paris, Brussels, Lisbon, Madrid or Amsterdam. If you do not hold a British or EU passport, '
            'check whether you need an airport transit visa for a connection in the Schengen area before booking.</p>'
            '<h3>Baggage for long stays</h3><p>Fares that look cheap often include one checked bag only. If you travel with gifts or a second suitcase, '
            'compare the price with the extra bag included, and check the weight limit per bag.</p>'
            '<h3>Paying less</h3><p>Turn on flexible dates (±3 days), avoid the school holidays and Christmas peak, and set a free price alert: '
            'fares often move by tens of pounds from one week to the next.</p></section>')


def london_faq(b):
    return [(f"Which London airport is best for flights to {b}?", f"Heathrow and Gatwick have most flights to {b}. Compare all London airports in one search, including the cost of getting there."),
            (f"Do I need a transit visa when flying from London to {b} via Europe?", "It depends on your passport. British and EU citizens do not; some other nationalities need an airport transit visa for a connection in the Schengen area. Check before booking.")]
