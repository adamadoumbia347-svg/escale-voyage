"""Guides pratiques (5 langues). Contenu volontairement général : les règles précises dépendent de la compagnie et du pays.

Structure : GUIDES = liste de guides ; chaque guide a, par langue : slug (chemin), title, desc, intro, sections [(titre, [paragraphes])].
Un paragraphe qui commence par « - » est affiché comme élément de liste.
"""

GUIDES = [
    {
        "key": "bagages",
        "fr": dict(
            slug="guides/bagages-avion", title="Bagages en avion : ne pas payer plus cher",
            desc="Bagage cabine, bagage en soute, tarifs « light » : comment comparer le vrai prix d’un billet d’avion, surtout pour les voyages en famille vers l’Afrique.",
            intro="Le billet le moins cher n’est pas toujours le voyage le moins cher. Les bagages changent souvent le classement, surtout quand on part en famille avec plusieurs valises.",
            sections=[
                ("Comprendre ce que comprend votre tarif", [
                    "Beaucoup de compagnies vendent des tarifs de base (« light », « basic », « essentiel ») qui n’incluent qu’un petit sac sous le siège ou un bagage cabine, sans valise en soute.",
                    "Avant de comparer deux offres, regardez pour chacune : le bagage cabine autorisé, le nombre de valises en soute incluses et leur poids maximal.",
                ]),
                ("Ajoutez la valise au bon moment", [
                    "En général, ajouter une valise au moment de la réservation coûte moins cher qu’après coup, et beaucoup moins cher qu’au comptoir de l’aéroport.",
                    "Si vous hésitez entre deux offres, ajoutez les bagages dans chacune avant de comparer le total. Notre calculateur du vrai prix, sur la page d’accueil, le fait pour vous.",
                ]),
                ("Évitez les mauvaises surprises à l’aéroport", [
                    "- Pesez vos valises la veille : l’excédent de poids se paie cher.",
                    "- Vérifiez les dimensions du bagage cabine sur le site de la compagnie : elles varient d’une compagnie à l’autre.",
                    "- Les batteries externes et cigarettes électroniques se transportent en cabine, pas en soute.",
                    "- Les liquides en cabine sont limités (petits contenants dans un sac transparent dans la plupart des aéroports) : vérifiez la règle de votre aéroport de départ.",
                ]),
                ("Bien préparer ses valises", [
                    "Prenez une photo de vos valises et de leur contenu, et glissez vos coordonnées à l’intérieur. En cas de perte, la déclaration se fait au comptoir de la compagnie avant de quitter l’aéroport.",
                ]),
            ],
            note="Les règles de bagages changent selon la compagnie, le tarif et la ligne : vérifiez toujours sur le site de la compagnie avant de payer."),
        "en": dict(
            slug="en/guides/baggage", title="Air baggage: don’t pay more than you need",
            desc="Cabin bag, checked bag, basic fares: how to compare the real price of a flight, especially for family trips to Africa.",
            intro="The cheapest ticket is not always the cheapest trip. Baggage often changes the ranking, especially when a family travels with several suitcases.",
            sections=[
                ("Know what your fare includes", [
                    "Many airlines sell basic fares (“light”, “basic”, “saver”) that only include a small under-seat bag or a cabin bag, with no checked suitcase.",
                    "Before comparing two offers, check for each one: the cabin allowance, how many checked bags are included and their maximum weight.",
                ]),
                ("Add your suitcase at the right time", [
                    "Adding a suitcase when you book is usually cheaper than adding it later, and much cheaper than paying at the airport desk.",
                    "If you are torn between two offers, add the baggage to both before comparing the total. Our real-price calculator on the home page does it for you.",
                ]),
                ("Avoid bad surprises at the airport", [
                    "- Weigh your bags the day before: excess weight is expensive.",
                    "- Check the cabin bag size on the airline’s website: it varies between airlines.",
                    "- Power banks and e-cigarettes go in the cabin, not in the hold.",
                    "- Liquids in the cabin are limited (small containers in a clear bag at most airports): check the rule at your departure airport.",
                ]),
                ("Pack smart", [
                    "Take a photo of your bags and their contents, and put your contact details inside. If a bag is lost, report it at the airline desk before leaving the airport.",
                ]),
            ],
            note="Baggage rules depend on the airline, the fare and the route: always check the airline’s website before paying."),
        "es": dict(
            slug="es/guias/equipaje", title="Equipaje en avión: no pagues de más",
            desc="Equipaje de mano, maleta facturada, tarifas básicas: cómo comparar el precio real de un vuelo, sobre todo en viajes en familia a África.",
            intro="El billete más barato no siempre es el viaje más barato. El equipaje cambia a menudo la clasificación, sobre todo cuando una familia viaja con varias maletas.",
            sections=[
                ("Entiende qué incluye tu tarifa", [
                    "Muchas aerolíneas venden tarifas básicas («light», «basic») que solo incluyen un bolso bajo el asiento o una maleta de mano, sin maleta facturada.",
                    "Antes de comparar dos ofertas, revisa en cada una: el equipaje de mano permitido, cuántas maletas facturadas incluye y su peso máximo.",
                ]),
                ("Añade la maleta en el momento adecuado", [
                    "Añadir una maleta al reservar suele ser más barato que hacerlo después, y mucho más que pagarla en el mostrador del aeropuerto.",
                    "Si dudas entre dos ofertas, añade el equipaje en ambas antes de comparar el total. Nuestra calculadora del precio real, en la página de inicio, lo hace por ti.",
                ]),
                ("Evita sorpresas en el aeropuerto", [
                    "- Pesa tus maletas el día antes: el exceso de peso sale caro.",
                    "- Revisa las medidas del equipaje de mano en la web de la aerolínea: cambian de una a otra.",
                    "- Las baterías externas y los cigarrillos electrónicos van en cabina, no en bodega.",
                    "- Los líquidos en cabina están limitados (envases pequeños en una bolsa transparente en la mayoría de aeropuertos): revisa la norma de tu aeropuerto.",
                ]),
                ("Prepara bien tus maletas", [
                    "Haz una foto de tus maletas y su contenido, y pon tus datos dentro. Si se pierde una, declárala en el mostrador de la aerolínea antes de salir del aeropuerto.",
                ]),
            ],
            note="Las normas de equipaje dependen de la aerolínea, la tarifa y la ruta: compruébalo siempre en la web de la aerolínea antes de pagar."),
        "pt": dict(
            slug="pt/guias/bagagem", title="Bagagem de avião: não pague mais do que precisa",
            desc="Bagagem de mão, bagagem de porão, tarifas básicas: como comparar o preço real de um voo, sobretudo em viagens em família para África.",
            intro="O bilhete mais barato nem sempre é a viagem mais barata. A bagagem muda muitas vezes a classificação, sobretudo quando uma família viaja com várias malas.",
            sections=[
                ("Perceba o que inclui a sua tarifa", [
                    "Muitas companhias vendem tarifas básicas («light», «basic») que só incluem uma mala pequena debaixo do assento ou uma mala de cabine, sem mala de porão.",
                    "Antes de comparar duas ofertas, veja em cada uma: a bagagem de mão permitida, quantas malas de porão estão incluídas e o peso máximo.",
                ]),
                ("Junte a mala no momento certo", [
                    "Juntar uma mala na reserva costuma ser mais barato do que depois, e muito mais barato do que pagar no balcão do aeroporto.",
                    "Se hesita entre duas ofertas, junte a bagagem às duas antes de comparar o total. A nossa calculadora do preço real, na página inicial, faz isso por si.",
                ]),
                ("Evite surpresas no aeroporto", [
                    "- Pese as malas na véspera: o excesso de peso sai caro.",
                    "- Verifique as dimensões da bagagem de mão no site da companhia: variam de uma para outra.",
                    "- Baterias externas e cigarros eletrónicos vão na cabine, não no porão.",
                    "- Os líquidos na cabine são limitados (embalagens pequenas num saco transparente na maioria dos aeroportos): verifique a regra do seu aeroporto.",
                ]),
                ("Prepare bem as malas", [
                    "Tire uma foto das malas e do conteúdo e ponha os seus contactos lá dentro. Em caso de perda, declare-a no balcão da companhia antes de sair do aeroporto.",
                ]),
            ],
            note="As regras de bagagem dependem da companhia, da tarifa e da rota: confirme sempre no site da companhia antes de pagar."),
        "ar": dict(
            slug="ar/guides/baggage", title="أمتعة الطائرة: لا تدفع أكثر من اللازم",
            desc="حقيبة اليد والحقيبة المشحونة والأسعار الأساسية: كيف تقارن السعر الحقيقي لتذكرة الطيران، خصوصًا في السفر العائلي إلى أفريقيا.",
            intro="أرخص تذكرة ليست دائمًا أرخص رحلة. الأمتعة تغيّر الترتيب غالبًا، خاصة عندما تسافر العائلة بعدة حقائب.",
            sections=[
                ("اعرف ما يشمله سعر تذكرتك", [
                    "تبيع شركات كثيرة أسعارًا أساسية لا تشمل إلا حقيبة صغيرة تحت المقعد أو حقيبة يد، دون حقيبة مشحونة.",
                    "قبل مقارنة عرضين، تحقّق في كل منهما من: حقيبة اليد المسموحة، وعدد الحقائب المشحونة المشمولة، ووزنها الأقصى.",
                ]),
                ("أضف الحقيبة في الوقت المناسب", [
                    "إضافة حقيبة عند الحجز أرخص عادةً من إضافتها لاحقًا، وأرخص بكثير من دفعها عند مكتب المطار.",
                    "إذا تردّدت بين عرضين، أضف الأمتعة إلى كليهما قبل مقارنة المجموع. حاسبة السعر الحقيقي في الصفحة الرئيسية تفعل ذلك عنك.",
                ]),
                ("تجنّب المفاجآت في المطار", [
                    "- زِن حقائبك في اليوم السابق: الوزن الزائد مكلف.",
                    "- تحقّق من مقاسات حقيبة اليد على موقع الشركة: تختلف من شركة لأخرى.",
                    "- البطاريات الخارجية والسجائر الإلكترونية تُحمل في المقصورة لا في الشحن.",
                    "- السوائل في المقصورة محدودة (عبوات صغيرة في كيس شفاف في معظم المطارات): تحقّق من قاعدة مطار المغادرة.",
                ]),
                ("جهّز حقائبك جيدًا", [
                    "التقط صورة لحقائبك ومحتواها، وضع بيانات الاتصال بك داخلها. عند الضياع، أبلغ مكتب الشركة قبل مغادرة المطار.",
                ]),
            ],
            note="قواعد الأمتعة تختلف حسب الشركة والسعر والخط: تحقّق دائمًا من موقع الشركة قبل الدفع."),
    },
    {
        "key": "reserver",
        "fr": dict(
            slug="guides/quand-reserver", title="Quand réserver son billet d’avion pour payer moins cher",
            desc="Été, Noël, Tabaski, Aïd : à quel moment réserver son vol pour l’Afrique, le Maghreb ou les Antilles, et les erreurs qui font payer plus cher.",
            intro="Il n’existe pas de jour magique, mais quelques habitudes font souvent économiser beaucoup, surtout pour les périodes de fêtes.",
            sections=[
                ("Pour un voyage hors vacances", [
                    "Réserver deux à trois mois à l’avance donne souvent de bons prix. Les dernières semaines avant le départ sont rarement les moins chères sur les lignes très demandées.",
                ]),
                ("Pour l’été, Noël et les fêtes religieuses", [
                    "Juillet-août et la fin d’année sont les périodes les plus chères vers l’Afrique et les Antilles. Réservez plutôt quatre à six mois avant.",
                    "La Tabaski (Aïd el-Kébir) et l’Aïd el-Fitr suivent le calendrier lunaire : elles avancent d’environ onze jours chaque année. Vérifiez les dates de l’année de votre voyage et réservez tôt si elles tombent pendant les vacances scolaires.",
                ]),
                ("Les réflexes qui font économiser", [
                    "- Regardez le calendrier des prix de votre trajet : décaler le départ de quelques jours change souvent beaucoup le prix.",
                    "- Les départs en milieu de semaine sont fréquemment moins chers que le vendredi ou le dimanche.",
                    "- Comparez les aéroports proches (Paris-Orly, Beauvais, Bruxelles…).",
                    "- Créez une alerte prix et attendez une baisse si votre voyage est encore loin.",
                ]),
                ("Les erreurs fréquentes", [
                    "- Attendre la dernière minute en espérant une promotion sur une ligne très demandée.",
                    "- Comparer des prix sans les bagages (voir notre guide sur les bagages).",
                    "- Oublier de vérifier les conditions de modification et d’annulation du billet.",
                ]),
            ],
            note="Ce sont des tendances générales observées sur les comparateurs : les prix dépendent de chaque ligne et de chaque compagnie."),
        "en": dict(
            slug="en/guides/when-to-book", title="When to book your flight to pay less",
            desc="Summer, Christmas, Eid: when to book flights to Africa, North Africa or the Caribbean, and the mistakes that make you pay more.",
            intro="There is no magic day, but a few habits often save a lot, especially for holiday periods.",
            sections=[
                ("For a trip outside the holidays", [
                    "Booking two to three months ahead often gives good prices. The last weeks before departure are rarely the cheapest on busy routes.",
                ]),
                ("For summer, Christmas and religious holidays", [
                    "July–August and the year-end are the most expensive periods to Africa and the Caribbean. Book four to six months ahead instead.",
                    "Eid al-Adha (Tabaski) and Eid al-Fitr follow the lunar calendar: they move about eleven days earlier each year. Check the dates for your travel year and book early if they fall during school holidays.",
                ]),
                ("Habits that save money", [
                    "- Look at your route’s price calendar: moving your departure by a few days often changes the price a lot.",
                    "- Mid-week departures are often cheaper than Friday or Sunday.",
                    "- Compare nearby airports (London Heathrow, Gatwick, Stansted…).",
                    "- Set a price alert and wait for a drop if your trip is still far away.",
                ]),
                ("Common mistakes", [
                    "- Waiting for a last-minute deal on a busy route.",
                    "- Comparing prices without baggage (see our baggage guide).",
                    "- Forgetting to check the change and cancellation rules of the ticket.",
                ]),
            ],
            note="These are general trends seen on comparison sites: prices depend on each route and airline."),
        "es": dict(
            slug="es/guias/cuando-reservar", title="Cuándo reservar tu vuelo para pagar menos",
            desc="Verano, Navidad, Eid: cuándo reservar vuelos a África, el Magreb o el Caribe, y los errores que hacen pagar más.",
            intro="No existe un día mágico, pero algunos hábitos suelen ahorrar mucho, sobre todo en temporada de fiestas.",
            sections=[
                ("Para un viaje fuera de vacaciones", [
                    "Reservar con dos o tres meses de antelación suele dar buenos precios. Las últimas semanas antes de salir rara vez son las más baratas en rutas muy demandadas.",
                ]),
                ("Para el verano, la Navidad y las fiestas religiosas", [
                    "Julio-agosto y fin de año son las épocas más caras hacia África y el Caribe. Reserva mejor con cuatro a seis meses de antelación.",
                    "El Eid al-Adha (Tabaski) y el Eid al-Fitr siguen el calendario lunar: se adelantan unos once días cada año. Comprueba las fechas del año de tu viaje y reserva pronto si caen en vacaciones escolares.",
                ]),
                ("Hábitos que ahorran", [
                    "- Mira el calendario de precios de tu ruta: mover la salida unos días suele cambiar mucho el precio.",
                    "- Salir entre semana suele ser más barato que el viernes o el domingo.",
                    "- Compara aeropuertos cercanos.",
                    "- Crea una alerta de precio y espera una bajada si tu viaje aún está lejos.",
                ]),
                ("Errores frecuentes", [
                    "- Esperar al último minuto en una ruta muy demandada.",
                    "- Comparar precios sin equipaje (ver nuestra guía de equipaje).",
                    "- Olvidar revisar las condiciones de cambio y cancelación del billete.",
                ]),
            ],
            note="Son tendencias generales observadas en los comparadores: los precios dependen de cada ruta y aerolínea."),
        "pt": dict(
            slug="pt/guias/quando-reservar", title="Quando reservar o voo para pagar menos",
            desc="Verão, Natal, Eid: quando reservar voos para África, o Magrebe ou as Caraíbas, e os erros que fazem pagar mais.",
            intro="Não há um dia mágico, mas alguns hábitos costumam poupar muito, sobretudo nas épocas festivas.",
            sections=[
                ("Para uma viagem fora das férias", [
                    "Reservar com dois a três meses de antecedência costuma dar bons preços. As últimas semanas antes da partida raramente são as mais baratas nas rotas mais procuradas.",
                ]),
                ("Para o verão, o Natal e as festas religiosas", [
                    "Julho-agosto e o fim do ano são as épocas mais caras para África e as Caraíbas. Reserve antes com quatro a seis meses de antecedência.",
                    "O Eid al-Adha (Tabaski) e o Eid al-Fitr seguem o calendário lunar: antecipam-se cerca de onze dias por ano. Verifique as datas do ano da sua viagem e reserve cedo se coincidirem com as férias escolares.",
                ]),
                ("Hábitos que poupam", [
                    "- Veja o calendário de preços da sua rota: mudar a partida alguns dias muda muitas vezes bastante o preço.",
                    "- Partir a meio da semana costuma ser mais barato do que à sexta ou ao domingo.",
                    "- Compare aeroportos próximos.",
                    "- Crie um alerta de preço e espere por uma descida se a viagem ainda estiver longe.",
                ]),
                ("Erros frequentes", [
                    "- Esperar pela última hora numa rota muito procurada.",
                    "- Comparar preços sem bagagem (veja o nosso guia de bagagem).",
                    "- Esquecer de verificar as condições de alteração e cancelamento do bilhete.",
                ]),
            ],
            note="São tendências gerais observadas nos comparadores: os preços dependem de cada rota e companhia."),
        "ar": dict(
            slug="ar/guides/when-to-book", title="متى تحجز تذكرة الطيران لتدفع أقل",
            desc="الصيف وعيد الميلاد والأعياد: متى تحجز رحلاتك إلى أفريقيا أو المغرب العربي أو الكاريبي، والأخطاء التي تجعلك تدفع أكثر.",
            intro="لا يوجد يوم سحري، لكن بعض العادات توفّر كثيرًا غالبًا، خصوصًا في مواسم الأعياد.",
            sections=[
                ("لرحلة خارج العطل", [
                    "الحجز قبل شهرين إلى ثلاثة أشهر يعطي غالبًا أسعارًا جيدة. نادرًا ما تكون الأسابيع الأخيرة قبل السفر الأرخص على الخطوط المزدحمة.",
                ]),
                ("للصيف وعيد الميلاد والأعياد الدينية", [
                    "يوليو وأغسطس ونهاية السنة أغلى الفترات نحو أفريقيا والكاريبي. احجز قبل أربعة إلى ستة أشهر.",
                    "عيد الأضحى (تاباسكي) وعيد الفطر يتبعان التقويم القمري: يتقدّمان نحو أحد عشر يومًا كل عام. تحقّق من التواريخ في سنة سفرك واحجز مبكرًا إذا وافقت العطل المدرسية.",
                ]),
                ("عادات توفّر المال", [
                    "- انظر إلى تقويم الأسعار لخطك: تغيير موعد المغادرة بضعة أيام يغيّر السعر كثيرًا غالبًا.",
                    "- المغادرة في منتصف الأسبوع أرخص غالبًا من الجمعة أو الأحد.",
                    "- قارن المطارات القريبة.",
                    "- فعّل تنبيه الأسعار وانتظر الانخفاض إذا كانت رحلتك بعيدة.",
                ]),
                ("أخطاء شائعة", [
                    "- انتظار اللحظة الأخيرة على خط مزدحم.",
                    "- مقارنة الأسعار دون الأمتعة (انظر دليل الأمتعة).",
                    "- نسيان التحقّق من شروط تعديل التذكرة وإلغائها.",
                ]),
            ],
            note="هذه اتجاهات عامة تُلاحظ على مواقع المقارنة: الأسعار تختلف حسب كل خط وكل شركة."),
    },
    {
        "key": "enfants",
        "fr": dict(
            slug="guides/voyager-avec-enfants", title="Voyager en avion avec des enfants : documents et conseils",
            desc="Passeport, autorisation de sortie du territoire, vaccins, tarifs bébé : la liste pour préparer un voyage en avion avec des enfants, notamment vers l’Afrique.",
            intro="Un voyage avec des enfants se prépare un peu plus tôt : certains documents demandent plusieurs semaines.",
            sections=[
                ("Les papiers de chaque enfant", [
                    "Chaque enfant, même un bébé, doit avoir son propre document de voyage (passeport, ou carte d’identité pour certains pays). Vérifiez sa date de validité : certains pays exigent qu’il soit valable plusieurs mois après le retour.",
                    "Renseignez-vous aussi sur le visa ou l’autorisation d’entrée du pays de destination : les enfants y sont généralement soumis comme les adultes.",
                ]),
                ("Enfant qui voyage sans ses deux parents (départ de France)", [
                    "Un mineur qui quitte la France sans être accompagné d’un titulaire de l’autorité parentale doit présenter une autorisation de sortie du territoire (formulaire Cerfa n° 15646), accompagnée de la copie de la pièce d’identité du parent signataire.",
                    "D’autres pays ont leurs propres règles : renseignez-vous auprès du consulat. Pour la France : service-public.fr.",
                ]),
                ("Santé et vaccins", [
                    "Certains pays, notamment en Afrique, exigent le vaccin contre la fièvre jaune à l’entrée, y compris pour les enfants à partir d’un certain âge. Consultez un centre de vaccinations internationales ou votre médecin plusieurs semaines avant le départ.",
                ]),
                ("Billets et confort à bord", [
                    "- Les bébés de moins de 2 ans voyagent en général sur les genoux d’un adulte, pour un prix réduit ; au-delà, ils ont leur propre siège.",
                    "- Choisissez des sièges côte à côte au moment de la réservation : ce n’est pas toujours automatique sur les tarifs de base.",
                    "- Vérifiez les règles de la compagnie pour la poussette et le siège auto.",
                    "- Prévoyez de quoi boire au décollage et à l’atterrissage pour les oreilles des plus petits.",
                ]),
            ],
            note="Informations générales : les règles d’entrée et de santé changent. Vérifiez toujours auprès des autorités officielles et de la compagnie."),
        "en": dict(
            slug="en/guides/travelling-with-children", title="Flying with children: documents and tips",
            desc="Passport, travel consent, vaccines, infant fares: the checklist to prepare a flight with children, especially to Africa.",
            intro="A trip with children needs a little more lead time: some documents take several weeks.",
            sections=[
                ("Each child’s documents", [
                    "Every child, even a baby, needs their own travel document (passport, or ID card for some countries). Check the expiry date: some countries require it to be valid for several months after your return.",
                    "Also check the visa or entry authorisation for your destination: children are usually subject to the same rules as adults.",
                ]),
                ("Child travelling without both parents", [
                    "Many countries ask for a consent letter signed by the absent parent(s). Leaving France, a minor travelling without a holder of parental authority needs an exit authorisation form (Cerfa no. 15646) with a copy of the signing parent’s ID.",
                    "Rules differ by country: check with the consulate or the official government website of your departure country.",
                ]),
                ("Health and vaccines", [
                    "Some countries, particularly in Africa, require a yellow fever vaccination on entry, including for children from a certain age. See a travel clinic or your doctor several weeks before departure.",
                ]),
                ("Tickets and comfort on board", [
                    "- Babies under 2 usually travel on an adult’s lap at a reduced price; older children have their own seat.",
                    "- Choose seats together when booking: it is not always automatic on basic fares.",
                    "- Check the airline’s rules for strollers and car seats.",
                    "- Bring something to drink at take-off and landing for little ears.",
                ]),
            ],
            note="General information: entry and health rules change. Always check with official authorities and the airline."),
        "es": dict(
            slug="es/guias/viajar-con-ninos", title="Viajar en avión con niños: documentos y consejos",
            desc="Pasaporte, autorización de viaje, vacunas, tarifas de bebé: la lista para preparar un vuelo con niños, sobre todo a África.",
            intro="Un viaje con niños se prepara con algo más de antelación: algunos documentos tardan varias semanas.",
            sections=[
                ("Los documentos de cada niño", [
                    "Cada niño, incluso un bebé, necesita su propio documento de viaje (pasaporte, o DNI para algunos países). Revisa la caducidad: algunos países exigen que sea válido varios meses después del regreso.",
                    "Infórmate también sobre el visado o la autorización de entrada del país de destino: los niños suelen estar sujetos a las mismas normas que los adultos.",
                ]),
                ("Niño que viaja sin sus dos padres", [
                    "Muchos países piden una autorización firmada por el padre o la madre ausente. Para salir de Francia, un menor que viaja sin un titular de la patria potestad necesita el formulario de autorización de salida (Cerfa n.º 15646) con copia del documento del firmante.",
                    "Las normas cambian según el país: consulta al consulado o la web oficial del gobierno de tu país de salida.",
                ]),
                ("Salud y vacunas", [
                    "Algunos países, sobre todo en África, exigen la vacuna de la fiebre amarilla a la entrada, también para niños a partir de cierta edad. Consulta un centro de vacunación internacional o a tu médico varias semanas antes.",
                ]),
                ("Billetes y comodidad a bordo", [
                    "- Los bebés menores de 2 años suelen viajar en el regazo de un adulto con precio reducido; los mayores tienen su propio asiento.",
                    "- Elige asientos juntos al reservar: no siempre es automático en las tarifas básicas.",
                    "- Revisa las normas de la aerolínea para el carrito y la silla de coche.",
                    "- Lleva algo de beber para el despegue y el aterrizaje, por los oídos de los más pequeños.",
                ]),
            ],
            note="Información general: las normas de entrada y de salud cambian. Comprueba siempre con las autoridades oficiales y la aerolínea."),
        "pt": dict(
            slug="pt/guias/viajar-com-criancas", title="Viajar de avião com crianças: documentos e dicas",
            desc="Passaporte, autorização de viagem, vacinas, tarifas de bebé: a lista para preparar um voo com crianças, sobretudo para África.",
            intro="Uma viagem com crianças prepara-se com mais antecedência: alguns documentos demoram várias semanas.",
            sections=[
                ("Os documentos de cada criança", [
                    "Cada criança, mesmo um bebé, precisa do seu próprio documento de viagem (passaporte, ou cartão de cidadão para alguns países). Verifique a validade: alguns países exigem que seja válido vários meses após o regresso.",
                    "Informe-se também sobre o visto ou a autorização de entrada do país de destino: as crianças estão geralmente sujeitas às mesmas regras que os adultos.",
                ]),
                ("Criança que viaja sem os dois pais", [
                    "Muitos países pedem uma autorização assinada pelo pai ou mãe ausente. Para sair de França, um menor que viaja sem um titular das responsabilidades parentais precisa do formulário de autorização de saída (Cerfa n.º 15646) com cópia do documento do signatário.",
                    "As regras variam conforme o país: consulte o consulado ou o site oficial do governo do seu país de partida.",
                ]),
                ("Saúde e vacinas", [
                    "Alguns países, sobretudo em África, exigem a vacina contra a febre-amarela à entrada, também para crianças a partir de certa idade. Consulte uma consulta do viajante ou o seu médico várias semanas antes.",
                ]),
                ("Bilhetes e conforto a bordo", [
                    "- Os bebés com menos de 2 anos viajam geralmente ao colo de um adulto a preço reduzido; os mais velhos têm o seu próprio lugar.",
                    "- Escolha lugares juntos ao reservar: nem sempre é automático nas tarifas básicas.",
                    "- Verifique as regras da companhia para o carrinho e a cadeirinha.",
                    "- Leve algo para beber na descolagem e na aterragem, por causa dos ouvidos dos mais pequenos.",
                ]),
            ],
            note="Informação geral: as regras de entrada e de saúde mudam. Confirme sempre junto das autoridades oficiais e da companhia."),
        "ar": dict(
            slug="ar/guides/travelling-with-children", title="السفر بالطائرة مع الأطفال: الوثائق والنصائح",
            desc="جواز السفر وإذن السفر واللقاحات وأسعار الرضّع: قائمة لتحضير رحلة جوية مع الأطفال، خاصة إلى أفريقيا.",
            intro="السفر مع الأطفال يحتاج تحضيرًا مبكرًا قليلًا: بعض الوثائق يستغرق عدة أسابيع.",
            sections=[
                ("وثائق كل طفل", [
                    "يحتاج كل طفل، حتى الرضيع، إلى وثيقة سفر خاصة به (جواز سفر، أو بطاقة هوية لبعض الدول). تحقّق من تاريخ الصلاحية: بعض الدول تشترط صلاحيته لعدة أشهر بعد العودة.",
                    "تحقّق أيضًا من التأشيرة أو إذن الدخول لبلد الوجهة: يخضع الأطفال عادةً للقواعد نفسها مثل البالغين.",
                ]),
                ("طفل يسافر دون والديه معًا", [
                    "تطلب دول كثيرة إذنًا موقّعًا من الوالد الغائب. عند المغادرة من فرنسا، يحتاج القاصر الذي يسافر دون صاحب السلطة الأبوية إلى استمارة إذن الخروج (Cerfa رقم 15646) مع نسخة من هوية الوالد الموقّع.",
                    "القواعد تختلف حسب البلد: استفسر لدى القنصلية أو الموقع الحكومي الرسمي لبلد المغادرة.",
                ]),
                ("الصحة واللقاحات", [
                    "تشترط بعض الدول، خاصة في أفريقيا، لقاح الحمى الصفراء عند الدخول، بما في ذلك للأطفال ابتداءً من سن معينة. راجع مركز التطعيمات الدولية أو طبيبك قبل السفر بعدة أسابيع.",
                ]),
                ("التذاكر والراحة على متن الطائرة", [
                    "- يسافر الرضّع دون سنتين عادةً في حضن شخص بالغ بسعر مخفّض؛ والأكبر سنًا لهم مقعد خاص.",
                    "- اختر مقاعد متجاورة عند الحجز: ليس ذلك تلقائيًا دائمًا في الأسعار الأساسية.",
                    "- تحقّق من قواعد الشركة بشأن عربة الأطفال ومقعد السيارة.",
                    "- أحضر ما يُشرب عند الإقلاع والهبوط لراحة آذان الصغار.",
                ]),
            ],
            note="معلومات عامة: قواعد الدخول والصحة تتغير. تحقّق دائمًا لدى السلطات الرسمية وشركة الطيران."),
    },
    {
        "key": "checklist",
        "fr": dict(
            slug="guides/check-list-depart", title="Check-list avant de partir en voyage : ne rien oublier",
            desc="Papiers, santé, argent, téléphone, bagages : la liste à vérifier dans les semaines et les jours avant un vol vers l’Afrique, le Maghreb ou ailleurs.",
            intro="Un oubli peut coûter cher ou faire rater un vol. Voici les points à vérifier, dans l’ordre, pour partir l’esprit tranquille.",
            sections=[
                ("Plusieurs semaines avant le départ", [
                    "- Vérifiez la date de validité de votre passeport : beaucoup de pays demandent qu’il reste valable plusieurs mois après le retour.",
                    "- Renseignez-vous sur le visa ou l’autorisation d’entrée auprès de l’ambassade ou du site officiel du pays de destination : les délais peuvent être longs.",
                    "- Demandez à votre médecin ou à un centre de vaccinations internationales quels vaccins et traitements sont recommandés ou obligatoires.",
                    "- Pensez à une assurance voyage (santé, rapatriement, annulation) et vérifiez ce que couvre déjà votre carte bancaire.",
                ]),
                ("La semaine du départ", [
                    "- Prévenez votre banque de votre voyage et vérifiez les plafonds de paiement et de retrait de votre carte.",
                    "- Préparez votre téléphone : forfait à l’étranger ou eSIM, applications de la compagnie et de votre banque à jour.",
                    "- Faites une copie (photo ou fichier) de votre passeport, visa, billet et attestation d’assurance, et gardez-la à part.",
                    "- Vérifiez les règles de bagages de votre billet et pesez vos valises.",
                ]),
                ("La veille et le jour du vol", [
                    "- Enregistrez-vous en ligne quand c’est possible et gardez votre carte d’embarquement sur le téléphone ou imprimée.",
                    "- Vérifiez l’heure et le terminal de départ sur le site de la compagnie : ils peuvent changer.",
                    "- Gardez dans le bagage cabine les papiers, les médicaments, les chargeurs et une tenue de rechange.",
                    "- Arrivez à l’aéroport en avance, surtout pour un vol international et en période de vacances.",
                ]),
                ("En cas de problème", [
                    "Si votre vol est retardé ou annulé, gardez vos justificatifs (cartes d’embarquement, reçus). Selon la ligne et la compagnie, vous pouvez avoir droit à une assistance ou à une indemnisation.",
                ]),
            ],
            note="Les règles d’entrée, de santé et de bagages changent : vérifiez toujours auprès des autorités officielles et de votre compagnie avant de partir."),
        "en": dict(
            slug="en/guides/travel-checklist", title="Pre-trip checklist: don’t forget anything",
            desc="Documents, health, money, phone, baggage: what to check in the weeks and days before a flight to Africa, North Africa or anywhere else.",
            intro="One forgotten item can cost a lot or make you miss a flight. Here is what to check, in order, to leave with peace of mind.",
            sections=[
                ("Several weeks before departure", [
                    "- Check your passport’s expiry date: many countries require it to stay valid for several months after your return.",
                    "- Look up visa or entry authorisation rules with the embassy or the destination country’s official website: processing can take time.",
                    "- Ask your doctor or a travel vaccination centre which vaccines and treatments are recommended or required.",
                    "- Consider travel insurance (health, repatriation, cancellation) and check what your bank card already covers.",
                ]),
                ("The week of departure", [
                    "- Tell your bank about your trip and check your card’s payment and withdrawal limits.",
                    "- Get your phone ready: roaming plan or eSIM, airline and banking apps up to date.",
                    "- Keep a copy (photo or file) of your passport, visa, ticket and insurance certificate, stored separately.",
                    "- Check the baggage rules of your ticket and weigh your suitcases.",
                ]),
                ("The day before and the day of the flight", [
                    "- Check in online when possible and keep your boarding pass on your phone or printed.",
                    "- Check the departure time and terminal on the airline’s website: they can change.",
                    "- Keep documents, medication, chargers and a change of clothes in your cabin bag.",
                    "- Arrive at the airport early, especially for an international flight and during holidays.",
                ]),
                ("If something goes wrong", [
                    "If your flight is delayed or cancelled, keep your proof (boarding passes, receipts). Depending on the route and the airline, you may be entitled to assistance or compensation.",
                ]),
            ],
            note="Entry, health and baggage rules change: always check with the official authorities and your airline before you travel."),
        "es": dict(
            slug="es/guias/lista-antes-de-viajar", title="Lista antes de viajar: no olvides nada",
            desc="Documentos, salud, dinero, teléfono, equipaje: qué revisar en las semanas y los días antes de un vuelo a África, el Magreb o cualquier destino.",
            intro="Un olvido puede salir caro o hacerte perder un vuelo. Esto es lo que conviene revisar, en orden, para viajar tranquilo.",
            sections=[
                ("Varias semanas antes de salir", [
                    "- Revisa la fecha de caducidad de tu pasaporte: muchos países exigen que siga vigente varios meses después del regreso.",
                    "- Infórmate sobre el visado o la autorización de entrada en la embajada o la web oficial del país de destino: los plazos pueden ser largos.",
                    "- Pregunta a tu médico o a un centro de vacunación internacional qué vacunas y tratamientos se recomiendan o son obligatorios.",
                    "- Piensa en un seguro de viaje (salud, repatriación, cancelación) y revisa lo que ya cubre tu tarjeta bancaria.",
                ]),
                ("La semana de la salida", [
                    "- Avisa a tu banco del viaje y revisa los límites de pago y de retirada de tu tarjeta.",
                    "- Prepara el teléfono: tarifa en el extranjero o eSIM, aplicaciones de la aerolínea y del banco actualizadas.",
                    "- Guarda una copia (foto o archivo) del pasaporte, visado, billete y certificado del seguro, aparte de los originales.",
                    "- Revisa las normas de equipaje de tu billete y pesa tus maletas.",
                ]),
                ("La víspera y el día del vuelo", [
                    "- Haz el check-in en línea cuando sea posible y lleva la tarjeta de embarque en el móvil o impresa.",
                    "- Comprueba la hora y la terminal de salida en la web de la aerolínea: pueden cambiar.",
                    "- Lleva en el equipaje de mano los documentos, los medicamentos, los cargadores y una muda de ropa.",
                    "- Llega pronto al aeropuerto, sobre todo en vuelos internacionales y en temporada de vacaciones.",
                ]),
                ("Si hay un problema", [
                    "Si tu vuelo se retrasa o se cancela, guarda los justificantes (tarjetas de embarque, recibos). Según la ruta y la aerolínea, puedes tener derecho a asistencia o a una compensación.",
                ]),
            ],
            note="Las normas de entrada, sanitarias y de equipaje cambian: consulta siempre a las autoridades oficiales y a tu aerolínea antes de viajar."),
        "pt": dict(
            slug="pt/guias/lista-antes-de-viajar", title="Lista antes de viajar: não se esqueça de nada",
            desc="Documentos, saúde, dinheiro, telemóvel, bagagem: o que verificar nas semanas e nos dias antes de um voo para África, o Magrebe ou outro destino.",
            intro="Um esquecimento pode sair caro ou fazer perder um voo. Eis o que verificar, por ordem, para partir tranquilo.",
            sections=[
                ("Várias semanas antes da partida", [
                    "- Verifique a validade do passaporte: muitos países exigem que continue válido vários meses após o regresso.",
                    "- Informe-se sobre o visto ou a autorização de entrada junto da embaixada ou do site oficial do país de destino: os prazos podem ser longos.",
                    "- Pergunte ao seu médico ou a um centro de vacinação internacional que vacinas e tratamentos são recomendados ou obrigatórios.",
                    "- Pense num seguro de viagem (saúde, repatriamento, cancelamento) e veja o que o seu cartão bancário já cobre.",
                ]),
                ("Na semana da partida", [
                    "- Avise o banco da viagem e verifique os limites de pagamento e levantamento do cartão.",
                    "- Prepare o telemóvel: tarifário no estrangeiro ou eSIM, aplicações da companhia e do banco atualizadas.",
                    "- Guarde uma cópia (foto ou ficheiro) do passaporte, visto, bilhete e certificado do seguro, separada dos originais.",
                    "- Verifique as regras de bagagem do seu bilhete e pese as malas.",
                ]),
                ("Na véspera e no dia do voo", [
                    "- Faça o check-in online quando possível e tenha o cartão de embarque no telemóvel ou impresso.",
                    "- Confirme a hora e o terminal de partida no site da companhia: podem mudar.",
                    "- Leve na bagagem de mão os documentos, os medicamentos, os carregadores e uma muda de roupa.",
                    "- Chegue cedo ao aeroporto, sobretudo num voo internacional e em época de férias.",
                ]),
                ("Se houver um problema", [
                    "Se o voo atrasar ou for cancelado, guarde os comprovativos (cartões de embarque, recibos). Conforme a rota e a companhia, pode ter direito a assistência ou a uma indemnização.",
                ]),
            ],
            note="As regras de entrada, de saúde e de bagagem mudam: confirme sempre junto das autoridades oficiais e da companhia antes de viajar."),
        "ar": dict(
            slug="ar/guides/travel-checklist", title="قائمة التحقق قبل السفر: لا تنسَ شيئًا",
            desc="الوثائق والصحة والمال والهاتف والأمتعة: ما يجب التحقق منه في الأسابيع والأيام التي تسبق رحلة إلى أفريقيا أو المغرب العربي أو أي وجهة أخرى.",
            intro="قد يكلّفك نسيان أمر واحد الكثير أو يجعلك تفوّت رحلتك. إليك ما يجب التحقق منه بالترتيب لتسافر مطمئنًا.",
            sections=[
                ("قبل السفر بعدة أسابيع", [
                    "- تحقّق من تاريخ انتهاء جواز سفرك: تشترط دول كثيرة أن يبقى صالحًا عدة أشهر بعد العودة.",
                    "- استعلم عن التأشيرة أو إذن الدخول لدى السفارة أو الموقع الرسمي لبلد الوجهة: قد تطول المدة.",
                    "- اسأل طبيبك أو مركز التطعيمات الدولية عن اللقاحات والعلاجات الموصى بها أو الإلزامية.",
                    "- فكّر في تأمين سفر (صحة، إعادة إلى الوطن، إلغاء) وتحقّق مما تغطيه بطاقتك المصرفية أصلًا.",
                ]),
                ("في أسبوع السفر", [
                    "- أبلغ مصرفك بسفرك وتحقّق من حدود الدفع والسحب لبطاقتك.",
                    "- جهّز هاتفك: باقة تجوال أو شريحة eSIM، وتطبيقات شركة الطيران والمصرف محدّثة.",
                    "- احتفظ بنسخة (صورة أو ملف) من جواز السفر والتأشيرة والتذكرة وشهادة التأمين، بعيدًا عن الأصول.",
                    "- تحقّق من قواعد الأمتعة في تذكرتك وزِن حقائبك.",
                ]),
                ("في اليوم السابق ويوم الرحلة", [
                    "- سجّل الدخول عبر الإنترنت إن أمكن واحتفظ ببطاقة الصعود على هاتفك أو مطبوعة.",
                    "- تحقّق من وقت المغادرة والمبنى على موقع شركة الطيران: قد يتغيران.",
                    "- ضع في حقيبة اليد الوثائق والأدوية والشواحن وملابس احتياطية.",
                    "- اذهب إلى المطار مبكرًا، خاصة في الرحلات الدولية وفترات العطل.",
                ]),
                ("إذا حدثت مشكلة", [
                    "إذا تأخرت رحلتك أو أُلغيت، احتفظ بالإثباتات (بطاقات الصعود والإيصالات). بحسب الخط وشركة الطيران، قد يحق لك الحصول على مساعدة أو تعويض.",
                ]),
            ],
            note="تتغير قواعد الدخول والصحة والأمتعة: تحقّق دائمًا لدى السلطات الرسمية وشركة الطيران قبل السفر."),
    },
]

INDEX = {
    "fr": dict(slug="guides", title="Guides pratiques du voyage", lead="Bagages, meilleur moment pour réserver, voyage avec des enfants, check-list avant le départ : nos conseils pour payer moins cher et voyager serein.", more="Lire le guide"),
    "en": dict(slug="en/guides", title="Practical travel guides", lead="Baggage, the best time to book, flying with children, a pre-trip checklist: our tips to pay less and travel with peace of mind.", more="Read the guide"),
    "es": dict(slug="es/guias", title="Guías prácticas de viaje", lead="Equipaje, el mejor momento para reservar, viajar con niños, la lista antes de viajar: nuestros consejos para pagar menos y viajar tranquilo.", more="Leer la guía"),
    "pt": dict(slug="pt/guias", title="Guias práticos de viagem", lead="Bagagem, o melhor momento para reservar, viajar com crianças, a lista antes de viajar: as nossas dicas para pagar menos e viajar tranquilo.", more="Ler o guia"),
    "ar": dict(slug="ar/guides", title="أدلة السفر العملية", lead="الأمتعة وأفضل وقت للحجز والسفر مع الأطفال وقائمة التحقق قبل السفر: نصائحنا لتدفع أقل وتسافر براحة.", more="اقرأ الدليل"),
}
