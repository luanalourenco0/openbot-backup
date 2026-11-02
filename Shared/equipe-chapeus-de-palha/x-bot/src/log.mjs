import { appendFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

// Uma linha JSON por evento. Só id e dados de controle: nunca o texto do
// tweet nem qualquer credencial.
export function registrar(raiz, evento, dados = {}) {
  mkdirSync(join(raiz, 'logs'), { recursive: true });
  const agora = new Date();
  const linha = {
    ts: agora.toISOString(),
    local: agora.toLocaleString('pt-BR', { timeZone: 'America/Sao_Paulo' }),
    evento,
    ...dados,
  };
  appendFileSync(join(raiz, 'logs', 'x-bot.jsonl'), JSON.stringify(linha) + '\n');
}
