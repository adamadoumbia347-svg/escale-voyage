/* « Que visiter » : jeu « Devine le pays ». Une vraie photo (créditée), quatre pays, dix manches, un score à partager.
   Tout se passe dans le navigateur ; seul le meilleur score est gardé dans le téléphone. */
(function () {
  "use strict";
  var box = document.getElementById("vx-jeu"), root = document.querySelector("[data-vx-data]"); if (!box || !root) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2); if (!/^(fr|en|it)$/.test(lang)) lang = "fr";
  var T = { fr: { q: "Dans quel pays se trouve ce lieu ?", n: "Photo {i} sur {t}", ok: "Bravo ! C'est {l}, {p}.", ko: "Raté : c'est {l}, {p}.", suiv: "Photo suivante", fin: "Voir mon score", voir: "Découvrir {p}",
      score: "{s} sur {t}", m: ["On voyage ensemble ? Il reste beaucoup à découvrir.", "Pas mal ! Encore quelques pays à explorer.", "Très bien ! Vous connaissez le monde.", "Parfait : rien ne vous échappe."],
      part: "Partager mon score", rej: "Rejouer", best: "Votre meilleur score : {s} sur {t}", txt: "J'ai reconnu {s} pays sur {t} en photo sur Escale. Et toi ?", photo: "Photo" },
    en: { q: "Which country is this place in?", n: "Photo {i} of {t}", ok: "Well done! It's {l}, {p}.", ko: "Not quite: it's {l}, {p}.", suiv: "Next photo", fin: "See my score", voir: "Discover {p}",
      score: "{s} out of {t}", m: ["Shall we travel together? There is a lot left to discover.", "Not bad! A few more countries to explore.", "Very good! You know your way around the world.", "Perfect: nothing gets past you."],
      part: "Share my score", rej: "Play again", best: "Your best score: {s} out of {t}", txt: "I recognised {s} countries out of {t} from photos on Escale. How about you?", photo: "Photo" },
    it: { q: "In quale paese si trova questo luogo?", n: "Foto {i} di {t}", ok: "Bravo! È {l}, {p}.", ko: "Sbagliato: è {l}, {p}.", suiv: "Foto successiva", fin: "Vedi il mio punteggio", voir: "Scopri {p}",
      score: "{s} su {t}", m: ["Viaggiamo insieme? C'è ancora molto da scoprire.", "Niente male! Ancora qualche paese da esplorare.", "Molto bene! Conosci il mondo.", "Perfetto: non ti sfugge nulla."],
      part: "Condividi il mio punteggio", rej: "Gioca ancora", best: "Il tuo punteggio migliore: {s} su {t}", txt: "Ho riconosciuto {s} paesi su {t} dalle foto su Escale. E tu?", photo: "Foto" } }[lang];
  var esc = function (t) { return String(t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var fmt = function (s, o) { return s.replace(/\{(\w+)\}/g, function (_, k) { return o[k]; }); };
  var mel = function (a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), x = a[i]; a[i] = a[j]; a[j] = x; } return a; };
  var N = 10, D = null, tours = [], i = 0, score = 0;
  var charger = function () { return D ? Promise.resolve(D) : fetch(root.dataset.vxData).then(function (r) { return r.json(); }).then(function (d) { D = d; return d; }); };
  var nouveau = function () {
    charger().then(function (d) {
      if (d.pays.length < 4) return;
      // dix pays différents, un lieu au hasard dans chacun ; trois autres pays en réponses (deux de la même région quand c'est possible)
      tours = mel(d.pays).slice(0, N).map(function (p) {
        var meme = mel(d.pays.filter(function (x) { return x.cc !== p.cc && x.region === p.region; })).slice(0, 2);
        var reste = mel(d.pays.filter(function (x) { return x.cc !== p.cc && meme.indexOf(x) < 0; })).slice(0, 3 - meme.length);
        return { p: p, l: p.lieux[Math.floor(Math.random() * p.lieux.length)], rep: mel([p].concat(meme, reste)) };
      });
      i = 0; score = 0; manche();
    }).catch(function () {});
  };
  var manche = function () {
    var t = tours[i];
    box.innerHTML = '<p class="vj-n">' + esc(fmt(T.n, { i: i + 1, t: tours.length })) + '</p><div class="vj-ph"><img src="/img/visiter/' + esc(t.l.k) + '.webp" alt="" width="1100" height="733"></div>' +
      '<p class="vx-cred">' + T.photo + " : " + esc(t.l.a) + ", " + esc(t.l.l) + ', Wikimedia Commons</p><h2 class="vj-q">' + esc(T.q) + '</h2><div class="vj-rep">' +
      t.rep.map(function (p) { return '<button type="button" data-cc="' + p.cc + '">' + p.flag + " " + esc(p.nom) + "</button>"; }).join("") + '</div><div class="vj-res" role="status"></div>';
    if (tours[i + 1]) { var pre = new Image(); pre.src = "/img/visiter/" + tours[i + 1].l.k + ".webp"; }
    box.scrollIntoView({ block: "nearest", behavior: "smooth" });
  };
  box.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest("button"); if (!b) return;
    if (b.id === "vj-go" || b.dataset.a === "rej") return nouveau();
    if (b.dataset.a === "suiv") { i++; return i < tours.length ? manche() : fin(); }
    if (b.dataset.a === "part") {
      var txt = fmt(T.txt, { s: score, t: tours.length }), url = location.origin + location.pathname;
      if (navigator.share) navigator.share({ text: txt, url: url }).catch(function () {}); else window.open("https://wa.me/?text=" + encodeURIComponent(txt + " " + url), "_blank", "noopener");
      return;
    }
    if (!b.dataset.cc || box.querySelector(".vj-rep.fait")) return;
    var t = tours[i], bon = b.dataset.cc === t.p.cc; if (bon) score++;
    var rep = box.querySelector(".vj-rep"); rep.classList.add("fait");
    [].forEach.call(rep.children, function (o) { o.disabled = true; if (o.dataset.cc === t.p.cc) o.classList.add("bon"); else if (o === b) o.classList.add("faux"); });
    box.querySelector(".vj-res").innerHTML = '<p class="' + (bon ? "bon" : "faux") + '">' + esc(fmt(bon ? T.ok : T.ko, { l: t.l.n, p: t.p.nom })) + '</p><p><button type="button" class="btn" data-a="suiv">' +
      esc(i + 1 < tours.length ? T.suiv : T.fin) + '</button> <a class="btn ghost" href="' + esc(D.base + t.p.slug + "/#" + t.l.k) + '">' + esc(fmt(T.voir, { p: t.p.nom })) + "</a></p>";
    box.querySelector(".vj-res .btn").focus();
  });
  var fin = function () {
    var best = 0; try { best = +localStorage.getItem("escale.jeu-pays") || 0; } catch (e) {}
    if (score > best) { best = score; try { localStorage.setItem("escale.jeu-pays", String(best)); } catch (e) {} }
    var m = T.m[score <= 3 ? 0 : score <= 6 ? 1 : score <= 9 ? 2 : 3];
    box.innerHTML = '<div class="vj-fin"><p class="vj-score">' + esc(fmt(T.score, { s: score, t: tours.length })) + "</p><p>" + esc(m) + '</p><p class="small">' + esc(fmt(T.best, { s: best, t: tours.length })) +
      '</p><p><button type="button" class="btn" data-a="part">' + esc(T.part) + '</button> <button type="button" class="btn ghost" data-a="rej">' + esc(T.rej) + "</button></p></div>";
  };
})();
