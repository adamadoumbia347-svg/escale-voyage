// Page « Ponts 2027 » : le visiteur choisit son trajet, et chaque ligne du calendrier ouvre la recherche en direct aux dates du pont.
// Le trajet est gardé dans ce navigateur pour la prochaine visite ; rien n'est envoyé.
(function () {
  "use strict";
  var f = document.getElementById("pt-form");
  if (!f || !window.EscaleAC) return;
  var from = document.getElementById("pt-from"), to = document.getElementById("pt-to"), msg = document.getElementById("pt-msg");
  var ddmm = function (d) { return d.slice(8, 10) + d.slice(5, 7); };
  var today = new Date().toISOString().slice(0, 10);
  var maj = function () {
    var a = from.dataset.code, b = to.dataset.code, ok = a && b && a !== b;
    [].forEach.call(document.querySelectorAll("a.pt-go"), function (l) {
      var dep = l.getAttribute("data-dep"), ret = l.getAttribute("data-ret");
      if (dep < today) { l.removeAttribute("href"); l.textContent = "Passé"; l.classList.add("pt-off"); return; }
      if (ok) { l.href = "/recherche/?flightSearch=" + a + ddmm(dep) + b + ddmm(ret) + "1"; l.target = "_blank"; l.rel = "noopener"; l.classList.remove("pt-off"); }
      else { l.href = "#pt-form"; l.removeAttribute("target"); l.classList.add("pt-off"); }
    });
    if (ok) { msg.textContent = "Trajet " + window.EscaleAC.name(a) + " → " + window.EscaleAC.name(b) + " : touchez « Voir les vols » sur la ligne de votre choix."; try { localStorage.setItem("escale.ponts", a + "-" + b); } catch (e) {} }
  };
  var A = window.EscaleAC.attach(from, maj), B = window.EscaleAC.attach(to, maj);
  from.addEventListener("input", maj); to.addEventListener("input", maj);
  window.EscaleAC.ready.then(function () {
    var s = ""; try { s = localStorage.getItem("escale.ponts") || ""; } catch (e) {}
    var m = s.match(/^([A-Z]{3})-([A-Z]{3})$/);
    if (m) { A.set(m[1]); B.set(m[2]); }
    maj();
  });
  f.addEventListener("submit", function (e) { e.preventDefault(); });
})();
