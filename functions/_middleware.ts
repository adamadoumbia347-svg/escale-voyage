import { Ctx } from "./_lib/common"
import { cheapestRoundTrip } from "./_lib/mail"
// Aperçus de liens (WhatsApp, Facebook, Telegram…) : ajoute le prix le plus bas au titre des pages trajets,
// par exemple « Vol pas cher Paris Dakar : comparer les prix · dès 389 € ». Seulement pour ces robots ;
// les visiteurs reçoivent la page telle quelle. Les chemins concernés sont listés dans site/_routes.json.
const BOTS = /facebookexternalhit|Facebot|WhatsApp|TelegramBot|Twitterbot|LinkedInBot|Slackbot|Discordbot|Pinterest|SkypeUriPreview|redditbot/i
const PAGES = /^\/(vol-|en\/flights-|es\/vuelos-|pt\/voos-|ar\/flights-)/
const LABEL: Record<string, string> = { fr: "dès", en: "from", es: "desde", pt: "desde", ar: "من" }

export const onRequest = async (ctx: Ctx) => {
  const { request, env } = ctx
  const path = new URL(request.url).pathname
  if (!PAGES.test(path) || !BOTS.test(request.headers.get("user-agent") || "") || !env.TRAVELPAYOUTS_TOKEN) return ctx.next()
  const response = await ctx.next()
  try {
    if (!(response.headers.get("content-type") || "").includes("text/html")) return response
    const html = await response.text()
    const route = html.match(/id="route-prices" data-from="([A-Z]{3})" data-to="([A-Z]{3})"/)
    const price = route ? await cheapestRoundTrip(env.TRAVELPAYOUTS_TOKEN, route[1], route[2], "EUR", 2500) : null
    const headers = new Headers(response.headers)
    headers.delete("content-length")
    if (!price) return new Response(html, { status: response.status, headers })
    const lang = (html.match(/<html lang="([a-z]{2})"/) || [])[1] || "fr"
    const money = new Intl.NumberFormat(lang === "ar" ? "ar-u-nu-latn" : lang, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(price)
    const label = LABEL[lang] || LABEL.fr
    const out = html
      .replace(/(<meta property="og:title" content=")([^"]*)(")/, (_m, a, t, b) => a + t + ` · ${label} ${money}` + b)
      .replace(/(<meta property="og:description" content=")([^"]*)(")/, (_m, a, t, b) => a + label + " " + money + " — " + t + b)
    return new Response(out, { status: response.status, headers })
  } catch {
    return response
  }
}
