// Pages trajets : formulaire « Alerte prix par e-mail ». N'apparaît que si l'envoi d'e-mails est configuré (/api/alert?action=status).
(function () {
  "use strict";
  var box = document.getElementById("price-alert");
  if (!box) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var L = {
    fr: { h: "Alerte prix par e-mail", p: "Recevez un e-mail quand un aller-retour passe sous votre budget. Gratuit, désinscription en un clic.", email: "Votre e-mail", max: "Budget maximum (€)", consent: "J’accepte de recevoir des e-mails pour cette alerte. Mon adresse sert uniquement à cela et est supprimée à la désinscription.", btn: "Créer l’alerte", ok: "C’est presque fini : confirmez votre alerte avec le lien envoyé à {e}.", err: "Vérifiez l’e-mail, le budget et la case de consentement.", fail: "L’alerte n’a pas pu être créée. Réessayez plus tard." },
    en: { h: "Price alert by email", p: "Get an email when a round trip drops below your budget. Free, one-click unsubscribe.", email: "Your email", max: "Maximum budget (€)", consent: "I agree to receive emails for this alert. My address is used only for this and deleted when I unsubscribe.", btn: "Create alert", ok: "Almost done: confirm your alert with the link sent to {e}.", err: "Check the email, the budget and the consent box.", fail: "The alert could not be created. Please try again later." },
    es: { h: "Alerta de precio por correo", p: "Recibe un correo cuando un ida y vuelta baje de tu presupuesto. Gratis, baja en un clic.", email: "Tu correo", max: "Presupuesto máximo (€)", consent: "Acepto recibir correos para esta alerta. Mi dirección solo se usa para esto y se borra al darme de baja.", btn: "Crear alerta", ok: "Casi listo: confirma tu alerta con el enlace enviado a {e}.", err: "Revisa el correo, el presupuesto y la casilla de consentimiento.", fail: "No se pudo crear la alerta. Inténtalo más tarde." },
    pt: { h: "Alerta de preço por e-mail", p: "Receba um e-mail quando uma ida e volta descer abaixo do seu orçamento. Grátis, cancelamento num clique.", email: "O seu e-mail", max: "Orçamento máximo (€)", consent: "Aceito receber e-mails para este alerta. O meu endereço só serve para isso e é apagado quando cancelar.", btn: "Criar alerta", ok: "Quase pronto: confirme o alerta com o link enviado para {e}.", err: "Verifique o e-mail, o orçamento e a caixa de consentimento.", fail: "Não foi possível criar o alerta. Tente mais tarde." },
    ar: { h: "تنبيه السعر عبر البريد", p: "تلقَّ رسالة عندما ينخفض سعر رحلة ذهاب وعودة إلى أقل من ميزانيتك. مجاني، والإلغاء بنقرة.", email: "بريدك الإلكتروني", max: "الميزانية القصوى (€)", consent: "أوافق على تلقي رسائل لهذا التنبيه. يُستخدم عنواني لذلك فقط ويُحذف عند الإلغاء.", btn: "أنشئ التنبيه", ok: "اقتربنا: أكّد التنبيه عبر الرابط المرسل إلى {e}.", err: "تحقّق من البريد والميزانية وخانة الموافقة.", fail: "تعذّر إنشاء التنبيه. حاول لاحقًا." },
    it: { h: "Avviso prezzo via e-mail", p: "Ricevi un'e-mail quando un andata e ritorno scende sotto il tuo budget. Gratis, cancellazione in un clic.", email: "La tua e-mail", max: "Budget massimo (€)", consent: "Accetto di ricevere e-mail per questo avviso. Il mio indirizzo serve solo a questo e viene cancellato quando mi disiscrivo.", btn: "Crea l’avviso", ok: "Quasi fatto: conferma l’avviso con il link inviato a {e}.", err: "Controlla l’e-mail, il budget e la casella del consenso.", fail: "Non è stato possibile creare l’avviso. Riprova più tardi." },
    de: { h: "Preisalarm per E-Mail", p: "Erhalte eine E-Mail, sobald ein Hin- und Rückflug unter dein Budget fällt. Kostenlos, mit einem Klick abbestellbar.", email: "Deine E-Mail", max: "Maximales Budget (€)", consent: "Ich bin einverstanden, E-Mails zu diesem Alarm zu erhalten. Meine Adresse dient nur dazu und wird beim Abbestellen gelöscht.", btn: "Alarm erstellen", ok: "Fast geschafft: Bestätige den Alarm über den Link, der an {e} geschickt wurde.", err: "Prüfe die E-Mail, das Budget und das Einverständnis-Kästchen.", fail: "Der Alarm konnte nicht erstellt werden. Bitte versuche es später erneut." },
    nl: { h: "Prijsalert per e-mail", p: "Ontvang een e-mail zodra een retourvlucht onder je budget zakt. Gratis, met één klik af te melden.", email: "Je e-mailadres", max: "Maximaal budget (€)", consent: "Ik ga akkoord met e-mails voor deze alert. Mijn adres wordt alleen hiervoor gebruikt en wordt verwijderd als ik me afmeld.", btn: "Alert aanmaken", ok: "Bijna klaar: bevestig de alert via de link die naar {e} is gestuurd.", err: "Controleer het e-mailadres, het budget en het toestemmingsvakje.", fail: "De alert kon niet worden aangemaakt. Probeer het later opnieuw." }
  }[lang];
  if (!L) return;
  var esc = function (t) { return String(t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  // Alerte par notification sur le téléphone (Web Push) : sans e-mail, avec l'accord du navigateur. Site/sw.js affiche le message.
  var N = { fr: ["🔔 Ou par notification sur ce téléphone", "Sans e-mail : une notification quand le prix passe sous votre budget.", "Recevoir une notification", "C’est fait : vous serez prévenu sur cet appareil.", "Notifications refusées : autorisez-les dans les réglages du navigateur.", "Sur iPhone : ajoutez d’abord Escale à l’écran d’accueil (Partager → Sur l’écran d’accueil), puis ouvrez-le depuis l’icône."],
    en: ["🔔 Or by notification on this phone", "No email needed: a notification when the price drops below your budget.", "Get a notification", "Done: you will be notified on this device.", "Notifications blocked: allow them in your browser settings.", "On iPhone: first add Escale to your Home Screen (Share → Add to Home Screen), then open it from the icon."],
    es: ["🔔 O por notificación en este teléfono", "Sin correo: una notificación cuando el precio baje de tu presupuesto.", "Recibir una notificación", "Listo: recibirás el aviso en este dispositivo.", "Notificaciones bloqueadas: permítelas en los ajustes del navegador.", "En iPhone: añade primero Escale a la pantalla de inicio (Compartir → Añadir a pantalla de inicio) y ábrelo desde el icono."],
    pt: ["🔔 Ou por notificação neste telemóvel", "Sem e-mail: uma notificação quando o preço descer abaixo do seu orçamento.", "Receber uma notificação", "Feito: será avisado neste aparelho.", "Notificações bloqueadas: permita-as nas definições do navegador.", "No iPhone: adicione primeiro a Escale ao ecrã principal (Partilhar → Adicionar ao ecrã principal) e abra-a pelo ícone."],
    ar: ["🔔 أو عبر إشعار على هذا الهاتف", "بلا بريد إلكتروني: إشعار عندما ينخفض السعر إلى أقل من ميزانيتك.", "تلقَّ إشعارًا", "تم: ستتلقى التنبيه على هذا الجهاز.", "الإشعارات محظورة: اسمح بها في إعدادات المتصفح.", "على آيفون: أضف Escale أولًا إلى الشاشة الرئيسية (مشاركة ← إضافة إلى الشاشة الرئيسية) ثم افتحه من الأيقونة."],
    it: ["🔔 Oppure con una notifica su questo telefono", "Senza e-mail: una notifica quando il prezzo scende sotto il tuo budget.", "Ricevi una notifica", "Fatto: riceverai l’avviso su questo dispositivo.", "Notifiche bloccate: consentile nelle impostazioni del browser.", "Su iPhone: aggiungi prima Escale alla schermata Home (Condividi → Aggiungi alla schermata Home), poi aprilo dall’icona."],
    de: ["🔔 Oder per Benachrichtigung auf diesem Handy", "Ohne E-Mail: eine Benachrichtigung, sobald der Preis unter dein Budget fällt.", "Benachrichtigung erhalten", "Erledigt: Du wirst auf diesem Gerät benachrichtigt.", "Benachrichtigungen blockiert: Erlaube sie in den Browser-Einstellungen.", "Auf dem iPhone: Füge Escale zuerst zum Home-Bildschirm hinzu (Teilen → Zum Home-Bildschirm) und öffne es über das Symbol."],
    nl: ["🔔 Of met een melding op deze telefoon", "Zonder e-mail: een melding zodra de prijs onder je budget zakt.", "Melding ontvangen", "Klaar: je krijgt een melding op dit apparaat.", "Meldingen geblokkeerd: sta ze toe in de browserinstellingen.", "Op iPhone: zet Escale eerst op je beginscherm (Deel → Zet op beginscherm) en open het via het icoon."] }[lang] || null;
  var b64 = function (s) { s = s.replace(/-/g, "+").replace(/_/g, "/"); while (s.length % 4) s += "="; var r = atob(s), u = new Uint8Array(r.length); for (var i = 0; i < r.length; i++) u[i] = r.charCodeAt(i); return u; };
  var pushOk = N && "serviceWorker" in navigator && "PushManager" in window && "Notification" in window;
  var ios = /iPhone|iPad|iPod/.test(navigator.userAgent) && !(window.navigator.standalone || (window.matchMedia && matchMedia("(display-mode: standalone)").matches));
  var renderPush = function () {
    if (!N || (!pushOk && !ios)) return;
    var d = document.createElement("div"); d.className = "push-box";
    d.innerHTML = "<h3>" + esc(N[0]) + '</h3><p class="small">' + esc(N[1]) + "</p>" +
      '<div class="alert-row"><label><span>' + esc(L.max) + '</span><input type="number" name="pmax" min="1" inputmode="numeric"></label></div>' +
      '<button class="btn ghost" type="button">' + esc(N[2]) + '</button><p class="small push-msg" role="status"></p>';
    box.appendChild(d); box.hidden = false;
    Array.prototype.forEach.call(document.querySelectorAll(".alert-cta"), function (a) { a.hidden = false; });
    var inp = d.querySelector("input"), btn = d.querySelector("button"), out = d.querySelector(".push-msg");
    var sug = function () { var st = document.querySelector("#hero-price strong"), n = st ? Number(st.textContent.replace(/[^0-9]/g, "")) : 0; if (n > 0 && !inp.value) inp.value = Math.max(1, Math.floor(n * 0.9 / 10) * 10); };
    sug(); setTimeout(sug, 2500);
    if (ios && !pushOk) { btn.hidden = true; inp.parentNode.parentNode.hidden = true; out.textContent = N[5]; return; }
    btn.addEventListener("click", function () {
      var max = Number(inp.value);
      if (!(max > 0)) { out.textContent = L.err; inp.focus(); return; }
      btn.disabled = true;
      Notification.requestPermission().then(function (perm) {
        if (perm !== "granted") { out.textContent = N[4]; btn.disabled = false; return null; }
        return Promise.all([navigator.serviceWorker.register("/sw.js").then(function () { return navigator.serviceWorker.ready; }),
          fetch("/api/push?action=key").then(function (r) { return r.json(); })]).then(function (res) {
          return res[0].pushManager.getSubscription().then(function (sub) { return sub || res[0].pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: b64(res[1].key) }); });
        }).then(function (sub) {
          return fetch("/api/push", { method: "POST", headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ endpoint: sub.endpoint, max: max, from: box.getAttribute("data-from"), to: box.getAttribute("data-to"), lang: lang, currency: "EUR" }) });
        }).then(function (r) { out.textContent = r && r.ok ? N[3] : L.fail; if (!(r && r.ok)) btn.disabled = false; });
      }).catch(function () { out.textContent = L.fail; btn.disabled = false; });
    });
  };
  fetch("/api/alert?action=status").then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }).then(function (s) {
    if (!s || !s.enabled) { renderPush(); return; }
    box.innerHTML = "<h2>" + esc(L.h) + '</h2><p class="small">' + esc(L.p) + "</p>" +
      '<form class="alert-form" novalidate><div class="alert-row">' +
      '<label><span>' + esc(L.email) + '</span><input type="email" name="email" required autocomplete="email"></label>' +
      '<label><span>' + esc(L.max) + '</span><input type="number" name="max" min="1" inputmode="numeric" required></label></div>' +
      '<label class="alert-consent"><input type="checkbox" name="consent" required> <span>' + esc(L.consent) + "</span></label>" +
      '<button class="btn" type="submit">' + esc(L.btn) + '</button><p class="small alert-msg" role="status"></p></form>';
    box.hidden = false;
    Array.prototype.forEach.call(document.querySelectorAll(".alert-cta"), function (a) { a.hidden = false; });
    renderPush();
    var form = box.querySelector("form"), msg = box.querySelector(".alert-msg");
    // Budget proposé : 90 % du prix le plus bas affiché en haut de la page (s'il est connu)
    var suggest = function () {
      var st = document.querySelector("#hero-price strong"), n = st ? Number(st.textContent.replace(/[^0-9]/g, "")) : 0;
      if (n > 0 && !form.max.value) form.max.value = Math.max(1, Math.floor(n * 0.9 / 10) * 10);
      return n > 0;
    };
    if (!suggest()) setTimeout(suggest, 2500);
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var email = form.email.value.trim(), max = Number(form.max.value);
      if (!/^\S+@\S+\.\S+$/.test(email) || !(max > 0) || !form.consent.checked) { msg.textContent = L.err; return; }
      form.querySelector("button").disabled = true;
      fetch("/api/alert", { method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email, max: max, from: box.getAttribute("data-from"), to: box.getAttribute("data-to"), lang: lang, currency: "EUR", consent: true }) })
        .then(function (r) { return r.ok; }).catch(function () { return false; }).then(function (ok) {
          if (ok) { form.reset(); msg.textContent = L.ok.replace("{e}", email); }
          else { msg.textContent = L.fail; form.querySelector("button").disabled = false; }
        });
    });
  });
})();
