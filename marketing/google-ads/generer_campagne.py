import csv, os, sys
OUT = "/home/user/escale-voyage/marketing/google-ads"
SITE = "https://escale.live"
CAMP = "Escale - Vols diaspora Afrique (FR)"
# (slug, nom affiché, variantes de mot-clé)
ROUTES = [
  ("bamako","Bamako",["bamako"]), ("dakar","Dakar",["dakar"]), ("abidjan","Abidjan",["abidjan"]),
  ("conakry","Conakry",["conakry"]), ("douala","Douala",["douala"]), ("yaounde","Yaoundé",["yaounde","yaoundé"]),
  ("kinshasa","Kinshasa",["kinshasa"]), ("cotonou","Cotonou",["cotonou"]), ("lome","Lomé",["lome","lomé"]),
  ("ouagadougou","Ouagadougou",["ouagadougou","ouaga"]), ("niamey","Niamey",["niamey"]), ("libreville","Libreville",["libreville"]),
]
def fit(cands, n):
    for c in cands:
        if len(c) <= n: return c
    raise SystemExit(f"trop long: {cands}")
GENERIC_H = ["Comparez les prix en 1 clic", "Calendrier des prix du mois", "Gratuit et sans inscription",
  "Tous les grands comparateurs", "Prix réels mis à jour", "Trouvez le jour le moins cher", "Vols directs et avec escale",
  "Escale, comparateur de vols", "Toutes les compagnies", "Aller-retour ou aller simple", "Réservez au bon moment"]
def headlines(c):
    hs = [fit([f"Vol Paris {c} pas cher", f"Vol Paris–{c}", f"Vols vers {c}"], 30),
          fit([f"Billet d'avion Paris {c}", f"Billet Paris {c}", f"Billet pour {c}"], 30),
          fit([f"Paris – {c} au meilleur prix", f"Paris–{c} moins cher", f"{c} au meilleur prix"], 30),
          fit([f"Prix des vols pour {c}", f"Prix vols {c}", f"Vols {c}"], 30)] + GENERIC_H
    hs = hs[:15]
    assert len(hs) == 15 and len(set(hs)) == 15 and all(len(h) <= 30 for h in hs), hs
    return hs
def descriptions(c):
    ds = [fit([f"Comparez les vols Paris–{c} sur les grands comparateurs en une seule recherche.",
               f"Comparez les vols Paris–{c} sur les grands comparateurs en une recherche."], 90),
          "Calendrier des prix, vols directs, bagages : trouvez le billet le moins cher. Gratuit.",
          "Prix repérés récemment et conseils pour payer moins cher. Sans inscription.",
          "Choisissez vos dates et voyez tout de suite les jours les moins chers du mois."]
    assert all(len(d) <= 90 for d in ds), [(len(d), d) for d in ds]
    return ds
def keywords(vs):
    out = []
    for v in vs:
        for k in [f"vol paris {v}", f"billet avion paris {v}", f"vol paris {v} pas cher", f"billet paris {v}",
                  f"prix billet paris {v}", f"billet d'avion paris {v}", f"paris {v} avion"]:
            out.append(k)
    return list(dict.fromkeys(out))
NEG = ["emploi", "recrutement", "stage", "salaire", "train", "bus", "bateau", "météo", "meteo", "heure", "décalage horaire",
  "distance", "carte", "plan", "statut", "suivi", "arrivée", "arrivées", "départs", "retard", "annulé", "bagage perdu",
  "réclamation", "remboursement", "service client", "numéro", "téléphone", "contact", "enregistrement", "check in",
  "visa", "ambassade", "consulat", "passeport", "covid", "gratuit", "hôtesse", "pilote", "flight simulator", "jeu",
  "colis", "fret", "cargo", "envoi", "transfert d'argent", "wikipedia"]

rows = []
H = ["Campaign","Campaign Type","Networks","Budget","Budget type","Bid Strategy Type","Max CPC Bid Limit","Languages","Location",
     "Campaign Status","Ad Group","Max CPC","Ad Group Status","Keyword","Criterion Type","Status","Ad type","Final URL","Path 1","Path 2"] \
    + [f"Headline {i}" for i in range(1,16)] + [f"Description {i}" for i in range(1,5)]
def row(**kw):
    r = {h: "" for h in H}; r.update(kw); rows.append(r)
row(**{"Campaign": CAMP, "Campaign Type": "Search", "Networks": "Google search", "Budget": "5.00", "Budget type": "Daily",
       "Bid Strategy Type": "Maximize clicks", "Max CPC Bid Limit": "0.50", "Languages": "fr", "Location": "France", "Campaign Status": "Paused"})
for slug, city, vs in ROUTES:
    ag = f"Paris - {city}"
    row(**{"Campaign": CAMP, "Ad Group": ag, "Max CPC": "0.50", "Ad Group Status": "Enabled"})
    for k in keywords(vs):
        for ct in ("Phrase", "Exact"):
            row(**{"Campaign": CAMP, "Ad Group": ag, "Keyword": k, "Criterion Type": ct, "Status": "Enabled"})
    ad = {"Campaign": CAMP, "Ad Group": ag, "Ad type": "Responsive search ad", "Status": "Enabled",
          "Final URL": f"{SITE}/vol-paris-{slug}/", "Path 1": "vols", "Path 2": fit([f"paris-{slug}", slug], 15)}
    for i, h in enumerate(headlines(city), 1): ad[f"Headline {i}"] = h
    for i, d in enumerate(descriptions(city), 1): ad[f"Description {i}"] = d
    row(**ad)
for n in NEG:
    row(**{"Campaign": CAMP, "Keyword": n, "Criterion Type": "Campaign Negative Broad", "Status": "Enabled"})
with open(os.path.join(OUT, "campagne-escale.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=H); w.writeheader(); w.writerows(rows)
kw = sum(1 for r in rows if r["Criterion Type"] in ("Phrase","Exact"))
print(len(ROUTES), "groupes,", kw, "mots-clés,", len(NEG), "exclusions,", len(rows), "lignes")
print(headlines("Ouagadougou")[:4], descriptions("Ouagadougou")[0], len(descriptions("Ouagadougou")[0]))
