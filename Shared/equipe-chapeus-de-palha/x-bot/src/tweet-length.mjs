// Contagem de caracteres no estilo do X (aproximação do twitter-text):
// link vale 23, emoji vale 2, letras latinas e acentos valem 1, CJK vale 2.
// Confira no X antes de postar algo no limite.

export const URL_PESO = 23;

const URL_RE = /https?:\/\/\S+/gu;
const EMOJI_RE = /\p{Extended_Pictographic}(?:️|⃣|[\u{1F3FB}-\u{1F3FF}]|‍\p{Extended_Pictographic})*/gu;

function pesoDoCaractere(cp) {
  const leve =
    (cp >= 0 && cp <= 4351) ||
    (cp >= 8192 && cp <= 8205) ||
    (cp >= 8208 && cp <= 8223) ||
    (cp >= 8242 && cp <= 8247);
  return leve ? 1 : 2;
}

export function pesoDoTweet(texto) {
  let total = 0;
  let resto = texto.normalize('NFC').replace(URL_RE, () => {
    total += URL_PESO;
    return '';
  });
  // símbolos antigos como © e ™ são Extended_Pictographic, mas contam 1
  resto = resto.replace(EMOJI_RE, (m) => {
    if (m.codePointAt(0) < 0x2000) return m;
    total += 2;
    return '';
  });
  for (const ch of resto) total += pesoDoCaractere(ch.codePointAt(0));
  return total;
}
