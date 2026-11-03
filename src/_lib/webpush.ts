// Notifications sur le téléphone (Web Push, norme RFC 8030 + VAPID RFC 8292), sans service extérieur.
// La paire de clés VAPID est créée au premier besoin et gardée dans l'espace KV ESCALE (« push:vapid ») : elle n'est jamais
// dans le code ni dans le dépôt. Les notifications partent SANS contenu chiffré : le téléphone, réveillé, demande lui-même
// le message à /api/push?action=msg (site/sw.js). Pas de chiffrement de charge à gérer, et rien de personnel ne transite.
const b64u = (buf: ArrayBuffer | Uint8Array) => {
  const b = buf instanceof Uint8Array ? buf : new Uint8Array(buf)
  let s = ""; for (const x of b) s += String.fromCharCode(x)
  return btoa(s).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "")
}
const enc = (s: string) => new TextEncoder().encode(s)

type Vapid = { publicKey: string; privateJwk: JsonWebKey }

export async function vapidKeys(kv: any): Promise<Vapid> {
  const saved = await kv.get("push:vapid", "json")
  if (saved && saved.publicKey && saved.privateJwk) return saved
  const pair: any = await crypto.subtle.generateKey({ name: "ECDSA", namedCurve: "P-256" }, true, ["sign", "verify"])
  const raw = await crypto.subtle.exportKey("raw", pair.publicKey) as ArrayBuffer
  const out = { publicKey: b64u(raw), privateJwk: await crypto.subtle.exportKey("jwk", pair.privateKey) as JsonWebKey }
  await kv.put("push:vapid", JSON.stringify(out))
  return out
}

// Envoie une notification « vide » à un abonnement. Renvoie le code HTTP du service de push (201 = envoyée ; 404/410 = abonnement expiré).
export async function sendPush(kv: any, endpoint: string, site: string): Promise<number> {
  const v = await vapidKeys(kv)
  const aud = new URL(endpoint).origin
  const head = b64u(enc(JSON.stringify({ typ: "JWT", alg: "ES256" })))
  const body = b64u(enc(JSON.stringify({ aud, exp: Math.floor(Date.now() / 1000) + 12 * 3600, sub: site })))
  const key = await crypto.subtle.importKey("jwk", v.privateJwk, { name: "ECDSA", namedCurve: "P-256" }, false, ["sign"])
  const sig = await crypto.subtle.sign({ name: "ECDSA", hash: "SHA-256" }, key, enc(`${head}.${body}`))
  const r = await fetch(endpoint, { method: "POST", headers: { TTL: "86400", Urgency: "normal", Authorization: `vapid t=${head}.${body}.${b64u(sig)}, k=${v.publicKey}`, "Content-Length": "0" } })
  return r.status
}

export const endpointId = async (endpoint: string) => b64u(await crypto.subtle.digest("SHA-256", enc(endpoint))).slice(0, 32)
