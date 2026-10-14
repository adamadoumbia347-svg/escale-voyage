import { Ctx, json } from "../_lib/common"
// Position approximative du visiteur (déduite par Cloudflare de l'adresse IP, rien n'est enregistré).
// Sert à préremplir l'aéroport de départ le plus proche et la devise.
export const onRequestGet = ({ request }: Ctx) => {
  const cf: any = (request as any).cf || {}
  const num = (v: any) => (v != null && v !== "" && !isNaN(Number(v)) ? Number(v) : null)
  return json({ country: cf.country ?? null, city: cf.city ?? null, lat: num(cf.latitude), lon: num(cf.longitude) },
    { headers: { "Cache-Control": "private, no-store" } })
}
