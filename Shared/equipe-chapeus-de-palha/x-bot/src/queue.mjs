import {
  existsSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  unlinkSync,
  writeFileSync,
} from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

export const PASTAS = ['rascunhos', 'aprovados', 'publicados', 'erros'];
export const SEPARADOR = '\n===\n';
const ID_RE = /^\d{4}-\d{2}-\d{2}-\d{3}$/;

export function raiz() {
  return process.env.X_BOT_RAIZ ?? join(dirname(fileURLToPath(import.meta.url)), '..');
}

export function lerConfig(base) {
  const padrao = { conta: '@luanzeraAI', limite: 280, fuso: 'America/Sao_Paulo' };
  const arquivo = join(base, 'config.json');
  if (!existsSync(arquivo)) return padrao;
  const cfg = { ...padrao, ...JSON.parse(readFileSync(arquivo, 'utf8')) };
  if (!Number.isInteger(cfg.limite) || cfg.limite < 20) {
    throw new Error('config.json: "limite" deve ser um inteiro maior ou igual a 20');
  }
  return cfg;
}

export function formatar(meta, partes) {
  const cabecalho = Object.entries(meta)
    .map(([k, v]) => `${k}: ${v}`)
    .join('\n');
  return `---\n${cabecalho}\n---\n${partes.join(SEPARADOR)}\n`;
}

export function interpretar(conteudo) {
  const m = conteudo.replace(/\r\n/g, '\n').match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!m) throw new Error('rascunho sem cabeçalho (--- ... ---)');
  const meta = {};
  for (const linha of m[1].split('\n')) {
    const i = linha.indexOf(':');
    if (i > 0) meta[linha.slice(0, i).trim()] = linha.slice(i + 1).trim();
  }
  const partes = m[2]
    .split(/\n===\n/)
    .map((p) => p.trim())
    .filter(Boolean);
  return { meta, partes };
}

export function idValido(id) {
  return typeof id === 'string' && ID_RE.test(id);
}

function pasta(base, nome) {
  return join(base, 'fila', nome);
}

export function listarIds(base, nome) {
  const dir = pasta(base, nome);
  if (!existsSync(dir)) return [];
  return readdirSync(dir)
    .filter((f) => f.endsWith('.md'))
    .map((f) => f.slice(0, -3))
    .sort();
}

export function proximoId(base, fuso) {
  const data = new Date().toLocaleDateString('sv-SE', { timeZone: fuso });
  let maior = 0;
  for (const nome of PASTAS) {
    for (const id of listarIds(base, nome)) {
      if (id.startsWith(`${data}-`)) maior = Math.max(maior, Number(id.slice(-3)));
    }
  }
  return `${data}-${String(maior + 1).padStart(3, '0')}`;
}

// Procura o rascunho nas quatro pastas. O id é validado para não sair da fila.
export function achar(base, id) {
  if (!idValido(id)) throw new Error(`id inválido: ${id}`);
  for (const nome of PASTAS) {
    const caminho = join(pasta(base, nome), `${id}.md`);
    if (existsSync(caminho)) return { pasta: nome, caminho };
  }
  return null;
}

export function ler(caminho) {
  return interpretar(readFileSync(caminho, 'utf8'));
}

export function gravar(base, nome, id, meta, partes) {
  const dir = pasta(base, nome);
  mkdirSync(dir, { recursive: true });
  const caminho = join(dir, `${id}.md`);
  writeFileSync(caminho, formatar(meta, partes), 'utf8');
  return caminho;
}

// Grava no destino antes de apagar a origem: uma falha no meio nunca perde o texto.
export function mover(base, id, de, para, meta, partes) {
  gravar(base, para, id, meta, partes);
  unlinkSync(join(pasta(base, de), `${id}.md`));
}
