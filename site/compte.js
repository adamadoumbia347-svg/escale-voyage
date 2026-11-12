// Page « Compte à rebours » : fabrique dans le navigateur une image 1080×1920 « J-45 avant Abidjan » à partager (statut WhatsApp).
// Rien n'est envoyé. Si la ville de départ est donnée, on ajoute le prix aller-retour le plus bas repéré pour le mois du départ (/api/prix).
(function () {
  "use strict";
  var f = document.getElementById("cr-form");
  if (!f || !window.EscaleAC) return;
  var to = document.getElementById("cr-to"), from = document.getElementById("cr-from"), date = document.getElementById("cr-date"), msg = document.getElementById("cr-msg");
  var out = document.getElementById("cr-out"), cv = document.getElementById("cr-canvas");
  var today = new Date(); today.setHours(0, 0, 0, 0);
  date.min = new Date(today.getTime() - today.getTimezoneOffset() * 6e4).toISOString().slice(0, 10);
  window.EscaleAC.attach(to); window.EscaleAC.attach(from);
  var flag = function (cc) { return cc && cc.length === 2 ? String.fromCodePoint.apply(null, cc.toUpperCase().split("").map(function (c) { return 127397 + c.charCodeAt(0); })) : "✈️"; };
  var FONT = '"Plus Jakarta Sans", "Segoe UI", system-ui, sans-serif';
  function fit(ctx, text, max, size, weight) { do { ctx.font = weight + " " + size + "px " + FONT; size -= 4; } while (ctx.measureText(text).width > max && size > 40); }
  function dessiner(o) {
    var c = cv.getContext("2d"), W = 1080, H = 1920;
    var g = c.createRadialGradient(W / 2, H * .42, 80, W / 2, H * .42, 1300); g.addColorStop(0, "#0e7a70"); g.addColorStop(.55, "#073a40"); g.addColorStop(1, "#031418");
    c.fillStyle = g; c.fillRect(0, 0, W, H);
    c.strokeStyle = "rgba(127,243,222,.14)"; c.lineWidth = 2;
    for (var i = 0; i < 14; i++) { c.beginPath(); c.arc(W / 2, H * .42, 120 + i * 90, 0, Math.PI * 2); c.stroke(); }
    c.textAlign = "center"; c.fillStyle = "#7ff3de";
    c.font = "800 54px " + FONT; c.fillText("✈ escale.live", W / 2, 230);
    c.fillStyle = "#fff"; c.font = "700 70px " + FONT; c.fillText(o.n === 0 ? "C’est aujourd’hui !" : o.n === 1 ? "Plus qu’un jour" : "Plus que", W / 2, 560);
    c.shadowColor = "rgba(0,0,0,.45)"; c.shadowBlur = 40; c.shadowOffsetY = 18;
    c.fillStyle = "#ffe08a"; fit(c, o.n === 0 ? "Jour J" : "J-" + o.n, 940, 430, 800); c.fillText(o.n === 0 ? "Jour J" : "J-" + o.n, W / 2, 960);
    c.shadowColor = "transparent"; c.shadowBlur = 0; c.shadowOffsetY = 0;
    c.fillStyle = "#fff"; c.font = "700 70px " + FONT; c.fillText("avant", W / 2, 1110);
    fit(c, o.ville + " " + o.flag, 960, 150, 800); c.fillText(o.ville + " " + o.flag, W / 2, 1270);
    c.fillStyle = "rgba(255,255,255,.9)"; c.font = "600 52px " + FONT; c.fillText("Départ le " + o.jour, W / 2, 1380);
    if (o.prix) {
      c.fillStyle = "rgba(255,255,255,.96)"; var bw = 880, bx = (W - bw) / 2, by = 1450, bh = 170, r = 40;
      c.beginPath(); c.moveTo(bx + r, by); c.arcTo(bx + bw, by, bx + bw, by + bh, r); c.arcTo(bx + bw, by + bh, bx, by + bh, r); c.arcTo(bx, by + bh, bx, by, r); c.arcTo(bx, by, bx + bw, by, r); c.fill();
      c.fillStyle = "#08303a"; fit(c, o.prix, 800, 54, 800); c.fillText(o.prix, W / 2, by + 78); c.fillStyle = "#5b6474"; c.font = "600 34px " + FONT; c.fillText(o.note, W / 2, by + 134);
    }
    c.fillStyle = "#7ff3de"; c.font = "700 46px " + FONT; c.fillText("Tape « escale live » sur Google", W / 2, 1760);
  }
  f.addEventListener("submit", function (e) {
    e.preventDefault();
    var b = to.dataset.code, d = date.value;
    if (!b || !d) { msg.textContent = "Choisissez la destination dans la liste, puis la date du départ."; return; }
    var dep = new Date(d + "T00:00:00"), n = Math.round((dep - today) / 864e5);
    if (n < 0) { msg.textContent = "Cette date est déjà passée."; return; }
    msg.textContent = "";
    var ville = window.EscaleAC.name(b), a = from.dataset.code;
    var o = { n: n, ville: ville, flag: flag(window.EscaleAC.cc(b)), jour: dep.toLocaleDateString("fr-FR", { weekday: "long", day: "numeric", month: "long", year: "numeric" }) };
    var finir = function () {
      (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(function () {
        dessiner(o); out.hidden = false;
        var texte = (n === 0 ? "C’est aujourd’hui : départ pour " : "J-" + n + " avant ") + ville + " " + o.flag + " ✈️ https://escale.live/compte-a-rebours/";
        document.getElementById("cr-wa").href = "https://wa.me/?text=" + encodeURIComponent(texte);
        cv.toBlob(function (blob) {
          if (!blob) return;
          var dl = document.getElementById("cr-dl"); if (dl.href) URL.revokeObjectURL(dl.href); dl.href = URL.createObjectURL(blob);
          var sh = document.getElementById("cr-share"), file = null;
          try { file = new File([blob], "escale-compte-a-rebours.jpg", { type: "image/jpeg" }); } catch (err) {}
          sh.hidden = !(file && navigator.canShare && navigator.canShare({ files: [file] }));
          sh.onclick = function () { navigator.share({ files: [file], text: texte }).catch(function () {}); };
        }, "image/jpeg", 0.9);
        out.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    };
    if (a && a !== b) {
      fetch("/api/prix?from=" + a + "&to=" + b + "&dep=" + d + "&rt=1&currency=EUR").then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }).then(function (j) {
        if (j && j.available && j.price > 0 && (!j.currency || j.currency === "EUR")) { o.prix = window.EscaleAC.name(a) + " → " + ville + " : dès " + Math.round(j.price).toLocaleString("fr-FR") + " € A/R"; o.note = "prix repéré récemment, à confirmer à la réservation"; }
        finir();
      });
    } else finir();
  });
})();
