import type { Config, Context } from "@netlify/functions"

// Position approximative du visiteur (déduite par Netlify de l'adresse IP, rien n'est enregistré).
// Sert à préremplir l'aéroport de départ le plus proche et la devise.
export default async (_req: Request, context: Context) => {
  const g = context.geo || {}
  return Response.json(
    {
      country: g.country?.code ?? null,
      city: g.city ?? null,
      lat: typeof g.latitude === "number" ? g.latitude : null,
      lon: typeof g.longitude === "number" ? g.longitude : null,
    },
    { headers: { "Cache-Control": "private, no-store" } },
  )
}

export const config: Config = { path: "/api/geo" }
