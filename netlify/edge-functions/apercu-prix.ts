import type { Config, Context } from "@netlify/edge-functions";

// Aperçus de liens (WhatsApp, Facebook, Telegram…) : ajoute le prix réel le plus bas au titre des pages trajets,
// par exemple « Vol pas cher Paris Dakar : comparer les prix · dès 389 € ». Ne s'exécute que pour ces robots.
const LABEL: Record<string, string> = { fr: "dès", en: "from", es: "desde", pt: "desde", ar: "من" };

async function cheapest(token: string, from: string, to: string): Promise<number | null> {
  const now = new Date();
  const months = [0, 1, 2].map((i) => new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth() + i, 1)).toISOString().slice(0, 7));
  const today = now.toISOString().slice(0, 10);
  const results = await Promise.all(months.map(async (m) => {
    const api = new URL("https://api.travelpayouts.com/aviasales/v3/prices_for_dates");
    api.search = new URLSearchParams({ origin: from, destination: to, departure_at: m, one_way: "false", sorting: "price", currency: "eur", limit: "5", token }).toString();
    try {
      const res = await fetch(api, { signal: AbortSignal.timeout(2500) });
      if (!res.ok) return null;
      const body = await res.json();
      const ok = (body?.data ?? []).filter((t: any) => t.price && String(t.departure_at || "").slice(0, 10) >= today);
      return ok.length ? Math.min(...ok.map((t: any) => t.price)) : null;
    } catch { return null; }
  }));
  const prices = results.filter((p): p is number => typeof p === "number");
  return prices.length ? Math.min(...prices) : null;
}

export default async (_request: Request, context: Context) => {
  const response = await context.next();
  const token = Netlify.env.get("TRAVELPAYOUTS_TOKEN");
  if (!token || !(response.headers.get("content-type") || "").includes("text/html")) return response;
  const html = await response.text();
  const route = html.match(/id="route-prices" data-from="([A-Z]{3})" data-to="([A-Z]{3})"/);
  if (!route) return new Response(html, response);
  const price = await cheapest(token, route[1], route[2]);
  if (!price) return new Response(html, response);
  const lang = (html.match(/<html lang="([a-z]{2})"/) || [])[1] || "fr";
  const money = new Intl.NumberFormat(lang === "ar" ? "ar-u-nu-latn" : lang, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(price);
  const suffix = ` · ${LABEL[lang] || LABEL.fr} ${money}`;
  const out = html
    .replace(/(<meta property="og:title" content=")([^"]*)(")/, (_m, a, t, b) => a + t + suffix + b)
    .replace(/(<meta property="og:description" content=")([^"]*)(")/, (_m, a, t, b) => a + (LABEL[lang] || LABEL.fr) + " " + money + " — " + t + b);
  const headers = new Headers(response.headers);
  headers.delete("content-length");
  return new Response(out, { status: response.status, headers });
};

export const config: Config = {
  path: ["/vol-*", "/en/flights-*", "/es/vuelos-*", "/pt/voos-*", "/ar/flights-*"],
  header: { "user-agent": "(facebookexternalhit|Facebot|WhatsApp|TelegramBot|Twitterbot|LinkedInBot|Slackbot|Discordbot|Pinterest|SkypeUriPreview|redditbot)" },
  onError: "bypass",
};
