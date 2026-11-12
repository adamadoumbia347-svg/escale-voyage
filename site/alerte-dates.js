// Page « Recherche en direct » : quand le visiteur change plusieurs fois de dates sur le même trajet (il hésite), on lui propose
// l'alerte prix par e-mail de ce trajet (même service que sur les pages trajets : /api/alert, confirmation par e-mail, désinscription en un clic).
// Petite pastille fixe en bas de l'écran, qui s'ouvre au toucher : elle ne déplace rien dans la page et se ferme d'un geste.
// Rien n'est envoyé tant que le formulaire n'est pas validé ; le compteur de changements reste dans ce navigateur (sessionStorage).
(function () {
  "use strict";
  var SEUIL = 2, PAUSE = 7 * 864e5; // proposée après 2 changements de dates ; refusée : plus proposée pendant 7 jours
  var LG = "fr"; try { LG = (localStorage.getItem("escale.lang") || (navigator.language || "fr").slice(0, 2)).toLowerCase(); } catch (e) {}
  var T = ({
    fr: { pill: "🔔 Tu hésites sur les dates ?", h: "On surveille ce trajet pour toi", p: "Reçois un e-mail quand l’aller-retour {r} passe sous ton budget. Gratuit, désinscription en un clic.", email: "Ton e-mail", max: "Budget maximum (€)", consent: "J’accepte de recevoir des e-mails pour cette alerte. Mon adresse ne sert qu’à cela.", btn: "Créer mon alerte", ok: "C’est noté : ouvre l’e-mail envoyé à {e} pour confirmer l’alerte.", err: "Vérifie l’e-mail, le budget et la case à cocher.", fail: "L’alerte n’a pas pu être créée. Réessaie dans un instant.", close: "Fermer", seen: "Prix repéré récemment : dès {p} €" },
    en: { pill: "🔔 Not sure about the dates?", h: "We watch this route for you", p: "Get an email when a {r} round trip drops below your budget. Free, one-click unsubscribe.", email: "Your email", max: "Maximum budget (€)", consent: "I agree to receive emails for this alert. My address is used for nothing else.", btn: "Create my alert", ok: "Done: open the email sent to {e} to confirm the alert.", err: "Check the email, the budget and the box.", fail: "The alert could not be created. Try again in a moment.", close: "Close", seen: "Recently spotted: from €{p}" },
    it: { pill: "🔔 Indeciso sulle date?", h: "Teniamo d’occhio questa tratta per te", p: "Ricevi un’e-mail quando l’andata e ritorno {r} scende sotto il tuo budget. Gratis, cancellazione in un clic.", email: "La tua e-mail", max: "Budget massimo (€)", consent: "Accetto di ricevere e-mail per questo avviso. Il mio indirizzo serve solo a questo.", btn: "Crea il mio avviso", ok: "Fatto: apri l’e-mail inviata a {e} per confermare l’avviso.", err: "Controlla l’e-mail, il budget e la casella.", fail: "Non è stato possibile creare l’avviso. Riprova tra un attimo.", close: "Chiudi", seen: "Prezzo rilevato di recente: da {p} €" },
    es: { pill: "🔔 ¿Dudas con las fechas?", h: "Vigilamos esta ruta por ti", p: "Recibe un correo cuando el ida y vuelta {r} baje de tu presupuesto. Gratis, baja en un clic.", email: "Tu correo", max: "Presupuesto máximo (€)", consent: "Acepto recibir correos para esta alerta. Mi dirección solo sirve para esto.", btn: "Crear mi alerta", ok: "Listo: abre el correo enviado a {e} para confirmar la alerta.", err: "Revisa el correo, el presupuesto y la casilla.", fail: "No se pudo crear la alerta. Inténtalo de nuevo en un momento.", close: "Cerrar", seen: "Precio visto hace poco: desde {p} €" },
    pt: { pill: "🔔 Indeciso nas datas?", h: "Vigiamos esta rota por si", p: "Receba um e-mail quando a ida e volta {r} descer abaixo do seu orçamento. Grátis, cancelamento num clique.", email: "O seu e-mail", max: "Orçamento máximo (€)", consent: "Aceito receber e-mails para este alerta. O meu endereço só serve para isto.", btn: "Criar o meu alerta", ok: "Feito: abra o e-mail enviado para {e} para confirmar o alerta.", err: "Verifique o e-mail, o orçamento e a caixa.", fail: "Não foi possível criar o alerta. Tente de novo daqui a pouco.", close: "Fechar", seen: "Preço visto recentemente: desde {p} €" },
    de: { pill: "🔔 Unsicher bei den Daten?", h: "Wir beobachten diese Strecke für dich", p: "Erhalte eine E-Mail, sobald der Hin- und Rückflug {r} unter dein Budget fällt. Kostenlos, mit einem Klick abbestellbar.", email: "Deine E-Mail", max: "Maximales Budget (€)", consent: "Ich bin mit E-Mails für diesen Alarm einverstanden. Meine Adresse wird nur dafür genutzt.", btn: "Preisalarm erstellen", ok: "Erledigt: Öffne die E-Mail an {e}, um den Alarm zu bestätigen.", err: "Prüfe E-Mail, Budget und Häkchen.", fail: "Der Alarm konnte nicht erstellt werden. Versuch es gleich noch einmal.", close: "Schließen", seen: "Kürzlich gesehen: ab {p} €" },
    ar: { pill: "🔔 متردد في التواريخ؟", h: "نراقب هذا المسار من أجلك", p: "تلقَّ رسالة عندما ينخفض سعر الذهاب والعودة {r} إلى أقل من ميزانيتك. مجاني، والإلغاء بنقرة.", email: "بريدك الإلكتروني", max: "الميزانية القصوى (€)", consent: "أوافق على تلقي رسائل لهذا التنبيه. عنواني يُستعمل لهذا فقط.", btn: "إنشاء التنبيه", ok: "تم: افتح الرسالة المرسلة إلى {e} لتأكيد التنبيه.", err: "تحقق من البريد والميزانية والخانة.", fail: "تعذر إنشاء التنبيه. حاول بعد لحظة.", close: "إغلاق", seen: "سعر شوهد مؤخرًا: من {p} €" }
  })[LG] || null;
  if (!T) T = null;
  var esc = function (t) { return String(t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var parse = function () {
    var q = new URLSearchParams(location.search).get("flightSearch") || "", m = q.match(/^([A-Z]{3})(\d{4})([A-Z]{3})(\d{4})?/);
    return m ? { r: m[1] + "-" + m[3], from: m[1], to: m[3], d: m[2] + (m[4] || "") } : null;
  };
  var sget = function (k) { try { return JSON.parse(sessionStorage.getItem(k) || "null"); } catch (e) { return null; } };
  var sset = function (k, v) { try { sessionStorage.setItem(k, JSON.stringify(v)); } catch (e) {} };
  var lget = function (k) { try { return JSON.parse(localStorage.getItem(k) || "null"); } catch (e) { return null; } };
  var lset = function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} };
  // Compteur anonyme (même service que site/clics.js) : pastille affichée, ouverte, alerte créée
  var compte = function (k) { var b = JSON.stringify({ k: k, p: "recherche" }); try { if (navigator.sendBeacon && navigator.sendBeacon("/api/clic", b)) return; } catch (e) {} try { fetch("/api/clic", { method: "POST", body: b, keepalive: true }); } catch (e) {} };
  // Les e-mails d'alerte existent dans les 7 langues de cette pastille (src/_lib/alert-texts.ts)
  var MAIL = LG;
  var shown = false;
  function compter() {
    var s = parse(); if (!s) return;
    var st = sget("escale.dates") || {};
    if (st.r === s.r) { if (st.d !== s.d) { st.n = (st.n || 0) + 1; st.d = s.d; } } else st = { r: s.r, d: s.d, n: 0 };
    sset("escale.dates", st);
    if (st.n >= SEUIL) proposer(s);
  }
  function proposer(s) {
    if (shown || !T) return;
    var mem = lget("escale.alerte-dates") || {};
    if ((mem.faites || []).indexOf(s.r) >= 0 || (mem.non && Date.now() - mem.non < PAUSE)) return;
    shown = true;
    fetch("/api/alert?action=status").then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }).then(function (ok) {
      if (!ok || !ok.enabled) return;
      var box = document.createElement("div"); box.className = "ad-box"; box.dir = LG === "ar" ? "rtl" : "ltr";
      var route = s.from + " → " + s.to;
      box.innerHTML = '<button type="button" class="ad-pill">' + esc(T.pill) + '</button><div class="ad-card" hidden><button type="button" class="ad-x" aria-label="' + esc(T.close) + '">×</button>' +
        "<p class=\"ad-h\">" + esc(T.h) + '</p><p class="small">' + esc(T.p.replace("{r}", route)) + '</p><p class="small ad-seen" hidden></p>' +
        '<form novalidate><div class="ad-row"><label><span>' + esc(T.email) + '</span><input type="email" name="email" required autocomplete="email"></label>' +
        "<label><span>" + esc(T.max) + '</span><input type="number" name="max" min="1" inputmode="numeric" required></label></div>' +
        '<label class="ad-consent"><input type="checkbox" name="consent" required> <span>' + esc(T.consent) + "</span></label>" +
        '<button class="btn" type="submit">' + esc(T.btn) + '</button><p class="small ad-msg" role="status"></p></form></div>';
      document.body.appendChild(box);
      // Bandeau des cookies encore affiché (nouveau visiteur) : la pastille se place juste au-dessus, puis redescend quand il disparaît
      var caler = function () { var cc = document.querySelector(".cc-bar"); box.style.bottom = cc && cc.offsetHeight ? (cc.offsetHeight + 12) + "px" : ""; };
      caler(); var tc = setInterval(function () { if (!document.body.contains(box)) { clearInterval(tc); return; } caler(); }, 800);
      compte("alerte-dates-vue");
      var pill = box.querySelector(".ad-pill"), card = box.querySelector(".ad-card"), form = box.querySelector("form"), msg = box.querySelector(".ad-msg");
      var fermer = function () { var m = lget("escale.alerte-dates") || {}; m.non = Date.now(); lset("escale.alerte-dates", m); box.remove(); };
      pill.addEventListener("click", function () {
        pill.hidden = true; card.hidden = false; form.email.focus();
        // Budget proposé : 90 % du prix repéré récemment pour ce trajet, s'il est connu
        fetch("/api/connus?r=" + s.r).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }).then(function (j) {
          var p = j && j.prix && j.prix[s.r] && j.prix[s.r].price;
          if (p > 0) { var e = box.querySelector(".ad-seen"); e.textContent = T.seen.replace("{p}", Math.round(p)); e.hidden = false; if (!form.max.value) form.max.value = Math.max(1, Math.floor(p * 0.9 / 10) * 10); }
        });
        compte("alerte-dates-ouverte");
      });
      box.querySelector(".ad-x").addEventListener("click", fermer);
      form.addEventListener("submit", function (ev) {
        ev.preventDefault();
        var email = form.email.value.trim(), max = Number(form.max.value);
        if (!/^\S+@\S+\.\S+$/.test(email) || !(max > 0) || !form.consent.checked) { msg.textContent = T.err; return; }
        var b = form.querySelector("button"); b.disabled = true;
        fetch("/api/alert", { method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: email, max: max, from: s.from, to: s.to, lang: MAIL, currency: "EUR", consent: true }) })
          .then(function (r) { return r.ok; }).catch(function () { return false; }).then(function (ok2) {
            if (ok2) { compte("alerte-dates-creee"); var m = lget("escale.alerte-dates") || {}; m.faites = (m.faites || []).concat([s.r]).slice(-30); lset("escale.alerte-dates", m);
              form.hidden = true; var p = document.createElement("p"); p.className = "ad-ok"; p.textContent = T.ok.replace("{e}", email); card.appendChild(p); }
            else { msg.textContent = T.fail; b.disabled = false; }
          });
      });
    });
  }
  compter();
  // Le moteur peut changer l'adresse sans recharger la page : on recompte alors
  var last = location.search;
  setInterval(function () { if (location.search !== last) { last = location.search; compter(); } }, 2000);
})();
