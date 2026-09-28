const LANGUAGE_CODES = new Set(['tr', 'en', 'de', 'ar', 'ru']);

export function normalizeLanguageCode(raw) {
  const value = String(raw || '').trim().toLowerCase().replaceAll('_', '-');
  const aliases = {
    turkish: 'tr', english: 'en', german: 'de', arabic: 'ar', russian: 'ru',
    'türkçe': 'tr', deutsch: 'de', 'русский': 'ru', 'العربية': 'ar',
  };
  const code = aliases[value] || value.split('-')[0];
  return LANGUAGE_CODES.has(code) ? code : '';
}

// V72 öncesi paylaşımlarda contentLanguage alanı yoktu. Bu küçük ve
// deterministik algılama, bu kayıtları otomatik Türkçe sayma hatasını giderir.
export function detectTranslationSource(text, hint) {
  const explicit = normalizeLanguageCode(hint);
  if (explicit) return explicit;
  const value = String(text || '').toLowerCase();
  if (/[؀-ۿ]/u.test(value)) return 'ar';
  if (/[Ѐ-ӿ]/u.test(value)) return 'ru';
  if (/[ğışç]/u.test(value) || /\b(ve|bir|bu|için|değil|çok|ile|gibi|ben|sen)\b/u.test(value)) return 'tr';
  if (/[äöüß]/u.test(value) || /\b(und|der|die|das|nicht|mit|für|ich|du)\b/u.test(value)) return 'de';
  return 'en';
}

export function captionMediaCandidates(body) {
  const raw = [body?.mediaUrl, ...(Array.isArray(body?.mediaUrls) ? body.mediaUrls : [])];
  return [...new Set(raw.map((x) => String(x || '').trim()).filter(Boolean))].slice(0, 8);
}
