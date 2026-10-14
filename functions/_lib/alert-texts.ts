// Textes des e-mails et pages d'alerte (5 langues)
export const TXT: Record<string, Record<string, string>> = {
  fr: {
    confirmSubject: "Confirmez votre alerte prix {a} → {b}",
    confirmBody: "<p>Bonjour,</p><p>Vous avez demandé à être prévenu quand un aller-retour <b>{a} → {b}</b> passe sous <b>{max}</b>.</p><p><a href=\"{link}\">Confirmer mon alerte</a></p><p>Si vous n’êtes pas à l’origine de cette demande, ignorez ce message : aucune alerte ne sera créée.</p>",
    dropSubject: "Prix en baisse : {a} → {b} dès {price}",
    dropBody: "<p>Bonne nouvelle : un aller-retour <b>{a} → {b}</b> a été repéré à <b>{price}</b>, sous votre seuil de {max}.</p><p><a href=\"{search}\">Voir les vols</a></p><p>Les prix changent vite : vérifiez le tarif final sur le site de réservation.</p>",
    footer: "<p style=\"color:#666;font-size:12px\">Escale · <a href=\"{unsub}\">Me désinscrire de cette alerte</a></p>",
    confirmed: "Votre alerte prix est confirmée. Nous vous écrirons quand le prix passera sous votre seuil.",
    unsubscribed: "Votre alerte a été supprimée, avec votre adresse e-mail.",
    invalid: "Ce lien n’est plus valable.", back: "Retour à Escale",
  },
  en: {
    confirmSubject: "Confirm your price alert {a} → {b}",
    confirmBody: "<p>Hello,</p><p>You asked to be told when a round trip <b>{a} → {b}</b> drops below <b>{max}</b>.</p><p><a href=\"{link}\">Confirm my alert</a></p><p>If you did not make this request, ignore this email: no alert will be created.</p>",
    dropSubject: "Price drop: {a} → {b} from {price}",
    dropBody: "<p>Good news: a round trip <b>{a} → {b}</b> was found at <b>{price}</b>, below your {max} threshold.</p><p><a href=\"{search}\">See flights</a></p><p>Prices change fast: check the final fare on the booking site.</p>",
    footer: "<p style=\"color:#666;font-size:12px\">Escale · <a href=\"{unsub}\">Unsubscribe from this alert</a></p>",
    confirmed: "Your price alert is confirmed. We will email you when the price drops below your threshold.",
    unsubscribed: "Your alert has been deleted, along with your email address.",
    invalid: "This link is no longer valid.", back: "Back to Escale",
  },
  es: {
    confirmSubject: "Confirma tu alerta de precio {a} → {b}",
    confirmBody: "<p>Hola:</p><p>Pediste que te avisáramos cuando un vuelo de ida y vuelta <b>{a} → {b}</b> baje de <b>{max}</b>.</p><p><a href=\"{link}\">Confirmar mi alerta</a></p><p>Si no lo pediste, ignora este mensaje: no se creará ninguna alerta.</p>",
    dropSubject: "Bajada de precio: {a} → {b} desde {price}",
    dropBody: "<p>Buenas noticias: se encontró un ida y vuelta <b>{a} → {b}</b> a <b>{price}</b>, por debajo de tu límite de {max}.</p><p><a href=\"{search}\">Ver vuelos</a></p><p>Los precios cambian rápido: revisa la tarifa final en el sitio de reserva.</p>",
    footer: "<p style=\"color:#666;font-size:12px\">Escale · <a href=\"{unsub}\">Darme de baja de esta alerta</a></p>",
    confirmed: "Tu alerta de precio está confirmada. Te escribiremos cuando el precio baje de tu límite.",
    unsubscribed: "Tu alerta se ha eliminado, junto con tu correo.",
    invalid: "Este enlace ya no es válido.", back: "Volver a Escale",
  },
  pt: {
    confirmSubject: "Confirme o seu alerta de preço {a} → {b}",
    confirmBody: "<p>Olá,</p><p>Pediu para ser avisado quando uma ida e volta <b>{a} → {b}</b> descer abaixo de <b>{max}</b>.</p><p><a href=\"{link}\">Confirmar o meu alerta</a></p><p>Se não fez este pedido, ignore esta mensagem: nenhum alerta será criado.</p>",
    dropSubject: "Preço em baixa: {a} → {b} desde {price}",
    dropBody: "<p>Boas notícias: foi encontrada uma ida e volta <b>{a} → {b}</b> a <b>{price}</b>, abaixo do seu limite de {max}.</p><p><a href=\"{search}\">Ver voos</a></p><p>Os preços mudam depressa: confirme a tarifa final no site de reserva.</p>",
    footer: "<p style=\"color:#666;font-size:12px\">Escale · <a href=\"{unsub}\">Cancelar este alerta</a></p>",
    confirmed: "O seu alerta de preço está confirmado. Escrevemos-lhe quando o preço descer abaixo do seu limite.",
    unsubscribed: "O seu alerta foi apagado, juntamente com o seu e-mail.",
    invalid: "Este link já não é válido.", back: "Voltar à Escale",
  },
  ar: {
    confirmSubject: "أكّد تنبيه السعر {a} ← {b}",
    confirmBody: "<p dir=\"rtl\">مرحبًا،</p><p dir=\"rtl\">طلبت أن نخبرك عندما ينخفض سعر رحلة ذهاب وعودة <b>{a} ← {b}</b> إلى أقل من <b>{max}</b>.</p><p dir=\"rtl\"><a href=\"{link}\">تأكيد التنبيه</a></p><p dir=\"rtl\">إذا لم تطلب ذلك، تجاهل هذه الرسالة: لن يُنشأ أي تنبيه.</p>",
    dropSubject: "انخفاض السعر: {a} ← {b} من {price}",
    dropBody: "<p dir=\"rtl\">خبر سار: وُجدت رحلة ذهاب وعودة <b>{a} ← {b}</b> بسعر <b>{price}</b>، أقل من حدّك {max}.</p><p dir=\"rtl\"><a href=\"{search}\">اعرض الرحلات</a></p><p dir=\"rtl\">الأسعار تتغير بسرعة: تحقّق من السعر النهائي على موقع الحجز.</p>",
    footer: "<p style=\"color:#666;font-size:12px\" dir=\"rtl\">Escale · <a href=\"{unsub}\">إلغاء هذا التنبيه</a></p>",
    confirmed: "تم تأكيد تنبيه السعر. سنراسلك عندما ينخفض السعر إلى أقل من حدّك.",
    unsubscribed: "تم حذف التنبيه مع بريدك الإلكتروني.",
    invalid: "هذا الرابط لم يعد صالحًا.", back: "العودة إلى Escale",
  },
}

export const fill = (s: string, v: Record<string, string>) => s.replace(/\{(\w+)\}/g, (m, k) => (k in v ? v[k] : m))

export function page(lang: string, message: string) {
  const t = TXT[lang] || TXT.fr
  return new Response(`<!doctype html><html lang="${lang}" dir="${lang === "ar" ? "rtl" : "ltr"}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Escale</title>
<style>body{margin:0;font:16px/1.6 system-ui,sans-serif;background:#f3f5f8;color:#141a24;display:grid;place-items:center;min-height:100vh;padding:16px}main{max-width:480px;background:#fff;border:1px solid #d9dee6;border-radius:14px;padding:28px}a{color:#0b5cd6;font-weight:700}</style>
</head><body><main><p><b>Escale</b></p><p>${message}</p><p><a href="/${lang === "fr" ? "" : "?lang=" + lang}">${t.back}</a></p></main></body></html>`,
    { headers: { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store" } })
}
