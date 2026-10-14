// Formulaire « Recevoir les bons plans » (Netlify Forms) : envoi sans quitter la page, messages dans la langue de la page.
(function () {
  "use strict";
  var M = {
    fr: { ok: "Merci ! Vous recevrez nos prochains bons plans.", need: "Indiquez un e-mail ou un numéro WhatsApp, et cochez la case de consentement.", fail: "L’inscription n’a pas abouti. Réessayez plus tard." },
    en: { ok: "Thank you! You will receive our next deals.", need: "Enter an email or a WhatsApp number, and tick the consent box.", fail: "Sign-up failed. Please try again later." },
    es: { ok: "¡Gracias! Recibirás nuestras próximas ofertas.", need: "Indica un correo o un número de WhatsApp y marca la casilla de consentimiento.", fail: "No se pudo completar la inscripción. Inténtalo más tarde." },
    pt: { ok: "Obrigado! Vai receber as nossas próximas promoções.", need: "Indique um e-mail ou um número de WhatsApp e marque a caixa de consentimento.", fail: "A inscrição falhou. Tente mais tarde." },
    ar: { ok: "شكرًا! ستصلك عروضنا القادمة.", need: "أدخل بريدًا إلكترونيًا أو رقم واتساب، وحدّد خانة الموافقة.", fail: "تعذّر التسجيل. حاول لاحقًا." }
  };
  document.querySelectorAll("form[name='bons-plans']").forEach(function (form) {
    var msg = form.querySelector(".nl-msg");
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var L = M[(document.documentElement.lang || "fr").slice(0, 2)] || M.fr;
      var email = form.email.value.trim(), wa = form.whatsapp.value.trim();
      if ((!/^\S+@\S+\.\S+$/.test(email) && !/^\+?[0-9 ]{8,20}$/.test(wa)) || !form.consent.checked) { msg.textContent = L.need; return; }
      form.langue.value = document.documentElement.lang || "fr";
      var data = new URLSearchParams(new FormData(form)).toString();
      form.querySelector("button").disabled = true;
      fetch("/", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: data })
        .then(function (r) { return r.ok; }).catch(function () { return false; }).then(function (ok) {
          msg.textContent = ok ? L.ok : L.fail;
          if (ok) form.reset(); else form.querySelector("button").disabled = false;
        });
    });
  });
})();
