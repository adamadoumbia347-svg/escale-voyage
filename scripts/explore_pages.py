"""Pages « Partout » (carte des prix dans le monde) et « Favoris » (sans compte), en 5 langues."""
import html

from build_i18n import ALL, SECTION_PATHS, write

E = html.escape

# Villes de départ proposées (Europe et Amérique du Nord), avec leur nom dans chaque langue
ORIGINS = [
    ("CDG", "Paris", "Paris", "París", "Paris", "باريس"),
    ("BRU", "Bruxelles", "Brussels", "Bruselas", "Bruxelas", "بروكسل"),
    ("LYS", "Lyon", "Lyon", "Lyon", "Lyon", "ليون"),
    ("MRS", "Marseille", "Marseille", "Marsella", "Marselha", "مرسيليا"),
    ("NCE", "Nice", "Nice", "Niza", "Nice", "نيس"),
    ("TLS", "Toulouse", "Toulouse", "Toulouse", "Toulouse", "تولوز"),
    ("BOD", "Bordeaux", "Bordeaux", "Burdeos", "Bordéus", "بوردو"),
    ("GVA", "Genève", "Geneva", "Ginebra", "Genebra", "جنيف"),
    ("ZRH", "Zurich", "Zurich", "Zúrich", "Zurique", "زيورخ"),
    ("LHR", "Londres", "London", "Londres", "Londres", "لندن"),
    ("MAN", "Manchester", "Manchester", "Mánchester", "Manchester", "مانشستر"),
    ("AMS", "Amsterdam", "Amsterdam", "Ámsterdam", "Amesterdão", "أمستردام"),
    ("FRA", "Francfort", "Frankfurt", "Fráncfort", "Frankfurt", "فرانكفورت"),
    ("MAD", "Madrid", "Madrid", "Madrid", "Madrid", "مدريد"),
    ("BCN", "Barcelone", "Barcelona", "Barcelona", "Barcelona", "برشلونة"),
    ("LIS", "Lisbonne", "Lisbon", "Lisboa", "Lisboa", "لشبونة"),
    ("FCO", "Rome", "Rome", "Roma", "Roma", "روما"),
    ("YUL", "Montréal", "Montreal", "Montreal", "Montreal", "مونتريال"),
    ("YYZ", "Toronto", "Toronto", "Toronto", "Toronto", "تورونتو"),
    ("JFK", "New York", "New York", "Nueva York", "Nova Iorque", "نيويورك"),
    ("IAD", "Washington", "Washington", "Washington", "Washington", "واشنطن"),
    ("ATL", "Atlanta", "Atlanta", "Atlanta", "Atlanta", "أتلانتا"),
]
COL = {"fr": 1, "en": 2, "es": 3, "pt": 4, "ar": 5}

ANY = {
    "fr": dict(title="Partout : la carte des vols pas chers depuis votre ville", h1="Partout dans le monde, <span>au meilleur prix</span>",
               desc="Pas d'idée de destination ? Voyez sur une carte du monde les vols aller-retour les moins chers depuis Paris, Bruxelles, Genève, Londres, Montréal, New York et d'autres villes.",
               lead="Choisissez votre ville et un mois : la carte montre les destinations les moins chères trouvées récemment par des voyageurs. Touchez un point pour voir les vols.",
               from_="Départ de", month="Mois", budget="Budget max", map="Carte des destinations et de leurs prix", list="Destinations"),
    "en": dict(title="Anywhere: map of cheap flights from your city", h1="Anywhere in the world, <span>at the best price</span>",
               desc="No idea where to go? See on a world map the cheapest round-trip flights from London, Paris, Brussels, Geneva, Montreal, New York and more.",
               lead="Pick your city and a month: the map shows the cheapest destinations recently found by travellers. Tap a dot to see the flights.",
               from_="From", month="Month", budget="Max budget", map="Map of destinations and their prices", list="Destinations"),
    "es": dict(title="Explorar: mapa de vuelos baratos desde tu ciudad", h1="A cualquier lugar del mundo, <span>al mejor precio</span>",
               desc="¿No sabes adónde ir? Mira en un mapa del mundo los vuelos de ida y vuelta más baratos desde Madrid, Barcelona, París, Londres, Nueva York y otras ciudades.",
               lead="Elige tu ciudad y un mes: el mapa muestra los destinos más baratos encontrados recientemente por viajeros. Toca un punto para ver los vuelos.",
               from_="Salida desde", month="Mes", budget="Presupuesto máximo", map="Mapa de destinos y sus precios", list="Destinos"),
    "pt": dict(title="Explorar: mapa de voos baratos a partir da sua cidade", h1="Para qualquer lugar do mundo, <span>ao melhor preço</span>",
               desc="Sem ideia de destino? Veja num mapa do mundo os voos de ida e volta mais baratos a partir de Lisboa, Paris, Londres, Bruxelas, Nova Iorque e outras cidades.",
               lead="Escolha a sua cidade e um mês: o mapa mostra os destinos mais baratos encontrados recentemente por viajantes. Toque num ponto para ver os voos.",
               from_="Partida de", month="Mês", budget="Orçamento máximo", map="Mapa dos destinos e dos seus preços", list="Destinos"),
    "ar": dict(title="استكشف: خريطة الرحلات الرخيصة من مدينتك", h1="إلى أي مكان في العالم <span>بأفضل سعر</span>",
               desc="لا تعرف إلى أين تسافر؟ شاهد على خريطة العالم أرخص رحلات الذهاب والعودة من باريس ولندن وبروكسل وجنيف ومونتريال ونيويورك ومدن أخرى.",
               lead="اختر مدينتك وشهرًا: تعرض الخريطة أرخص الوجهات التي وجدها المسافرون مؤخرًا. المس نقطة لرؤية الرحلات.",
               from_="المغادرة من", month="الشهر", budget="الميزانية القصوى", map="خريطة الوجهات وأسعارها", list="الوجهات"),
}

FAVS = {
    "fr": dict(title="Mes favoris", h1="Mes <span>favoris</span>",
               desc="Vos trajets, hôtels et recherches de vols enregistrés sur cet appareil, sans compte.",
               lead="Les trajets, hôtels et recherches que vous avez marqués d’une étoile. Ils restent sur cet appareil : aucun compte, rien n’est envoyé à Escale."),
    "en": dict(title="My favorites", h1="My <span>favorites</span>",
               desc="Your saved routes, hotels and flight searches on this device, no account needed.",
               lead="The routes, hotels and searches you starred. They stay on this device: no account, nothing is sent to Escale."),
    "es": dict(title="Mis favoritos", h1="Mis <span>favoritos</span>",
               desc="Tus rutas, hoteles y búsquedas de vuelos guardados en este dispositivo, sin cuenta.",
               lead="Las rutas, hoteles y búsquedas que marcaste con una estrella. Se quedan en este dispositivo: sin cuenta, no se envía nada a Escale."),
    "pt": dict(title="Os meus favoritos", h1="Os meus <span>favoritos</span>",
               desc="As suas rotas, hotéis e pesquisas de voos guardados neste dispositivo, sem conta.",
               lead="As rotas, hotéis e pesquisas que marcou com uma estrela. Ficam neste dispositivo: sem conta, nada é enviado para a Escale."),
    "ar": dict(title="المفضلة", h1="<span>المفضلة</span> لديّ",
               desc="رحلاتك وفنادقك وعمليات البحث المحفوظة على هذا الجهاز، دون حساب.",
               lead="الرحلات والفنادق وعمليات البحث التي ميّزتها بنجمة. تبقى على هذا الجهاز: لا حساب، ولا يُرسل شيء إلى Escale."),
}
EMPTY = {'fr': 'Aucun favori pour l’instant. Touchez l’étoile sur un trajet, un hôtel ou une recherche pour le retrouver ici.', 'en': 'No favorites yet. Tap the star on a route, a hotel page or a search to find it here.', 'es': 'Aún no tienes favoritos. Toca la estrella en una ruta, un hotel o una búsqueda para encontrarlo aquí.', 'pt': 'Ainda não tem favoritos. Toque na estrela de uma rota, de um hotel ou de uma pesquisa para a encontrar aqui.', 'ar': 'لا توجد عناصر مفضلة بعد. المس النجمة في صفحة رحلة أو فندق أو بحث لتجده هنا.'}
CLEAR = {"fr": "Tout effacer", "en": "Clear all", "es": "Borrar todo", "pt": "Apagar tudo", "ar": "حذف الكل"}


def build_anywhere(site, ctx):
    paths = {l: SECTION_PATHS["anywhere"][l] for l in ALL}
    urls = []
    for lang in ALL:
        a = ANY[lang]
        opts = "".join(f'<option value="{o[0]}">{E(o[COL[lang]])} ({o[0]})</option>' for o in ORIGINS)
        hero = f'<h1>{a["h1"]}</h1><p class="hero-lead">{E(a["lead"])}</p>'
        body = f'''<section id="anywhere" class="anywhere">
<div class="any-controls">
  <label class="any-field"><span>{E(a["from_"])}</span><select id="any-from">{opts}</select></label>
  <div class="any-field"><span id="any-months-l">{E(a["month"])}</span><div class="chips" id="any-months" role="group" aria-labelledby="any-months-l"></div></div>
  <label class="any-field any-budget"><span>{E(a["budget"])}</span><input type="range" id="any-max" min="0" max="100" disabled><output id="any-max-out" for="any-max"></output></label>
</div>
<div class="any-map-wrap">
  <div class="any-scroll" id="any-scroll"><div class="any-map"><div class="any-land" aria-hidden="true"></div>
  <svg id="any-dots" viewBox="0 0 2000 789" role="group" aria-label="{E(a["map"])}"></svg></div></div>
  <div class="any-tip" id="any-tip" hidden></div>
</div>
<p class="small any-status" id="any-status" role="status"></p>
<h2 class="sr-only">{E(a["list"])}</h2>
<ol class="any-list" id="any-list"></ol>
</section>
<script src="/partout.js" defer></script>'''
        urls.append(write(site, paths[lang], lang, a["title"] + " | Escale", a["desc"], hero, body, "", paths, ctx))
    return urls


def build_favs(site, ctx):
    paths = {l: SECTION_PATHS["favs"][l] for l in ALL}
    urls = []
    for lang in ALL:
        f = FAVS[lang]
        hero = f'<h1>{f["h1"]}</h1><p class="hero-lead">{E(f["lead"])}</p>'
        body = (f'<section class="favs"><div id="fav-list" aria-live="polite"><p class="fav-empty">{E(EMPTY[lang])}</p></div>'
                f'<p><button type="button" class="btn ghost" id="fav-clear" hidden>{E(CLEAR[lang])}</button></p></section>')
        urls.append(write(site, paths[lang], lang, f["title"] + " | Escale", f["desc"], hero, body, "", paths, ctx))
    return urls
