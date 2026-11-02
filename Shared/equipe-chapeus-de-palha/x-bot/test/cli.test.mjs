import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { existsSync, mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { formatar, interpretar } from '../src/queue.mjs';

const CLI = join(dirname(fileURLToPath(import.meta.url)), '..', 'src', 'cli.mjs');

function ambiente() {
  const raiz = mkdtempSync(join(tmpdir(), 'x-bot-'));
  const rodar = (args, input) =>
    spawnSync(process.execPath, [CLI, ...args], {
      env: { ...process.env, X_BOT_RAIZ: raiz },
      input,
      encoding: 'utf8',
    });
  const eventos = () => {
    const arq = join(raiz, 'logs', 'x-bot.jsonl');
    if (!existsSync(arq)) return [];
    return readFileSync(arq, 'utf8').trim().split('\n').map((l) => JSON.parse(l));
  };
  return { raiz, rodar, eventos, limpar: () => rmSync(raiz, { recursive: true, force: true }) };
}

const idDe = (saida) => saida.match(/\d{4}-\d{2}-\d{2}-\d{3}/)[0];

test('formatar e interpretar são inversos', () => {
  const texto = formatar({ id: 'x', status: 'rascunho' }, ['um', 'dois\ncom quebra']);
  assert.deepEqual(interpretar(texto), {
    meta: { id: 'x', status: 'rascunho' },
    partes: ['um', 'dois\ncom quebra'],
  });
});

test('fluxo completo: novo, aprovar, publicado, com log em ordem', () => {
  const a = ambiente();
  try {
    const novo = a.rodar(['novo'], 'primeiro tweet\n===\nsegundo tweet');
    assert.equal(novo.status, 0, novo.stderr);
    const id = idDe(novo.stdout);
    assert.match(a.rodar(['listar', 'rascunhos']).stdout, new RegExp(id));
    assert.match(a.rodar(['mostrar', id]).stdout, /primeiro tweet/);

    const aprovar = a.rodar(['aprovar', id]);
    assert.equal(aprovar.status, 0, aprovar.stderr);
    assert.match(a.rodar(['listar', 'aprovados']).stdout, new RegExp(id));
    assert.doesNotMatch(a.rodar(['listar', 'rascunhos']).stdout, new RegExp(id));

    const pub = a.rodar(['publicado', id, '--url', 'https://x.com/luanzeraAI/status/1']);
    assert.equal(pub.status, 0, pub.stderr);
    assert.match(a.rodar(['listar', 'publicados']).stdout, new RegExp(id));

    const eventos = a.eventos();
    assert.deepEqual(eventos.map((e) => e.evento), ['rascunho_gerado', 'aprovado', 'publicado']);
    assert.ok(eventos.every((e) => e.ts && e.local && e.id === id));
  } finally {
    a.limpar();
  }
});

test('rascunho longo de uma parte é dividido em thread ao aprovar', () => {
  const a = ambiente();
  try {
    const id = idDe(a.rodar(['novo', '--texto', 'palavra '.repeat(120).trim()]).stdout);
    assert.equal(a.rodar(['aprovar', id]).status, 0);
    const { partes } = interpretar(readFileSync(join(a.raiz, 'fila', 'aprovados', `${id}.md`), 'utf8'));
    assert.ok(partes.length > 1);
    assert.match(partes[0], /\(1\/\d+\)$/);
  } finally {
    a.limpar();
  }
});

test('thread com tweet acima do limite não é aprovada', () => {
  const a = ambiente();
  try {
    const id = idDe(a.rodar(['novo'], `curto\n===\n${'b'.repeat(300)}`).stdout);
    const r = a.rodar(['aprovar', id]);
    assert.equal(r.status, 1);
    assert.match(r.stderr, /não aprovado/);
    assert.ok(existsSync(join(a.raiz, 'fila', 'rascunhos', `${id}.md`)));
  } finally {
    a.limpar();
  }
});

test('não dá para marcar como publicado sem aprovação', () => {
  const a = ambiente();
  try {
    const id = idDe(a.rodar(['novo', '--texto', 'oi']).stdout);
    const r = a.rodar(['publicado', id]);
    assert.equal(r.status, 1);
    assert.match(r.stderr, /aprovado/);
    assert.deepEqual(a.eventos().map((e) => e.evento), ['rascunho_gerado']);
  } finally {
    a.limpar();
  }
});

test('id fora do formato é recusado (sem path traversal)', () => {
  const a = ambiente();
  try {
    for (const ruim of ['../../config', '..\\..\\config', 'abc', '2026-11-01-1']) {
      const r = a.rodar(['mostrar', ruim]);
      assert.equal(r.status, 1, ruim);
      assert.match(r.stderr, /id inválido/);
    }
  } finally {
    a.limpar();
  }
});

test('erro move para erros e registra o motivo; publicado não vira erro', () => {
  const a = ambiente();
  try {
    const id = idDe(a.rodar(['novo', '--texto', 'oi']).stdout);
    assert.equal(a.rodar(['erro', id, 'postei errado']).status, 0);
    assert.match(a.rodar(['listar', 'erros']).stdout, new RegExp(id));
    const ev = a.eventos().at(-1);
    assert.equal(ev.evento, 'erro');
    assert.equal(ev.motivo, 'postei errado');

    const id2 = idDe(a.rodar(['novo', '--texto', 'outro']).stdout);
    a.rodar(['aprovar', id2]);
    a.rodar(['publicado', id2]);
    assert.equal(a.rodar(['erro', id2, 'x']).status, 1);
  } finally {
    a.limpar();
  }
});

test('ids do mesmo dia são sequenciais', () => {
  const a = ambiente();
  try {
    const um = idDe(a.rodar(['novo', '--texto', 'um']).stdout);
    const dois = idDe(a.rodar(['novo', '--texto', 'dois']).stdout);
    assert.equal(Number(dois.slice(-3)), Number(um.slice(-3)) + 1);
  } finally {
    a.limpar();
  }
});
