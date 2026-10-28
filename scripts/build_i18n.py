"""Pages trajets et hôtels traduites (anglais, espagnol, portugais, arabe).

Appelé par build_pages.py. Chaque page a ses équivalents dans toutes les langues (balises hreflang)
et un sélecteur de langue. Les textes propres à chaque page viennent de translations.py.
"""
import trajets_en as TEN
import html
import json
import re
import urllib.parse

import translations as TR

E = html.escape
LANGS = ["en", "es", "pt", "ar"]
COL = {"en": 0, "es": 1, "pt": 2, "ar": 3}
NAMES = {"fr": "Français", "en": "English", "es": "Español", "pt": "Português", "ar": "العربية"}
LOCALE = {"fr": "fr_FR", "en": "en_GB", "es": "es_ES", "pt": "pt_PT", "ar": "ar"}

UI = {
    "en": dict(
        flight_slug="flights", hotel_slug="cheap-hotels", app_lang="en", arrow="→",
        title_route="Cheap flights {a} to {b}: compare prices",
        desc_route="Cheap flight {a} – {b} ({fa} → {ta}): flight time, best time to book and prices compared on Skyscanner, Kayak and momondo.",
        h1_route="Cheap flights {a} <span>→</span> {b}", cta="Compare prices now", back="Return trip {b} → {a}",
        duration="Flight time", arrival="Arrival", peak="Most expensive periods",
        dur_direct="About {d} on a direct flight", dur_var="Varies: most trips have at least one stop",
        prices_h="Prices found recently", prices_p="Lowest round-trip prices found by travellers in the last few days, by departure month. The exact available fare is shown on the booking sites.",
        tip_h="Our tip for this route", cheap_h="How to pay less",
        steps=["<strong>Turn on flexible dates.</strong> Moving your departure by a day or two often changes the price more than the choice of site.",
               "<strong>Compare at least three sites.</strong> Escale opens your search, already sorted by price, on Skyscanner, Kayak, momondo and Aviasales.",
               "<strong>Check the baggage allowance.</strong> Add the price of a suitcase before comparing two fares.",
               "<strong>Set a price alert</strong> on Kayak or Skyscanner if you are travelling in several months."],
        launch="Search {a} → {b}", direct_h="Go straight to the comparison sites",
        sky="Monthly prices on Skyscanner", hotels_in="Hotels in {b}", cars_in="Car rental in {b}",
        faq_h="Frequently asked questions", other_routes="Other routes",
        faq=[("How long is a flight from {a} to {b}?", "{dur_long}. With a stop, the total trip often takes several hours more depending on the connection."),
             ("When should I book a cheap flight from {a} to {b}?", "Usually two to three months before departure. Prices rise sharply during {peak}: book earlier for those periods."),
             ("Which airport in {b}?", "Flights arrive at {airport} ({ta})."),
             ("Is baggage included?", "Not always. The lowest fares sometimes include only a small bag. Check the checked-baggage allowance before paying.")],
        dur_long_direct="About {d} on a direct flight", dur_long_var="It varies: most trips have at least one stop",
        title_hotel="Cheap hotels in {c}: compare prices",
        desc_hotel="Cheap hotel in {c} ({country}): where to stay, tips to pay less and prices compared on Booking, Agoda and Airbnb.",
        h1_hotel="Cheap hotels in <span>{c}</span>", hotel_codes="hotels and apartments", hotel_cta="Compare hotel prices", flights_to="Flights to {c}",
        where_h="Where to stay in {c}", our_tip="Our tip",
        hsteps=["<strong>Compare at least three sites.</strong> The same hotel does not always have the same price on Booking, Hotels.com or Agoda.",
                "<strong>Choose free cancellation.</strong> You can rebook elsewhere if the price drops.",
                "<strong>Look at the total price.</strong> Tourist tax, breakfast and cleaning fees change the ranking.",
                "<strong>For 3 nights or more, look at apartments</strong>: often cheaper for a family."],
        hlaunch="Search hotels in {c}", booking_l="Hotels in {c} on Booking.com, cheapest first", google_l="Compare prices on Google Hotels",
        airbnb_l="Apartments in {c} on Airbnb", other_cities="Other cities", hotels_short="Hotels in {c}",
        hfaq=[("Which area should I stay in, in {c}?", "{areas}."),
              ("How do I find a cheap hotel in {c}?", "Compare several sites for the same dates, sort by price, choose free cancellation and book early for holiday periods. Apartments are often good value from 3 nights."),
              ("Should I book with free cancellation?", "Yes, especially if your flights are not booked yet: you can switch to a better deal if the price drops.")],
        conj=" and ", lang_label="Language", disclaimer="Escale does not sell tickets or set any prices. Times and information are indicative: airline schedules change, always check on the booking site.",
        home="Compare flights, hotels and cars", legal="Legal notice (FR)", privacy="Privacy (FR)", cookies="Cookie settings",
        area_names={"Centre-ville": "City centre", "Quartier administratif": "Administrative district"}),
    "es": dict(
        flight_slug="vuelos", hotel_slug="hoteles-baratos", app_lang="es", arrow="→",
        title_route="Vuelos baratos {a} – {b}: compara precios",
        desc_route="Vuelo barato {a} – {b} ({fa} → {ta}): duración, mejor época para reservar y precios comparados en Skyscanner, Kayak y momondo.",
        h1_route="Vuelos baratos {a} <span>→</span> {b}", cta="Comparar precios ahora", back="Vuelta {b} → {a}",
        duration="Duración", arrival="Llegada", peak="Precios más altos",
        dur_direct="Unas {d} en vuelo directo", dur_var="Variable: la mayoría de los trayectos tiene al menos una escala",
        prices_h="Precios encontrados recientemente", prices_p="Precios de ida y vuelta más bajos encontrados por viajeros en los últimos días, por mes de salida. La tarifa exacta disponible aparece en los sitios de reserva.",
        tip_h="Nuestro consejo para esta ruta", cheap_h="Cómo pagar menos",
        steps=["<strong>Activa las fechas flexibles.</strong> Mover la salida uno o dos días suele cambiar el precio más que el sitio elegido.",
               "<strong>Compara al menos tres sitios.</strong> Escale abre tu búsqueda, ya ordenada por precio, en Skyscanner, Kayak, momondo y Aviasales.",
               "<strong>Revisa el equipaje.</strong> Suma el precio de la maleta antes de comparar dos tarifas.",
               "<strong>Crea una alerta de precio</strong> en Kayak o Skyscanner si viajas dentro de varios meses."],
        launch="Buscar {a} → {b}", direct_h="Acceso directo a los comparadores",
        sky="Precios del mes en Skyscanner", hotels_in="Hoteles en {b}", cars_in="Alquiler de coches en {b}",
        faq_h="Preguntas frecuentes", other_routes="Otras rutas",
        faq=[("¿Cuánto dura un vuelo {a} – {b}?", "{dur_long}. Con escala, el viaje total suele durar varias horas más según la conexión."),
             ("¿Cuándo reservar un vuelo barato {a} – {b}?", "En general, dos o tres meses antes de la salida. Los precios suben mucho durante {peak}: reserva antes para esas fechas."),
             ("¿A qué aeropuerto de {b} se llega?", "Los vuelos llegan a {airport} ({ta})."),
             ("¿El equipaje está incluido?", "No siempre. Las tarifas más baratas a veces solo incluyen un bolso pequeño. Revisa el equipaje facturado antes de pagar.")],
        dur_long_direct="Unas {d} en vuelo directo", dur_long_var="Depende: la mayoría de los trayectos tiene al menos una escala",
        title_hotel="Hoteles baratos en {c}: compara precios",
        desc_hotel="Hotel barato en {c} ({country}): dónde alojarse, consejos para pagar menos y precios comparados en Booking, Agoda y Airbnb.",
        h1_hotel="Hoteles baratos en <span>{c}</span>", hotel_codes="hoteles y apartamentos", hotel_cta="Comparar precios de hoteles", flights_to="Vuelos a {c}",
        where_h="Dónde alojarse en {c}", our_tip="Nuestro consejo",
        hsteps=["<strong>Compara al menos tres sitios.</strong> El mismo hotel no siempre cuesta lo mismo en Booking, Hotels.com o Agoda.",
                "<strong>Elige cancelación gratuita.</strong> Podrás reservar en otro sitio si el precio baja.",
                "<strong>Mira el precio total.</strong> La tasa turística, el desayuno y la limpieza cambian la clasificación.",
                "<strong>Para 3 noches o más, mira los apartamentos</strong>: suelen ser más baratos para una familia."],
        hlaunch="Buscar hoteles en {c}", booking_l="Hoteles en {c} en Booking.com, del más barato al más caro", google_l="Comparar precios en Google Hoteles",
        airbnb_l="Apartamentos en {c} en Airbnb", other_cities="Otras ciudades", hotels_short="Hoteles en {c}",
        hfaq=[("¿En qué barrio alojarse en {c}?", "{areas}."),
              ("¿Cómo encontrar un hotel barato en {c}?", "Compara varios sitios para las mismas fechas, ordena por precio, elige cancelación gratuita y reserva pronto en temporada alta. Los apartamentos suelen compensar a partir de 3 noches."),
              ("¿Conviene reservar con cancelación gratuita?", "Sí, sobre todo si aún no tienes los vuelos: podrás cambiar a una oferta mejor si el precio baja.")],
        conj=" y ", lang_label="Idioma", disclaimer="Escale no vende billetes ni fija precios. Las duraciones y datos son orientativos: los horarios de las aerolíneas cambian, compruébalo siempre en el sitio de reserva.",
        home="Comparar vuelos, hoteles y coches", legal="Aviso legal (FR)", privacy="Privacidad (FR)", cookies="Gestionar cookies",
        area_names={"Centre-ville": "Centro", "Quartier administratif": "Barrio administrativo"}),
    "pt": dict(
        flight_slug="voos", hotel_slug="hoteis-baratos", app_lang="pt", arrow="→",
        title_route="Voos baratos {a} – {b}: compare preços",
        desc_route="Voo barato {a} – {b} ({fa} → {ta}): duração, melhor época para reservar e preços comparados no Skyscanner, Kayak e momondo.",
        h1_route="Voos baratos {a} <span>→</span> {b}", cta="Comparar preços agora", back="Regresso {b} → {a}",
        duration="Duração", arrival="Chegada", peak="Preços mais altos",
        dur_direct="Cerca de {d} em voo direto", dur_var="Variável: a maioria das viagens tem pelo menos uma escala",
        prices_h="Preços encontrados recentemente", prices_p="Preços de ida e volta mais baixos encontrados por viajantes nos últimos dias, por mês de partida. A tarifa exata disponível aparece nos sites de reserva.",
        tip_h="O nosso conselho para esta rota", cheap_h="Como pagar menos",
        steps=["<strong>Ative as datas flexíveis.</strong> Mudar a partida um ou dois dias costuma alterar o preço mais do que o site escolhido.",
               "<strong>Compare pelo menos três sites.</strong> A Escale abre a sua pesquisa, já ordenada por preço, no Skyscanner, Kayak, momondo e Aviasales.",
               "<strong>Verifique a bagagem.</strong> Some o preço da mala antes de comparar duas tarifas.",
               "<strong>Crie um alerta de preço</strong> no Kayak ou Skyscanner se viajar daqui a alguns meses."],
        launch="Pesquisar {a} → {b}", direct_h="Acesso direto aos comparadores",
        sky="Preços do mês no Skyscanner", hotels_in="Hotéis em {b}", cars_in="Aluguer de carros em {b}",
        faq_h="Perguntas frequentes", other_routes="Outras rotas",
        faq=[("Quanto tempo dura um voo {a} – {b}?", "{dur_long}. Com escala, a viagem total costuma demorar várias horas a mais, conforme a ligação."),
             ("Quando reservar um voo barato {a} – {b}?", "Em geral, dois a três meses antes da partida. Os preços sobem muito durante {peak}: reserve mais cedo nessas alturas."),
             ("Em que aeroporto de {b} se chega?", "Os voos chegam a {airport} ({ta})."),
             ("A bagagem está incluída?", "Nem sempre. As tarifas mais baratas às vezes incluem só uma mala pequena. Verifique a bagagem de porão antes de pagar.")],
        dur_long_direct="Cerca de {d} em voo direto", dur_long_var="Depende: a maioria das viagens tem pelo menos uma escala",
        title_hotel="Hotéis baratos em {c}: compare preços",
        desc_hotel="Hotel barato em {c} ({country}): onde ficar, dicas para pagar menos e preços comparados no Booking, Agoda e Airbnb.",
        h1_hotel="Hotéis baratos em <span>{c}</span>", hotel_codes="hotéis e apartamentos", hotel_cta="Comparar preços de hotéis", flights_to="Voos para {c}",
        where_h="Onde ficar em {c}", our_tip="O nosso conselho",
        hsteps=["<strong>Compare pelo menos três sites.</strong> O mesmo hotel nem sempre tem o mesmo preço no Booking, Hotels.com ou Agoda.",
                "<strong>Escolha cancelamento gratuito.</strong> Pode reservar noutro lado se o preço baixar.",
                "<strong>Veja o preço total.</strong> Taxa turística, pequeno-almoço e limpeza mudam a classificação.",
                "<strong>Para 3 noites ou mais, veja apartamentos</strong>: muitas vezes mais baratos para uma família."],
        hlaunch="Pesquisar hotéis em {c}", booking_l="Hotéis em {c} no Booking.com, do mais barato ao mais caro", google_l="Comparar preços no Google Hotéis",
        airbnb_l="Apartamentos em {c} no Airbnb", other_cities="Outras cidades", hotels_short="Hotéis em {c}",
        hfaq=[("Em que bairro ficar em {c}?", "{areas}."),
              ("Como encontrar um hotel barato em {c}?", "Compare vários sites para as mesmas datas, ordene por preço, escolha cancelamento gratuito e reserve cedo nas épocas festivas. Os apartamentos costumam compensar a partir de 3 noites."),
              ("Devo reservar com cancelamento gratuito?", "Sim, sobretudo se ainda não tiver os voos: pode mudar para uma oferta melhor se o preço baixar.")],
        conj=" e ", lang_label="Idioma", disclaimer="A Escale não vende bilhetes nem fixa preços. As durações e informações são indicativas: os horários das companhias mudam, confirme sempre no site de reserva.",
        home="Comparar voos, hotéis e carros", legal="Aviso legal (FR)", privacy="Privacidade (FR)", cookies="Gerir cookies",
        area_names={"Centre-ville": "Centro", "Quartier administratif": "Bairro administrativo"}),
    "ar": dict(
        flight_slug="flights", hotel_slug="hotels", app_lang="ar", arrow="←",
        title_route="رحلات طيران رخيصة من {a} إلى {b}: قارن الأسعار",
        desc_route="رحلة رخيصة من {a} إلى {b} ({fa} → {ta}): مدة الرحلة، أفضل وقت للحجز ومقارنة الأسعار على Skyscanner وKayak وmomondo.",
        h1_route="رحلات رخيصة {a} <span>←</span> {b}", cta="قارن الأسعار الآن", back="رحلة العودة {b} ← {a}",
        duration="مدة الرحلة", arrival="الوصول", peak="أغلى الفترات",
        dur_direct="حوالي {d} في رحلة مباشرة", dur_var="متغيرة: معظم الرحلات فيها توقف واحد على الأقل",
        prices_h="أسعار وُجدت مؤخرًا", prices_p="أقل أسعار الذهاب والعودة التي وجدها المسافرون في الأيام الأخيرة، حسب شهر المغادرة. السعر النهائي المتاح يظهر على مواقع الحجز.",
        tip_h="نصيحتنا لهذا الخط", cheap_h="كيف تدفع أقل",
        steps=["<strong>فعّل التواريخ المرنة.</strong> تغيير موعد المغادرة يومًا أو يومين يغيّر السعر غالبًا أكثر من اختيار الموقع.",
               "<strong>قارن ثلاثة مواقع على الأقل.</strong> يفتح Escale بحثك مرتّبًا حسب السعر على Skyscanner وKayak وmomondo وAviasales.",
               "<strong>تحقّق من الأمتعة.</strong> أضف ثمن الحقيبة قبل المقارنة بين سعرين.",
               "<strong>فعّل تنبيه الأسعار</strong> على Kayak أو Skyscanner إذا كان سفرك بعد عدة أشهر."],
        launch="ابحث {a} ← {b}", direct_h="روابط مباشرة إلى مواقع المقارنة",
        sky="أسعار الشهر على Skyscanner", hotels_in="فنادق في {b}", cars_in="تأجير سيارات في {b}",
        faq_h="أسئلة شائعة", other_routes="خطوط أخرى",
        faq=[("كم تستغرق الرحلة من {a} إلى {b}؟", "{dur_long}. مع التوقف، تطول الرحلة غالبًا عدة ساعات حسب مدة الانتظار."),
             ("متى أحجز رحلة رخيصة من {a} إلى {b}؟", "عادةً قبل شهرين إلى ثلاثة أشهر من السفر. ترتفع الأسعار كثيرًا خلال: {peak}. احجز مبكرًا لهذه الفترات."),
             ("في أي مطار تصل الرحلات إلى {b}؟", "تصل الرحلات إلى {airport} ({ta})."),
             ("هل الأمتعة مشمولة؟", "ليس دائمًا. أرخص الأسعار تشمل أحيانًا حقيبة صغيرة فقط. تحقّق من وزن الأمتعة المسموح قبل الدفع.")],
        dur_long_direct="حوالي {d} في رحلة مباشرة", dur_long_var="تختلف: معظم الرحلات فيها توقف واحد على الأقل",
        title_hotel="فنادق رخيصة في {c}: قارن الأسعار",
        desc_hotel="فندق رخيص في {c} ({country}): أين تقيم، نصائح لتدفع أقل ومقارنة الأسعار على Booking وAgoda وAirbnb.",
        h1_hotel="فنادق رخيصة في <span>{c}</span>", hotel_codes="فنادق وشقق", hotel_cta="قارن أسعار الفنادق", flights_to="رحلات إلى {c}",
        where_h="أين تقيم في {c}", our_tip="نصيحتنا",
        hsteps=["<strong>قارن ثلاثة مواقع على الأقل.</strong> سعر الفندق نفسه ليس دائمًا واحدًا على Booking وHotels.com وAgoda.",
                "<strong>اختر الإلغاء المجاني.</strong> يمكنك الحجز في مكان آخر إذا انخفض السعر.",
                "<strong>انظر إلى السعر الإجمالي.</strong> ضريبة الإقامة والفطور ورسوم التنظيف تغيّر الترتيب.",
                "<strong>لثلاث ليالٍ أو أكثر، اطّلع على الشقق</strong>: غالبًا أرخص للعائلات."],
        hlaunch="ابحث عن فنادق في {c}", booking_l="فنادق {c} على Booking.com من الأرخص إلى الأغلى", google_l="قارن الأسعار على Google Hotels",
        airbnb_l="شقق في {c} على Airbnb", other_cities="مدن أخرى", hotels_short="فنادق في {c}",
        hfaq=[("في أي حي أقيم في {c}؟", "{areas}."),
              ("كيف أجد فندقًا رخيصًا في {c}؟", "قارن عدة مواقع للتواريخ نفسها، ورتّب حسب السعر، واختر الإلغاء المجاني، واحجز مبكرًا في المواسم. الشقق غالبًا مناسبة ابتداءً من ثلاث ليالٍ."),
              ("هل أحجز مع إلغاء مجاني؟", "نعم، خصوصًا إذا لم تحجز رحلتك بعد: يمكنك الانتقال إلى عرض أفضل إذا انخفض السعر.")],
        conj=" & ", lang_label="اللغة", disclaimer="لا يبيع Escale التذاكر ولا يحدد الأسعار. المدد والمعلومات تقريبية: جداول شركات الطيران تتغير، تحقّق دائمًا على موقع الحجز.",
        home="قارن الرحلات والفنادق والسيارات", legal="الإشعار القانوني (FR)", privacy="الخصوصية (FR)", cookies="إعدادات ملفات تعريف الارتباط",
        area_names={"Centre-ville": "وسط المدينة", "Quartier administratif": "الحي الإداري"}),
}


EST = {
    "en": "About {d} non-stop (estimate based on the {km} km distance)",
    "es": "Unas {d} sin escalas (estimación según la distancia de {km} km)",
    "pt": "Cerca de {d} sem escalas (estimativa pela distância de {km} km)",
    "ar": "حوالي {d} دون توقف (تقدير حسب المسافة {km} كم)",
}


def slugify(t):
    t = t.lower().replace("'", "-")
    for a, b in (("é", "e"), ("è", "e"), ("ê", "e"), ("ë", "e"), ("à", "a"), ("á", "a"), ("â", "a"), ("ã", "a"), ("í", "i"), ("ï", "i"),
                 ("î", "i"), ("ó", "o"), ("ô", "o"), ("õ", "o"), ("ú", "u"), ("û", "u"), ("ü", "u"), ("ç", "c"), ("ñ", "n")):
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def tr(table, key, lang):
    v = table.get(key)
    return v[COL[lang]] if v else key


def city(name, lang):
    return tr(TR.CITIES, name, lang)


def slug_city(name, lang):
    # Les URL arabes utilisent les noms anglais en caractères latins
    return slugify(city(name, "en" if lang == "ar" else lang))


def route_path(r, lang):
    return f"{lang}/{UI[lang]['flight_slug']}-{slug_city(r[2], lang)}-{slug_city(r[3], lang)}"


def hotel_path(h, lang):
    return f"{lang}/{UI[lang]['hotel_slug']}-{slug_city(h[0], lang)}"


def duration(d, lang):
    """« 5 h 30 » -> texte lisible dans la langue."""
    m = re.match(r"(\d+) h(?: (\d+))?", d)
    h, mn = int(m.group(1)), int(m.group(2) or 0)
    if lang != "ar":
        return f"{h} h {mn:02d}" if mn else f"{h} h"
    hh = "ساعة" if h == 1 else "ساعتين" if h == 2 else f"{h} ساعات" if h <= 10 else f"{h} ساعة"
    return hh + (f" و{mn} دقيقة" if mn else "")


def alternates(paths, domain):
    """paths : {"fr": "vol-paris-dakar", "en": "en/flights-paris-dakar", ...}"""
    full = lambda p: f"{domain}/{p}/" if p else f"{domain}/"
    out = [f'<link rel="alternate" hreflang="{l}" href="{full(p)}">' for l, p in paths.items()]
    out.append(f'<link rel="alternate" hreflang="x-default" href="{full(paths["fr"])}">')
    return "\n".join(out)


def switcher(paths, current):
    cur = ' aria-current="page"'
    items = "".join(
        f'<a href="/{p + "/" if p else ""}" hreflang="{l}" lang="{l}" title="{NAMES[l]}"{cur if l == current else ""}>{l.upper()}</a>'
        for l, p in paths.items())
    return f'<nav class="lang-nav" aria-label="Langue / Language">{items}</nav>'


# Menu du haut, identique sur toutes les pages (Vols · Hôtels · Voitures · Bons plans · Partout · Guides · Favoris)
SECTION_PATHS = {
    "deals": {"fr": "bons-plans", "en": "en/deals", "es": "es/ofertas", "pt": "pt/promocoes", "ar": "ar/deals"},
    "fetes": {"fr": "vols-fetes", "en": "en/holiday-flights", "es": "es/vuelos-fiestas", "pt": "pt/voos-festas", "ar": "ar/holiday-flights"},
    "anywhere": {"fr": "partout", "en": "en/anywhere", "es": "es/explorar", "pt": "pt/explorar", "ar": "ar/anywhere"},
    "guides": {"fr": "guides", "en": "en/guides", "es": "es/guias", "pt": "pt/guias", "ar": "ar/guides"},
    "favs": {"fr": "favoris", "en": "en/favorites", "es": "es/favoritos", "pt": "pt/favoritos", "ar": "ar/favorites"},
}
FETES_LABEL = {"fr": "Fêtes", "en": "Holidays", "es": "Fiestas", "pt": "Festas", "ar": "الأعياد"}
NAV_LABELS = {
    "fr": ("Vols", "Hôtels", "Voitures", "Bons plans", "Partout", "Guides", "Favoris", "Menu principal", "Escale, accueil"),
    "en": ("Flights", "Hotels", "Cars", "Deals", "Anywhere", "Guides", "Favorites", "Main menu", "Escale, home"),
    "es": ("Vuelos", "Hoteles", "Coches", "Ofertas", "Explorar", "Guías", "Favoritos", "Menú principal", "Escale, inicio"),
    "pt": ("Voos", "Hotéis", "Carros", "Promoções", "Explorar", "Guias", "Favoritos", "Menu principal", "Escale, início"),
    "ar": ("رحلات", "فنادق", "سيارات", "العروض", "استكشف", "أدلة", "المفضلة", "القائمة الرئيسية", "Escale، الرئيسية"),
}
STAR = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 3 2.7 5.6 6.1.8-4.5 4.2 1.1 6.1L12 16.8 6.6 19.7l1.1-6.1L3.2 9.4l6.1-.8z" fill="currentColor"/></svg>'
PLANE = '<svg class="brand-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z" fill="currentColor"/></svg>'


HUB_LINK = {'en': 'All flights to {b}', 'es': 'Todos los vuelos a {b}', 'pt': 'Todos os voos para {b}', 'ar': 'كل الرحلات إلى {b}'}
FAV_LABEL = {"fr": "Ajouter aux favoris", "en": "Add to favorites", "es": "Añadir a favoritos", "pt": "Adicionar aos favoritos", "ar": "أضف إلى المفضلة"}


def fav_btn(lang, path, title, sub, kind):
    """Étoile « favori » (favs.js garde la page dans ce navigateur)."""
    star = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 3 2.7 5.6 6.1.8-4.5 4.2 1.1 6.1L12 16.8 6.6 19.7l1.1-6.1L3.2 9.4l6.1-.8z"/></svg>'
    return (f'<button type="button" class="btn ghost fav-btn" data-fav="/{E(path)}/" data-fav-title="{E(title)}" data-fav-sub="{E(sub)}" '
            f'data-fav-kind="{kind}" aria-pressed="false">{star}<span>{E(FAV_LABEL[lang])}</span></button>')


def site_header(lang, path, switch):
    """En-tête commun : logo, menu principal (la rubrique en cours est signalée) et choix de la langue."""
    n = NAV_LABELS[lang]
    q = "" if lang == "fr" else "?lang=" + {"fr": "fr", "en": "en", "es": "es", "pt": "pt", "ar": "ar"}[lang]
    cur = lambda key: ' aria-current="page"' if path and (path == SECTION_PATHS[key][lang] or path.startswith(SECTION_PATHS[key][lang] + "/")) else ""
    sec = lambda key: "/" + SECTION_PATHS[key][lang] + "/"
    links = (f'<a href="/{q}">{n[0]}</a><a href="/{q}#hotels">{n[1]}</a><a href="/{q}#voitures">{n[2]}</a>'
             f'<a href="{sec("deals")}"{cur("deals")}>{E(n[3])}</a><a href="{sec("fetes")}"{cur("fetes")}>{E(FETES_LABEL[lang])}</a>'
             f'<a href="{sec("anywhere")}"{cur("anywhere")}>{E(n[4])}</a>'
             f'<a href="{sec("guides")}"{cur("guides")}>{E(n[5])}</a>'
             f'<a class="nav-fav" href="{sec("favs")}"{cur("favs")}>{STAR}<span>{E(n[6])}</span><b class="fav-count" data-fav-count hidden></b></a>')
    return (f'<header class="site-head"><div class="wrap head-row">'
            f'<a class="brand" href="/{q}" aria-label="{E(n[8])}">{PLANE}<span>escale</span></a>'
            f'<nav class="main-nav" aria-label="{E(n[7])}">{links}</nav>{switch}</div></header>')


HEAD = """<!doctype html>
<html lang="{lang}" dir="{dir}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{tp}
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
{alts}
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" href="/icon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
<meta property="og:type" content="article">
<meta property="og:locale" content="{oglocale}">
<meta property="og:site_name" content="Escale">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{domain}/{ogimg}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="/fonts/instrument-sans-latin-f587e7.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/fonts/fonts.css">{arpreload}
<link rel="stylesheet" href="/pages.css">
{ld}
</head>
<body>
{header}
<main>
<div class="board"><div class="wrap">
  {hero}
</div></div>
<div class="wrap">
{body}
</div>
</main>
<footer class="wrap">
  <nav class="foot-nav"><a href="/{homeq}">{home}</a><a href="/mentions-legales/">{legal}</a><a href="/confidentialite/">{privacy}</a><a href="/contact/">Contact</a><a href="/{aboutp}/">{aboutl}</a><a href="/{guidesp}/">Guides</a><a href="/{fetesp}/">{fetesl}</a><a href="/{dealsp}/">{dealsl}</a><a href="#cookies" data-open-consent>{cookies}</a></nav>
  <p>{disclaimer}</p>
</footer>
<script src="/favs.js" defer></script>
</body>
</html>
"""


HOME_NAME = {"fr": "Accueil", "en": "Home", "es": "Inicio", "pt": "Início", "ar": "الرئيسية"}
GUIDES_DIR = {"fr": "guides", "en": "en/guides", "es": "es/guias", "pt": "pt/guias", "ar": "ar/guides"}


def breadcrumb_ld(domain, path, lang, hero):
    """Fil d'Ariane (BreadcrumbList) : Google l'affiche à la place de l'adresse dans les résultats."""
    m = re.search(r"<h1[^>]*>(.*?)</h1>", hero, re.S)
    name = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", m.group(1)))).strip() if m else ""
    if not name or not path:
        return ""
    home = f"{domain}/" if lang == "fr" else f"{domain}/{lang}/"
    items = [(HOME_NAME[lang], home)]
    g = GUIDES_DIR[lang]
    if path.startswith(g + "/"):
        items.append(("Guides", f"{domain}/{g}/"))
    items.append((name, f"{domain}/{path}/"))
    return '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]
    }, ensure_ascii=False) + "</script>"


def faq_ld(faq):
    return '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]
    }, ensure_ascii=False) + "</script>"


def fit(title, desc):
    """Garde titre et description dans ce que Google affiche (~65 et ~160 caractères), pour toutes les pages."""
    if len(title) > 65 and title.endswith(" | Escale"):
        title = title[: -len(" | Escale")]
    if len(desc) > 160:
        cut = desc[:158]
        cut = cut[: cut.rfind(" ")] if " " in cut else cut
        desc = cut.rstrip(" ,;:–-") + "…"
    return title, desc


def write(site, path, lang, title, desc, hero, body, ld, paths, ctx, og="og-image.png"):
    u = UI[lang]
    title, desc = fit(title, desc)
    ld = (ld + "\n" + breadcrumb_ld(ctx["domain"], path, lang, hero)).strip()
    out = HEAD.format(
        lang=lang, dir="rtl" if lang == "ar" else "ltr", tp=ctx["tp"], title=E(title), desc=E(desc),
        url=f"{ctx['domain']}/{path}/", alts=alternates(paths, ctx["domain"]), oglocale=LOCALE[lang], domain=ctx["domain"],
        ogimg=og, arpreload=('\n<link rel="preload" href="/fonts/noto-sans-arabic-arabic-378a89.woff2" as="font" type="font/woff2" crossorigin>' if lang == "ar" else ""), ld=ld, homeq="" if lang == "fr" else "?lang=" + u["app_lang"],
        dealsp={"fr": "bons-plans", "en": "en/deals", "es": "es/ofertas", "pt": "pt/promocoes", "ar": "ar/deals"}[lang],
        dealsl={"fr": "Bons plans", "en": "Deals", "es": "Ofertas", "pt": "Promoções", "ar": "العروض"}[lang],
        aboutp={"fr": "a-propos", "en": "en/about", "es": "es/acerca-de", "pt": "pt/sobre", "ar": "ar/about"}[lang],
        aboutl={"fr": "À propos", "en": "About", "es": "Acerca de", "pt": "Sobre", "ar": "عن Escale"}[lang],
        fetesp={"fr": "vols-fetes", "en": "en/holiday-flights", "es": "es/vuelos-fiestas", "pt": "pt/voos-festas", "ar": "ar/holiday-flights"}[lang],
        fetesl={"fr": "Vols pour les fêtes", "en": "Holiday flights", "es": "Vuelos para las fiestas", "pt": "Voos para as festas", "ar": "رحلات الأعياد"}[lang],
        guidesp={"fr": "guides", "en": "en/guides", "es": "es/guias", "pt": "pt/guias", "ar": "ar/guides"}[lang],
        header=site_header(lang, path, switcher(paths, lang)), hero=hero, body=body, home=E(u["home"]), legal=E(u["legal"]), privacy=E(u["privacy"]),
        cookies=E(u["cookies"]), disclaimer=E(u["disclaimer"]))
    d = site / path
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(out, encoding="utf-8")
    return f"{ctx['domain']}/{path}/"


def build(site, ctx):
    """ctx : domain, tp (script Travelpayouts), routes, hotels, route_slug, hotel_slug, airports, related"""
    routes, hotels = ctx["routes"], ctx["hotels"]
    route_paths = {r: {"fr": ctx["route_slug"](r), **{l: route_path(r, l) for l in LANGS}} for r in routes}
    hotel_paths = {h[0]: {"fr": ctx["hotel_slug"](h), **{l: hotel_path(h, l) for l in LANGS}} for h in hotels}
    urls = []
    for lang in LANGS:
        u = UI[lang]
        for r in routes:
            fr_, to, cf, ct, country, _airport, dur, peak, _note = r
            a, b = city(cf, lang), city(ct, lang)
            ap = ctx["airports"].get(to)
            airport = ap[2] if ap else to
            km = ctx.get("distances", {}).get((fr_, to))
            if dur and dur.startswith("~"):
                kms = f"{km:,}".replace(",", " " if lang != "en" else ",")
                dur_txt = EST[lang].format(d=duration(dur[1:], lang), km=kms)
                dur_long = dur_txt
            else:
                dur_txt = u["dur_direct"].format(d=duration(dur, lang)) if dur else u["dur_var"]
                dur_long = u["dur_long_direct"].format(d=duration(dur, lang)) if dur else u["dur_long_var"]
            peak_t = tr(TR.PEAKS, peak, lang)
            note = TR.NOTES[f"{fr_}-{to}"][COL[lang]]
            app = "/?" + urllib.parse.urlencode({"type": "vols", "from": fr_, "to": to, "lang": u["app_lang"]})
            backl = "/?" + urllib.parse.urlencode({"type": "vols", "from": to, "to": fr_, "lang": u["app_lang"]})
            hp = next((h for h in hotels if h[0] == ct), None)
            hotels_l = f"/{hotel_paths[hp[0]][lang]}/" if hp else "/?" + urllib.parse.urlencode({"type": "hotels", "dest": b, "lang": u["app_lang"]})
            cars_l = "/?" + urllib.parse.urlencode({"type": "voitures", "pick": to, "lang": u["app_lang"]})
            sky = f"https://www.skyscanner.net/transport/flights/{fr_.lower()}/{to.lower()}/"
            f = dict(a=a, b=b, fa=fr_, ta=to, peak=peak_t, airport=airport, dur_long=dur_long)
            faq = [(q.format(**f), ans.format(**f)) for q, ans in u["faq"]]
            ten = TEN.ROUTES.get((fr_, to)) if lang == "en" else None  # contenu unique en anglais (grands trajets)
            if ten:
                faq = ten["faq"] + faq
            hero = f"""<p class="eyebrow">{E(tr(TR.COUNTRIES, country, lang))}</p>
  <h1>{u["h1_route"].format(a=E(a), b=E(b))}</h1>
  <p class="codes" dir="ltr">{fr_} → {to}</p>
  <p class="hero-price" id="hero-price" hidden></p>
  <div class="cta-row"><a class="btn" href="{E(app)}">{E(u["cta"])}</a><a class="btn ghost" href="{E(backl)}">{E(u["back"].format(a=a, b=b))}</a>{fav_btn(lang, route_paths[r][lang], f"{a} → {b}", f"{fr_} → {to}", "route")}</div>"""
            others = "".join(f'<li><a href="/{route_paths[o][lang]}/">{E(city(o[2], lang))} {u["arrow"]} {E(city(o[3], lang))}</a></li>'
                             for o in ctx["related"](r))
            body = f"""<dl class="facts">
  <div><dt>{E(u["duration"])}</dt><dd>{E(dur_txt)}</dd></div>
  <div><dt>{E(u["arrival"])}</dt><dd>{E(airport)} ({to})</dd></div>
  <div><dt>{E(u["peak"])}</dt><dd>{E(peak_t[0].upper() + peak_t[1:])}</dd></div>
</dl>
<section id="route-prices" data-from="{fr_}" data-to="{to}" hidden><h2>{E(u["prices_h"])}</h2>
<p class="small">{E(u["prices_p"])}</p>
<ul class="price-list"></ul></section>
<script src="/route-prices.js" defer></script>
{calendar_html(lang, fr_, to)}
{extras_html(site, lang, b, city(ct, "en"), to)}
{TEN.route_html(ten, a, b, {p["key"]: p for p in partners(site)}) if ten else ""}<section><h2>{E(u["tip_h"])}</h2><p>{E(note)}</p></section>
<section><h2>{E(u["cheap_h"])}</h2>
<ol class="steps">{"".join(f"<li>{s}</li>" for s in u["steps"])}</ol>
<p><a class="btn" href="{E(app)}">{E(u["launch"].format(a=a, b=b))}</a></p>
</section>
<section><h2>{E(u["direct_h"])}</h2>
<ul class="links">
  <li><a href="{E(sky)}" target="_blank" rel="noopener noreferrer">{E(u["sky"])}</a></li>
  <li><a href="{E(hotels_l)}">{E(u["hotels_in"].format(b=b))}</a></li>
  <li><a href="{E(cars_l)}">{E(u["cars_in"].format(b=b))}</a></li>{f'<li><a href="/{ctx["hubs"][ct][lang]}/">{E(HUB_LINK[lang].format(b=b))}</a></li>' if ct in ctx.get("hubs", {}) else ''}
</ul></section>
<section class="faq"><h2>{E(u["faq_h"])}</h2>
{"".join(f"<details><summary>{E(q)}</summary><p>{E(ans)}</p></details>" for q, ans in faq)}
</section>
<section><h2>{E(u["other_routes"])}</h2><ul class="route-links">{others}</ul></section>"""
            urls.append(write(site, route_paths[r][lang], lang, u["title_route"].format(a=a, b=b),
                              u["desc_route"].format(a=a, b=b, fa=fr_, ta=to), hero, body, faq_ld(faq), route_paths[r], ctx,
                              f"og/{fr_}-{to}.jpg" if (site / "og" / f"{fr_}-{to}.jpg").exists() else "og-image.png"))

        for h in hotels:
            cname, country, areas, _tip, code = h
            c = city(cname, lang)
            cn = tr(TR.COUNTRIES, country, lang)
            app = "/?" + urllib.parse.urlencode({"type": "hotels", "dest": city(cname, "en"), "lang": u["app_lang"]})
            booking = "https://www.booking.com/searchresults.html?" + urllib.parse.urlencode({"ss": city(cname, "en"), "order": "price"})
            google = "https://www.google.com/travel/search?" + urllib.parse.urlencode({"q": f"hotels {city(cname, 'en')}", "hl": lang, "curr": "EUR"})
            airbnb = f"https://www.airbnb.com/s/{urllib.parse.quote(city(cname, 'en'))}/homes"
            cars_l = "/?" + urllib.parse.urlencode({"type": "voitures", "pick": code, "lang": u["app_lang"]})
            flights = [r for r in routes if r[3] == cname]
            aname = lambda n: u["area_names"].get(n, n.replace(" et ", u["conj"]))
            area_items = [(aname(n), tr(TR.AREAS, d, lang)) for n, d in areas]
            faq = [(q.format(c=c), ans.format(c=c, areas=" ; ".join(f"{n}: {d}" for n, d in area_items))) for q, ans in u["hfaq"]]
            hen = TEN.HOTELS.get(cname) if lang == "en" else None
            if hen:
                faq = hen["faq"] + faq
            hero = f"""<p class="eyebrow">{E(cn)}</p>
  <h1>{u["h1_hotel"].format(c=E(c))}</h1>
  <p class="codes"><span dir="ltr">{code}</span> · {E(u["hotel_codes"])}</p>
  <div class="cta-row"><a class="btn" href="{E(app)}">{E(u["hotel_cta"])}</a>{f'<a class="btn ghost" href="/{route_paths[flights[0]][lang]}/">{E(u["flights_to"].format(c=c))}</a>' if flights else ''}{fav_btn(lang, hotel_paths[h[0]][lang], u["h1_hotel"].format(c=c), cn, "hotel")}</div>"""
            areas_html = "".join(f"<div><dt>{E(n)}</dt><dd>{E(d[0].upper() + d[1:])}</dd></div>" for n, d in area_items)
            fl_html = ""
            if flights:
                fl_html = f'<section><h2>{E(u["flights_to"].format(c=c))}</h2><ul class="route-links">' + "".join(
                    f'<li><a href="/{route_paths[r][lang]}/">{E(city(r[2], lang))} {u["arrow"]} {E(city(r[3], lang))}</a></li>' for r in flights) + "</ul></section>"
            body = f"""<section><h2>{E(u["where_h"].format(c=c))}</h2><dl class="facts">{areas_html}</dl></section>{TEN.hotel_html(hen, c, {p["key"]: p for p in partners(site)}) if hen else ""}
<section><h2>{E(u["our_tip"])}</h2><p>{E(TR.HOTEL_TIPS[cname][COL[lang]])}</p></section>
<section><h2>{E(u["cheap_h"])}</h2>
<ol class="steps">{"".join(f"<li>{s}</li>" for s in u["hsteps"])}</ol>
<p><a class="btn" href="{E(app)}">{E(u["hlaunch"].format(c=c))}</a></p>
</section>
<section><h2>{E(u["direct_h"])}</h2>
<ul class="links">
  <li><a href="{E(stay22(f"{city(cname, 'en')}, {tr(TR.COUNTRIES, country, 'en')}", "page-hotels-" + lang))}" target="_blank" rel="sponsored noopener noreferrer"><strong>{E(STAY22_L[lang].format(c=c))}</strong></a></li>
  <li><a href="{E(booking)}" target="_blank" rel="noopener noreferrer">{E(u["booking_l"].format(c=c))}</a></li>
  <li><a href="{E(google)}" target="_blank" rel="noopener noreferrer">{E(u["google_l"])}</a></li>
  <li><a href="{E(airbnb)}" target="_blank" rel="noopener noreferrer">{E(u["airbnb_l"].format(c=c))}</a></li>
  <li><a href="{E(cars_l)}">{E(u["cars_in"].format(b=c))}</a></li>
</ul></section>
{fl_html}
{extras_html(site, lang, c, city(cname, "en"), code)}
<section class="faq"><h2>{E(u["faq_h"])}</h2>
{"".join(f"<details><summary>{E(q)}</summary><p>{E(ans)}</p></details>" for q, ans in faq)}
</section>
<section><h2>{E(u["other_cities"])}</h2><ul class="route-links">{"".join(f'<li><a href="/{hotel_paths[o[0]][lang]}/">{E(u["hotels_short"].format(c=city(o[0], lang)))}</a></li>' for o in hotels if o is not h)}</ul></section>"""
            urls.append(write(site, hotel_paths[h[0]][lang], lang, u["title_hotel"].format(c=c),
                              u["desc_hotel"].format(c=c, country=cn), hero, body, faq_ld(faq), hotel_paths[h[0]], ctx))
    return urls, route_paths, hotel_paths


INDEX = {
    "en": ("Cheap flights to Africa, the Maghreb and worldwide", "Route guides with flight times, airlines, the best time to book and where to stay, plus real fares found recently.", "Flights from {c}", "Cheap hotels"),
    "es": ("Guías de vuelos y hoteles", "Duración, aeropuertos, mejor época para reservar y dónde alojarse: nuestros consejos ruta por ruta.", "Vuelos desde {c}", "Hoteles baratos"),
    "pt": ("Guias de voos e hotéis", "Duração, aeroportos, melhor época para reservar e onde ficar: as nossas dicas rota a rota.", "Voos a partir de {c}", "Hotéis baratos"),
    "ar": ("أدلة الرحلات والفنادق", "مدة الرحلة والمطارات وأفضل وقت للحجز وأين تقيم: نصائحنا خطًا بخط.", "رحلات من {c}", "فنادق رخيصة"),
}


def build_indexes(site, ctx, route_paths, hotel_paths):
    urls = []
    paths = {"fr": "", **{l: l for l in LANGS}}
    for lang in LANGS:
        u, (title, lead, from_t, hotels_t) = UI[lang], INDEX[lang]
        groups = {}
        for r in ctx["routes"]:
            groups.setdefault(r[2], []).append(r)
        body = "".join(
            f'<section><h2>{E(from_t.format(c=city(o, lang)))}</h2><ul class="route-links">' + "".join(
                f'<li><a href="/{route_paths[r][lang]}/">{E(city(r[2], lang))} {u["arrow"]} {E(city(r[3], lang))}</a></li>' for r in rs) + "</ul></section>"
            for o, rs in groups.items())
        body += f'<section><h2>{E(hotels_t)}</h2><ul class="route-links">' + "".join(
            f'<li><a href="/{hotel_paths[h[0]][lang]}/">{E(u["hotels_short"].format(c=city(h[0], lang)))}</a></li>' for h in ctx["hotels"]) + "</ul></section>"
        hero = f'<h1>{E(title)}</h1><p class="hero-lead">{E(lead)}</p><div class="cta-row"><a class="btn" href="/?lang={u["app_lang"]}">{E(u["home"])}</a></div>'
        idx_paths = {"fr": "", **{l: l for l in LANGS}}
        out_url = write(site, lang, lang, f"{title} | Escale", lead, hero, body, "", idx_paths, ctx)
        urls.append(out_url)
    return urls


# ---------------------------------------------------------------------------
# Calendrier des prix, « Avant de partir » et page des bons plans (5 langues)
# ---------------------------------------------------------------------------
ALL = ["fr"] + LANGS
_PARTNERS = None


def partners(site):
    global _PARTNERS
    if _PARTNERS is None:
        _PARTNERS = json.loads((site / "data" / "partners.json").read_text(encoding="utf-8"))["services"]
    return _PARTNERS


BLOCKS = {
    "fr": dict(cal_h="Calendrier des prix", cal_p="Prix aller-retour le plus bas trouvé pour chaque jour de départ. Cliquez sur un jour pour lancer la recherche.",
               go_h="Avant de partir", go_p="Les services utiles pour votre voyage à {c}.", go_btn="Voir l’offre"),
    "en": dict(cal_h="Price calendar", cal_p="Lowest round-trip price found for each departure day. Click a day to start the search.",
               go_h="Before you go", go_p="Useful services for your trip to {c}.", go_btn="See offer"),
    "es": dict(cal_h="Calendario de precios", cal_p="Precio de ida y vuelta más bajo encontrado para cada día de salida. Haz clic en un día para buscar.",
               go_h="Antes de salir", go_p="Servicios útiles para tu viaje a {c}.", go_btn="Ver oferta"),
    "pt": dict(cal_h="Calendário de preços", cal_p="Preço de ida e volta mais baixo encontrado para cada dia de partida. Clique num dia para pesquisar.",
               go_h="Antes de partir", go_p="Serviços úteis para a sua viagem a {c}.", go_btn="Ver oferta"),
    "ar": dict(cal_h="تقويم الأسعار", cal_p="أقل سعر ذهاب وعودة وُجد لكل يوم مغادرة. انقر على يوم لبدء البحث.",
               go_h="قبل السفر", go_p="خدمات مفيدة لرحلتك إلى {c}.", go_btn="اعرض العرض"),
}


def calendar_html(lang, fr_, to):
    b = BLOCKS[lang]
    return (f'<section id="route-calendar" data-from="{fr_}" data-to="{to}" hidden><h2>{E(b["cal_h"])}</h2>'
            f'<p class="small">{E(b["cal_p"])}</p><div class="chips cal-months" role="group"></div>'
            f'<div class="cal-grid" dir="ltr"></div><p class="small cal-legend"></p></section>\n'
            f'<script src="/route-calendar.js" defer></script>\n'
            f'<section id="price-alert" class="price-alert" data-from="{fr_}" data-to="{to}" hidden></section>\n'
            f'<script src="/alerts.js" defer></script>')


STAY22_L = {"fr": "Hôtels à {c} au meilleur prix (Booking, Expedia, Agoda…)", "en": "Hotels in {c} at the best price (Booking, Expedia, Agoda…)",
            "es": "Hoteles en {c} al mejor precio (Booking, Expedia, Agoda…)", "pt": "Hotéis em {c} ao melhor preço (Booking, Expedia, Agoda…)",
            "ar": "فنادق {c} بأفضل سعر (بوكينغ، إكسبيديا، أغودا…)"}


def stay22(address, campaign):
    """Lien Stay22 « roam » (partenaire rémunéré) : envoie vers le site d'hôtels le moins cher pour cette destination."""
    return "https://www.stay22.com/allez/roam?" + urllib.parse.urlencode({"aid": "escalelive", "address": address, "campaign": campaign})


def extras_html(site, lang, city_label, city_en, code):
    b = BLOCKS[lang]
    cards = []
    for p in partners(site):
        if "{city}" in p["url"] and not city_en:
            continue  # lien qui a besoin de la ville (hôtels) : rien à proposer sans destination
        url = p["url"].replace("{city}", urllib.parse.quote(city_en)).replace("{code}", code)
        cards.append(f'<li class="extra"><span class="logo" style="background:{p["color"]}" aria-hidden="true">{E(p["name"][0])}</span>'
                     f'<div><strong>{E(p["title"][lang])}</strong><span>{E(p["desc"][lang])}</span></div>'
                     f'<a class="price-go" href="{E(url)}" target="_blank" rel="sponsored noopener noreferrer">{E(b["go_btn"])} · {E(p["name"])}</a></li>')
    return (f'<section class="extras"><h2>{E(b["go_h"])}</h2><p class="small">{E(b["go_p"].format(c=city_label))}</p>'
            f'<ul class="extra-list">{"".join(cards)}</ul></section>')


UI["fr"] = dict(app_lang="fr", home="Comparer vols, hôtels et voitures", legal="Mentions légales", privacy="Confidentialité",
                cookies="Gérer les cookies",
                disclaimer="Escale ne vend pas de billets et ne fixe aucun prix. Les prix affichés sont des prix réels trouvés récemment : le tarif exact s’affiche sur le site de réservation.")

DEALS = {
    "fr": dict(path="bons-plans", title="Bons plans vols de la semaine", h1="Bons plans <span>de la semaine</span>",
               desc="Les vols aller-retour les moins chers trouvés cette semaine au départ de Paris, Bruxelles, Lyon, Marseille, Genève, Londres, New York et Montréal.",
               lead="Les destinations les moins chères trouvées par des voyageurs ces derniers jours, au départ de grandes villes. Mis à jour automatiquement toutes les 6 heures."),
    "en": dict(path="en/deals", title="This week's flight deals", h1="Flight deals <span>this week</span>",
               desc="The cheapest round-trip flights found this week from Paris, Brussels, Lyon, Marseille, Geneva, London, New York and Montreal.",
               lead="The cheapest destinations found by travellers in the last few days, from major cities. Updated automatically every 6 hours."),
    "es": dict(path="es/ofertas", title="Ofertas de vuelos de la semana", h1="Ofertas de vuelos <span>de la semana</span>",
               desc="Los vuelos de ida y vuelta más baratos encontrados esta semana desde París, Bruselas, Lyon, Marsella, Ginebra, Londres, Nueva York y Montreal.",
               lead="Los destinos más baratos encontrados por viajeros en los últimos días, desde grandes ciudades. Se actualiza automáticamente cada 6 horas."),
    "pt": dict(path="pt/promocoes", title="Promoções de voos da semana", h1="Promoções de voos <span>da semana</span>",
               desc="Os voos de ida e volta mais baratos encontrados esta semana a partir de Paris, Bruxelas, Lyon, Marselha, Genebra, Londres, Nova Iorque e Montreal.",
               lead="Os destinos mais baratos encontrados por viajantes nos últimos dias, a partir de grandes cidades. Atualizado automaticamente a cada 6 horas."),
    "ar": dict(path="ar/deals", title="عروض الطيران لهذا الأسبوع", h1="عروض الطيران <span>لهذا الأسبوع</span>",
               desc="أرخص رحلات الذهاب والعودة التي وُجدت هذا الأسبوع من باريس وبروكسل وليون ومرسيليا وجنيف ولندن ونيويورك ومونتريال.",
               lead="أرخص الوجهات التي وجدها المسافرون في الأيام الأخيرة من مدن كبرى. يُحدَّث تلقائيًا كل 6 ساعات."),
}


NEWSLETTER = json.loads((__import__("pathlib").Path(__file__).parent / "newsletter_forms.json").read_text(encoding="utf-8"))


def build_deals(site, ctx):
    paths = {l: DEALS[l]["path"] for l in ALL}
    urls = []
    for lang in ALL:
        d = DEALS[lang]
        hero = (f'<h1>{d["h1"]}</h1><p class="hero-lead">{E(d["lead"])}</p>'
                f'<p class="small deal-updated" id="deal-updated"></p>')
        body = ('<section id="deals"><div class="chips deal-origins" id="deal-origins" role="group"></div>'
                '<div class="deal-grid" id="deal-grid">' + '<div class="ex-skel"></div>' * 12 + '</div></section>'
                '<script src="/deals.js" defer></script>'
                '<section class="nl-block">' + NEWSLETTER[lang] + '</section><script src="/newsletter.js" defer></script>')
        urls.append(write(site, d["path"], lang, d["title"] + " | Escale", d["desc"], hero, body, "", paths, ctx))
    return urls


# ---------------------------------------------------------------------------
# Guides pratiques (5 langues)
# ---------------------------------------------------------------------------
GUIDE_UI = {
    "fr": dict(cta="Comparer les prix des vols", others="Autres guides", eyebrow="Guide pratique"),
    "en": dict(cta="Compare flight prices", others="Other guides", eyebrow="Practical guide"),
    "es": dict(cta="Comparar precios de vuelos", others="Otras guías", eyebrow="Guía práctica"),
    "pt": dict(cta="Comparar preços de voos", others="Outros guias", eyebrow="Guia prático"),
    "ar": dict(cta="قارن أسعار الرحلات", others="أدلة أخرى", eyebrow="دليل عملي"),
}


def _para_html(items):
    out, ul = [], []
    for t in items:
        if t.startswith("- "):
            ul.append(f"<li>{E(t[2:])}</li>")
            continue
        if ul:
            out.append('<ul class="links">' + "".join(ul) + "</ul>")
            ul = []
        out.append(f"<p>{E(t)}</p>")
    if ul:
        out.append('<ul class="links">' + "".join(ul) + "</ul>")
    return "".join(out)


def build_guides(site, ctx):
    import guides as G
    urls = []
    for g in G.GUIDES:
        paths = {l: g[l]["slug"] for l in ALL}
        for lang in ALL:
            d, gu = g[lang], GUIDE_UI[lang]
            homeq = "" if lang == "fr" else f"?lang={lang}"
            hero = (f'<p class="eyebrow">{E(gu["eyebrow"])}</p><h1>{E(d["title"])}</h1>'
                    f'<p class="hero-lead">{E(d["intro"])}</p>'
                    f'<div class="cta-row"><a class="btn" href="/{homeq}">{E(gu["cta"])}</a></div>')
            body = "".join(f"<section><h2>{E(h)}</h2>{_para_html(items)}</section>" for h, items in d["sections"])
            body += f'<section><p class="small">{E(d["note"])}</p></section>'
            others = [o for o in G.GUIDES if o is not g]
            body += (f'<section><h2>{E(gu["others"])}</h2><ul class="route-links">' +
                     "".join(f'<li><a href="/{o[lang]["slug"]}/">{E(o[lang]["title"])}</a></li>' for o in others) + "</ul></section>")
            ld = '<script type="application/ld+json">' + json.dumps({
                "@context": "https://schema.org", "@type": "Article", "headline": d["title"], "description": d["desc"],
                "inLanguage": lang, "author": {"@type": "Organization", "name": "Escale"}}, ensure_ascii=False) + "</script>"
            urls.append(write(site, d["slug"], lang, d["title"] + " | Escale", d["desc"], hero, body, ld, paths, ctx))
    ipaths = {l: G.INDEX[l]["slug"] for l in ALL}
    for lang in ALL:
        ix = G.INDEX[lang]
        hero = f'<h1>{E(ix["title"])}</h1><p class="hero-lead">{E(ix["lead"])}</p>'
        body = '<section><ul class="extra-list">' + "".join(
            f'<li class="extra"><span class="logo" style="background:#0b5cd6" aria-hidden="true">{i + 1}</span>'
            f'<div><strong>{E(g[lang]["title"])}</strong><span>{E(g[lang]["desc"])}</span></div>'
            f'<a class="price-go" href="/{g[lang]["slug"]}/">{E(ix["more"])}</a></li>' for i, g in enumerate(G.GUIDES)) + "</ul></section>"
        urls.append(write(site, ix["slug"], lang, ix["title"] + " | Escale", ix["lead"], hero, body, "", ipaths, ctx))
    return urls


def build_about(site, ctx):
    import about as A
    paths = {l: A.ABOUT[l]["slug"] for l in ALL}
    urls = []
    for lang in ALL:
        d = A.ABOUT[lang]
        hero = f'<h1>{E(d["title"])}</h1><p class="hero-lead">{E(d["lead"])}</p>'
        body = "".join(f"<section><h2>{E(h)}</h2>{_para_html(ps)}</section>" for h, ps in d["sections"])
        body += f'<p><a class="btn" href="/contact/">{E(d["contact"])}</a></p>'
        ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "AboutPage", "name": d["title"], "inLanguage": lang}, ensure_ascii=False) + "</script>"
        urls.append(write(site, d["slug"], lang, d["title"] + " | Escale", d["lead"], hero, body, ld, paths, ctx))
    return urls


def build_fetes(site, ctx):
    """Pages « Vols pour les fêtes » (voir scripts/fetes.py) et page d'ensemble, en 5 langues."""
    import fetes as F
    urls = []

    def cname(n, lang):
        return n if lang == "fr" else city(n, lang)

    def route_page(code, city_fr, lang):
        r = ("CDG", code, "Paris", city_fr)
        p = f"vol-paris-{slugify(city_fr)}" if lang == "fr" else route_path(r, lang)
        return p if (site / p / "index.html").exists() else None

    for f in F.FETES:
        paths = {l: f[l]["slug"] for l in ALL}
        for lang in ALL:
            d, u = f[lang], F.UI[lang]
            homeq = "" if lang == "fr" else f"&lang={lang}"
            rows = []
            for code, city_fr in f["routes"]:
                search = f"/?type=vols&from=CDG&to={code}&dep={f['dep']}&ret={f['ret']}{homeq}"
                rp = route_page(code, city_fr, lang)
                alert = f' <a class="fete-alert" href="/{rp}/#price-alert">{E(u["alert"])}</a>' if rp else ""
                rows.append(f'<tr data-from="CDG" data-to="{code}"><th scope="row"><bdi>{E(cname("Paris", lang))} → {E(cname(city_fr, lang))}</bdi></th>'
                            f'<td class="fp" aria-live="polite">{E(u["loading"])}</td>'
                            f'<td><a class="price-go" href="{E(search)}">{E(u["see"])}</a>{alert}</td></tr>')
            hero = (f'<p class="eyebrow">{E(u["eyebrow"])}</p><h1>{E(d["title"])}</h1><p class="hero-lead">{E(d["lead"])}</p>'
                    f'<div class="cta-row"><a class="btn" href="/{"" if lang == "fr" else "?lang=" + lang}">{E(u["cta"])}</a></div>')
            body = f'<section><h2>{E(u["dates_label"])}</h2>{_para_html(d["dates"])}</section>'
            body += (f'<section><h2>{E(u["table_h"])}</h2>'
                     f'<table class="fete-table" data-dep="{f["dep"]}" data-ret="{f["ret"]}" data-from-label="{E(u["from_"])}" data-none="{E(u["none"])}">'
                     f'<thead><tr><th scope="col">{E(u["route"])}</th><th scope="col">{E(u["price"])}</th><th scope="col"><span class="sr-only">{E(u["see"])}</span></th></tr></thead>'
                     f'<tbody>{"".join(rows)}</tbody></table><p class="small">{E(u["table_note"])}</p></section>')
            body += f'<section><h2>{E(u["book_h"])}</h2><ul>' + "".join(f"<li>{E(x)}</li>" for x in d["book"]) + "</ul></section>"
            body += f'<section><h2>{E(u["alert_h"])}</h2><p>{E(u["alert_p"])}</p></section>'
            others = [o for o in F.FETES if o is not f]
            body += (f'<section><h2>{E(u["others"])}</h2><ul class="route-links">' +
                     "".join(f'<li><a href="/{o[lang]["slug"]}/">{E(o[lang]["title"])}</a></li>' for o in others) + "</ul></section>")
            body += '<script src="/fetes.js" defer></script>'
            ld = '<script type="application/ld+json">' + json.dumps({
                "@context": "https://schema.org", "@type": "Article", "headline": d["title"], "description": d["desc"],
                "inLanguage": lang, "author": {"@type": "Organization", "name": "Escale"}}, ensure_ascii=False) + "</script>"
            urls.append(write(site, d["slug"], lang, d["title"] + " | Escale", d["desc"], hero, body, ld, paths, ctx))
    ipaths = dict(F.INDEX_SLUG)
    for lang in ALL:
        u = F.UI[lang]
        hero = f'<p class="eyebrow">{E(u["eyebrow"])}</p><h1>{E(u["index_title"])}</h1><p class="hero-lead">{E(u["index_lead"])}</p>'
        body = '<section><ul class="extra-list">' + "".join(
            f'<li class="extra"><span class="logo" style="background:#0b5cd6" aria-hidden="true">{i + 1}</span>'
            f'<div><strong>{E(f[lang]["title"])}</strong><span>{E(f[lang]["lead"])}</span></div>'
            f'<a class="price-go" href="/{f[lang]["slug"]}/">{E(u["more"])}</a></li>' for i, f in enumerate(F.FETES)) + "</ul></section>"
        urls.append(write(site, ipaths[lang], lang, u["index_title"] + " | Escale", u["index_lead"], hero, body, "", ipaths, ctx))
    return urls
