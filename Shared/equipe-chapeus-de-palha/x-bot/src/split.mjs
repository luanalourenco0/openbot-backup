import { pesoDoTweet } from './tweet-length.mjs';

// " (10/10)": espaço reservado para a numeração da thread
const RESERVA_NUMERACAO = 8;

function posicaoDoCorte(texto, orcamento) {
  const palavras = texto.match(/\S+\s*/gu) ?? [];
  let acumulado = '';
  let fim = 0;
  let fimDeFrase = 0;
  for (const palavra of palavras) {
    const candidato = acumulado + palavra;
    if (pesoDoTweet(candidato.trimEnd()) > orcamento) break;
    acumulado = candidato;
    fim = acumulado.length;
    if (/[.!?…]["')]?\s*$/u.test(palavra)) fimDeFrase = fim;
  }
  if (fim === 0) return corteForcado(texto, orcamento);
  // prefere terminar numa frase se isso aproveitar pelo menos metade do espaço
  if (fimDeFrase > 0 && pesoDoTweet(texto.slice(0, fimDeFrase).trimEnd()) >= orcamento / 2) {
    return fimDeFrase;
  }
  return fim;
}

// palavra maior que o tweet inteiro: corta no caractere
function corteForcado(texto, orcamento) {
  let saida = '';
  for (const ch of texto) {
    if (pesoDoTweet(saida + ch) > orcamento) break;
    saida += ch;
  }
  return Math.max(saida.length, 1);
}

// Divide um texto longo em tweets numerados "(i/n)", sem cortar palavra nem link.
export function dividirEmThread(texto, limite = 280) {
  const limpo = texto.trim();
  if (pesoDoTweet(limpo) <= limite) return [limpo];
  const orcamento = limite - RESERVA_NUMERACAO;
  const pedacos = [];
  let resto = limpo;
  while (pesoDoTweet(resto) > orcamento) {
    const corte = posicaoDoCorte(resto, orcamento);
    pedacos.push(resto.slice(0, corte).trim());
    resto = resto.slice(corte).trim();
  }
  if (resto) pedacos.push(resto);
  const n = pedacos.length;
  return pedacos.map((p, i) => `${p} (${i + 1}/${n})`);
}

// Rascunho de uma parte só: divide sozinho se passar do limite.
// Rascunho que já é thread: não mexe nos tweets, só avisa os que passaram.
export function planejar(partes, limite = 280) {
  if (partes.length === 0) return { tweets: [], problemas: ['rascunho vazio'] };
  if (partes.length === 1) return { tweets: dividirEmThread(partes[0], limite), problemas: [] };
  const problemas = [];
  partes.forEach((p, i) => {
    const peso = pesoDoTweet(p);
    if (peso > limite) problemas.push(`tweet ${i + 1} da thread tem ${peso}/${limite}`);
  });
  return { tweets: partes, problemas };
}
