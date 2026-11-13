"""Outil « Partage des frais du voyage » (fr, en, es, pt, ar) : qui a payé quoi, qui doit combien à qui.
Tout le calcul se fait dans le navigateur (site/frais.js) ; rien n'est envoyé à Escale, aucun prix n'est écrit dans la page.
Le lien de partage contient le compte lui-même (après le #)."""
import html
import json

import build_i18n as B

E = html.escape
LIENS = [("partage-frais-voyage", "Partage des frais du voyage : qui doit combien à qui ?")]

T = {
    "fr": dict(
        path="partage-frais-voyage", title="Partage des frais de voyage : qui doit combien à qui ? | Escale",
        desc="Voyage en famille ou entre amis : notez qui a payé quoi, Escale calcule qui doit combien à qui, avec le moins de virements possible. Gratuit, sans inscription.",
        eyebrow="Outil gratuit", h1="Partage des frais <span>du voyage</span>",
        lead="Billets, location, courses, taxi : notez qui a payé quoi. Escale calcule qui doit combien à qui, avec le moins de virements possible.",
        h_people="1. Les voyageurs", name="Prénom", cur="Monnaie", add="Ajouter", need="Ajoutez au moins deux voyageurs pour noter les dépenses.",
        h_exp="2. Les dépenses", label="Quoi ?", label_ph="Location, courses, taxi…", amount="Montant", by="Payé par", for_="Pour qui ?", add_exp="Ajouter la dépense",
        h_res="3. Qui doit combien à qui ?", wa="Envoyer sur WhatsApp", copy="Copier le lien du compte", reset="Tout effacer",
        t=dict(all="tout le monde", expense="Dépense", paidby="Payé par {n} · pour {f}", total="Total des dépenses :", owes="{a} doit {x} à {b}", even="Les comptes sont bons : personne ne doit rien.",
               c_paid="A payé", c_share="Sa part", c_bal="Solde", del_="Supprimer {n}", dup="Ce prénom est déjà dans la liste.", used="{n} a des dépenses : supprimez-les d'abord.",
               e_amount="Indiquez un montant.", e_for="Cochez au moins une personne.", wa_head="💸 Frais du voyage", wa_total="Total : {t}", wa_link="Le détail :",
               copied="Lien copié ✓", copy="Copiez ce lien :", reset_q="Effacer les voyageurs et toutes les dépenses ?", replace="Ce lien contient un autre compte. Remplacer celui de cet appareil ?"),
        h_how="Comment ça marche ?",
        how=["Ajoutez le prénom de chaque voyageur et choisissez la monnaie du compte.",
             "Notez chaque dépense : ce que c'est, le montant, qui a payé et pour qui. Quelqu'un n'était pas concerné ? Décochez-le.",
             "Escale calcule la part de chacun et la liste des virements à faire, la plus courte possible.",
             "Envoyez le résultat sur WhatsApp : le lien ouvre le même compte chez les autres voyageurs."],
        h_faq="Questions fréquentes",
        faq=[("Où sont gardées mes dépenses ?", "Dans votre téléphone ou votre ordinateur seulement. Rien n'est envoyé à Escale et il n'y a pas de compte à créer. Si vous effacez les données du navigateur, le compte est effacé."),
             ("Que contient le lien de partage ?", "Le compte lui-même : les prénoms, les dépenses et la monnaie. Toute personne qui reçoit le lien peut donc les lire. Si quelqu'un ajoute une dépense de son côté, il doit renvoyer son lien pour que les autres la voient."),
             ("Comment sont calculés les virements ?", "Escale additionne ce que chacun a payé, retire sa part de chaque dépense, puis fait payer ceux qui doivent de l'argent à ceux qui en ont avancé, en commençant par les plus gros montants. Chacun retrouve sa mise avec peu de virements."),
             ("Et si les dépenses sont dans plusieurs monnaies ?", "Un compte utilise une seule monnaie. Convertissez les montants vous-même avant de les saisir, par exemple au taux réellement payé avec votre carte."),
             ("Une dépense ne concerne qu'une partie du groupe ?", "Décochez les personnes qui ne sont pas concernées dans « Pour qui ? » : la dépense est partagée entre les autres seulement.")],
        h_more="Pour préparer le voyage",
        more=[("/budget-voyage-famille/", "Le vrai budget du voyage en famille"), ("/guides/argent-en-voyage/", "Argent en voyage : carte, change et Mobile Money"), ("/guides/check-list-depart/", "Check-list du départ")]),
    "en": dict(
        path="en/split-trip-costs", title="Split trip costs: who owes whom? Free calculator | Escale",
        desc="Travelling with family or friends? Note who paid for what and Escale works out who owes whom, with as few transfers as possible. Free, no sign-up.",
        eyebrow="Free tool", h1="Split the costs <span>of the trip</span>",
        lead="Tickets, rental, groceries, taxi: note who paid for what. Escale works out who owes whom, with as few transfers as possible.",
        h_people="1. Travellers", name="First name", cur="Currency", add="Add", need="Add at least two travellers to enter expenses.",
        h_exp="2. Expenses", label="What?", label_ph="Rental, groceries, taxi…", amount="Amount", by="Paid by", for_="For whom?", add_exp="Add the expense",
        h_res="3. Who owes whom?", wa="Send on WhatsApp", copy="Copy the link to this tally", reset="Clear everything",
        t=dict(all="everyone", expense="Expense", paidby="Paid by {n} · for {f}", total="Total spent:", owes="{a} owes {b} {x}", even="All square: nobody owes anything.",
               c_paid="Paid", c_share="Share", c_bal="Balance", del_="Remove {n}", dup="This name is already in the list.", used="{n} has expenses: remove them first.",
               e_amount="Enter an amount.", e_for="Tick at least one person.", wa_head="💸 Trip costs", wa_total="Total: {t}", wa_link="Details:",
               copied="Link copied ✓", copy="Copy this link:", reset_q="Clear the travellers and all expenses?", replace="This link contains another tally. Replace the one on this device?"),
        h_how="How does it work?",
        how=["Add each traveller's first name and choose the currency.",
             "Enter each expense: what it was, the amount, who paid and for whom. Someone was not involved? Untick them.",
             "Escale works out everyone's share and the shortest possible list of transfers.",
             "Send the result on WhatsApp: the link opens the same tally for the other travellers."],
        h_faq="Frequently asked questions",
        faq=[("Where are my expenses stored?", "Only on your phone or computer. Nothing is sent to Escale and there is no account to create. If you clear your browser data, the tally is erased."),
             ("What does the sharing link contain?", "The tally itself: the names, the expenses and the currency. Anyone who receives the link can therefore read them. If someone adds an expense on their side, they need to send their link again for the others to see it."),
             ("How are the transfers calculated?", "Escale adds up what each person paid, subtracts their share of each expense, then has those who owe money pay those who advanced it, starting with the largest amounts. Everyone gets their money back with few transfers."),
             ("What if expenses are in several currencies?", "A tally uses a single currency. Convert the amounts yourself before entering them, for example at the rate your card actually charged."),
             ("An expense only concerns part of the group?", "Untick the people who are not involved under “For whom?”: the expense is split among the others only.")],
        h_more="To prepare the trip",
        more=[("/en/family-trip-budget/", "The real cost of a family trip"), ("/en/guides/", "All travel guides")]),
    "es": dict(
        path="es/dividir-gastos-viaje", title="Dividir los gastos del viaje: ¿quién debe a quién? | Escale",
        desc="Viaje en familia o con amigos: apunta quién pagó qué y Escale calcula quién debe cuánto a quién, con el menor número de pagos posible. Gratis, sin registro.",
        eyebrow="Herramienta gratuita", h1="Dividir los gastos <span>del viaje</span>",
        lead="Billetes, alquiler, compras, taxi: apunta quién pagó qué. Escale calcula quién debe cuánto a quién, con el menor número de pagos posible.",
        h_people="1. Los viajeros", name="Nombre", cur="Moneda", add="Añadir", need="Añade al menos dos viajeros para apuntar los gastos.",
        h_exp="2. Los gastos", label="¿Qué?", label_ph="Alquiler, compras, taxi…", amount="Importe", by="Pagado por", for_="¿Para quién?", add_exp="Añadir el gasto",
        h_res="3. ¿Quién debe cuánto a quién?", wa="Enviar por WhatsApp", copy="Copiar el enlace de la cuenta", reset="Borrar todo",
        t=dict(all="todos", expense="Gasto", paidby="Pagado por {n} · para {f}", total="Total de gastos:", owes="{a} debe {x} a {b}", even="Las cuentas están claras: nadie debe nada.",
               c_paid="Pagó", c_share="Su parte", c_bal="Saldo", del_="Quitar {n}", dup="Ese nombre ya está en la lista.", used="{n} tiene gastos: bórralos primero.",
               e_amount="Indica un importe.", e_for="Marca al menos una persona.", wa_head="💸 Gastos del viaje", wa_total="Total: {t}", wa_link="El detalle:",
               copied="Enlace copiado ✓", copy="Copia este enlace:", reset_q="¿Borrar los viajeros y todos los gastos?", replace="Este enlace contiene otra cuenta. ¿Sustituir la de este dispositivo?"),
        h_how="¿Cómo funciona?",
        how=["Añade el nombre de cada viajero y elige la moneda de la cuenta.",
             "Apunta cada gasto: qué es, el importe, quién pagó y para quién. ¿Alguien no participaba? Desmárcalo.",
             "Escale calcula la parte de cada uno y la lista de pagos más corta posible.",
             "Envía el resultado por WhatsApp: el enlace abre la misma cuenta a los demás viajeros."],
        h_faq="Preguntas frecuentes",
        faq=[("¿Dónde se guardan mis gastos?", "Solo en tu teléfono o tu ordenador. No se envía nada a Escale y no hay que crear una cuenta. Si borras los datos del navegador, la cuenta se borra."),
             ("¿Qué contiene el enlace para compartir?", "La cuenta misma: los nombres, los gastos y la moneda. Cualquier persona que reciba el enlace puede leerlos. Si alguien añade un gasto por su lado, debe volver a enviar su enlace para que los demás lo vean."),
             ("¿Cómo se calculan los pagos?", "Escale suma lo que pagó cada uno, resta su parte de cada gasto y hace que quienes deben dinero paguen a quienes lo adelantaron, empezando por los importes más altos. Cada uno recupera lo suyo con pocos pagos."),
             ("¿Y si los gastos están en varias monedas?", "Una cuenta usa una sola moneda. Convierte tú mismo los importes antes de apuntarlos, por ejemplo al tipo que realmente te cobró la tarjeta."),
             ("¿Un gasto solo afecta a una parte del grupo?", "Desmarca en «¿Para quién?» a las personas que no participan: el gasto se reparte solo entre las demás.")],
        h_more="Para preparar el viaje", more=[("/es/guias/", "Todas las guías de viaje")]),
    "pt": dict(
        path="pt/dividir-despesas-viagem", title="Dividir as despesas da viagem: quem deve a quem? | Escale",
        desc="Viagem em família ou com amigos: anote quem pagou o quê e a Escale calcula quem deve quanto a quem, com o menor número de transferências. Grátis, sem registo.",
        eyebrow="Ferramenta gratuita", h1="Dividir as despesas <span>da viagem</span>",
        lead="Bilhetes, aluguer, compras, táxi: anote quem pagou o quê. A Escale calcula quem deve quanto a quem, com o menor número de transferências possível.",
        h_people="1. Os viajantes", name="Nome", cur="Moeda", add="Adicionar", need="Adicione pelo menos dois viajantes para anotar as despesas.",
        h_exp="2. As despesas", label="O quê?", label_ph="Aluguer, compras, táxi…", amount="Valor", by="Pago por", for_="Para quem?", add_exp="Adicionar a despesa",
        h_res="3. Quem deve quanto a quem?", wa="Enviar pelo WhatsApp", copy="Copiar a ligação da conta", reset="Apagar tudo",
        t=dict(all="todos", expense="Despesa", paidby="Pago por {n} · para {f}", total="Total das despesas:", owes="{a} deve {x} a {b}", even="As contas estão certas: ninguém deve nada.",
               c_paid="Pagou", c_share="A sua parte", c_bal="Saldo", del_="Remover {n}", dup="Esse nome já está na lista.", used="{n} tem despesas: apague-as primeiro.",
               e_amount="Indique um valor.", e_for="Marque pelo menos uma pessoa.", wa_head="💸 Despesas da viagem", wa_total="Total: {t}", wa_link="O detalhe:",
               copied="Ligação copiada ✓", copy="Copie esta ligação:", reset_q="Apagar os viajantes e todas as despesas?", replace="Esta ligação contém outra conta. Substituir a deste dispositivo?"),
        h_how="Como funciona?",
        how=["Adicione o nome de cada viajante e escolha a moeda da conta.",
             "Anote cada despesa: o que é, o valor, quem pagou e para quem. Alguém não participou? Desmarque-o.",
             "A Escale calcula a parte de cada um e a lista de transferências mais curta possível.",
             "Envie o resultado pelo WhatsApp: a ligação abre a mesma conta aos outros viajantes."],
        h_faq="Perguntas frequentes",
        faq=[("Onde ficam guardadas as minhas despesas?", "Apenas no seu telemóvel ou computador. Nada é enviado à Escale e não é preciso criar conta. Se apagar os dados do navegador, a conta é apagada."),
             ("O que contém a ligação de partilha?", "A própria conta: os nomes, as despesas e a moeda. Qualquer pessoa que receba a ligação pode lê-los. Se alguém adicionar uma despesa do seu lado, tem de voltar a enviar a sua ligação para os outros a verem."),
             ("Como são calculadas as transferências?", "A Escale soma o que cada um pagou, retira a sua parte de cada despesa e faz com que quem deve dinheiro pague a quem o adiantou, começando pelos valores mais altos. Cada um recupera o que é seu com poucas transferências."),
             ("E se as despesas estiverem em várias moedas?", "Uma conta usa uma só moeda. Converta os valores antes de os anotar, por exemplo à taxa realmente cobrada pelo seu cartão."),
             ("Uma despesa só diz respeito a parte do grupo?", "Desmarque em «Para quem?» as pessoas que não participam: a despesa é dividida apenas entre as outras.")],
        h_more="Para preparar a viagem", more=[("/pt/guias/", "Todos os guias de viagem")]),
    "ar": dict(
        path="ar/split-trip-costs", title="تقسيم مصاريف السفر: من يدين لمن؟ حاسبة مجانية | Escale",
        desc="سفر مع العائلة أو الأصدقاء؟ سجّل من دفع ماذا، وEscale يحسب من يدين لمن وبكم، بأقل عدد ممكن من التحويلات. مجاني وبدون تسجيل.",
        eyebrow="أداة مجانية", h1="تقسيم مصاريف <span>السفر</span>",
        lead="التذاكر، الإيجار، المشتريات، التاكسي: سجّل من دفع ماذا. Escale يحسب من يدين لمن وبكم، بأقل عدد ممكن من التحويلات.",
        h_people="1. المسافرون", name="الاسم", cur="العملة", add="إضافة", need="أضف مسافرَين على الأقل لتسجيل المصاريف.",
        h_exp="2. المصاريف", label="ماذا؟", label_ph="إيجار، مشتريات، تاكسي…", amount="المبلغ", by="دفعه", for_="لمن؟", add_exp="إضافة المصروف",
        h_res="3. من يدين لمن وبكم؟", wa="إرسال عبر واتساب", copy="نسخ رابط الحساب", reset="مسح الكل",
        t=dict(all="الجميع", expense="مصروف", paidby="دفعه {n} · لـ {f}", total="مجموع المصاريف:", owes="{a} يدفع {x} إلى {b}", even="الحسابات متساوية: لا أحد مدين بشيء.",
               c_paid="دفع", c_share="حصته", c_bal="الرصيد", del_="حذف {n}", dup="هذا الاسم موجود في القائمة.", used="{n} له مصاريف: احذفها أولاً.",
               e_amount="أدخل مبلغاً.", e_for="اختر شخصاً واحداً على الأقل.", wa_head="💸 مصاريف السفر", wa_total="المجموع: {t}", wa_link="التفاصيل:",
               copied="تم نسخ الرابط ✓", copy="انسخ هذا الرابط:", reset_q="مسح المسافرين وكل المصاريف؟", replace="هذا الرابط يحتوي على حساب آخر. هل تريد استبدال حساب هذا الجهاز؟"),
        h_how="كيف يعمل؟",
        how=["أضف اسم كل مسافر واختر عملة الحساب.",
             "سجّل كل مصروف: ما هو، المبلغ، من دفع ولمن. شخص غير معنيّ؟ أزل علامته.",
             "Escale يحسب حصة كل واحد وأقصر قائمة ممكنة من التحويلات.",
             "أرسل النتيجة عبر واتساب: الرابط يفتح الحساب نفسه عند بقية المسافرين."],
        h_faq="أسئلة شائعة",
        faq=[("أين تُحفظ مصاريفي؟", "في هاتفك أو حاسوبك فقط. لا يُرسل شيء إلى Escale ولا حاجة لإنشاء حساب. إذا مسحت بيانات المتصفح يُمسح الحساب."),
             ("ماذا يحتوي رابط المشاركة؟", "الحساب نفسه: الأسماء والمصاريف والعملة. كل من يستلم الرابط يستطيع قراءتها. إذا أضاف أحدهم مصروفاً من جهته فعليه إرسال رابطه من جديد ليراه الآخرون."),
             ("كيف تُحسب التحويلات؟", "Escale يجمع ما دفعه كل شخص، ويطرح حصته من كل مصروف، ثم يجعل المدينين يدفعون لمن دفعوا مسبقاً، بدءاً بأكبر المبالغ. هكذا يسترجع كل واحد ماله بعدد قليل من التحويلات."),
             ("وإذا كانت المصاريف بعدة عملات؟", "الحساب يستعمل عملة واحدة. حوّل المبالغ بنفسك قبل إدخالها، مثلاً بالسعر الذي خصمته بطاقتك فعلاً."),
             ("مصروف يخص جزءاً من المجموعة فقط؟", "أزل في «لمن؟» علامة الأشخاص غير المعنيين: يُقسم المصروف على الباقين فقط.")],
        h_more="للتحضير للسفر", more=[("/ar/guides/", "كل أدلة السفر")]),
}


def build(site, ctx):
    paths = {l: t["path"] for l, t in T.items()}
    urls = []
    for lang, t in T.items():
        js = dict(t["t"]); js["del"] = js.pop("del_")
        hero = f'<p class="eyebrow">{E(t["eyebrow"])}</p><h1>{t["h1"]}</h1><p class="hero-lead">{E(t["lead"])}</p>'
        body = (
            f'<div id="pf" data-t="{E(json.dumps(js, ensure_ascii=False))}">'
            f'<section><h2>{E(t["h_people"])}</h2><form id="pf-pform" class="tool-form" novalidate><div class="tool-grid">'
            f'<label><span>{E(t["name"])}</span><input id="pf-name" maxlength="24" autocomplete="off" enterkeyhint="done"></label>'
            f'<label><span>{E(t["cur"])}</span><select id="pf-cur"></select></label></div>'
            f'<button class="btn" type="submit">{E(t["add"])}</button><ul id="pf-people" class="pf-chips"></ul><p id="pf-pmsg" class="small" role="status"></p></form></section>'
            f'<section><h2>{E(t["h_exp"])}</h2><p id="pf-need" class="small">{E(t["need"])}</p><form id="pf-eform" class="tool-form" novalidate hidden><div class="tool-grid">'
            f'<label><span>{E(t["label"])}</span><input id="pf-label" maxlength="40" placeholder="{E(t["label_ph"])}" autocomplete="off"></label>'
            f'<label><span>{E(t["amount"])}</span><input id="pf-amount" type="number" min="0" step="0.01" inputmode="decimal"></label>'
            f'<label><span>{E(t["by"])}</span><select id="pf-by"></select></label></div>'
            f'<fieldset class="pf-for"><legend>{E(t["for_"])}</legend><div id="pf-for"></div></fieldset>'
            f'<button class="btn" type="submit">{E(t["add_exp"])}</button><p id="pf-emsg" class="small" role="status"></p></form><ul id="pf-exp" class="pf-exp"></ul></section>'
            f'<section id="pf-res" hidden><h2>{E(t["h_res"])}</h2><div id="pf-out" aria-live="polite"></div>'
            f'<p class="pf-btns"><a class="btn wa-btn" id="pf-wa" target="_blank" rel="noopener">{E(t["wa"])}</a>'
            f'<button type="button" class="btn ghost" id="pf-copy">{E(t["copy"])}</button><button type="button" class="btn ghost" id="pf-reset">{E(t["reset"])}</button></p></section></div>'
            f'<section><h2>{E(t["h_how"])}</h2><ol>' + "".join(f"<li>{E(x)}</li>" for x in t["how"]) + "</ol></section>"
            f'<section class="faq"><h2>{E(t["h_faq"])}</h2>' + "".join(f"<details><summary>{E(q)}</summary><p>{E(r)}</p></details>" for q, r in t["faq"]) + "</section>"
            f'<section><h2>{E(t["h_more"])}</h2><ul>' + "".join(f'<li><a href="{p}">{E(x)}</a></li>' for p, x in t["more"]) + "</ul></section>"
            + B.faq_ld(t["faq"]) + '<script src="/frais.js" defer></script>')
        urls.append(B.write(site, t["path"], lang, t["title"], t["desc"], hero, body, "", paths, ctx))
    return urls
