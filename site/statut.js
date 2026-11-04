// Bouton « Partager en statut » : crée une image verticale (1080×1920) avec les 5 meilleurs prix aller-retour du moment
// depuis la ville du visiteur (/api/explore, mois prochain), à publier en statut WhatsApp / story. Rien n'est envoyé ailleurs.
(function () {
  "use strict";
  var btn = document.getElementById("statut-btn");
  if (!btn) return;
  var get = function (u) { return fetch(u).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); };
  var L = function () {
    var l = (document.documentElement.lang || "fr").slice(0, 2);
    return l === "fr" ? { loc: "fr-FR", t: "Les bons plans du jour", from: "depuis", rt: "aller-retour", foot: "Prix trouvés le {d} · ils changent chaque jour", wait: "Création de l'image…", none: "Pas de prix disponible pour l'instant, réessayez plus tard.", dl: "Image enregistrée : publiez-la dans votre statut WhatsApp." }
      : { loc: "en-GB", t: "Today's best deals", from: "from", rt: "round trip", foot: "Prices found on {d} · they change every day", wait: "Creating the image…", none: "No prices available right now, try again later.", dl: "Image saved: post it to your WhatsApp status." };
  };
  var rr = function (c, x, y, w, h, r) { c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); };
  btn.addEventListener("click", function () {
    var t = L(), msg = document.getElementById("statut-msg"), fr = window.ESCALE_FROM || { code: "PAR", name: "Paris" };
    var from = /^(CDG|ORY|BVA)$/.test(fr.code) ? "PAR" : fr.code;
    if (msg) msg.textContent = t.wait;
    btn.disabled = true;
    var d = new Date(), m = new Date(d.getFullYear(), d.getMonth() + 1, 1), month = m.getFullYear() + "-" + ("0" + (m.getMonth() + 1)).slice(-2);
    Promise.all([get("/api/explore?from=" + from + "&month=" + month + "&currency=EUR"), get("/data/airports.json")]).then(function (r) {
      var items = (r[0] && r[0].available && r[0].items || []).slice(0, 5), ap = {};
      (r[1] || []).forEach(function (a) { ap[a[0]] = a; });
      if (!items.length) { if (msg) msg.textContent = t.none; btn.disabled = false; return; }
      var cv = document.createElement("canvas"); cv.width = 1080; cv.height = 1920; var c = cv.getContext("2d");
      var g = c.createLinearGradient(0, 0, 0, 1920); g.addColorStop(0, "#0f8f80"); g.addColorStop(.55, "#0a5c63"); g.addColorStop(1, "#062b3a");
      c.fillStyle = g; c.fillRect(0, 0, 1080, 1920);
      c.fillStyle = "rgba(255,255,255,.08)"; for (var i = 0; i < 6; i++) { c.beginPath(); c.arc(150 + i * 170, 260 + (i % 2) * 90, 60 + i * 8, 0, 7); c.fill(); }
      var font = "'Instrument Sans', 'Segoe UI', system-ui, sans-serif";
      c.fillStyle = "#fff"; c.textAlign = "center";
      c.font = "700 64px " + font; c.fillText("✈️ escale.live", 540, 200);
      c.font = "700 92px " + font; c.fillText(t.t, 540, 420);
      c.font = "600 54px " + font; c.fillStyle = "#ffe14a"; c.fillText(t.from + " " + (fr.name || from), 540, 510);
      var money = function (n) { try { return new Intl.NumberFormat(t.loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n); } catch (e) { return Math.round(n) + " €"; } };
      var day = function (s) { try { return new Date(String(s).slice(0, 10) + "T12:00:00").toLocaleDateString(t.loc, { day: "numeric", month: "short" }); } catch (e) { return ""; } };
      items.forEach(function (it, k) {
        var y = 620 + k * 220, a = ap[it.to], city = a ? a[1] : it.to;
        c.fillStyle = "rgba(255,255,255,.95)"; rr(c, 80, y, 920, 180, 36); c.fill();
        c.textAlign = "left"; c.fillStyle = "#0f172a"; c.font = "700 58px " + font; c.fillText(city.length > 16 ? city.slice(0, 15) + "…" : city, 130, y + 85);
        c.fillStyle = "#64748b"; c.font = "600 34px " + font; c.fillText(day(it.departure_at) + (it.return_at ? " → " + day(it.return_at) : "") + " · " + t.rt, 130, y + 140);
        c.textAlign = "right"; c.fillStyle = "#0b8577"; c.font = "700 72px " + font; c.fillText(money(it.price), 950, y + 112);
      });
      c.textAlign = "center"; c.fillStyle = "#fff"; c.font = "700 50px " + font; c.fillText("👉 escale.live", 540, 1760);
      c.fillStyle = "rgba(255,255,255,.75)"; c.font = "500 30px " + font; c.fillText(t.foot.replace("{d}", d.toLocaleDateString(t.loc, { day: "numeric", month: "long" })), 540, 1830);
      cv.toBlob(function (blob) {
        btn.disabled = false;
        var file = new File([blob], "escale-bons-plans.png", { type: "image/png" });
        if (navigator.canShare && navigator.canShare({ files: [file] })) {
          navigator.share({ files: [file], text: "escale.live" }).catch(function () {}); if (msg) msg.textContent = "";
        } else {
          var u = URL.createObjectURL(blob), a2 = document.createElement("a"); a2.href = u; a2.download = "escale-bons-plans.png"; document.body.appendChild(a2); a2.click(); a2.remove();
          setTimeout(function () { URL.revokeObjectURL(u); }, 4000); if (msg) msg.textContent = t.dl;
        }
      }, "image/png");
    });
  });
})();
