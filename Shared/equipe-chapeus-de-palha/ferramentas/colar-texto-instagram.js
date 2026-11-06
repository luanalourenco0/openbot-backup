// Cola o texto aprovado na caixa do direct e confere. NUNCA envia. Copie tudo sem alterar.
const PARTES = [
"Ol\u00e1! Somos a Luz & Encanto e trabalhamos com velas e decora\u00e7\u00e3o artesanal de cimento. Entre elas est\u00e3o velas orat\u00f3rias. \ud83d\udd6f\ufe0f",
"Gostar\u00edamos de saber se a igreja tem lojinha, livraria ou espa\u00e7o para lembran\u00e7as e como costuma tratar parcerias desse tipo. Seria poss\u00edvel conversarmos sobre deixar velas orat\u00f3rias \u00e0 mostra nesse espa\u00e7o?",
"Agradecemos pela aten\u00e7\u00e3o!",
"K\u00e1tia Ribeiro, respons\u00e1vel pelo Luz & Encanto"
];
const ESPERADO = "97aca6f3";
const NL = "String.fromCharCode(10)";
const TEXTO = PARTES.join(String.fromCharCode(10, 10));
const CAIXA = "[...document.querySelectorAll('div[role=textbox][contenteditable=true]')].filter(e => e.offsetParent).pop()";
const espera = (ms) => evaluate("new Promise(r => setTimeout(() => r(true), " + ms + "))");
const ler = () => evaluate("(() => { const el = " + CAIXA + "; if (!el) return { caixa: false, url: location.href }; const todas = (el.innerText || '').split(" + NL + ").map(s => s.trim()); const cheias = todas.filter(Boolean); const n = cheias.join(" + NL + "); let h = 0x811c9dc5; for (let i = 0; i < n.length; i++) { h ^= n.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; } let sep = cheias.length > 0, visto = 0, branco = false; for (const l of todas) { if (l) { if (visto && !branco) sep = false; visto++; branco = false; } else if (visto) branco = true; } return { caixa: true, url: location.href, fnv: h.toString(16).padStart(8, '0'), paragrafos: cheias.length, separados: sep }; })()");
const certo = (r) => r && r.caixa && r.fnv === ESPERADO && r.paragrafos === PARTES.length && r.separados;
const limpar = () => evaluate("(() => { const el = " + CAIXA + "; if (!el) return false; el.focus(); document.execCommand('selectAll'); document.execCommand('delete'); return true; })()");
const colar = () => evaluate("(() => { const el = " + CAIXA + "; if (!el) return false; el.focus(); const d = new DataTransfer(); d.setData('text/plain', " + JSON.stringify(TEXTO) + "); el.dispatchEvent(new ClipboardEvent('paste', { clipboardData: d, bubbles: true, cancelable: true })); return true; })()");
const inserir = () => evaluate("(() => { const el = " + CAIXA + "; if (!el) return false; el.focus(); return document.execCommand('insertText', false, " + JSON.stringify(TEXTO) + "); })()");
let r = await ler();
let tentativas = 0;
while (!certo(r) && tentativas < 3) {
  tentativas++;
  if (r && r.caixa && r.paragrafos > 0) { await limpar(); await espera(500); }
  if (tentativas < 3) await colar(); else await inserir();
  await espera(1500);
  r = await ler();
}
await espera(5000);
r = await ler();
return { identico: !!certo(r), tentativas, leitura: r };
