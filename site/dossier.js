// « Mon dossier de visa » : check-list cochable (gardée dans ce navigateur) + modèle de lettre d'invitation à copier.
(function () {
  "use strict";
  var box = document.getElementById("dv-app");
  if (!box) return;
  var T = JSON.parse(box.getAttribute("data-t")), L = JSON.parse(box.getAttribute("data-l"));
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var sel = document.getElementById("dv-dest"), list = document.getElementById("dv-list"), bar = document.getElementById("dv-bar");
  var key = function () { return "escale.dossier." + sel.value; };
  var load = function () { try { return JSON.parse(localStorage.getItem(key()) || "{}"); } catch (e) { return {}; } };
  var save = function (o) { try { localStorage.setItem(key(), JSON.stringify(o)); } catch (e) {} };
  var draw = function () {
    var d = L[sel.value], st = load();
    list.innerHTML = d.items.map(function (x, i) {
      return '<li><label class="dv-item"><input type="checkbox" data-i="' + i + '"' + (st[i] ? " checked" : "") + "> <span><strong>" + esc(x[0]) + "</strong>" + (x[1] ? "<small>" + esc(x[1]) + "</small>" : "") + "</span></label></li>";
    }).join("");
    document.getElementById("dv-off").innerHTML = '<a href="' + esc(d.url) + '" target="_blank" rel="noopener">' + esc(d.off) + "</a>";
    document.getElementById("dv-when").textContent = d.when || "";
    prog();
  };
  var prog = function () {
    var all = list.querySelectorAll("input"), done = list.querySelectorAll("input:checked").length;
    bar.style.setProperty("--p", (all.length ? Math.round(done / all.length * 100) : 0) + "%");
    bar.textContent = T.prog.replace("{d}", done).replace("{n}", all.length);
  };
  list.addEventListener("change", function (e) { var i = e.target.getAttribute("data-i"); if (i == null) return; var st = load(); st[i] = e.target.checked; save(st); prog(); });
  sel.addEventListener("change", draw);
  draw();
  // Lettre d'invitation
  var lf = document.getElementById("dv-letter");
  if (lf) lf.addEventListener("submit", function (e) {
    e.preventDefault();
    var v = function (n) { return (lf.querySelector('[name="' + n + '"]').value || "").trim() || "…"; };
    var txt = T.letter.replace(/\{(\w+)\}/g, function (_, k) { return v(k); });
    var out = document.getElementById("dv-letter-out");
    out.hidden = false; out.querySelector("textarea").value = txt;
  });
  var cp = document.getElementById("dv-copy");
  if (cp) cp.addEventListener("click", function () {
    var ta = document.querySelector("#dv-letter-out textarea"); ta.select();
    (navigator.clipboard ? navigator.clipboard.writeText(ta.value) : Promise.reject()).then(function () { cp.textContent = T.copied; }, function () { document.execCommand("copy"); cp.textContent = T.copied; });
  });
})();
