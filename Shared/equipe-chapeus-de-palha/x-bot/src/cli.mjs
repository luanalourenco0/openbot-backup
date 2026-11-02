#!/usr/bin/env node
import { readFileSync } from 'node:fs';
import { pesoDoTweet } from './tweet-length.mjs';
import { planejar } from './split.mjs';
import { registrar } from './log.mjs';
import {
  PASTAS,
  SEPARADOR,
  achar,
  gravar,
  idValido,
  lerConfig,
  ler,
  listarIds,
  mover,
  proximoId,
  raiz,
} from './queue.mjs';

const AJUDA = `uso: node src/cli.mjs <comando>

  novo --texto "..."          cria um rascunho (ou --arquivo caminho.txt, ou texto por stdin)
                              uma linha só com === separa os tweets de uma thread
  listar [pasta]              rascunhos, aprovados, publicados ou erros (sem argumento: todas)
  validar [id]                confere o tamanho (sem id: todos os rascunhos)
  mostrar <id>                texto pronto para colar no X, com contador
  aprovar <id>                move para aprovados; divide em thread se passar do limite
  publicado <id> [--url ...]  marca como publicado, depois que você postou à mão
  erro <id> <motivo>          move para erros

Este bot não fala com o X: nada é publicado por ele. Veja README.md.`;

function falhar(msg) {
  console.error(`erro: ${msg}`);
  process.exit(1);
}

function valorDe(args, flag) {
  const i = args.indexOf(flag);
  if (i === -1) return undefined;
  const v = args[i + 1];
  if (v === undefined) falhar(`${flag} precisa de um valor`);
  return v;
}

function contagem(tweets, limite) {
  return tweets.map((t, i) => {
    const peso = pesoDoTweet(t);
    return `  tweet ${i + 1}/${tweets.length}: ${peso}/${limite}${peso > limite ? '  PASSOU' : ''}`;
  });
}

function carregar(base, id) {
  let achado;
  try {
    achado = achar(base, id);
  } catch (e) {
    falhar(e.message);
  }
  if (!achado) falhar(`rascunho ${id} não encontrado`);
  return { ...achado, ...ler(achado.caminho) };
}

function cmdNovo(base, cfg, args) {
  let texto = valorDe(args, '--texto');
  const arquivo = valorDe(args, '--arquivo');
  if (texto === undefined && arquivo !== undefined) texto = readFileSync(arquivo, 'utf8');
  if (texto === undefined) {
    if (process.stdin.isTTY) falhar('passe --texto "...", --arquivo caminho ou envie o texto por stdin');
    texto = readFileSync(0, 'utf8');
  }
  const partes = texto
    .replace(/\r\n/g, '\n')
    .split(SEPARADOR)
    .map((p) => p.trim())
    .filter(Boolean);
  if (partes.length === 0) falhar('texto vazio');
  const id = proximoId(base, cfg.fuso);
  gravar(base, 'rascunhos', id, { id, status: 'rascunho', criado: new Date().toISOString() }, partes);
  registrar(base, 'rascunho_gerado', { id, tweets: partes.length });
  const { tweets, problemas } = planejar(partes, cfg.limite);
  console.log(`rascunho criado: ${id}`);
  console.log(contagem(partes, cfg.limite).join('\n'));
  if (problemas.length) console.log(`atenção: ${problemas.join('; ')}`);
  else if (tweets.length > partes.length) {
    console.log(`passa do limite: será dividido em ${tweets.length} tweets ao aprovar`);
  }
}

function cmdListar(base, args) {
  const nomes = args[0] ? [args[0]] : PASTAS;
  for (const nome of nomes) {
    if (!PASTAS.includes(nome)) falhar(`pasta desconhecida: ${nome} (use ${PASTAS.join(', ')})`);
    const ids = listarIds(base, nome);
    console.log(`${nome} (${ids.length})`);
    for (const id of ids) {
      const { partes } = ler(achar(base, id).caminho);
      const inicio = (partes[0] ?? '').replace(/\s+/g, ' ').slice(0, 60);
      console.log(`  ${id}  [${partes.length}]  ${inicio}`);
    }
  }
}

function cmdValidar(base, cfg, args) {
  const ids = args[0] ? [args[0]] : listarIds(base, 'rascunhos');
  if (ids.length === 0) return console.log('nenhum rascunho para validar');
  let ruim = false;
  for (const id of ids) {
    const { pasta, partes } = carregar(base, id);
    const { tweets, problemas } = planejar(partes, cfg.limite);
    const situacao = problemas.length ? `PROBLEMA: ${problemas.join('; ')}` : 'ok';
    console.log(`${id} (${pasta}): ${situacao}`);
    console.log(contagem(tweets, cfg.limite).join('\n'));
    if (problemas.length) ruim = true;
  }
  if (ruim) process.exit(1);
}

function cmdMostrar(base, cfg, args) {
  if (!args[0]) falhar('mostrar precisa de um id');
  const { pasta, partes } = carregar(base, args[0]);
  const { tweets, problemas } = planejar(partes, cfg.limite);
  console.log(`${args[0]} (${pasta}) para ${cfg.conta}: ${tweets.length} tweet(s)`);
  if (problemas.length) console.log(`atenção: ${problemas.join('; ')}`);
  tweets.forEach((t, i) => {
    console.log(`\n--- ${i + 1}/${tweets.length} · ${pesoDoTweet(t)}/${cfg.limite} ---`);
    console.log(t);
  });
}

function cmdAprovar(base, cfg, args) {
  if (!args[0]) falhar('aprovar precisa de um id');
  const r = carregar(base, args[0]);
  if (r.pasta !== 'rascunhos') falhar(`${args[0]} está em ${r.pasta}, só rascunhos podem ser aprovados`);
  const { tweets, problemas } = planejar(r.partes, cfg.limite);
  if (problemas.length) falhar(`não aprovado: ${problemas.join('; ')}. Edite o rascunho e tente de novo`);
  const meta = { ...r.meta, status: 'aprovado', aprovado: new Date().toISOString() };
  mover(base, args[0], 'rascunhos', 'aprovados', meta, tweets);
  registrar(base, 'aprovado', { id: args[0], tweets: tweets.length });
  console.log(`aprovado: ${args[0]} (${tweets.length} tweet(s)). Use "mostrar ${args[0]}" para copiar.`);
}

function cmdPublicado(base, args) {
  if (!args[0]) falhar('publicado precisa de um id');
  const r = carregar(base, args[0]);
  if (r.pasta !== 'aprovados') falhar(`${args[0]} está em ${r.pasta}: só um rascunho aprovado pode ser marcado como publicado`);
  const url = valorDe(args, '--url');
  const meta = { ...r.meta, status: 'publicado', publicado: new Date().toISOString() };
  if (url) meta.url = url;
  mover(base, args[0], 'aprovados', 'publicados', meta, r.partes);
  registrar(base, 'publicado', { id: args[0], ...(url ? { url } : {}) });
  console.log(`publicado: ${args[0]}`);
}

function cmdErro(base, args) {
  if (!args[0] || args.length < 2) falhar('uso: erro <id> <motivo>');
  const r = carregar(base, args[0]);
  if (r.pasta === 'publicados') falhar(`${args[0]} já foi publicado`);
  const motivo = args.slice(1).join(' ');
  const meta = { ...r.meta, status: 'erro', erro: motivo, erro_em: new Date().toISOString() };
  mover(base, args[0], r.pasta, 'erros', meta, r.partes);
  registrar(base, 'erro', { id: args[0], de: r.pasta, motivo });
  console.log(`movido para erros: ${args[0]}`);
}

const [cmd, ...args] = process.argv.slice(2);
const base = raiz();
let cfg;
try {
  cfg = lerConfig(base);
} catch (e) {
  falhar(e.message);
}

if (args[0] && !args[0].startsWith('--') && /^\d/.test(args[0]) && !idValido(args[0])) {
  falhar(`id inválido: ${args[0]}`);
}

switch (cmd) {
  case 'novo':
    cmdNovo(base, cfg, args);
    break;
  case 'listar':
    cmdListar(base, args);
    break;
  case 'validar':
    cmdValidar(base, cfg, args);
    break;
  case 'mostrar':
    cmdMostrar(base, cfg, args);
    break;
  case 'aprovar':
    cmdAprovar(base, cfg, args);
    break;
  case 'publicado':
    cmdPublicado(base, args);
    break;
  case 'erro':
    cmdErro(base, args);
    break;
  default:
    console.log(AJUDA);
    process.exit(cmd ? 1 : 0);
}
