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
    ar: { h: "تنبيه السعر عبر البريد", p: "تلقَّ رسالة عندما ينخفض سعر رحلة ذهاب وعودة إلى أقل من ميزانيتك. مجاني، والإلغاء بنقرة.", email: "بريدك الإلكتروني", max: "الميزانية القصوى (€)", consent: "أوافق على تلقي رسائل لهذا التنبيه. يُستخدم عنواني لذلك فقط ويُحذف عند الإلغاء.", btn: "أنشئ التنبيه", ok: "اقتربنا: أكّد التنبيه عبر الرابط المرسل إلى {e}.", err: "تحقّق من البريد والميزانية وخانة الموافقة.", fail: "تعذّر إنشاء التنبيه. حاول لاحقًا." }
  }[lang];
  if (!L) return;
  var esc = function (t) { return String(t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  fetch("/api/alert?action=status").then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }).then(function (s) {
    if (!s || !s.enabled) return;
    box.innerHTML = "<h2>" + esc(L.h) + '</h2><p class="small">' + esc(L.p) + "</p>" +
      '<form class="alert-form" novalidate><div class="alert-row">' +
      '<label><span>' + esc(L.email) + '</span><input type="email" name="email" required autocomplete="email"></label>' +
      '<label><span>' + esc(L.max) + '</span><input type="number" name="max" min="1" inputmode="numeric" required></label></div>' +
      '<label class="alert-consent"><input type="checkbox" name="consent" required> <span>' + esc(L.consent) + "</span></label>" +
      '<button class="btn" type="submit">' + esc(L.btn) + '</button><p class="small alert-msg" role="status"></p></form>';
    box.hidden = false;
    Array.prototype.forEach.call(document.querySelectorAll(".alert-cta"), function (a) { a.hidden = false; });
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
