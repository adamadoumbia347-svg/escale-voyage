"""Traductions des pages trajets et hôtels : anglais, espagnol, portugais, arabe.

Chaque entrée : (en, es, pt, ar). Les clés sont les textes français de scripts/build_pages.py.
Pour ajouter une langue : ajouter une colonne partout et une entrée dans LANGS (build_pages.py).
"""

CITIES = {
    "Paris": ("Paris", "París", "Paris", "باريس"),
    "Bruxelles": ("Brussels", "Bruselas", "Bruxelas", "بروكسل"),
    "Marseille": ("Marseille", "Marsella", "Marselha", "مرسيليا"),
    "Lyon": ("Lyon", "Lyon", "Lyon", "ليون"),
    "Genève": ("Geneva", "Ginebra", "Genebra", "جنيف"),
    "Bamako": ("Bamako", "Bamako", "Bamako", "باماكو"),
    "Dakar": ("Dakar", "Dakar", "Dacar", "داكار"),
    "Abidjan": ("Abidjan", "Abiyán", "Abidjan", "أبيدجان"),
    "Conakry": ("Conakry", "Conakri", "Conacri", "كوناكري"),
    "Douala": ("Douala", "Duala", "Douala", "دوالا"),
    "Lomé": ("Lomé", "Lomé", "Lomé", "لومي"),
    "Cotonou": ("Cotonou", "Cotonú", "Cotonou", "كوتونو"),
    "Ouagadougou": ("Ouagadougou", "Uagadugú", "Uagadugu", "واغادوغو"),
    "Kinshasa": ("Kinshasa", "Kinsasa", "Kinshasa", "كينشاسا"),
    "Casablanca": ("Casablanca", "Casablanca", "Casablanca", "الدار البيضاء"),
    "Alger": ("Algiers", "Argel", "Argel", "الجزائر العاصمة"),
    "Tunis": ("Tunis", "Túnez", "Túnis", "تونس العاصمة"),
    "Montréal": ("Montreal", "Montreal", "Montreal", "مونتريال"),
    "Dubaï": ("Dubai", "Dubái", "Dubai", "دبي"),
    "Libreville": ("Libreville", "Libreville", "Libreville", "ليبرفيل"),
    "Yaoundé": ("Yaoundé", "Yaundé", "Iaundé", "ياوندي"),
    "Nouakchott": ("Nouakchott", "Nuakchot", "Nouakchott", "نواكشوط"),
    "Niamey": ("Niamey", "Niamey", "Niamey", "نيامي"),
    "Marrakech": ("Marrakesh", "Marrakech", "Marraquexe", "مراكش"),
    "Istanbul": ("Istanbul", "Estambul", "Istambul", "إسطنبول"),
    "Djeddah": ("Jeddah", "Yeda", "Jidá", "جدة"),
    "Pointe-à-Pitre": ("Pointe-à-Pitre", "Pointe-à-Pitre", "Pointe-à-Pitre", "بوانت آ بيتر"),
    "La Réunion": ("Réunion", "Reunión", "Reunião", "لا ريونيون"),
}

COUNTRIES = {
    "Algérie": ("Algeria", "Argelia", "Argélia", "الجزائر"),
    "Arabie saoudite": ("Saudi Arabia", "Arabia Saudí", "Arábia Saudita", "السعودية"),
    "Burkina Faso": ("Burkina Faso", "Burkina Faso", "Burkina Faso", "بوركينا فاسو"),
    "Bénin": ("Benin", "Benín", "Benim", "بنين"),
    "Cameroun": ("Cameroon", "Camerún", "Camarões", "الكاميرون"),
    "Canada": ("Canada", "Canadá", "Canadá", "كندا"),
    "Côte d'Ivoire": ("Côte d'Ivoire", "Costa de Marfil", "Costa do Marfim", "ساحل العاج"),
    "France": ("France", "Francia", "França", "فرنسا"),
    "Gabon": ("Gabon", "Gabón", "Gabão", "الغابون"),
    "Guadeloupe": ("Guadeloupe", "Guadalupe", "Guadalupe", "غوادلوب"),
    "Guinée": ("Guinea", "Guinea", "Guiné", "غينيا"),
    "La Réunion": ("Réunion", "Reunión", "Reunião", "لا ريونيون"),
    "Mali": ("Mali", "Malí", "Mali", "مالي"),
    "Maroc": ("Morocco", "Marruecos", "Marrocos", "المغرب"),
    "Mauritanie": ("Mauritania", "Mauritania", "Mauritânia", "موريتانيا"),
    "Niger": ("Niger", "Níger", "Níger", "النيجر"),
    "RD Congo": ("DR Congo", "R. D. del Congo", "RD Congo", "الكونغو الديمقراطية"),
    "Sénégal": ("Senegal", "Senegal", "Senegal", "السنغال"),
    "Togo": ("Togo", "Togo", "Togo", "توغو"),
    "Tunisie": ("Tunisia", "Túnez", "Tunísia", "تونس"),
    "Turquie": ("Turkey", "Turquía", "Turquia", "تركيا"),
    "Émirats arabes unis": ("United Arab Emirates", "Emiratos Árabes Unidos", "Emirados Árabes Unidos", "الإمارات"),
}

PEAKS = {
    "de novembre à mars, quand il fait moins chaud": (
        "November to March, when it is cooler", "de noviembre a marzo, cuando hace menos calor",
        "de novembro a março, quando faz menos calor", "من نوفمبر إلى مارس، حين يكون الطقس أقل حرارة"),
    "juillet-août et décembre-janvier": (
        "July–August and December–January", "julio-agosto y diciembre-enero", "julho-agosto e dezembro-janeiro",
        "يوليو وأغسطس، وديسمبر ويناير"),
    "juillet-août et l'Aïd": (
        "July–August and Eid", "julio-agosto y el Eid", "julho-agosto e o Eid", "يوليو وأغسطس والعيد"),
    "juillet-août et les fêtes de fin d'année": (
        "July–August and the year-end holidays", "julio-agosto y las fiestas de fin de año",
        "julho-agosto e as festas de fim de ano", "يوليو وأغسطس وعطلات نهاية السنة"),
    "juillet-août et les vacances de printemps": (
        "July–August and the spring holidays", "julio-agosto y las vacaciones de primavera",
        "julho-agosto e as férias da primavera", "يوليو وأغسطس وعطلة الربيع"),
    "juillet-août, Noël et le carnaval": (
        "July–August, Christmas and Carnival", "julio-agosto, Navidad y el carnaval", "julho-agosto, Natal e o carnaval",
        "يوليو وأغسطس وعيد الميلاد والكرنفال"),
    "juillet-août, l'Aïd et les vacances scolaires": (
        "July–August, Eid and the school holidays", "julio-agosto, el Eid y las vacaciones escolares",
        "julho-agosto, o Eid e as férias escolares", "يوليو وأغسطس والعيد والعطل المدرسية"),
    "juillet-août, les fêtes de fin d'année et la Tabaski": (
        "July–August, the year-end holidays and Tabaski", "julio-agosto, las fiestas de fin de año y la Tabaski",
        "julho-agosto, as festas de fim de ano e a Tabaski", "يوليو وأغسطس وعطلات نهاية السنة وعيد الأضحى (تاباسكي)"),
    "juillet-août, les fêtes de fin d'année, la Tabaski et le Magal de Touba": (
        "July–August, the year-end holidays, Tabaski and the Grand Magal of Touba",
        "julio-agosto, las fiestas de fin de año, la Tabaski y el Magal de Touba",
        "julho-agosto, as festas de fim de ano, a Tabaski e o Magal de Touba",
        "يوليو وأغسطس وعطلات نهاية السنة وعيد الأضحى (تاباسكي) وماغال طوبى"),
    "juillet-août, les vacances scolaires et l'Aïd": (
        "July–August, the school holidays and Eid", "julio-agosto, las vacaciones escolares y el Eid",
        "julho-agosto, as férias escolares e o Eid", "يوليو وأغسطس والعطل المدرسية والعيد"),
    "le Ramadan, le Hajj et les vacances scolaires": (
        "Ramadan, Hajj and the school holidays", "el Ramadán, el Hach y las vacaciones escolares",
        "o Ramadão, o Hajj e as férias escolares", "رمضان وموسم الحج والعطل المدرسية"),
    "les vacances scolaires, Noël et Pâques": (
        "the school holidays, Christmas and Easter", "las vacaciones escolares, Navidad y Semana Santa",
        "as férias escolares, o Natal e a Páscoa", "العطل المدرسية وعيد الميلاد وعيد الفصح"),
}

NOTES = {
    "CDG-BKO": (
        "Direct flights from Paris are rare or suspended at times: most trips connect via Casablanca, Algiers, Tunis, Istanbul or Addis Ababa. Compare the total travel time, not just the price.",
        "Los vuelos directos desde París son escasos o se suspenden según la época: la mayoría hace escala en Casablanca, Argel, Túnez, Estambul o Adís Abeba. Compara la duración total, no solo el precio.",
        "Os voos diretos a partir de Paris são raros ou suspensos conforme a época: a maioria faz escala em Casablanca, Argel, Túnis, Istambul ou Adis Abeba. Compare a duração total, não só o preço.",
        "الرحلات المباشرة من باريس نادرة أو متوقفة أحيانًا: معظم الرحلات تمر عبر الدار البيضاء أو الجزائر أو تونس أو إسطنبول أو أديس أبابا. قارن مدة الرحلة الإجمالية وليس السعر فقط."),
    "CDG-DSS": (
        "Flights also leave from Orly: select both Paris airports in the comparison sites to widen your choice.",
        "También hay vuelos desde Orly: marca los dos aeropuertos de París en los comparadores para tener más opciones.",
        "Também há voos a partir de Orly: selecione os dois aeroportos de Paris nos comparadores para ter mais opções.",
        "توجد رحلات من مطار أورلي أيضًا: اختر مطارَي باريس معًا في مواقع المقارنة لتوسيع الخيارات."),
    "CDG-ABJ": (
        "Several airlines fly the route from Roissy and Orly: competition often pushes prices down in the low season.",
        "Varias aerolíneas cubren la ruta desde Roissy y Orly: la competencia suele bajar los precios en temporada baja.",
        "Várias companhias fazem a rota a partir de Roissy e Orly: a concorrência costuma baixar os preços na época baixa.",
        "عدة شركات طيران تسيّر هذا الخط من مطارَي رواسي وأورلي: المنافسة تخفض الأسعار غالبًا خارج موسم الذروة."),
    "CDG-CKY": (
        "Flights with a stop in Casablanca, Dakar or Brussels are sometimes much cheaper than the direct flight.",
        "Los vuelos con escala en Casablanca, Dakar o Bruselas a veces son bastante más baratos que el directo.",
        "Os voos com escala em Casablanca, Dacar ou Bruxelas às vezes são bem mais baratos do que o direto.",
        "الرحلات مع توقف في الدار البيضاء أو داكار أو بروكسل تكون أحيانًا أرخص بكثير من الرحلة المباشرة."),
    "CDG-DLA": (
        "Also consider Yaoundé-Nsimalen (NSI) if your final destination is in the centre of the country.",
        "Considera también Yaundé-Nsimalen (NSI) si tu destino final está en el centro del país.",
        "Considere também Iaundé-Nsimalen (NSI) se o seu destino final for no centro do país.",
        "فكّر أيضًا في مطار ياوندي-نسيمالين (NSI) إذا كانت وجهتك النهائية في وسط البلاد."),
    "CDG-LFW": (
        "Compare with a flight to Cotonou (COO) or Accra (ACC) and then the road: it is sometimes cheaper.",
        "Compara con un vuelo a Cotonú (COO) o Acra (ACC) y después la carretera: a veces sale más barato.",
        "Compare com um voo para Cotonou (COO) ou Acra (ACC) seguido de estrada: às vezes sai mais barato.",
        "قارن مع رحلة إلى كوتونو (COO) أو أكرا (ACC) ثم الطريق البري: يكون ذلك أرخص أحيانًا."),
    "CDG-COO": (
        "Compare with Lomé (LFW): the two cities are close and prices vary a lot.",
        "Compara con Lomé (LFW): las dos ciudades están cerca y los precios varían mucho.",
        "Compare com Lomé (LFW): as duas cidades são próximas e os preços variam muito.",
        "قارن مع لومي (LFW): المدينتان متقاربتان والأسعار تختلف كثيرًا."),
    "CDG-OUA": (
        "Direct flight options vary with the situation: trips connecting via Abidjan, Casablanca, Algiers or Istanbul are common.",
        "La oferta de vuelos directos varía según la situación: son habituales los trayectos con escala en Abiyán, Casablanca, Argel o Estambul.",
        "A oferta de voos diretos varia conforme a situação: são comuns as viagens com escala em Abidjan, Casablanca, Argel ou Istambul.",
        "تتغير الرحلات المباشرة حسب الظروف: الرحلات مع توقف في أبيدجان أو الدار البيضاء أو الجزائر أو إسطنبول شائعة."),
    "BRU-FIH": (
        "From Paris, compare with a departure from Brussels: it is often better value, even with the train ticket.",
        "Desde París, compara con una salida desde Bruselas: suele salir mejor, incluso sumando el tren.",
        "A partir de Paris, compare com uma partida de Bruxelas: costuma compensar, mesmo somando o comboio.",
        "من باريس، قارن مع الانطلاق من بروكسل: غالبًا يكون أوفر حتى مع ثمن القطار."),
    "ORY-CMN": (
        "Low-cost airlines also fly to Marrakesh, Rabat and Tangier: look at the city closest to your destination.",
        "Las aerolíneas de bajo coste también vuelan a Marrakech, Rabat y Tánger: mira la ciudad más cercana a tu destino.",
        "As companhias low-cost também voam para Marraquexe, Rabat e Tânger: veja a cidade mais próxima do seu destino.",
        "تخدم شركات الطيران منخفضة التكلفة أيضًا مراكش والرباط وطنجة: اختر المدينة الأقرب إلى وجهتك."),
    "CDG-ALG": (
        "Compare with Lyon, Marseille or Bordeaux if you can leave from another city: summer prices vary a lot between airports.",
        "Compara con Lyon, Marsella o Burdeos si puedes salir desde otra ciudad: los precios de verano cambian mucho entre aeropuertos.",
        "Compare com Lyon, Marselha ou Bordéus se puder partir de outra cidade: os preços de verão mudam muito entre aeroportos.",
        "قارن مع ليون أو مرسيليا أو بوردو إن أمكنك السفر من مدينة أخرى: أسعار الصيف تختلف كثيرًا من مطار لآخر."),
    "CDG-TUN": (
        "Also consider Djerba (DJE) and Monastir (MIR), often served by cheaper flights in summer.",
        "Considera también Yerba (DJE) y Monastir (MIR), con vuelos a menudo más baratos en verano.",
        "Considere também Djerba (DJE) e Monastir (MIR), muitas vezes com voos mais baratos no verão.",
        "فكّر أيضًا في جربة (DJE) والمنستير (MIR)، وغالبًا ما تكون رحلاتهما أرخص في الصيف."),
    "CDG-YUL": (
        "Most travellers need an Electronic Travel Authorization (eTA): check before you book.",
        "La mayoría de los viajeros necesita una Autorización Electrónica de Viaje (eTA): compruébalo antes de reservar.",
        "A maioria dos viajantes precisa de uma Autorização Eletrónica de Viagem (eTA): verifique antes de reservar.",
        "يحتاج معظم المسافرين إلى تصريح سفر إلكتروني (eTA): تحقق من ذلك قبل الحجز."),
    "CDG-DXB": (
        "Dubai is also a handy stopover towards Asia and East Africa: a few days' stop sometimes costs nothing extra.",
        "Dubái también es una escala práctica hacia Asia y África oriental: una parada de unos días a veces no cuesta más.",
        "Dubai também é uma escala prática para a Ásia e a África Oriental: uma paragem de alguns dias às vezes não custa mais.",
        "دبي محطة توقف عملية نحو آسيا وشرق أفريقيا: التوقف لبضعة أيام لا يكلّف أحيانًا شيئًا إضافيًا."),
    "CDG-FIH": (
        "Compare with a departure from Brussels, traditionally very well connected to Kinshasa: the price gap can cover the Paris–Brussels train.",
        "Compara con una salida desde Bruselas, tradicionalmente muy bien conectada con Kinsasa: la diferencia puede cubrir el tren París–Bruselas.",
        "Compare com uma partida de Bruxelas, tradicionalmente muito bem ligada a Kinshasa: a diferença pode pagar o comboio Paris–Bruxelas.",
        "قارن مع الانطلاق من بروكسل، المرتبطة تقليديًا بكينشاسا بشكل جيد جدًا: فرق السعر قد يغطي قطار باريس–بروكسل."),
    "CDG-LBV": (
        "Few airlines fly the route direct: book early for summer and also look at connections via Casablanca, Addis Ababa or Douala.",
        "Pocas aerolíneas vuelan directo: reserva pronto para el verano y mira también escalas en Casablanca, Adís Abeba o Duala.",
        "Poucas companhias voam direto: reserve cedo para o verão e veja também escalas em Casablanca, Adis Abeba ou Douala.",
        "قليل من الشركات تسيّر رحلات مباشرة: احجز مبكرًا للصيف وابحث أيضًا عن رحلات عبر الدار البيضاء أو أديس أبابا أو دوالا."),
    "CDG-NSI": (
        "Compare with Douala (DLA): depending on the dates, landing in Douala and taking the road or a domestic flight can be cheaper.",
        "Compara con Duala (DLA): según las fechas, llegar a Duala y seguir por carretera o en vuelo interno puede salir más barato.",
        "Compare com Douala (DLA): conforme as datas, chegar a Douala e seguir por estrada ou voo doméstico pode sair mais barato.",
        "قارن مع دوالا (DLA): حسب التواريخ، قد يكون الوصول إلى دوالا ثم الطريق البري أو رحلة داخلية أرخص."),
    "CDG-NKC": (
        "Trips with a stop in Casablanca, Tunis or Dakar are common: compare the connection time.",
        "Son habituales los trayectos con escala en Casablanca, Túnez o Dakar: compara el tiempo de conexión.",
        "São comuns as viagens com escala em Casablanca, Túnis ou Dacar: compare o tempo de ligação.",
        "الرحلات مع توقف في الدار البيضاء أو تونس أو داكار شائعة: قارن مدة الانتظار بين الرحلتين."),
    "CDG-NIM": (
        "Flight options change with the situation: use the comparison sites to see which connections are available (Casablanca, Algiers, Istanbul, Addis Ababa…).",
        "La oferta de vuelos cambia según la situación: usa los comparadores para ver las escalas disponibles (Casablanca, Argel, Estambul, Adís Abeba…).",
        "A oferta de voos muda conforme a situação: use os comparadores para ver as escalas disponíveis (Casablanca, Argel, Istambul, Adis Abeba…).",
        "تتغير الرحلات المتاحة حسب الظروف: استخدم مواقع المقارنة لمعرفة محطات التوقف المتاحة (الدار البيضاء، الجزائر، إسطنبول، أديس أبابا…)."),
    "CDG-RAK": (
        "Many low-cost flights leave from Orly and Beauvais: check all three Paris airports.",
        "Muchos vuelos de bajo coste salen de Orly y Beauvais: revisa los tres aeropuertos de París.",
        "Muitos voos low-cost partem de Orly e Beauvais: verifique os três aeroportos de Paris.",
        "كثير من الرحلات منخفضة التكلفة تنطلق من أورلي وبوفيه: تحقق من مطارات باريس الثلاثة."),
    "CDG-IST": (
        "Also consider Sabiha Gökçen airport (SAW), on the Asian side, often served by cheaper airlines.",
        "Considera también el aeropuerto Sabiha Gökçen (SAW), en el lado asiático, con aerolíneas a menudo más baratas.",
        "Considere também o aeroporto Sabiha Gökçen (SAW), do lado asiático, muitas vezes com companhias mais baratas.",
        "فكّر أيضًا في مطار صبيحة كوكجن (SAW) في الجانب الآسيوي، وغالبًا ما تخدمه شركات أرخص."),
    "CDG-JED": (
        "For Umrah, book as early as possible before Ramadan: prices rise sharply. Medina (MED) is an alternative arrival airport.",
        "Para la Umrah, reserva lo antes posible antes del Ramadán: los precios suben mucho. Medina (MED) es una alternativa de llegada.",
        "Para a Umrah, reserve o mais cedo possível antes do Ramadão: os preços sobem muito. Medina (MED) é uma alternativa de chegada.",
        "للعمرة، احجز في أقرب وقت ممكن قبل رمضان: ترتفع الأسعار كثيرًا. المدينة المنورة (MED) بديل للوصول."),
    "CDG-PTP": (
        "Flights leave from Roissy and Orly: compare both, price gaps are common.",
        "Hay vuelos desde Roissy y Orly: compara los dos, las diferencias son frecuentes.",
        "Há voos a partir de Roissy e Orly: compare os dois, as diferenças são frequentes.",
        "تنطلق الرحلات من رواسي وأورلي: قارن بينهما، ففروق الأسعار شائعة."),
    "CDG-RUN": (
        "Also compare arriving at Saint-Pierre Pierrefonds (ZSE) if you are heading to the south of the island.",
        "Compara también la llegada a Saint-Pierre Pierrefonds (ZSE) si vas al sur de la isla.",
        "Compare também a chegada a Saint-Pierre Pierrefonds (ZSE) se for para o sul da ilha.",
        "قارن أيضًا الوصول إلى مطار سان بيير بيرفون (ZSE) إذا كنت متجهًا إلى جنوب الجزيرة."),
    "MRS-ALG": (
        "In summer prices climb very fast: book in spring and compare with a departure from Lyon or Montpellier.",
        "En verano los precios suben muy rápido: reserva en primavera y compara con una salida desde Lyon o Montpellier.",
        "No verão os preços sobem muito depressa: reserve na primavera e compare com uma partida de Lyon ou Montpellier.",
        "في الصيف ترتفع الأسعار بسرعة كبيرة: احجز في الربيع وقارن مع الانطلاق من ليون أو مونبلييه."),
    "MRS-TUN": (
        "Compare with Djerba (DJE) and Monastir (MIR) depending on your final destination.",
        "Compara con Yerba (DJE) y Monastir (MIR) según tu destino final.",
        "Compare com Djerba (DJE) e Monastir (MIR) conforme o seu destino final.",
        "قارن مع جربة (DJE) والمنستير (MIR) حسب وجهتك النهائية."),
    "MRS-DSS": (
        "Compare a flight from Marseille with a stop against a train to Paris followed by a direct flight: the second is sometimes cheaper.",
        "Compara un vuelo con escala desde Marsella con un tren a París y un vuelo directo: lo segundo a veces es más barato.",
        "Compare um voo com escala a partir de Marselha com um comboio até Paris seguido de um voo direto: o segundo às vezes é mais barato.",
        "قارن بين رحلة من مرسيليا مع توقف، وبين قطار إلى باريس ثم رحلة مباشرة: الخيار الثاني أرخص أحيانًا."),
    "LYS-CMN": (
        "Also look at Lyon–Marrakesh and Lyon–Oujda flights depending on your final destination.",
        "Mira también los vuelos Lyon–Marrakech y Lyon–Uchda según tu destino final.",
        "Veja também os voos Lyon–Marraquexe e Lyon–Oujda conforme o seu destino final.",
        "ابحث أيضًا عن رحلات ليون–مراكش وليون–وجدة حسب وجهتك النهائية."),
    "LYS-DSS": (
        "Compare with a departure from Geneva, under 2 hours from Lyon: there are sometimes more options.",
        "Compara con una salida desde Ginebra, a menos de 2 horas de Lyon: a veces hay más opciones.",
        "Compare com uma partida de Genebra, a menos de 2 horas de Lyon: às vezes há mais opções.",
        "قارن مع الانطلاق من جنيف، على بعد أقل من ساعتين من ليون: الخيارات هناك أوسع أحيانًا."),
    "BRU-DSS": (
        "From northern France, compare with Paris: the price difference often covers the train.",
        "Desde el norte de Francia, compara con París: la diferencia de precio suele cubrir el tren.",
        "A partir do norte de França, compare com Paris: a diferença de preço costuma pagar o comboio.",
        "من شمال فرنسا، قارن مع باريس: فرق السعر يغطي ثمن القطار غالبًا."),
    "BRU-ABJ": (
        "Compare with a departure from Paris: competition is stronger there and deals are more frequent.",
        "Compara con una salida desde París: allí hay más competencia y más ofertas.",
        "Compare com uma partida de Paris: lá a concorrência é maior e as promoções mais frequentes.",
        "قارن مع الانطلاق من باريس: المنافسة هناك أقوى والعروض أكثر."),
    "BRU-DLA": (
        "Compare the total travel time: some flights make a technical stop in West or Central Africa.",
        "Compara la duración total: algunos vuelos hacen una escala técnica en África occidental o central.",
        "Compare a duração total: alguns voos fazem uma escala técnica na África Ocidental ou Central.",
        "قارن مدة الرحلة الإجمالية: بعض الرحلات تتوقف توقفًا فنيًا في غرب أفريقيا أو وسطها."),
    "GVA-CMN": (
        "If you live in neighbouring France, compare with Lyon: both airports are less than 2 hours away.",
        "Si vives en la Francia vecina, compara con Lyon: los dos aeropuertos están a menos de 2 horas.",
        "Se vive na França vizinha, compare com Lyon: os dois aeroportos ficam a menos de 2 horas.",
        "إذا كنت تسكن في فرنسا المجاورة، قارن مع ليون: المطاران على بعد أقل من ساعتين."),
    "GVA-DSS": (
        "Flights often connect via Paris, Brussels, Lisbon or Casablanca: compare the layover time.",
        "Los vuelos suelen hacer escala en París, Bruselas, Lisboa o Casablanca: compara la duración de la escala.",
        "Os voos fazem muitas vezes escala em Paris, Bruxelas, Lisboa ou Casablanca: compare a duração da escala.",
        "غالبًا ما تمر الرحلات عبر باريس أو بروكسل أو لشبونة أو الدار البيضاء: قارن مدة التوقف."),
}

HOTEL_TIPS = {
    "Dakar": (
        "Blaise Diagne airport is far from the centre (about 45 km): for a late arrival, a night near the airport or in Saly can be more practical.",
        "El aeropuerto Blaise Diagne está lejos del centro (unos 45 km): si llegas tarde, una noche cerca del aeropuerto o en Saly puede ser más práctica.",
        "O aeroporto Blaise Diagne fica longe do centro (cerca de 45 km): para uma chegada tardia, uma noite perto do aeroporto ou em Saly pode ser mais prática.",
        "مطار بليز دياني بعيد عن وسط المدينة (حوالي 45 كم): عند الوصول متأخرًا، قد تكون ليلة قرب المطار أو في سالي أكثر عملية."),
    "Abidjan": (
        "Marcory and Zone 4 are the closest areas to Félix-Houphouët-Boigny airport: handy for a short stay.",
        "Marcory y la Zona 4 son los barrios más cercanos al aeropuerto Félix-Houphouët-Boigny: prácticos para una estancia corta.",
        "Marcory e a Zona 4 são os bairros mais próximos do aeroporto Félix-Houphouët-Boigny: práticos para uma estadia curta.",
        "ماركوري والمنطقة 4 هما الأقرب إلى مطار فيليكس هوفويت بوانيي: مناسبان للإقامة القصيرة."),
    "Bamako": (
        "Check your government's travel advice before booking, and prefer free cancellation.",
        "Consulta las recomendaciones de viaje de tu gobierno antes de reservar y elige cancelación gratuita.",
        "Consulte os conselhos de viagem do seu governo antes de reservar e prefira o cancelamento gratuito.",
        "اطّلع على إرشادات السفر الصادرة عن حكومتك قبل الحجز، وفضّل الحجوزات القابلة للإلغاء مجانًا."),
    "Casablanca": (
        "A train links Mohammed V airport to the centre: no need to pay for a hotel near the airport.",
        "Un tren une el aeropuerto Mohammed V con el centro: no hace falta pagar un hotel cerca del aeropuerto.",
        "Um comboio liga o aeroporto Mohammed V ao centro: não é preciso pagar um hotel perto do aeroporto.",
        "يربط القطار مطار محمد الخامس بوسط المدينة: لا داعي لدفع ثمن فندق قرب المطار."),
    "Marrakech": (
        "Medina riads often show lower prices for direct bookings out of season: compare with Booking.",
        "Los riads de la medina suelen tener precios más bajos reservando directamente fuera de temporada: compara con Booking.",
        "Os riads da medina costumam ter preços mais baixos com reserva direta fora de época: compare com o Booking.",
        "كثيرًا ما تعرض رياضات المدينة القديمة أسعارًا أقل عند الحجز المباشر خارج الموسم: قارن مع Booking."),
    "Douala": (
        "Traffic jams are common: choose a hotel close to your appointments rather than the cheapest one.",
        "Los atascos son frecuentes: elige un hotel cerca de tus citas en lugar del más barato.",
        "Os engarrafamentos são frequentes: escolha um hotel perto dos seus compromissos em vez do mais barato.",
        "الازدحام المروري شائع: اختر فندقًا قريبًا من مواعيدك بدلًا من الأرخص."),
    "Conakry": (
        "Kaloum is far from the airport and often congested: check the travel time before booking.",
        "Kaloum está lejos del aeropuerto y suele haber atascos: comprueba el tiempo de trayecto antes de reservar.",
        "Kaloum fica longe do aeroporto e é muitas vezes congestionado: verifique o tempo de viagem antes de reservar.",
        "كالوم بعيدة عن المطار وغالبًا مزدحمة: تحقق من مدة الطريق قبل الحجز."),
    "Lomé": (
        "Lomé is compact: a beachfront hotel is still close to everything.",
        "Lomé es compacta: un hotel frente al mar sigue cerca de todo.",
        "Lomé é compacta: um hotel à beira-mar fica perto de tudo.",
        "لومي مدينة صغيرة: الفندق المطل على البحر يبقى قريبًا من كل شيء."),
    "Cotonou": (
        "Haie Vive is close to the airport: handy for a night-time arrival or departure.",
        "Haie Vive está cerca del aeropuerto: práctico para llegar o salir de noche.",
        "Haie Vive fica perto do aeroporto: prático para chegadas ou partidas à noite.",
        "حي هاي فيف قريب من المطار: مناسب للوصول أو المغادرة ليلًا."),
    "Kinshasa": (
        "N'djili airport is far from Gombe: allow plenty of travel time, especially in the late afternoon.",
        "El aeropuerto de N'djili está lejos de la Gombe: calcula bastante tiempo de trayecto, sobre todo al final del día.",
        "O aeroporto de N'djili fica longe da Gombe: preveja bastante tempo de viagem, sobretudo ao fim do dia.",
        "مطار نجيلي بعيد عن حي غومبي: خصص وقتًا كافيًا للطريق، خصوصًا في آخر النهار."),
    "Alger": (
        "Bab Ezzouar is handy for a short stay or a connection, a few minutes from the airport.",
        "Bab Ezzouar es práctico para una estancia corta o una conexión, a pocos minutos del aeropuerto.",
        "Bab Ezzouar é prático para uma estadia curta ou uma ligação, a poucos minutos do aeroporto.",
        "باب الزوار مناسب للإقامة القصيرة أو الترانزيت، على بعد دقائق من المطار."),
    "Tunis": (
        "Outside summer, the beachfront hotels in Gammarth cut their prices a lot.",
        "Fuera del verano, los hoteles frente al mar de Gammarth bajan mucho sus precios.",
        "Fora do verão, os hotéis à beira-mar de Gammarth baixam muito os preços.",
        "خارج فصل الصيف، تخفض فنادق قمرت المطلة على البحر أسعارها كثيرًا."),
    "Paris": (
        "For an early-morning flight, a hotel near the RER B line (Roissy) or Orlyval saves you an expensive taxi.",
        "Para un vuelo temprano, un hotel cerca de la línea RER B (Roissy) o del Orlyval te ahorra un taxi caro.",
        "Para um voo de manhã cedo, um hotel perto da linha RER B (Roissy) ou do Orlyval poupa-lhe um táxi caro.",
        "لرحلة في الصباح الباكر، فندق قرب خط RER B (رواسي) أو أورليفال يوفّر عليك سيارة أجرة مكلفة."),
    "Dubaï": (
        "Prices drop in summer (June–August) but it is very hot: ideal for a hotel stay with a pool.",
        "Los precios bajan en verano (junio-agosto) pero hace mucho calor: ideal para un hotel con piscina.",
        "Os preços descem no verão (junho-agosto), mas faz muito calor: ideal para um hotel com piscina.",
        "تنخفض الأسعار في الصيف (يونيو–أغسطس) لكن الحر شديد: مثالي للإقامة في فندق بمسبح."),
    "Istanbul": (
        "The new Istanbul Airport is far from the centre: allow at least an hour of travel.",
        "El nuevo aeropuerto de Estambul está lejos del centro: calcula al menos una hora de trayecto.",
        "O novo aeroporto de Istambul fica longe do centro: conte com pelo menos uma hora de viagem.",
        "مطار إسطنبول الجديد بعيد عن وسط المدينة: احسب ساعة على الأقل للطريق."),
    "Montréal": (
        "Winter (January–March) is the cheapest season for hotels, except during festivals.",
        "El invierno (enero-marzo) es la temporada más barata para los hoteles, salvo durante los festivales.",
        "O inverno (janeiro-março) é a época mais barata para hotéis, exceto durante os festivais.",
        "الشتاء (يناير–مارس) أرخص موسم للفنادق، إلا خلال المهرجانات."),
    "Accra": (
        "Kotoka airport is inside the city: a hotel in Osu or near the airport keeps journeys short, as traffic jams often slow them down.",
        "El aeropuerto de Kotoka está dentro de la ciudad: un hotel en Osu o cerca del aeropuerto acorta los trayectos, a menudo frenados por los atascos.",
        "O aeroporto de Kotoka fica dentro da cidade: um hotel em Osu ou perto do aeroporto encurta as deslocações, muitas vezes atrasadas pelo trânsito.",
        "مطار كوتوكا داخل المدينة: الإقامة في أوسو أو قرب المطار تختصر التنقلات التي تبطئها الاختناقات المرورية غالبًا."),
    "Lagos": (
        "Traffic between the mainland and the islands can be very slow: for a late arrival or an early departure, a night in Ikeja, near the airport, is often more practical.",
        "Los atascos entre el continente y las islas pueden ser muy largos: si llegas tarde o sales temprano, una noche en Ikeja, cerca del aeropuerto, suele ser más práctica.",
        "O trânsito entre o continente e as ilhas pode ser muito lento: para uma chegada tardia ou uma partida cedo, uma noite em Ikeja, perto do aeroporto, costuma ser mais prática.",
        "قد تطول الاختناقات المرورية كثيرًا بين البر والجزر: عند الوصول متأخرًا أو المغادرة باكرًا، تكون ليلة في إيكيجا قرب المطار أكثر عملية غالبًا."),
}

AREAS = {
    "proche des administrations et du centre d'affaires": ("close to government offices and the business district", "cerca de la administración y del centro de negocios", "perto da administração e do centro de negócios", "قريب من الإدارات ومركز الأعمال"),
    "bord de mer, restaurants, plus calme": ("seafront, restaurants, quieter", "frente al mar, restaurantes, más tranquilo", "à beira-mar, restaurantes, mais calmo", "على البحر، مطاعم، أهدأ"),
    "résidentiel, bon rapport qualité-prix": ("residential, good value", "residencial, buena relación calidad-precio", "residencial, boa relação qualidade-preço", "سكني، قيمة جيدة مقابل السعر"),
    "quartier des affaires": ("business district", "distrito de negocios", "bairro de negócios", "حي الأعمال"),
    "résidentiel, hôtels et restaurants": ("residential, hotels and restaurants", "residencial, hoteles y restaurantes", "residencial, hotéis e restaurantes", "سكني، فنادق ومطاعم"),
    "vie nocturne, proche de l'aéroport": ("nightlife, close to the airport", "vida nocturna, cerca del aeropuerto", "vida noturna, perto do aeroporto", "حياة ليلية، قريب من المطار"),
    "quartier moderne, hôtels d'affaires": ("modern area, business hotels", "barrio moderno, hoteles de negocios", "bairro moderno, hotéis de negócios", "حي حديث، فنادق أعمال"),
    "animé, restaurants": ("lively, restaurants", "animado, restaurantes", "animado, restaurantes", "حيوي، مطاعم"),
    "rive droite, plus calme": ("right bank, quieter", "orilla derecha, más tranquilo", "margem direita, mais calmo", "الضفة اليمنى، أهدأ"),
    "commerces, transports, prix moyens": ("shops, transport, mid-range prices", "comercios, transporte, precios medios", "comércio, transportes, preços médios", "متاجر، مواصلات، أسعار متوسطة"),
    "corniche et bord de mer": ("corniche and seafront", "paseo marítimo y frente al mar", "marginal e beira-mar", "الكورنيش والواجهة البحرية"),
    "central et calme": ("central and quiet", "céntrico y tranquilo", "central e calmo", "مركزي وهادئ"),
    "riads traditionnels, au cœur de la ville": ("traditional riads, in the heart of the city", "riads tradicionales, en el corazón de la ciudad", "riads tradicionais, no coração da cidade", "رياضات تقليدية في قلب المدينة"),
    "ville moderne, restaurants": ("modern city, restaurants", "ciudad moderna, restaurantes", "cidade moderna, restaurantes", "المدينة الحديثة، مطاعم"),
    "hôtels avec piscine, plus chic": ("hotels with pools, more upmarket", "hoteles con piscina, más elegante", "hotéis com piscina, mais requintado", "فنادق بمسابح، أرقى"),
    "quartier administratif et des affaires": ("government and business district", "barrio administrativo y de negocios", "bairro administrativo e de negócios", "الحي الإداري وحي الأعمال"),
    "commerçant et animé": ("shopping area, lively", "comercial y animado", "comercial e animado", "تجاري وحيوي"),
    "résidentiel, plus calme": ("residential, quieter", "residencial, más tranquilo", "residencial, mais calmo", "سكني، أهدأ"),
    "centre administratif et des affaires": ("administrative and business centre", "centro administrativo y de negocios", "centro administrativo e de negócios", "المركز الإداري ومركز الأعمال"),
    "résidentiel, hôtels récents": ("residential, newer hotels", "residencial, hoteles recientes", "residencial, hotéis recentes", "سكني، فنادق حديثة"),
    "restaurants, plus calme": ("restaurants, quieter", "restaurantes, más tranquilo", "restaurantes, mais calmo", "مطاعم، أهدأ"),
    "marché, commerces": ("market, shops", "mercado, comercios", "mercado, comércio", "سوق ومتاجر"),
    "plages et maquis": ("beaches and local eateries (maquis)", "playas y restaurantes locales (maquis)", "praias e restaurantes locais (maquis)", "شواطئ ومطاعم محلية (ماكي)"),
    "calme, proche des institutions": ("quiet, close to the institutions", "tranquilo, cerca de las instituciones", "calmo, perto das instituições", "هادئ، قريب من المؤسسات"),
    "restaurants et vie nocturne": ("restaurants and nightlife", "restaurantes y vida nocturna", "restaurantes e vida noturna", "مطاعم وحياة ليلية"),
    "centre des affaires": ("business centre", "centro de negocios", "centro de negócios", "مركز الأعمال"),
    "bord de mer, plus détendu": ("seafront, more relaxed", "frente al mar, más relajado", "à beira-mar, mais descontraído", "على البحر، أكثر استرخاء"),
    "centre des affaires, hôtels internationaux": ("business centre, international hotels", "centro de negocios, hoteles internacionales", "centro de negócios, hotéis internacionais", "مركز الأعمال، فنادق دولية"),
    "résidentiel": ("residential", "residencial", "residencial", "سكني"),
    "commerçant": ("shopping area", "comercial", "comercial", "تجاري"),
    "transports et commerces": ("transport and shops", "transporte y comercios", "transportes e comércio", "مواصلات ومتاجر"),
    "résidentiel et calme": ("residential and quiet", "residencial y tranquilo", "residencial e calmo", "سكني وهادئ"),
    "proche de l'aéroport, hôtels d'affaires": ("close to the airport, business hotels", "cerca del aeropuerto, hoteles de negocios", "perto do aeroporto, hotéis de negócios", "قريب من المطار، فنادق أعمال"),
    "médina et avenue Bourguiba": ("medina and Avenue Bourguiba", "medina y avenida Burguiba", "medina e avenida Bourguiba", "المدينة العتيقة وشارع بورقيبة"),
    "moderne, hôtels d'affaires": ("modern, business hotels", "moderno, hoteles de negocios", "moderno, hotéis de negócios", "حديث، فنادق أعمال"),
    "bord de mer": ("seafront", "frente al mar", "à beira-mar", "على البحر"),
    "bien reliés à Roissy (RER B)": ("well connected to Roissy (RER B)", "bien conectados con Roissy (RER B)", "bem ligados a Roissy (RER B)", "متصلان جيدًا بمطار رواسي (RER B)"),
    "prix plus doux, bien desservis": ("lower prices, good transport links", "precios más bajos, bien comunicados", "preços mais baixos, bem servidos", "أسعار أقل، مواصلات جيدة"),
    "pratique pour Orly": ("handy for Orly", "práctico para Orly", "prático para Orly", "مناسب لمطار أورلي"),
    "les plus abordables, proches de l'aéroport et du métro": ("the most affordable, close to the airport and the metro", "los más asequibles, cerca del aeropuerto y del metro", "os mais acessíveis, perto do aeroporto e do metro", "الأرخص، قريبان من المطار والمترو"),
    "Burj Khalifa et Dubai Mall": ("Burj Khalifa and Dubai Mall", "Burj Khalifa y Dubai Mall", "Burj Khalifa e Dubai Mall", "برج خليفة ودبي مول"),
    "bord de mer, plus cher": ("seafront, more expensive", "frente al mar, más caro", "à beira-mar, mais caro", "على البحر، أغلى"),
    "monuments à pied": ("monuments within walking distance", "monumentos a pie", "monumentos a pé", "المعالم على مسافة مشي"),
    "côté asiatique, plus local et abordable": ("Asian side, more local and affordable", "lado asiático, más local y asequible", "lado asiático, mais local e acessível", "الجانب الآسيوي، طابع محلي وأسعار معقولة"),
    "proche de tout, métro": ("close to everything, metro", "cerca de todo, metro", "perto de tudo, metro", "قريب من كل شيء، مترو"),
    "quartier vivant, appartements": ("lively area, apartments", "barrio animado, apartamentos", "bairro animado, apartamentos", "حي حيوي، شقق"),
    "charme historique, plus cher": ("historic charm, more expensive", "encanto histórico, más caro", "charme histórico, mais caro", "طابع تاريخي، أغلى"),
    "animé, restaurants et commerces": ("lively, restaurants and shops", "animado, restaurantes y comercios", "animado, restaurantes e comércio", "حيوي، مطاعم ومتاجر"),
    "quartier des affaires, hôtels et restaurants": ("business district, hotels and restaurants", "distrito de negocios, hoteles y restaurantes", "bairro de negócios, hotéis e restaurantes", "حي الأعمال، فنادق ومطاعم"),
    "résidentiel et chic, plus calme": ("upmarket residential, quieter", "residencial y elegante, más tranquilo", "residencial e requintado, mais calmo", "سكني راقٍ، أهدأ"),
    "proche de l'aéroport, sur le continent": ("close to the airport, on the mainland", "cerca del aeropuerto, en el continente", "perto do aeroporto, no continente", "قريب من المطار، على البر الرئيسي"),
}
